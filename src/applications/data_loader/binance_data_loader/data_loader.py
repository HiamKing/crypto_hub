
import os
from confluent_kafka import Consumer

from applications.utils.logger import get_logger
from ..base_data_loader.data_loader import DataLoader
from .normalizer import BinanceDataNormalizer
from .constants import FE_KLINES_KAFKA_TOPIC, FE_TICKER_INFO_KAFKA_TOPIC
from .config import CONSUMER_KAFKA_CONFIG


class BinanceDataLoader(DataLoader):
    def __init__(self) -> None:
        super().__init__()
        self.consumer = Consumer(CONSUMER_KAFKA_CONFIG)
        self.normalizer = BinanceDataNormalizer()
        self.logger = get_logger(
            "Binance data loader",
            f"{os.path.dirname(os.path.realpath(__file__))}/logs/binance_data_loader.log")

    def load_data(self) -> None:
        while True:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            hdfs_file = msg.value().decode("utf-8")
            self.normalizer.normalize_data(msg.topic(), hdfs_file)
            # self.consumer.commit(msg)

    def start(self) -> None:
        self.logger.info("Starting Binance data loader...")
        self.consumer.subscribe([FE_KLINES_KAFKA_TOPIC, FE_TICKER_INFO_KAFKA_TOPIC])
        try:
            self.load_data()
        except Exception as e:
            self.logger.error(f"{e}")
        finally:
            self.stop()

    def stop(self) -> None:
        self.logger.info("Stop Binance data loader...")
        self.consumer.close()
