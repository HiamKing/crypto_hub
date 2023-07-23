from typing import Dict, Any
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, explode, to_timestamp, concat_ws
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
        self.normalizers[topic].normalize_data(file_path)


class NewsDataNormalizer(SparkNormalizer):
    def __init__(self, app_name: str, master: str, config: Dict[str, Any]) -> None:
        super().__init__(app_name, master, config)

    def normalize_data(self, file_path: str) -> None:
        df = self.spark.read.format("avro")\
            .option("avroSchema", CMC_NEWS_SCHEMA)\
            .load(file_path)

        assoc_df = df.select(explode(col("assets")).alias("asset"), col("meta.id").alias("news_id"), col("meta.updated_at").alias("updated_at"))
        assoc_df = assoc_df.select(col("asset.name").alias("coin_name"), col("asset.coin_id"), col("news_id"), col("updated_at"))
        assoc_df = assoc_df.withColumn("updated_at", to_timestamp(col("updated_at")))
        assoc_df = assoc_df.withColumn("_id", concat_ws(",", "news_id", "coin_id"))
        df = df.select("cover", "meta.*")
        df = df.withColumnRenamed("id", "_id").drop("type", "visibility")
        df = df.withColumn("created_at", to_timestamp(col("created_at")))
        df = df.withColumn("updated_at", to_timestamp(col("updated_at")))
        df = df.withColumn("released_at", to_timestamp(col("released_at")))
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
        assoc_df = df.select(
            col("gravity_id").alias("post_id"), explode("currencies").alias("currency"), col("post_time"))
        assoc_df = assoc_df.select("post_id", "currency.*", "post_time")
        assoc_df = assoc_df.withColumnRenamed("id", "symbol_id").drop("slug")
        assoc_df = assoc_df.withColumn("_id", concat_ws(",", "post_id", "symbol_id"))
        df = df.withColumnRenamed("gravity_id", "_id")\
            .drop("owner", "root_id", "type", "currencies")
        df = df.withColumn("post_time", to_timestamp(col("post_time") / 1000))
        assoc_df = assoc_df.withColumn("post_time", to_timestamp(col("post_time") / 1000))
        self.save_data(assoc_df, "cmc.posts_assoc")
        self.save_data(df, "cmc.posts")

    def save_data(self, df: DataFrame, collection: str) -> None:
        if df.isEmpty():
            return

        df.write.format("mongodb")\
            .option("collection", collection)\
            .mode("append")\
            .save()
