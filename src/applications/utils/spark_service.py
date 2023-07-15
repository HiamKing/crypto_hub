from typing import Dict, Any
from pyspark import SparkConf
from pyspark.sql import SparkSession


class SparkService:
    def __init__(self, app_name: str, master: str, config: Dict[str, Any]) -> None:
        self.app_name = app_name
        self.master = master
        self.config = config
        self._spark = self.create_spark_session()

    def build_spark_config(self) -> SparkConf:
        conf = SparkConf().setAppName(self.app_name).setMaster(self.master)
        [conf.set(key, val) for key, val in self.config.items()]
        return conf

    def create_spark_session(self) -> SparkSession:
        spark_conf = self.build_spark_config()
        return SparkSession.builder.config(conf=spark_conf).getOrCreate()

    def is_running(self) -> bool:
        return self._spark and not self._spark._jsc.sc().isStopped()

    @property
    def spark(self) -> SparkSession:
        if not self.is_running():
            self._spark = self.create_spark_session()

        return self._spark
