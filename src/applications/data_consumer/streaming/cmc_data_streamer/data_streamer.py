import os
from typing import Dict, Any
from pyspark.sql import DataFrame

from ...base.data_streamer import DataStreamer
from .normalizer import CMCDataNormalizer
from .config import KAFKA_BOOTSTRAP_SERVERS
from .constants import CMC_NEWS_KAFKA_TOPIC, CMC_POSTS_KAFKA_TOPIC
from applications.utils.logger import get_logger


class CMCDataStreamer(DataStreamer):
    def __init__(self, app_name: str, master: str, config: Dict[str, Any]) -> None:
        super().__init__(app_name, master, config)
        self.normalizer = CMCDataNormalizer(self.spark)
        self.sq = None
        self.logger = get_logger(
            "CMC data streamer",
            f"{os.path.dirname(os.path.realpath(__file__))}/logs/cmc_data_streamer.log")

    def stream_data(self, df: DataFrame, batch_id: int) -> None:
        self.normalizer.normalize_data(df)

    def start(self) -> None:
        self.logger.info("Starting CMC data streamer...")
        try:
            df = self.spark.readStream.format("kafka")\
                .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)\
                .option("subscribe", f"{CMC_NEWS_KAFKA_TOPIC},{CMC_POSTS_KAFKA_TOPIC}")\
                .load()
            self.sq = df.writeStream.foreachBatch(self.stream_data).start()
            self.sq.awaitTermination()
        except Exception as e:
            self.logger.error(f"An error happened while streaming data: {e}")
        finally:
            self.stop()

    def stop(self) -> None:
        self.logger.info("Stoping CMC data streamer...")
        if self.sq:
            self.sq.stop()
