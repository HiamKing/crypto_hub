from typing import Dict, Any

from ..base_data_loader.normalizer import SparkNormalizer
from .constants import FE_KLINES_KAFKA_TOPIC, FE_TICKER_INFO_KAFKA_TOPIC
from .config import SPARK_APP_NAME, SPARK_CONFIG, SPARK_MASTER
from applications.utils.schema import KLINES_FILE_SCHEMA


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
        df.show()


class TickerInfoDataNormalizer(SparkNormalizer):
    def __init__(self, app_name: str, master: str, config: Dict[str, Any]) -> None:
        super().__init__(app_name, master, config)

    def normalize_data(self, file_path: str) -> None:
        pass
