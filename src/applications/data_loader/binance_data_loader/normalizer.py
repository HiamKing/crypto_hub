from typing import Dict, Any
from pyspark.sql import DataFrame
from pyspark.sql.functions import to_timestamp, col
from ..base_data_loader.normalizer import SparkNormalizer
from .constants import FE_KLINES_KAFKA_TOPIC, FE_TICKER_INFO_KAFKA_TOPIC, KLINES_INTERVAL
from .config import SPARK_APP_NAME, SPARK_CONFIG, SPARK_MASTER
from applications.utils.schema import KLINES_FILE_SCHEMA, TICKER_INFO_FILE_SCHEMA


class BinanceDataNormalizer:
    def __init__(self) -> None:
        self.normalizers = {
            FE_KLINES_KAFKA_TOPIC: KlinesDataNormalizer(
                SPARK_APP_NAME, SPARK_MASTER, SPARK_CONFIG),
            FE_TICKER_INFO_KAFKA_TOPIC: TickerInfoDataNormalizer(
                SPARK_APP_NAME, SPARK_MASTER, SPARK_CONFIG)
        }

    def normalize_data(self, topic: str, file_path: str) -> None:
        self.normalizers[topic].normalize_data(file_path)


class KlinesDataNormalizer(SparkNormalizer):
    def __init__(self, app_name: str, master: str, config: Dict[str, Any]) -> None:
        super().__init__(app_name, master, config)

    def normalize_data(self, file_path: str) -> None:
        df = self.spark.read.format("avro")\
            .option("avroSchema", KLINES_FILE_SCHEMA)\
            .load(file_path)
        df = df.select("kline.*")
        df = df.withColumn("start_time", to_timestamp(col("start_time") / 1000))
        df = df.withColumn("close_time", to_timestamp(col("close_time") / 1000))
        df = df.filter(col("is_closed") == True)  # noqa

        for interval in KLINES_INTERVAL:
            i_df = df.filter(col("interval") == interval)
            self.save_data(i_df, "binance.klines." + interval)

    def save_data(self, df: DataFrame, collection: str) -> None:
        if df.isEmpty():
            return

        df.write.format("mongodb")\
            .option("collection", collection)\
            .option("upsertDocument", False)\
            .mode("append")\
            .save()


class TickerInfoDataNormalizer(SparkNormalizer):
    def __init__(self, app_name: str, master: str, config: Dict[str, Any]) -> None:
        super().__init__(app_name, master, config)

    def normalize_data(self, file_path: str) -> None:
        df = self.spark.read.format("avro")\
            .option("avroSchema", TICKER_INFO_FILE_SCHEMA)\
            .load(file_path)
        df = df.withColumn("stats_open_time", to_timestamp(col("stats_open_time") / 1000))
        df = df.withColumn("stats_close_time", to_timestamp(col("stats_close_time") / 1000))
        df = df.select("symbol", "last_price", "stats_open_time", "stats_close_time")
        self.save_data(df, "binance.24h_ticker")

    def save_data(self, df: DataFrame, collection: str) -> None:
        if df.isEmpty():
            return

        df.write.format("mongodb")\
            .option("collection", collection)\
            .option("upsertDocument", False)\
            .mode("append")\
            .save()
