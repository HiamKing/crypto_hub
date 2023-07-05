import os
from confluent_kafka import Consumer

from ...base.data_consumer import DataConsumer
from .config import KAFKA_CONFIG
from .constants import (
    TICKER_INFO_KAFKA_TOPIC, KLINES_KAFKA_TOPIC,
    KLINES_FIELDS_MAPPING, TICKER_INFO_FIELDS_MAPPING
)
from applications.utils.logger import get_logger
from .writer import KlinesDataWriter, TickerInfoDataWriter
from ....utils.schema import KLINES_FILE_SCHEMA, TICKER_INFO_FILE_SCHEMA


class BinanceDataConsumer(DataConsumer):
    def __init__(self) -> None:
        super().__init__()
        self.consumer = Consumer(KAFKA_CONFIG)
        self.logger = get_logger(
            "Binance data consumer",
            f"{os.path.dirname(os.path.realpath(__file__))}/logs/binance_data_consumer.log")
        self.kline_writer = KlinesDataWriter(
            KLINES_FILE_SCHEMA, KLINES_FIELDS_MAPPING, self.logger)
        self.ticker_info_writer = TickerInfoDataWriter(
            TICKER_INFO_FILE_SCHEMA, TICKER_INFO_FIELDS_MAPPING, self.logger)

    def consume_data(self) -> None:
        while True:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            hdfs_commit = False
            if msg.topic() == TICKER_INFO_KAFKA_TOPIC:
                hdfs_commit = self.ticker_info_writer.write(msg.value().decode("utf-8"))
            if msg.topic() == KLINES_KAFKA_TOPIC:
                hdfs_commit = self.kline_writer.write(msg.value().decode("utf-8"))
            # if hdfs_commit:
            #     self.consumer.commit(msg)

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
