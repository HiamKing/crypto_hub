from typing import Dict, Any
from logging import Logger
from datetime import datetime

from ...base.writer import ReLabelAvroHDFSWriter
from .constants import MAX_FILE_SIZE
from .config import HADOOP_URL, HADOOP_USER


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
