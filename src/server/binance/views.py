from flask import Blueprint
from flask_apispec import marshal_with

from .schemas import (
    PriceChangeResponseSchema
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
