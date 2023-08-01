from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from datetime import datetime, timedelta

from .utils import get_statistics_post_pipeline, get_statistics_news_pipeline
from .schemas import (
    AnalyticsSearch, StatisticsResponseSchema
)
from .constants import (
    CMC_NEWS_ASSOC_COLLECTION, CMC_STREAM_NEWS_ASSOC_COLLECTION,
    CMC_POSTS_ASSOC_COLLECTION, CMC_STREAM_POSTS_ASSOC_COLLECTION,
    COIN_NAME_MAPPING
)
from server.services.mongodb import crypto_hub_db

analytics_bp = Blueprint("analytics_bp", __name__)


@analytics_bp.route("/search-statistics", methods=["POST"])
@use_kwargs(args=AnalyticsSearch, location="json")
@marshal_with(StatisticsResponseSchema)
def search_statistics(symbol, start_time, end_time, granularity):
    response = {}
    posts_series = []
    news_series = []
    start_time = datetime.fromisoformat(start_time.replace("Z", ""))
    end_time = datetime.fromisoformat(end_time.replace("Z", ""))

    batch_pipeline = get_statistics_post_pipeline(symbol, start_time, end_time, granularity)
    latest_batch_post = crypto_hub_db[CMC_POSTS_ASSOC_COLLECTION].find_one(
        {"symbol": symbol}, sort=[("post_time", -1)])
    stream_start_time = start_time if start_time > latest_batch_post["post_time"] else latest_batch_post["post_time"] + timedelta(minutes=1)
    stream_end_time = end_time
    stream_pipeline = get_statistics_post_pipeline(symbol, stream_start_time, stream_end_time, granularity)
    posts_series.extend(crypto_hub_db[CMC_STREAM_POSTS_ASSOC_COLLECTION].aggregate(stream_pipeline))
    batch_posts_series = list(crypto_hub_db[CMC_POSTS_ASSOC_COLLECTION].aggregate(batch_pipeline))
    posts_series_dict = {val["stats_time"].strftime("%Y-%m-%d %H:%M:%S"): val["posts_count"] for val in posts_series}
    for val in batch_posts_series:
        if val["stats_time"].strftime("%Y-%m-%d %H:%M:%S") in posts_series_dict:
            posts_series_dict[val["stats_time"].strftime("%Y-%m-%d %H:%M:%S")] += val["posts_count"]
        else:
            posts_series_dict[val["stats_time"].strftime("%Y-%m-%d %H:%M:%S")] = val["posts_count"]

    posts_series = [{"stats_time": key, "posts_count": val} for key, val in posts_series_dict.items()]
    posts_series.sort(key=lambda x: x["stats_time"])

    coin_name = COIN_NAME_MAPPING[symbol]
    batch_pipeline = get_statistics_news_pipeline(coin_name, start_time, end_time, granularity)
    latest_batch_news = crypto_hub_db[CMC_NEWS_ASSOC_COLLECTION].find_one(
        {"coin_name": coin_name}, sort=[("updated_at", -1)])
    stream_start_time = start_time if start_time > latest_batch_news["updated_at"] else latest_batch_news["updated_at"] + timedelta(minutes=1)
    stream_end_time = end_time
    stream_pipeline = get_statistics_news_pipeline(coin_name, stream_start_time, stream_end_time, granularity)
    news_series.extend(crypto_hub_db[CMC_STREAM_NEWS_ASSOC_COLLECTION].aggregate(stream_pipeline))
    batch_news_series = list(crypto_hub_db[CMC_NEWS_ASSOC_COLLECTION].aggregate(batch_pipeline))
    news_series_dict = {val["stats_time"].strftime("%Y-%m-%d %H:%M:%S"): val["news_count"] for val in news_series}
    for val in batch_news_series:
        if val["stats_time"].strftime("%Y-%m-%d %H:%M:%S") in news_series_dict:
            news_series_dict[val["stats_time"].strftime("%Y-%m-%d %H:%M:%S")] += val["news_count"]
        else:
            news_series_dict[val["stats_time"].strftime("%Y-%m-%d %H:%M:%S")] = val["news_count"]

    news_series = [{"stats_time": key, "news_count": val} for key, val in news_series_dict.items()]
    news_series.sort(key=lambda x: x["stats_time"])

    response["posts_series"] = posts_series
    response["news_series"] = news_series
    return response
