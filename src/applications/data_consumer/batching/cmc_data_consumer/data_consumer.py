import os
from confluent_kafka import Consumer

from ...base.data_consumer import DataConsumer
from .config import KAFKA_CONFIG
from .constants import (
    CMC_POSTS_KAFKA_TOPIC, CMC_NEWS_KAFKA_TOPIC,
    NEWS_FIELDS_MAPPING, POSTS_FIELDS_MAPPING
)
from applications.utils.logger import get_logger
from .writer import NewsDataWriter, PostsDataWriter
from ....utils.schema import CMC_NEWS_SCHEMA, CMC_POSTS_SCHEMA


class CMCDataConsumer(DataConsumer):
    def __init__(self) -> None:
        super().__init__()
        self.consumer = Consumer(KAFKA_CONFIG)
        self.logger = get_logger(
            "CMC data consumer",
            f"{os.path.dirname(os.path.realpath(__file__))}/logs/cmc_data_consumer.log")
        self.news_writer = NewsDataWriter(
            CMC_NEWS_SCHEMA, NEWS_FIELDS_MAPPING, self.logger)
        self.posts_writer = PostsDataWriter(
            CMC_POSTS_SCHEMA, POSTS_FIELDS_MAPPING, self.logger)

    def consume_data(self) -> None:
        while True:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            hdfs_commit = False
            if msg.topic() == CMC_NEWS_KAFKA_TOPIC:
                hdfs_commit = self.news_writer.write(msg.value().decode("utf-8"))
            if msg.topic() == CMC_POSTS_KAFKA_TOPIC:
                hdfs_commit = self.posts_writer.write(msg.value().decode("utf-8"))
            if hdfs_commit:
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
        self.consumer.close()
