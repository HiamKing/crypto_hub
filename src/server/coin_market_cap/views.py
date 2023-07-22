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
    stream_filters = copy.deepcopy(filters)
    models = []
    latest_batch_post = list(crypto_hub_db[CMC_POSTS_COLLECTION].find(filters).sort([("post_time", -1)]).limit(1))
    if ("post_time" not in stream_filters or "$gte" not in stream_filters["post_time"]) and len(latest_batch_post):
        if "post_time" not in stream_filters:
            stream_filters["post_time"] = {}
        stream_filters["post_time"]["$gt"] = latest_batch_post[0]["post_time"]

    stream_posts_count = crypto_hub_db[CMC_STREAM_POSTS_COLLECTION].count_documents(stream_filters)
    if offset < stream_posts_count:
        models.extend(crypto_hub_db[CMC_STREAM_POSTS_COLLECTION].find(stream_filters)
                      .sort([("post_time", -1)])
                      .limit(limit).skip(offset))
        limit = limit - len(models)
        offset = 0
    else:
        offset = offset - stream_posts_count

    if limit > 0:
        models.extend(crypto_hub_db[CMC_POSTS_COLLECTION].find(filters)
                      .sort([("post_time", -1)])
                      .limit(limit).skip(offset))

    response["models"] = models
    if with_count:
        response["count"] = crypto_hub_db[CMC_POSTS_COLLECTION].count_documents(filters) + stream_posts_count

    return response
