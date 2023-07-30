import os
from pymongo import MongoClient
import requests
import json
from confluent_kafka import Producer

from applications.utils.logger import get_logger
from ..base_data_collector.data_collector import DataCollector
from .constants import (
    SYMBOL_ID_MAPPING, CMC_POSTS_KAFKA_TOPIC, CMC_NEWS_KAFKA_TOPIC
)
from .config import KAFKA_CONFIG, MONGO_DB_HOST

crypto_hub_db = MongoClient(MONGO_DB_HOST).get_database("crypto_hub")
check_point_collection = crypto_hub_db["cmc.checkpoints"]


class CMCNewsDataCollector(DataCollector):
    def __init__(self, symbol) -> None:
        super().__init__()
        self.symbol = symbol
        self.base_url = "https://api.coinmarketcap.com/content/v3/news/aggregated"
        self.last_news_id = self.get_last_news_id()
        self.producer = Producer(KAFKA_CONFIG)
        self.logger = get_logger(
            f"CMC {symbol} news data collector",
            f"{os.path.dirname(os.path.realpath(__file__))}/logs/cmc_data_collector.log")

    def get_last_news_id(self) -> str:
        check_point = check_point_collection.find_one({
            "symbol": self.symbol,
            "type": "news",
        })
        if not check_point:
            return ""
        return check_point["check_point"]

    def collect_data(self) -> None:
        params = {
            "coins": SYMBOL_ID_MAPPING[self.symbol],
            "page": "1",
            "size": 20
        }
        res = requests.get(self.base_url, params=params).json()
        cmc_news = res["data"]
        first_news_id = None
        for news in cmc_news:
            if news["meta"]["id"] == self.last_news_id:
                break
            if "updatedAt" not in news["meta"]:
                continue

            self.producer.produce(CMC_NEWS_KAFKA_TOPIC, json.dumps(news))
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
        self.producer.flush()
        self.logger.info("Saving checkpoint for CMC news...")
        check_point_collection.find_one_and_update(
            {
                "symbol": self.symbol,
                "type": "news",
            },
            {
                "$set": {"check_point": self.last_news_id}
            },
            upsert=True
        )
        self.logger.info(f"Stop collecting news for symbol {self.symbol}...")


class CMCPostsDataCollector(DataCollector):
    def __init__(self, symbol) -> None:
        super().__init__()
        self.symbol = symbol
        self.base_url = "https://api-gravity.coinmarketcap.com/gravity/v3/gravity/condition/query"
        self.last_post_id = self.get_last_post_id()
        self.producer = Producer(KAFKA_CONFIG)
        self.logger = get_logger(
            f"CMC {symbol} posts data collector",
            f"{os.path.dirname(os.path.realpath(__file__))}/logs/cmc_data_collector.log")

    def get_last_post_id(self) -> str:
        check_point = check_point_collection.find_one({
            "symbol": self.symbol,
            "type": "posts",
        })
        if not check_point:
            return ""
        return check_point["check_point"]

    def collect_data(self) -> None:
        payload = {
            "cryptoId": SYMBOL_ID_MAPPING[self.symbol],
            "overView": False,
            "type": "ALL"
        }
        res = requests.post(self.base_url, json=payload).json()
        cmc_posts = res["data"]["tweetDTOList"]
        first_post_id = None
        for post in cmc_posts:
            if post["gravityId"] == self.last_post_id:
                break
            if "textContent" not in post:
                continue

            self.producer.produce(CMC_POSTS_KAFKA_TOPIC, json.dumps(post))
            if not first_post_id:
                first_post_id = post["gravityId"]

        if first_post_id:
            self.last_post_id = first_post_id

    def start(self) -> None:
        self.logger.info(f"Start collecting posts for symbol {self.symbol}...")
        try:
            self.collect_data()
        except Exception as e:
            self.logger.error(f"{e}")

    def stop(self) -> None:
        self.producer.flush()
        self.logger.info("Saving checkpoint for CMC posts...")
        check_point_collection.find_one_and_update(
            {
                "symbol": self.symbol,
                "type": "posts",
            },
            {
                "$set": {"check_point": self.last_post_id}
            },
            upsert=True
        )
        self.logger.info(f"Stop collecting posts for symbol {self.symbol}...")
