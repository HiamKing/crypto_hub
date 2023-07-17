import os
from confluent_kafka import Consumer, Producer

from ...base.data_consumer import DataConsumer
from .config import KAFKA_CONFIG, FE_KAFKA_CONFIG
from .constants import (
    CMC_POSTS_KAFKA_TOPIC, CMC_NEWS_KAFKA_TOPIC,
    FE_TOPIC_MAPPING
)
from applications.utils.logger import get_logger
from .writer import CMCDataWriter


class CMCDataConsumer(DataConsumer):
    def __init__(self) -> None:
        super().__init__()
        self.consumer = Consumer(KAFKA_CONFIG)
        self.fe_producer = Producer(FE_KAFKA_CONFIG)
        self.logger = get_logger(
            "CMC data consumer",
            f"{os.path.dirname(os.path.realpath(__file__))}/logs/cmc_data_consumer.log")
        self.writer = CMCDataWriter(self.logger)

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
        self.consumer.subscribe([CMC_POSTS_KAFKA_TOPIC, CMC_NEWS_KAFKA_TOPIC])
        self.logger.info("Start consuming CMC data")
        try:
            self.consume_data()
        except Exception as e:
            self.logger.error(f"{e}")
        finally:
            self.stop()

    def stop(self) -> None:
        self.logger.info("Stop consuming CMC data")
        self.fe_producer.flush()
        self.consumer.close()
