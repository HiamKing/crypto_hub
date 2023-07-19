import os
from typing import Dict, Any
from ...base.data_streamer import DataStreamer
from applications.utils.logger import get_logger


class CMCDataStreamer(DataStreamer):
    def __init__(self, app_name: str, master: str, config: Dict[str, Any]) -> None:
        super().__init__(app_name, master, config)
        self.logger = get_logger(
            "CMC data streamer",
            f"{os.path.dirname(os.path.realpath(__file__))}/logs/cmc_data_streamer.log")

    def stream_data(self) -> None:
        return super().stream_data()

    def start(self) -> None:
        return super().start()

    def stop(self) -> None:
        return super().stop()
