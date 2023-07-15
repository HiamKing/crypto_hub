import logging
from typing import Dict, Any
from logging import Logger
from datetime import datetime

from .config import HADOOP_URL, HADOOP_USER
from .constants import (
    MAX_FILE_SIZE, KLINES_FIELDS_MAPPING, TICKER_INFO_FIELDS_MAPPING,
    TICKER_INFO_KAFKA_TOPIC, KLINES_KAFKA_TOPIC
)
from ...base.writer import ReLabelAvroHDFSWriter
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


class KlinesDataWriter(ReLabelAvroHDFSWriter):
    def __init__(
            self, schema: str, fields_mapping: Dict[str, Any], logger: Logger) -> None:
        super().__init__(HADOOP_URL, HADOOP_USER, schema, fields_mapping, MAX_FILE_SIZE, logger)

    def get_hdfs_file_name(self) -> str:
        now = datetime.utcnow()
        return f"/data/binance/klines_data/{now.date().strftime('%Y/%m/%d')}/records.{int(round(now.timestamp()))}.avro"


class TickerInfoDataWriter(ReLabelAvroHDFSWriter):
    def __init__(
            self, schema: str, fields_mapping: Dict[str, Any], logger: Logger) -> None:
        super().__init__(HADOOP_URL, HADOOP_USER, schema, fields_mapping, MAX_FILE_SIZE, logger)

    def get_hdfs_file_name(self) -> str:
        now = datetime.utcnow()
        return f"/data/binance/ticker_info_data/{now.date().strftime('%Y/%m/%d')}/records.{int(round(now.timestamp()))}.avro"
