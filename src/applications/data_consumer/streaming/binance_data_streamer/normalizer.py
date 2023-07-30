from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, decode, to_timestamp

from .constants import (
    KLINES_KAFKA_TOPIC, TICKER_INFO_KAFKA_TOPIC,
    KLINES_INTERVAL, KLINES_COLS_NORMALIZED_COLS,
    TICKER_INFO_COLS_NORMALIZED_COLS
)
from ...base.normalizer import DataNormalizer


class BinanceDataNormalizer:
    def __init__(self, spark: SparkSession) -> None:
        self.normalizers = [KlinesNormalizer(spark), TickerInfoNormalizer(spark)]

    def normalize_data(self, df: DataFrame) -> None:
        for normalizer in self.normalizers:
            normalizer.normalize_data(df)


class KlinesNormalizer(DataNormalizer):
    def __init__(self, spark: SparkSession) -> None:
        super().__init__()
        self.spark = spark

    def normalize_data(self, df: DataFrame) -> None:
        n_df = df.filter(col("topic") == KLINES_KAFKA_TOPIC)
        if n_df.isEmpty():
            return

        n_df = n_df.select(decode(col('value'), 'UTF-8').alias('value'))
        n_df = self.spark.read.json(n_df.rdd.map(lambda r: r[0]))
        n_df = n_df.select("k.*")
        n_df = n_df.select(
            *[
                col(column).cast(attrs["type"]).alias(attrs["name"])
                for column, attrs in KLINES_COLS_NORMALIZED_COLS.items()
            ]
        )
        n_df = n_df.withColumn("start_time", to_timestamp(col("start_time") / 1000))
        n_df = n_df.withColumn("close_time", to_timestamp(col("close_time") / 1000))

        for interval in KLINES_INTERVAL:
            i_df = n_df.filter(col("interval") == interval)
            self.save_data(i_df, "binance.stream.klines." + interval)

    def save_data(self, df: DataFrame, collection: str) -> None:
        if df.isEmpty():
            return

        df.write.format("mongodb")\
            .option("collection", collection)\
            .option("upsertDocument", False)\
            .mode("append")\
            .save()


class TickerInfoNormalizer(DataNormalizer):
    def __init__(self, spark: SparkSession) -> None:
        super().__init__()
        self.spark = spark

    def normalize_data(self, df: DataFrame) -> None:
        n_df = df.filter(col("topic") == TICKER_INFO_KAFKA_TOPIC)
        if n_df.isEmpty():
            return

        n_df = n_df.select(decode(col('value'), 'UTF-8').alias('value'))
        n_df = self.spark.read.json(n_df.rdd.map(lambda r: r[0]))
        n_df = n_df.select(
            *[
                col(column).cast(attrs["type"]).alias(attrs["name"])
                for column, attrs in TICKER_INFO_COLS_NORMALIZED_COLS.items()
            ]
        )
        n_df = n_df.withColumn("stats_open_time", to_timestamp(col("stats_open_time") / 1000))
        n_df = n_df.withColumn("stats_close_time", to_timestamp(col("stats_close_time") / 1000))

        self.save_data(n_df, "binance.stream.24h_ticker")

    def save_data(self, df: DataFrame, collection: str) -> None:
        if df.isEmpty():
            return

        df.write.format("mongodb")\
            .option("collection", collection)\
            .option("upsertDocument", False)\
            .mode("append")\
            .save()
