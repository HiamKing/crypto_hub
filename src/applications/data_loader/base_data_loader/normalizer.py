from applications.utils.spark_service import SparkService
from typing import Dict, Any


class SparkNormalizer(SparkService):
    def __init__(self, app_name: str, master: str, config: Dict[str, Any]) -> None:
        super().__init__(app_name, master, config)

    def normalize_data(self, file_path: str) -> None:
        raise NotImplementedError()
