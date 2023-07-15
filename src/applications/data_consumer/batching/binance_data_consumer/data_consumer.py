import os
import logging
from confluent_kafka import Consumer, Producer

from ...base.data_consumer import DataConsumer
from .config import CONSUMER_KAFKA_CONFIG, FE_KAFKA_CONFIG
from .constants import (
    TICKER_INFO_KAFKA_TOPIC, KLINES_KAFKA_TOPIC,
    KLINES_FIELDS_MAPPING, TICKER_INFO_FIELDS_MAPPING,
    FE_TOPIC_MAPPING
)
from applications.utils.logger import get_logger
from .writer import KlinesDataWriter, TickerInfoDataWriter
from ....utils.schema import KLINES_FILE_SCHEMA, TICKER_INFO_FILE_SCHEMA


class BinanceDataWriter:
    def __init__(self, logger: logging.Logger) -> None:
        self.writers = {
            TICKER_INFO_KAFKA_TOPIC: TickerInfoDataWriter(
                TICKER_INFO_FILE_SCHEMA, TICKER_INFO_FIELDS_MAPPING, logger),
            KLINES_KAFKA_TOPIC: KlinesDataWriter(
                KLINES_FILE_SCHEMA, KLINES_FIELDS_MAPPING, logger)
        }

    def write(self, topic: str, msg: str) -> str:
        return self.writers[topic].write(msg)


class BinanceDataConsumer(DataConsumer):
    def __init__(self) -> None:
        super().__init__()
        self.consumer = Consumer(CONSUMER_KAFKA_CONFIG)
        self.fe_producer = Producer(FE_KAFKA_CONFIG)
        self.logger = get_logger(
            "Binance data consumer",
            f"{os.path.dirname(os.path.realpath(__file__))}/logs/binance_data_consumer.log")
        self.writer = BinanceDataWriter(self.logger)

    def consume_data(self) -> None:
        while True:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            hdfs_file = ""
            hdfs_file = self.writer.write(msg.topic(), msg.value().decode("utf-8"))
            if hdfs_file:
                self.fe_producer.produce(
                    FE_TOPIC_MAPPING[msg.topic()],
                    bytes(hdfs_file, encoding='utf-8'))
                self.consumer.commit(msg)

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
        self.fe_producer.flush()
        self.consumer.close()
