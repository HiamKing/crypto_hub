import os
import json
import time
import snscrape.modules.twitter as snstwitter

from ..base_data_collector.data_collector import DataCollector
from .constants import SYMBOL_LIST, MAX_PULL_TWEETS, CRAWL_INTERVAL
from utils.logger import get_logger


class TwitterDataCollector(DataCollector):
    def __init__(self) -> None:
        super().__init__()
        self.twitter_crawler = snstwitter.TwitterSearchScraper(self.build_twitter_query())
        # Last news should be get from db
        self.last_tweet_id = None
        self.logger = get_logger(
            "Twitter data collector",
            f"{os.path.dirname(os.path.realpath(__file__))}/logs/twitter_data_collector.log")

    def build_twitter_query(self) -> str:
        symbols = " OR #".join(SYMBOL_LIST)
        query = "(#" + symbols + ")"
        return query

    def collect_data(self) -> None:
        cnt = 0
        first_tweet_id = None
        for tweet in self.twitter_crawler.get_items():
            parsed_tweet = json.loads(tweet.json())
            cnt += 1
            if parsed_tweet["id"] == self.last_tweet_id:
                break

            # Process message here
            print(parsed_tweet["content"])
            if not first_tweet_id:
                first_tweet_id = parsed_tweet["id"]
            if cnt == MAX_PULL_TWEETS:
                break

        if first_tweet_id:
            self.last_tweet_id = first_tweet_id
        # Update metrics here...............................

    def start(self) -> None:
        self.logger.info("Start collecting Twitter data...")
        try:
            while True:
                self.collect_data()
                print("-" * 150)
                time.sleep(CRAWL_INTERVAL)
        except Exception as e:
            self.logger.error(f"{e}")

    def stop(self) -> None:
        self.logger.info("Stop collecting Twitter data...")
