from typing import Dict, Any
from pyspark.sql import DataFrame
from pyspark.sql.functions import to_timestamp, col, explode
from ..base_data_loader.normalizer import SparkNormalizer
from .constants import FE_CMC_NEWS_KAFKA_TOPIC, FE_CMC_POSTS_KAFKA_TOPIC
from .config import SPARK_APP_NAME, SPARK_CONFIG, SPARK_MASTER
from applications.utils.schema import CMC_NEWS_SCHEMA, CMC_POSTS_SCHEMA


class CMCDataNormalizer:
    def __init__(self) -> None:
        self.normalizers = {
            FE_CMC_NEWS_KAFKA_TOPIC: NewsDataNormalizer(
                SPARK_APP_NAME, SPARK_MASTER, SPARK_CONFIG),
            FE_CMC_POSTS_KAFKA_TOPIC: PostsDataNormalizer(
                SPARK_APP_NAME, SPARK_MASTER, SPARK_CONFIG)
        }

    def normalize_data(self, topic: str, file_path: str) -> None:
        if topic == FE_CMC_POSTS_KAFKA_TOPIC:
            return
        self.normalizers[topic].normalize_data(file_path)


class NewsDataNormalizer(SparkNormalizer):
    def __init__(self, app_name: str, master: str, config: Dict[str, Any]) -> None:
        super().__init__(app_name, master, config)

    def normalize_data(self, file_path: str) -> None:
        df = self.spark.read.format("avro")\
            .option("avroSchema", CMC_NEWS_SCHEMA)\
            .load(file_path)

        assoc_df = df.select("assets", "meta.id")
        assoc_df = assoc_df.withColumn("asset", explode(col("assets"))).drop("assets")
        assoc_df = assoc_df.select(col("asset.name"), col("asset.coin_id"), col("id").alias("news_id"))
        df = df.select("cover", "meta.*")
        df = df.withColumn("_id", col("id"))
        df = df.drop("id", "type", "visibility")
        self.save_data(assoc_df, "cmc.news_assoc")
        self.save_data(df, "cmc.news")

    def save_data(self, df: DataFrame, collection: str) -> None:
        if df.isEmpty():
            return

        df.write.format("mongodb")\
            .option("collection", collection)\
            .mode("append")\
            .save()


class PostsDataNormalizer(SparkNormalizer):
    def __init__(self, app_name: str, master: str, config: Dict[str, Any]) -> None:
        super().__init__(app_name, master, config)

    def normalize_data(self, file_path: str) -> None:
        df = self.spark.read.format("avro")\
            .option("avroSchema", CMC_POSTS_SCHEMA)\
            .load(file_path)
        df = df.withColumn("stats_open_time", to_timestamp(col("stats_open_time") / 1000))
        df = df.withColumn("stats_close_time", to_timestamp(col("stats_close_time") / 1000))
        df = df.select("symbol", "last_price", "stats_open_time", "stats_close_time")
        self.save_data(df)

    def save_data(self, df: DataFrame) -> None:
        if df.isEmpty():
            return

        df.write.format("mongodb")\
            .option("collection", "24h_ticker_info")\
            .option("upsertDocument", False)\
            .mode("append")\
            .save()
