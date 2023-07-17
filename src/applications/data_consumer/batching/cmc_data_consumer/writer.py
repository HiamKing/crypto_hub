from typing import Dict, Any
from logging import Logger
from datetime import datetime

from applications.utils.schema import CMC_NEWS_SCHEMA, CMC_POSTS_SCHEMA
from ...base.writer import ReLabelAvroHDFSWriter
from .constants import (
    MAX_FILE_SIZE, NEWS_FIELDS_MAPPING, POSTS_FIELDS_MAPPING,
    CMC_POSTS_KAFKA_TOPIC, CMC_NEWS_KAFKA_TOPIC
)
from .config import HADOOP_URL, HADOOP_USER


class CMCDataWriter:
    def __init__(self, logger: Logger) -> None:
        self.writers = {
            CMC_NEWS_KAFKA_TOPIC: NewsDataWriter(
                CMC_NEWS_SCHEMA, NEWS_FIELDS_MAPPING, logger),
            CMC_POSTS_KAFKA_TOPIC: PostsDataWriter(
                CMC_POSTS_SCHEMA, POSTS_FIELDS_MAPPING, logger)
        }

    def write(self, topic: str, msg: str) -> str:
        self.writers[topic].write(msg)


class NewsDataWriter(ReLabelAvroHDFSWriter):
    def __init__(
            self, schema: str, fields_mapping: Dict[str, Any], logger: Logger) -> None:
        super().__init__(HADOOP_URL, HADOOP_USER, schema, fields_mapping, MAX_FILE_SIZE, logger)

    def get_hdfs_file_name(self) -> str:
        now = datetime.utcnow()
        return f"/data/coinmarketcap/news_data/{now.date().strftime('%Y/%m/%d')}/records.{int(round(now.timestamp()))}.avro"


class PostsDataWriter(ReLabelAvroHDFSWriter):
    def __init__(
            self, schema: str, fields_mapping: Dict[str, Any], logger: Logger) -> None:
        super().__init__(HADOOP_URL, HADOOP_USER, schema, fields_mapping, MAX_FILE_SIZE, logger)

    def get_hdfs_file_name(self) -> str:
        now = datetime.utcnow()
        return f"/data/coinmarketcap/posts_data/{now.date().strftime('%Y/%m/%d')}/records.{int(round(now.timestamp()))}.avro"
