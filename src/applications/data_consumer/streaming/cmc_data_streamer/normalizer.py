from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, decode, explode, to_timestamp, concat_ws

from .constants import CMC_NEWS_KAFKA_TOPIC, CMC_POSTS_KAFKA_TOPIC
from ...base.normalizer import DataNormalizer


class CMCDataNormalizer:
    def __init__(self, spark: SparkSession) -> None:
        self.normalizers = [NewsNormalizer(spark), PostsNormalizer(spark)]

    def normalize_data(self, df: DataFrame) -> None:
        for normalizer in self.normalizers:
            normalizer.normalize_data(df)


class PostsNormalizer(DataNormalizer):
    def __init__(self, spark: SparkSession) -> None:
        super().__init__()
        self.spark = spark

    def normalize_data(self, df: DataFrame) -> None:
        n_df = df.filter(col("topic") == CMC_POSTS_KAFKA_TOPIC)
        if n_df.isEmpty():
            return

        n_df = n_df.select(decode(col('value'), 'UTF-8').alias('value'))
        n_df = self.spark.read.json(n_df.rdd.map(lambda r: r[0]))

        n_df = self.rename_snake_case_cols(n_df)
        if "currencies" not in n_df.columns:
            return
        assoc_df = n_df.select(
            col("gravity_id").alias("post_id"), explode("currencies").alias("currency"), col("post_time"))
        assoc_df = assoc_df.select("post_id", "currency.*", "post_time")
        assoc_df = assoc_df.withColumnRenamed("id", "symbol_id").drop("slug")
        assoc_df = assoc_df.withColumn("_id", concat_ws(",", "post_id", "symbol_id"))
        n_df = n_df.withColumnRenamed("gravity_id", "_id")\
            .drop("owner", "root_id", "type", "currencies", "has_vote", "images",
                  "is_announcement", "is_liked", "is_live", "is_yours", "link_card_visible",
                  "original_content", "photo_ids", "pinned", "project_user", "repost_content",
                  "source_created_at", "source_display_name", "source_id", "source_type", "source_user_name",
                  "status")
        n_df = n_df.withColumn("post_time", to_timestamp(col("post_time") / 1000))
        assoc_df = assoc_df.withColumn("post_time", to_timestamp(col("post_time") / 1000))
        self.save_data(assoc_df, "cmc.stream.posts_assoc")
        self.save_data(n_df, "cmc.stream.posts")

    def save_data(self, df: DataFrame, collection: str) -> None:
        if df.isEmpty():
            return

        df.write.format("mongodb")\
            .option("collection", collection)\
            .mode("append")\
            .save()


class NewsNormalizer(DataNormalizer):
    def __init__(self, spark: SparkSession) -> None:
        super().__init__()
        self.spark = spark

    def normalize_data(self, df: DataFrame) -> None:
        n_df = df.filter(col("topic") == CMC_NEWS_KAFKA_TOPIC)
        if n_df.isEmpty():
            return

        n_df = n_df.select(decode(col('value'), 'UTF-8').alias('value'))
        n_df = self.spark.read.json(n_df.rdd.map(lambda r: r[0]))

        n_df = self.rename_snake_case_cols(n_df)
        assoc_df = n_df.select(
            explode(col("assets")).alias("asset"), col("meta.id").alias("news_id"), col("meta.updatedAt").alias("updated_at"))
        assoc_df = assoc_df.select(
            col("asset.name").alias("coin_name"), col("asset.coinId").alias("coin_id"), col("news_id"), col("updated_at"))
        assoc_df = assoc_df.withColumn("updated_at", to_timestamp(col("updated_at")))
        assoc_df = assoc_df.withColumn("_id", concat_ws(",", "news_id", "coin_id"))
        n_df = n_df.select("cover", "meta.*")
        n_df = self.rename_snake_case_cols(n_df)
        n_df = n_df.withColumnRenamed("id", "_id").drop("type", "visibility")
        n_df = n_df.withColumn("created_at", to_timestamp(col("created_at")))
        n_df = n_df.withColumn("updated_at", to_timestamp(col("updated_at")))
        n_df = n_df.withColumn("released_at", to_timestamp(col("released_at")))
        n_df = n_df.drop("downvotes", "upvotes", "content")
        self.save_data(assoc_df, "cmc.stream.news_assoc")
        self.save_data(n_df, "cmc.stream.news")

    def save_data(self, df: DataFrame, collection: str) -> None:
        if df.isEmpty():
            return

        df.write.format("mongodb")\
            .option("collection", collection)\
            .mode("append")\
            .save()
