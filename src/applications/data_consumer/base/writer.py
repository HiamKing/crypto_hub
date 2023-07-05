
import tempfile
import avro.schema
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
