
import tempfile
import json
import avro.schema
from typing import Dict, Any
from avro.datafile import DataFileWriter
from avro.io import DatumWriter
from logging import Logger
from hdfs import InsecureClient


class HDFSWriter:
    def __init__(self, hdfs_url: str, user: str, logger: Logger) -> None:
        self.hdfs_client = InsecureClient(hdfs_url, user)
        self.logger = logger

    def flush_to_hdfs(self, file_name: str, hdfs_file_name: str) -> None:
        self.logger.info(
            f'Starting flush file {file_name} to hdfs')
        flush_status = self.hdfs_client.upload(hdfs_file_name, file_name)
        if flush_status:
            self.logger.info(f'Flush file {file_name} to hdfs as {hdfs_file_name} successfully')
        else:
            raise RuntimeError(f'Failed to flush file {file_name} to hdfs')

    def write(self, message: str) -> bool:
        raise NotImplementedError()


class AvroHDFSWriter(HDFSWriter):
    def __init__(self, schema: str, hdfs_url: str, user: str, logger: Logger) -> None:
        super().__init__(hdfs_url, user, logger)
        self.schema = avro.schema.parse(schema)
        self.tmp_file = tempfile.NamedTemporaryFile()
        self.avro_writer = DataFileWriter(open(self.tmp_file.name, 'wb'), DatumWriter(), self.schema)

    def recreate_tmpfile(self) -> tuple[tempfile._TemporaryFileWrapper, DataFileWriter]:
        self.tmp_file = tempfile.NamedTemporaryFile()
        self.avro_writer = DataFileWriter(open(self.tmp_file.name, 'wb'), DatumWriter(), self.schema)

    def close_tmpfile(self) -> None:
        self.tmp_file.close()
        self.avro_writer.close()


class ReLabelAvroHDFSWriter(AvroHDFSWriter):
    def __init__(
            self, hdfs_url: str, user: str, schema: str,
            fields_mapping: Dict[str, Any], max_file_size: int, logger: Logger) -> None:
        super().__init__(schema, hdfs_url, user, logger)
        self.fields_mapping = fields_mapping
        self.max_file_size = max_file_size

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
        if self.avro_writer.sync() > self.max_file_size:
            self.flush_to_hdfs(self.tmp_file, self.get_hdfs_file_name())
            self.close_tmpfile()
            self.recreate_tmpfile()
            return True

        return False
