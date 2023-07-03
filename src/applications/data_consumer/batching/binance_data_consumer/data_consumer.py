import os
import json
from confluent_kafka import Consumer

from ...base.data_consumer import DataConsumer
from .config import KAFKA_CONFIG
from .constants import TICKER_INFO_KAFKA_TOPIC, KLINES_KAFKA_TOPIC
from applications.utils.logger import get_logger


class BinanceDataConsumer(DataConsumer):
    def __init__(self) -> None:
        super().__init__()
        self.consumer = Consumer(KAFKA_CONFIG)
        self.logger = get_logger(
            "Binance data consumer",
            f"{os.path.dirname(os.path.realpath(__file__))}/logs/binance_data_consumer.log")

    def consume_data(self) -> None:
        while True:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            print('Received message: {}'.format(msg.value().decode('utf-8')))

    def start(self) -> None:
        self.consumer.subscribe([TICKER_INFO_KAFKA_TOPIC, KLINES_KAFKA_TOPIC])
        self.logger.info("Start consuming Binance data")
        try:
            self.consume_data()
        except Exception as e:
            self.logger.error(f"{e}")
        finally:
            self.stop()

    def stop(self) -> None:
        self.logger.info("Stop consuming Binance data")
        self.consumer.close()
