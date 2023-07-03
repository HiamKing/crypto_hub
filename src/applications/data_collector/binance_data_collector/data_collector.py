import os
import json
from typing import Dict, Any
from unicorn_binance_websocket_api import BinanceWebSocketApiManager
from confluent_kafka import Producer

from ..base_data_collector.data_collector import DataCollector
from .config import KAFKA_CONFIG
from .constants import SUBCRIBE_CHANNELS, SYMBOL_LIST
from utils.logger import get_logger


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
        # Check using type for now
        if "result" in json_result and not json_result["result"]:
            return
        json_result = json_result["data"]

        if json_result["e"] == "24hrTicker":
            self.ticker_handler(json_result)
        if json_result["e"] == "kline":
            self.klines_handler(json_result)
        # Update metrics here...................................

    def ticker_handler(self, ticker_info: Dict[str, Any]) -> None:
        print(ticker_info["s"], "ticket info")
        # self.producer.produce(f"ticket.{self.symbol}.24h-info", json.dumps(ticker_info))

    def klines_handler(self, klines_result: Dict[str, Any]) -> None:
        # Get sample kline time to get the right appending topic
        if klines_result["k"]["i"] == "1m":
            print(klines_result["s"], "minute kline")
        if klines_result["k"]["i"] == "1h":
            print(klines_result["s"], "hour kline")
        if klines_result["k"]["i"] == "1d":
            print(klines_result["s"], "day kline")
        if klines_result["k"]["i"] == "1w":
            print(klines_result["s"], "week kline")
        if klines_result["k"]["i"] == "1M":
            print(klines_result["s"], "Month kline")
        # self.producer.produce(f"ticket.{self.symbol}.24h-info", json.dumps({
        #     "symbol": self.symbol,
        #     "result": klines_result,
        # }))

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
