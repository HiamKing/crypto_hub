CMC_POSTS_KAFKA_TOPIC = "cmc.posts"
CMC_NEWS_KAFKA_TOPIC = "cmc.news"
FE_CMC_POSTS_KAFKA_TOPIC = "cmc.posts.file_event"
FE_CMC_NEWS_KAFKA_TOPIC = "cmc.news.file_event"

FE_TOPIC_MAPPING = {
    CMC_POSTS_KAFKA_TOPIC: FE_CMC_POSTS_KAFKA_TOPIC,
    CMC_NEWS_KAFKA_TOPIC: FE_CMC_NEWS_KAFKA_TOPIC,
}

MAX_FILE_SIZE = 5242880  # 5 mb

NEWS_FIELDS_MAPPING = {
    "slug": {"name": "slug", "type": "string"},
    "cover": {"name": "cover", "type": "string"},
    "assets": {"name": "assets", "type": "array"},
    "name": {"name": "name", "type": "string"},
    "coinId": {"name": "coin_id", "type": "int"},
    "type": {"name": "type", "type": "string"},
    "createdAt": {"name": "created_at", "type": "string"},
    "meta": {"name": "meta", "type": "dict"},
    "title": {"name": "title", "type": "string"},
    "subtitle": {"name": "subtitle", "type": "string"},
    "sourceName": {"name": "source_name", "type": "string"},
    "maxChar": {"name": "max_char", "type": "int"},
    "language": {"name": "language", "type": "string"},
    "status": {"name": "status", "type": "string"},
    "visibility": {"name": "visibility", "type": "boolean"},
    "sourceUrl": {"name": "source_url", "type": "string"},
    "id": {"name": "id", "type": "string"},
    "views": {"name": "views", "type": "long"},
    "updatedAt": {"name": "updated_at", "type": "string"},
    "releasedAt": {"name": "released_at", "type": "string"}
}

POSTS_FIELDS_MAPPING = {
    "gravityId": {"name": "gravity_id", "type": "string"},
    "owner": {"name": "owner", "type": "dict"},
    "nickname": {"name": "nickname", "type": "string"},
    "handle": {"name": "handle", "type": "string"},
    "avatarId": {"name": "avatar_id", "type": "string"},
    "createdTime": {"name": "created_time", "type": "long"},
    "lastUpdateNickname": {"name": "last_update_nickname", "type": "long"},
    "avatar": {"name": "avatar", "type": "dict"},
    "url": {"name": "url", "type": "string"},
    "vip": {"name": "vip", "type": "boolean"},
    "guid": {"name": "guid", "type": "string"},
    "rootId": {"name": "root_id", "type": "string"},
    "textContent": {"name": "text_content", "type": "string"},
    "commentCount": {"name": "comment_count", "type": "int"},
    "likeCount": {"name": "like_count", "type": "int"},
    "reactions": {"name": "reactions", "type": "array"},
    "type": {"name": "type", "type": "int"},
    "count": {"name": "count", "type": "int"},
    "postTime": {"name": "post_time", "type": "long"},
    "topics": {"name": "topics", "type": "array"},
    "currencies": {"name": "currencies", "type": "array"},
    "id": {"name": "id", "type": "int"},
    "symbol": {"name": "symbol", "type": "string"},
    "slug": {"name": "slug", "type": "string"},
    "bullish": {"name": "bullish", "type": "boolean"},
    "repostCount": {"name": "repost_count", "type": "int"},
    "languageCode": {"name": "language_code", "type": "string"}
}
