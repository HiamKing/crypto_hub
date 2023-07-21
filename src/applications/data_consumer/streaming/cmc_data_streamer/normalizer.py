from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, decode, explode, to_timestamp

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

        renamed_cols = {}
        for col_name in n_df.columns:
            renamed_cols[col_name] = self.camel_to_snake(col_name)

        n_df = n_df.withColumnsRenamed(renamed_cols)
        assoc_df = n_df.select(
            col("gravity_id").alias("post_id"), explode("currencies").alias("currency"), col("post_time"))
        assoc_df = assoc_df.select("post_id", "currency.*", "post_time")
        assoc_df = assoc_df.withColumnRenamed("id", "symbol_id").drop("slug")
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
        pass

    def save_data(self, df: DataFrame) -> None:
        pass
