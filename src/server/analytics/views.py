from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from datetime import datetime, timedelta

from .utils import get_statistics_post_pipeline, get_statistics_news_pipeline, get_symbol_price_pipeline
from .schemas import (
    AnalyticsSearch, StatisticsResponseSchema, RelationsResponseSchema
)
from .constants import (
    CMC_NEWS_ASSOC_COLLECTION, CMC_STREAM_NEWS_ASSOC_COLLECTION,
    CMC_POSTS_ASSOC_COLLECTION, CMC_STREAM_POSTS_ASSOC_COLLECTION,
    COIN_NAME_MAPPING, TIME_FORMAT, BINANCE_STREAM_TICKER_INFO, BINANCE_TICKER_INFO
)
from server.services.mongodb import crypto_hub_db

analytics_bp = Blueprint("analytics_bp", __name__)


def get_statistics(symbol, start_time, end_time, granularity):
    result = {}
    start_time = datetime.fromisoformat(start_time.replace("Z", ""))
    end_time = datetime.fromisoformat(end_time.replace("Z", ""))

    batch_pipeline = get_statistics_post_pipeline(symbol, start_time, end_time, granularity)
    latest_batch_post = crypto_hub_db[CMC_POSTS_ASSOC_COLLECTION].find_one(
        {"symbol": symbol}, sort=[("post_time", -1)])
    stream_start_time = start_time if start_time > latest_batch_post["post_time"] else latest_batch_post["post_time"] + timedelta(minutes=1)
    stream_end_time = end_time
    stream_pipeline = get_statistics_post_pipeline(symbol, stream_start_time, stream_end_time, granularity)
    stream_posts_series = list(crypto_hub_db[CMC_STREAM_POSTS_ASSOC_COLLECTION].aggregate(stream_pipeline))
    batch_posts_series = list(crypto_hub_db[CMC_POSTS_ASSOC_COLLECTION].aggregate(batch_pipeline))
    posts_series_dict = {val["stats_time"].strftime(TIME_FORMAT): val["posts_count"] for val in stream_posts_series}
    for val in batch_posts_series:
        if val["stats_time"].strftime(TIME_FORMAT) in posts_series_dict:
            posts_series_dict[val["stats_time"].strftime(TIME_FORMAT)] += val["posts_count"]
        else:
            posts_series_dict[val["stats_time"].strftime(TIME_FORMAT)] = val["posts_count"]

    coin_name = COIN_NAME_MAPPING[symbol]
    batch_pipeline = get_statistics_news_pipeline(coin_name, start_time, end_time, granularity)
    latest_batch_news = crypto_hub_db[CMC_NEWS_ASSOC_COLLECTION].find_one(
        {"coin_name": coin_name}, sort=[("updated_at", -1)])
    stream_start_time = start_time if start_time > latest_batch_news["updated_at"] else latest_batch_news["updated_at"] + timedelta(minutes=1)
    stream_end_time = end_time
    stream_pipeline = get_statistics_news_pipeline(coin_name, stream_start_time, stream_end_time, granularity)
    stream_news_series = list(crypto_hub_db[CMC_STREAM_NEWS_ASSOC_COLLECTION].aggregate(stream_pipeline))
    batch_news_series = list(crypto_hub_db[CMC_NEWS_ASSOC_COLLECTION].aggregate(batch_pipeline))
    news_series_dict = {val["stats_time"].strftime(TIME_FORMAT): val["news_count"] for val in stream_news_series}
    for val in batch_news_series:
        if val["stats_time"].strftime(TIME_FORMAT) in news_series_dict:
            news_series_dict[val["stats_time"].strftime(TIME_FORMAT)] += val["news_count"]
        else:
            news_series_dict[val["stats_time"].strftime(TIME_FORMAT)] = val["news_count"]

    stats_series_dict = {key: {"posts_count": val} for key, val in posts_series_dict.items()}
    for key, val in news_series_dict.items():
        if key not in stats_series_dict:
            stats_series_dict[key] = {"news_count": val}
        else:
            stats_series_dict[key]["news_count"] = val
    for key in stats_series_dict:
        if "news_count" not in stats_series_dict[key]:
            stats_series_dict[key]["news_count"] = 0
        if "posts_count" not in stats_series_dict[key]:
            stats_series_dict[key]["posts_count"] = 0
    stats_series = [[key, val["posts_count"], val["news_count"]] for key, val in stats_series_dict.items()]

    result["models"] = stats_series

    return result


@analytics_bp.route("/search-statistics", methods=["POST"])
@use_kwargs(args=AnalyticsSearch, location="json")
@marshal_with(StatisticsResponseSchema)
def search_statistics(symbol, start_time, end_time, granularity):
    response = get_statistics(symbol, start_time, end_time, granularity)
    return response


@analytics_bp.route("/search-relations", methods=["POST"])
@use_kwargs(args=AnalyticsSearch, location="json")
@marshal_with(RelationsResponseSchema)
def search_relations(symbol, start_time, end_time, granularity):
    response = {}
    str_start_time = start_time
    str_end_time = end_time
    symbol_split = symbol.split("/")
    base_symbol = symbol_split[0]
    quote_symbol = symbol_split[1]
    symbol = symbol.replace("/", "")

    start_time = datetime.fromisoformat(start_time.replace("Z", ""))
    end_time = datetime.fromisoformat(end_time.replace("Z", ""))
    batch_pipeline = get_symbol_price_pipeline(symbol, start_time, end_time, granularity)
    latest_batch_price = crypto_hub_db[BINANCE_TICKER_INFO].find_one(
        {"symbol": symbol}, sort=[("stats_close_time", -1)])
    stream_start_time = start_time if start_time > latest_batch_price["stats_close_time"] else latest_batch_price["stats_close_time"] + timedelta(minutes=1)
    stream_end_time = end_time
    stream_pipeline = get_symbol_price_pipeline(symbol, stream_start_time, stream_end_time, granularity)
    stream_price_series = list(crypto_hub_db[BINANCE_STREAM_TICKER_INFO].aggregate(stream_pipeline))
    batch_price_series = list(crypto_hub_db[BINANCE_TICKER_INFO].aggregate(batch_pipeline))
    price_series_dict = {val["stats_time"].strftime(TIME_FORMAT): val["last_price"] for val in stream_price_series}
    for val in batch_price_series:
        if val["stats_time"].strftime(TIME_FORMAT) not in price_series_dict:
            price_series_dict[val["stats_time"].strftime(TIME_FORMAT)] = val["last_price"]

    base_stats = get_statistics(base_symbol, str_start_time, str_end_time, granularity)
    quote_stats = get_statistics(quote_symbol, str_start_time, str_end_time, granularity)
    base_series = base_stats["models"]
    quote_series = quote_stats["models"]
    for idx, val in enumerate(base_series):
        if val[0] in price_series_dict:
            base_series[idx] = [val[0], price_series_dict[val[0]]] + val[1:]
        else:
            base_series[idx] = [val[0], 0] + val[1:]

    for idx, val in enumerate(quote_series):
        if val[0] in price_series_dict:
            quote_series[idx] = [val[0], price_series_dict[val[0]]] + val[1:]
        else:
            quote_series[idx] = [val[0], 0] + val[1:]

    base_series.sort(key=lambda r: r[0])
    quote_series.sort(key=lambda r: r[0])
    response["base_series"] = base_series
    response["quote_series"] = quote_series

    return response
