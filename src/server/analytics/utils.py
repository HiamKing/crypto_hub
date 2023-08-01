from typing import List, Dict, Any
from datetime import datetime


def get_statistics_post_pipeline(symbol: str, start_time: datetime, end_time: datetime, granularity: str) -> List[Dict[str, Any]]:
    if granularity == "hour":
        time_format = "%Y-%m-%d %H:00:00"
    elif granularity == "day":
        time_format = "%Y-%m-%d 00:00:00"
    elif granularity == "month":
        time_format = "%Y-%m-01 00:00:00"

    pipeline = [
        {
            # Filter documents within the specified time range
            "$match": {
                "post_time": {
                    "$gte": start_time,
                    "$lte": end_time
                },
                "symbol": symbol
            }
        },
        {
            # Group by hour and count documents in each group
            "$group": {
                "_id": {
                    "stats_time": {
                        "$dateToString": {
                            "format": time_format,
                            "date": "$post_time",
                            "timezone": "UTC"
                        }
                    }
                },
                "posts_count": {"$sum": 1}
            }
        },
        {
            # Project to rename fields and format the hour
            "$project": {
                "_id": 0,
                "stats_time": {
                    "$dateFromString": {
                        "dateString": "$_id.stats_time",
                        "timezone": "UTC"
                    }
                },
                "posts_count": 1
            }
        },
        {
            # Sort by hour
            "$sort": {"stats_time": 1}
        }
    ]

    return pipeline


def get_statistics_news_pipeline(coin_name: str, start_time: datetime, end_time: datetime, granularity: str) -> List[Dict[str, Any]]:
    if granularity == "hour":
        time_format = "%Y-%m-%d %H:00:00"
    elif granularity == "day":
        time_format = "%Y-%m-%d 00:00:00"
    elif granularity == "month":
        time_format = "%Y-%m-01 00:00:00"

    pipeline = [
        {
            # Filter documents within the specified time range
            "$match": {
                "updated_at": {
                    "$gte": start_time,
                    "$lte": end_time
                },
                "coin_name": coin_name
            }
        },
        {
            # Group by hour and count documents in each group
            "$group": {
                "_id": {
                    "stats_time": {
                        "$dateToString": {
                            "format": time_format,
                            "date": "$updated_at",
                            "timezone": "UTC"
                        }
                    }
                },
                "news_count": {"$sum": 1}
            }
        },
        {
            # Project to rename fields and format the hour
            "$project": {
                "_id": 0,
                "stats_time": {
                    "$dateFromString": {
                        "dateString": "$_id.stats_time",
                        "timezone": "UTC"
                    }
                },
                "news_count": 1
            }
        },
        {
            # Sort by hour
            "$sort": {"stats_time": 1}
        }
    ]

    return pipeline


def get_symbol_price_pipeline(coin_name: str, start_time: datetime, end_time: datetime, granularity: str) -> List[Dict[str, Any]]:
    if granularity == "hour":
        time_format = "%Y-%m-%d %H:00:00"
    elif granularity == "day":
        time_format = "%Y-%m-%d 00:00:00"
    elif granularity == "month":
        time_format = "%Y-%m-01 00:00:00"

    pipeline = [
        {
            # Filter documents within the specified time range
            "$match": {
                "stats_close_time": {
                    "$gte": start_time,
                    "$lte": end_time
                },
                "symbol": coin_name
            }
        },
        {
            '$group': {
                '_id': {
                    '$dateToString': {
                        'format': time_format,  # Format for grouping by hour
                        'date': '$stats_close_time'
                    }
                },
                'last_price': {
                    '$last': '$last_price'
                }
            }
        },
        {
            # Project to rename fields and format the hour
            "$project": {
                "_id": 0,
                "stats_time": {
                    "$dateFromString": {
                        "dateString": "$_id",
                        "timezone": "UTC"
                    }
                },
                "last_price": 1
            }
        }
    ]

    return pipeline
