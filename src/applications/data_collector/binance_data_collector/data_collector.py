import os
import json
from unicorn_binance_websocket_api import BinanceWebSocketApiManager
from confluent_kafka import Producer

from applications.utils.logger import get_logger
from ..base_data_collector.data_collector import DataCollector
from .config import KAFKA_CONFIG
from .constants import (
    SUBCRIBE_CHANNELS, SYMBOL_LIST, TICKER_INFO_EVENT_TYPE,
    KLINES_EVENT_TYPE, TICKER_INFO_KAFKA_TOPIC, KLINES_KAFKA_TOPIC
)


class BinanceDataCollector(DataCollector):
    def __init__(self) -> None:
        super().__init__()
        self.binance_client = BinanceWebSocketApiManager()
        self.producer = Producer(KAFKA_CONFIG)
        self.logger = get_logger(
            "Binance data collector",
            f"{os.path.dirname(os.path.realpath(__file__))}/logs/binance_data_collector.log")

    def message_handler(self, message: str) -> None:
        json_result = json.loads(message)
        if "result" in json_result and not json_result["result"]:
            return

        json_result = json_result["data"]

        if json_result["e"] == TICKER_INFO_EVENT_TYPE:
            self.producer.produce(TICKER_INFO_KAFKA_TOPIC, json.dumps(json_result))
        if json_result["e"] == KLINES_EVENT_TYPE:
            self.producer.produce(KLINES_KAFKA_TOPIC, json.dumps(json_result))
        # Update metrics here...................................

    def collect_data(self) -> None:
        self.binance_client.create_stream(
            channels=SUBCRIBE_CHANNELS,
            markets=SYMBOL_LIST,
            process_stream_data=self.message_handler
        )

    def start(self) -> None:
        self.logger.info("Start collecting Binance data")
        try:
            self.collect_data()
        except Exception as e:
            self.logger.error(f"{e}")
            self.stop()

    def stop(self) -> None:
        self.logger.info("Stop collecting Binance data")
        self.binance_client.stop_manager_with_all_streams()
