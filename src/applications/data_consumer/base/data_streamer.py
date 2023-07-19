from typing import Dict, Any
from applications.utils.spark_service import SparkService


class DataStreamer(SparkService):
    def __init__(self, app_name: str, master: str, config: Dict[str, Any]) -> None:
        super().__init__(app_name, master, config)

    def stream_data(self) -> None:
        raise NotImplementedError()

    def start(self) -> None:
        raise NotImplementedError()

    def stop(self) -> None:
        raise NotImplementedError()
