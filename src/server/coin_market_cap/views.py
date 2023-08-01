import copy
from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from datetime import datetime

from .schemas import SearchPostsResponseSchema, SearchNewsResponseSchema
from .constants import (
    CMC_POSTS_COLLECTION, CMC_STREAM_POSTS_COLLECTION,
    CMC_NEWS_COLLECTION, CMC_STREAM_NEWS_COLLECTION
)
from server.schemas import SearchSchema
from server.services.mongodb import crypto_hub_db

cmc_bp = Blueprint("cmc_bp", __name__)


@cmc_bp.route("/search-posts", methods=["POST"])
@use_kwargs(args=SearchSchema, location="json")
@marshal_with(SearchPostsResponseSchema)
def search_posts(filters, limit, offset, with_count, sort_by):
    response = {}
    if "post_time" in filters:
        for key, val in filters["post_time"].items():
            filters["post_time"][key] = datetime.fromisoformat(val.replace("Z", ""))
    if "text_content" in filters:
        filters["text_content"] = filters["text_content"].replace("$", "\$")
        filters["text_content"] = {"$regex": f"{filters['text_content']}"}
    stream_filters = copy.deepcopy(filters)
    models = []
    latest_batch_post = crypto_hub_db[CMC_POSTS_COLLECTION].find_one(filters, sort=[(sort_by, -1)])
    if "post_time" not in stream_filters:
        stream_filters["post_time"] = {}
    if "$gte" not in stream_filters["post_time"] or (latest_batch_post and latest_batch_post["post_time"] > stream_filters["post_time"]["$gte"]):
        stream_filters["post_time"]["$gt"] = latest_batch_post["post_time"]

    stream_cursor = crypto_hub_db[CMC_STREAM_POSTS_COLLECTION]
    batch_cursor = crypto_hub_db[CMC_POSTS_COLLECTION]
    stream_posts_count = stream_cursor.count_documents(stream_filters)

    if with_count:
        response["count"] = batch_cursor.count_documents(filters) + stream_posts_count

    if offset < stream_posts_count:
        models.extend(stream_cursor.find(stream_filters)
                                   .sort([(sort_by, -1)])
                                   .limit(limit).skip(offset))
        limit = limit - len(models)
        offset = 0
    else:
        offset = offset - stream_posts_count

    if limit > 0:
        models.extend(batch_cursor.find(filters)
                                  .sort([(sort_by, -1)])
                                  .limit(limit).skip(offset))

    response["models"] = models
    return response


@cmc_bp.route("/search-news", methods=["POST"])
@use_kwargs(args=SearchSchema, location="json")
@marshal_with(SearchNewsResponseSchema)
def search_news(filters, limit, offset, with_count, sort_by):
    response = {}
    if "updated_at" in filters:
        for key, val in filters["updated_at"].items():
            filters["updated_at"][key] = datetime.fromisoformat(val.replace("Z", ""))
    if "title" in filters:
        filters["title"] = filters["title"].replace("$", "\$")
        filters["title"] = {"$regex": f"{filters['title']}"}
    stream_filters = copy.deepcopy(filters)
    models = []
    latest_batch_news = crypto_hub_db[CMC_NEWS_COLLECTION].find_one(filters, sort=[(sort_by, -1)])
    if "updated_at" not in stream_filters:
        stream_filters["updated_at"] = {}
    if "$gte" not in stream_filters["updated_at"] or (latest_batch_news and latest_batch_news["updated_at"] > stream_filters["updated_at"]["$gte"]):
        stream_filters["updated_at"]["$gt"] = latest_batch_news["updated_at"]

    stream_cursor = crypto_hub_db[CMC_STREAM_NEWS_COLLECTION]
    batch_cursor = crypto_hub_db[CMC_NEWS_COLLECTION]
    stream_news_count = stream_cursor.count_documents(stream_filters)

    if with_count:
        response["count"] = batch_cursor.count_documents(filters) + stream_news_count

    if offset < stream_news_count:
        models.extend(stream_cursor.find(stream_filters)
                                   .sort([(sort_by, -1)])
                                   .limit(limit).skip(offset))
        limit = limit - len(models)
        offset = 0
    else:
        offset = offset - stream_news_count

    if limit > 0:
        models.extend(batch_cursor.find(filters)
                                  .sort([(sort_by, -1)])
                                  .limit(limit).skip(offset))

    response["models"] = models
    return response
