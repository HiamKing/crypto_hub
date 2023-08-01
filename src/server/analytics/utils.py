from typing import List, Dict, Any
from datetime import datetime


def get_statistics_post_pipeline(symbol: str, start_time: datetime, end_time: datetime, granularity: str) -> List[Dict[str, Any]]:
    if granularity == "hour":
        start_time = start_time.replace(minute=0, second=0)
        end_time = end_time.replace(minute=59, second=59)
        format = "%Y-%m-%d %H:00:00"
    elif granularity == "day":
        start_time = start_time.replace(hour=0, minute=0, second=0)
        end_time = end_time.replace(hour=23, minute=59, second=59)
        format = "%Y-%m-%d 00:00:00"
    elif granularity == "month":
        start_time = start_time.replace(day=1, hour=0, minute=0, second=0)
        end_time = end_time.replace(day=31, hour=23, minute=59, second=59)
        format = "%Y-%m-01 00:00:00"

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
                            "format": format,
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
        start_time = start_time.replace(minute=0, second=0)
        end_time = end_time.replace(minute=59, second=59)
        format = "%Y-%m-%d %H:00:00"
    elif granularity == "day":
        start_time = start_time.replace(hour=0, minute=0, second=0)
        end_time = end_time.replace(hour=23, minute=59, second=59)
        format = "%Y-%m-%d 00:00:00"
    elif granularity == "month":
        start_time = start_time.replace(day=1, hour=0, minute=0, second=0)
        end_time = end_time.replace(day=31, hour=23, minute=59, second=59)
        format = "%Y-%m-01 00:00:00"

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
                            "format": format,
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
