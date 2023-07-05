import json
from typing import Dict, Any
from logging import Logger

from ...base.writer import AvroHDFSWriter
from .constants import MAX_FILE_SIZE
from .config import HADOOP_URL, HADOOP_USER


class BinanceDataWriter(AvroHDFSWriter):
    def __init__(self, schema: str, fields_mapping: Dict[str, Any], logger: Logger) -> None:
        super().__init__(schema, HADOOP_URL, HADOOP_USER, logger)
        self.fields_mapping = fields_mapping

    def convert_field_name(self, record: Dict[str, Any], new_record: Dict[str, Any]) -> None:
        # Only support for dict and atomic fields for now
        for key, val in record.items():
            if key not in self.fields_mapping:
                continue

            if type(val) == dict:
                new_record[self.fields_mapping[key]["name"]] = {}
                self.convert_field_name(val, new_record[self.fields_mapping[key]["name"]])
            elif self.fields_mapping[key]["type"] == "long":
                new_record[self.fields_mapping[key]["name"]] = int(val)
            elif self.fields_mapping[key]["type"] == "double":
                new_record[self.fields_mapping[key]["name"]] = float(val)
            elif self.fields_mapping[key]["type"] == "boolean":
                new_record[self.fields_mapping[key]["name"]] = bool(val)
            else:
                new_record[self.fields_mapping[key]["name"]] = val

    def get_hdfs_file_name(self) -> str:
        raise NotImplementedError()

    def write(self, message: str) -> bool:
        record = json.loads(message)
        normalized_record = {}
        self.convert_field_name(record, normalized_record)
        self.avro_writer.append(normalized_record)
        self.avro_writer.flush()

        # # If current file size > MAX_FILE_SIZE flush to hdfs
        if self.avro_writer.sync() > MAX_FILE_SIZE:
            self.flush_to_hdfs(self.tmp_file, self.get_hdfs_file_name())
            self.recreate_tmpfile()
            return True

        return False
