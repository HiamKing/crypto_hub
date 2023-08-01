import copy
from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from datetime import datetime

from .schemas import (
    AnalyticsSearch, StatisticsResponseSchema
)
from server.services.mongodb import crypto_hub_db

analytics_bp = Blueprint("analytics_bp", __name__)


@analytics_bp.route("/search-statistics", methods=["POST"])
@use_kwargs(args=AnalyticsSearch, location="json")
@marshal_with(StatisticsResponseSchema)
def search_news(symbol, start_time, end_time, granularity):
    response = {}
    models = []
    start_time = datetime.fromisoformat(start_time.replace("Z", ""))
    end_time = datetime.fromisoformat(end_time.replace("Z", ""))
    
    response["models"] = models
    return response
