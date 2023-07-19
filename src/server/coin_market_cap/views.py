from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with

from .schemas import SearchPostsResponseSchema
from server.schemas import SearchSchema
from server.services.mongodb import crypto_hub_db

cmc_bp = Blueprint("cmc_bp", __name__)

@cmc_bp.route("/post", methods=["POST"])
@use_kwargs(args=SearchSchema, location="json")
@marshal_with(SearchPostsResponseSchema)
def get_post(filters, limit, offser, with_count, sort_by):
    response = {}

    if with_count:
        response["count"] = crypto_hub_db["cmc.posts"].count_documents()

    return response
