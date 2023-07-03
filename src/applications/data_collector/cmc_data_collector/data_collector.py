import os
from datetime import datetime, timedelta
import requests

from ..base_data_collector.data_collector import DataCollector
from .constants import SYMBOL_ID_MAPPING
from applications.utils.logger import get_logger


class CMCNewsDataCollector(DataCollector):
    def __init__(self, symbol) -> None:
        super().__init__()
        self.symbol = symbol
        self.base_url = "https://api.coinmarketcap.com/content/v3/news/aggregated"
        # Last news should be get from db
        self.last_news_id = None
        self.logger = get_logger(
            f"CMC {symbol} news data collector",
            f"{os.path.dirname(os.path.realpath(__file__))}/logs/cmc_data_collector.log")

    def collect_data(self) -> None:
        params = {
            "coins": SYMBOL_ID_MAPPING[self.symbol],
            "page": "1",
            "size": 10
        }
        res = requests.get(self.base_url, params=params).json()
        cmc_news = res["data"]
        first_news_id = None
        for news in cmc_news:
            if news["meta"]["id"] == self.last_news_id:
                break

            print(news)
            if not first_news_id:
                first_news_id = news["meta"]["id"]

        if first_news_id:
            self.last_news_id = first_news_id

    def start(self) -> None:
        self.logger.info(f"Start collecting news for symbol {self.symbol}...")
        try:
            self.collect_data()
        except Exception as e:
            self.logger.error(f"{e}")

    def stop(self) -> None:
        self.logger.info(f"Stop collecting news for symbol {self.symbol}...")


class CMCPostsDataCollector(DataCollector):
    def __init__(self, symbol) -> None:
        super().__init__()
        self.symbol = symbol
        self.base_url = "https://api-gravity.coinmarketcap.com/gravity/v3/gravity/condition/query"
        # Last post id should be get from db
        self.last_post_id = None
        self.logger = get_logger(
            f"CMC {symbol} news data collector",
            f"{os.path.dirname(os.path.realpath(__file__))}/logs/cmc_data_collector.log")

    def collect_data(self) -> None:
        payload = {
            "cryptoId": SYMBOL_ID_MAPPING[self.symbol],
            "lastScore": int((datetime.now() - timedelta(hours=1)).timestamp() * 1000),
            "overView": False,
            "type": "ALL"
        }
        res = requests.post(self.base_url, json=payload).json()
        cmc_posts = res["data"]["tweetDTOList"]
        first_post_id = None
        for post in cmc_posts:
            if post["gravityId"] == self.last_post_id:
                break

            print(post)
            if not first_post_id:
                first_post_id = post["gravityId"]

        if first_post_id:
            self.last_post_id = first_post_id

    def start(self) -> None:
        self.logger.info(f"Start collecting news for symbol {self.symbol}...")
        try:
            self.collect_data()
        except Exception as e:
            self.logger.error(f"{e}")

    def stop(self) -> None:
        self.logger.info(f"Stop collecting news for symbol {self.symbol}...")
