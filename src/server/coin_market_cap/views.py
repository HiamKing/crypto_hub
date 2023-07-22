import copy
from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with

from .schemas import SearchPostsResponseSchema
from .constants import CMC_POSTS_COLLECTION, CMC_STREAM_POSTS_COLLECTION
from server.schemas import SearchSchema
from server.services.mongodb import crypto_hub_db

cmc_bp = Blueprint("cmc_bp", __name__)


@cmc_bp.route("/search-posts", methods=["POST"])
@use_kwargs(args=SearchSchema, location="json")
@marshal_with(SearchPostsResponseSchema)
def search_post(filters, limit, offset, with_count, sort_by):
    response = {}
    if "text_content" in filters:
        filters["text_content"] = {"$regex": f"\${filters['text_content']}"}
    stream_filters = copy.deepcopy(filters)
    models = []
    latest_batch_post = list(crypto_hub_db[CMC_POSTS_COLLECTION].find(filters).sort([("post_time", -1)]).limit(1))
    if ("post_time" not in stream_filters or "$gte" not in stream_filters["post_time"]) and len(latest_batch_post):
        if "post_time" not in stream_filters:
            stream_filters["post_time"] = {}
        stream_filters["post_time"]["$gt"] = latest_batch_post[0]["post_time"]

    stream_cursor = crypto_hub_db[CMC_STREAM_POSTS_COLLECTION]
    batch_cursor = crypto_hub_db[CMC_POSTS_COLLECTION]
    stream_posts_count = stream_cursor.count_documents(stream_filters)

    if with_count:
        response["count"] = batch_cursor.count_documents(filters) + stream_posts_count

    if offset < stream_posts_count:
        models.extend(stream_cursor.find(stream_filters)
                                   .sort([("post_time", -1)])
                                   .limit(limit).skip(offset))
        limit = limit - len(models)
        offset = 0
    else:
        offset = offset - stream_posts_count

    if limit > 0:
        models.extend(batch_cursor.find(filters)
                                  .sort([("post_time", -1)])
                                  .limit(limit).skip(offset))

    response["models"] = models
    return response
