import os
import json
from typing import Dict, Any
from binance.websocket.spot.websocket_api import SpotWebsocketAPIClient

from ..base_data_collector.data_collector import DataCollector
from .config import BINANCE_API_KEY, BINANCE_SECRET
from utils.logger import get_logger


class BinanceDataCollector(DataCollector):
    def __init__(self, symbol) -> None:
        super().__init__()
        self.symbol = symbol
        self.binance_client = SpotWebsocketAPIClient(
            api_key=BINANCE_API_KEY,
            api_secret=BINANCE_SECRET,
            on_message=self.message_handler)
        self.logger = get_logger(
            f"{symbol} data collector",
            f"{os.path.dirname(os.path.realpath(__file__))}/logs/binance_data_collector.log")

    def message_handler(self, _, message: str) -> None:
        json_result = json.loads(message)
        # Check using type for now
        if isinstance(json_result["result"], list):
            self.klines_handler(json_result["result"])
        if isinstance(json_result["result"], dict):
            self.ticker_handler(json_result["result"])
        print(json_result["rateLimits"][0]["count"])
        # Update metrics here...................................

    def ticker_handler(self, message: Dict[str, Any]) -> None:
        print(message)

    def klines_handler(self, message: list[Any]) -> None:
        print(self.symbol, message)

    def collect_data(self) -> None:
        self.binance_client.ticker(symbol=self.symbol, type="FULL")
        self.binance_client.klines(symbol=self.symbol, interval="1m", limit=1)
        self.binance_client.klines(symbol=self.symbol, interval="1h", limit=1)
        self.binance_client.klines(symbol=self.symbol, interval="1d", limit=1)
        self.binance_client.klines(symbol=self.symbol, interval="1w", limit=1)
        self.binance_client.klines(symbol=self.symbol, interval="1M", limit=1)

    def start(self) -> None:
        self.logger.info(f"Start collecting data for symbol {self.symbol}...")
        try:
            self.collect_data()
        except Exception as e:
            self.logger.error(f"{e}")

    def stop(self) -> None:
        self.binance_client.stop()
