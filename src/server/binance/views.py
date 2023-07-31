import copy
from flask import Blueprint
from flask_apispec import marshal_with

from .schemas import (
    PriceChangeResponseSchema, KlinesResponseSchema,
    Symbol24HStatsResponseSchema
)
from server.services.mongodb import crypto_hub_db

binance_bp = Blueprint("binance_bp", __name__)


@binance_bp.route("/price-change", methods=["GET"])
@marshal_with(PriceChangeResponseSchema)
def get_price_change():
    response = {"models": []}
    query = [
        {"$sort": {"stats_close_time": -1}},
        {
            "$group": {
                "_id": "$symbol",
                "latest_last_price": {"$first": "$last_price"},
                "latest_price_change_percent": {"$first": "$price_change_percent"},
                "latest_stats_close_time": {"$first": "$stats_close_time"},
            },
        },
        {
            "$project": {
                "_id": 0,
                "symbol": "$_id",
                "last_price": "$latest_last_price",
                "price_change_percent": "$latest_price_change_percent",
            },
        },
        {"$sort": {"symbol": 1}},
    ]

    docs = crypto_hub_db["binance.stream.24h_ticker"].aggregate(query)

    for doc in docs:
        response["models"].append(doc)
    return response


@binance_bp.route("/klines/<symbol>/<interval>", methods=["GET"])
@marshal_with(KlinesResponseSchema)
def get_symbol_klines(symbol, interval):
    limit = 99
    response = {}
    models = []
    query = {
        "symbol": symbol,
        "is_closed": True
    }

    projection = {
        "start_time": 1, "open_price": 1,
        "high_price": 1, "low_price": 1,
        "close_price": 1, "base_asset_vol": 1,
        "_id": 0
    }
    stream_query = copy.deepcopy(query)
    stream_cursor = crypto_hub_db["binance.stream.klines." + interval]
    batch_cursor = crypto_hub_db["binance.klines." + interval]

    latest_batch_doc = batch_cursor.find_one(query, sort=[("start_time", -1)])
    stream_query["start_time"] = {"$gt": latest_batch_doc["start_time"]}

    models.extend(stream_cursor.find(stream_query, projection)
                  .sort([("start_time", -1)]).limit(limit))

    if len(models) < limit:
        limit = limit - len(models)
        models.extend(batch_cursor.find(query, projection)
                      .sort([("start_time", -1)]).limit(limit))

    stream_query.pop("is_closed")
    models.reverse()
    last_candle = stream_cursor.find_one(stream_query, projection, sort=[("last_trade_id", -1)])
    models.append(last_candle)
    response["models"] = models

    return response


@binance_bp.route("/<symbol>/24h-stats", methods=["GET"])
@marshal_with(Symbol24HStatsResponseSchema)
def get_symbol_24h_stats(symbol):
    response = None
    query = {
        "symbol": symbol,
    }

    projection = {
        "last_price": 1, "price_change": 1,
        "price_change_percent": 1, "high_price": 1,
        "low_price": 1, "base_asset_vol": 1,
        "quote_asset_vol": 1, "_id": 0
    }
    stream_cursor = crypto_hub_db["binance.stream.24h_ticker"]

    docs = stream_cursor.find(query, projection).sort([("stats_close_time", -1)])

    for doc in docs:
        if not response:
            response = doc
        else:
            response["last_price_state"] = "bullish" if response["last_price"] > doc["last_price"] else "bearish"
            break

    return response
