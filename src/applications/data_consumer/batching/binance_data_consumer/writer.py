from typing import Dict, Any
from logging import Logger

from ...base.writer import ReLabelAvroHDFSWriter
from .constants import MAX_FILE_SIZE
from .config import HADOOP_URL, HADOOP_USER


class KlinesDataWriter(ReLabelAvroHDFSWriter):
    def __init__(
            self, schema: str, fields_mapping: Dict[str, Any], logger: Logger) -> None:
        super().__init__(HADOOP_URL, HADOOP_USER, schema, fields_mapping, MAX_FILE_SIZE, logger)

    def get_hdfs_file_name(self) -> str:
        return "/binance_data/klines_data"


class TickerInfoDataWriter(ReLabelAvroHDFSWriter):
    def __init__(
            self, schema: str, fields_mapping: Dict[str, Any], logger: Logger) -> None:
        super().__init__(HADOOP_URL, HADOOP_USER, schema, fields_mapping, MAX_FILE_SIZE, logger)

    def get_hdfs_file_name(self) -> str:
        return "/"
