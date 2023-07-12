import json

# Note: This is avro file schema. All parent fields and nested fields need to have different names

KLINES_FILE_SCHEMA = json.dumps({
    "type": "record",
    "name": "KlinesEvent",
    "fields": [
        {"name": "event_type", "type": "string"},
        {"name": "event_time", "type": "long"},
        {"name": "symbol", "type": "string"},
        {"name": "kline", "type": {
            "type": "record",
            "name": "KlinesData",
            "fields": [
                {"name": "start_time", "type": "long"},
                {"name": "close_time", "type": "long"},
                {"name": "symbol", "type": "string"},
                {"name": "interval", "type": "string"},
                {"name": "first_trade_id", "type": "long"},
                {"name": "last_trade_id", "type": "long"},
                {"name": "open_price", "type": "double"},
                {"name": "close_price", "type": "double"},
                {"name": "high_price", "type": "double"},
                {"name": "low_price", "type": "double"},
                {"name": "base_asset_vol", "type": "double"},
                {"name": "number_of_trade", "type": "long"},
                {"name": "is_closed", "type": "boolean"},
                {"name": "quote_asset_vol", "type": "double"},
                {"name": "buy_base_asset_vol", "type": "double"},
                {"name": "buy_quote_asset_vol", "type": "double"}
            ]
        }}
    ]
})

TICKER_INFO_FILE_SCHEMA = json.dumps({
    "type": "record",
    "name": "TickerInfoEvent",
    "fields": [
        {"name": "event_type", "type": "string"},
        {"name": "event_time", "type": "long"},
        {"name": "symbol", "type": "string"},
        {"name": "price_change", "type": "double"},
        {"name": "price_change_percent", "type": "double"},
        {"name": "weighted_avg_price", "type": "double"},
        {"name": "first_trade_price", "type": "double"},
        {"name": "last_price", "type": "double"},
        {"name": "last_quantity", "type": "double"},
        {"name": "best_bid_price", "type": "double"},
        {"name": "best_bid_quantity", "type": "double"},
        {"name": "best_ask_price", "type": "double"},
        {"name": "best_ask_quantity", "type": "double"},
        {"name": "open_price", "type": "double"},
        {"name": "high_price", "type": "double"},
        {"name": "low_price", "type": "double"},
        {"name": "base_asset_vol", "type": "double"},
        {"name": "quote_asset_vol", "type": "double"},
        {"name": "stats_open_time", "type": "long"},
        {"name": "stats_close_time", "type": "long"},
        {"name": "first_trade_id", "type": "long"},
        {"name": "last_trade_id", "type": "long"},
        {"name": "number_of_trade", "type": "long"}
    ]
})

CMC_NEWS_SCHEMA = json.dumps({
    "type": "record",
    "name": "CMCNews",
    "fields": [
        {"name": "slug", "type": "string"},
        {"name": "cover", "type": "string"},
        {"name": "assets", "type": {
            "type": "array",
            "items": {
                "type": "record",
                "name": "NewsAssets",
                "fields": [
                    {"name": "name", "type": "string"},
                    {"name": "coin_id", "type": "int"},
                    {"name": "type", "type": "string"}
                ]
            }
        }},
        {"name": "created_at", "type": "string"},
        {"name": "meta", "type": {
            "type": "record",
            "name": "CMCNewsMeta",
            "fields": [
                {"name": "title", "type": "string"},
                {"name": "subtitle", "type": "string"},
                {"name": "source_name", "type": "string"},
                {"name": "max_char", "type": "int"},
                {"name": "language", "type": "string"},
                {"name": "status", "type": "string"},
                {"name": "type", "type": "string"},
                {"name": "visibility", "type": "boolean"},
                {"name": "source_url", "type": "string"},
                {"name": "id", "type": "string"},
                {"name": "views", "type": "long"},
                {"name": "created_at", "type": "string"},
                {"name": "updated_at", "type": "string"},
                {"name": "released_at", "type": "string"}
            ]
        }},
        {"name": "type", "type": "string"}
    ]
})

CMC_POSTS_SCHEMA = json.dumps({
    "type": "record",
    "name": "CMCPost",
    "fields": [
        {"name": "gravity_id", "type": "string"},
        {"name": "owner", "type": {
            "type": "record",
            "name": "PostOwner",
            "fields": [
                {"name": "nickname", "type": "string"},
                {"name": "handle", "type": "string"},
                {"name": "avatar_id", "type": "string"},
                {"name": "created_time", "type": "long"},
                {"name": "type", "type": "int"},
                {"name": "last_update_nickname", "type": ["long", "null"]},
                {"name": "avatar", "type": {
                    "type": "record",
                    "name": "OwnerAvatar",
                    "fields": [
                        {"name": "url", "type": "string"},
                    ]
                }},
                {"name": "vip", "type": "boolean"},
                {"name": "guid", "type": "string"}
            ]
        }},
        {"name": "root_id", "type": "string"},
        {"name": "text_content", "type": "string"},
        {"name": "comment_count", "type": "int"},
        {"name": "like_count", "type": "int"},
        {"name": "reactions", "type": {
            "type": "array",
            "items": {
                "type": "record",
                "name": "PostReactions",
                "fields": [
                    {"name": "gravity_id", "type": "string"},
                    {"name": "type", "type": "int"},
                    {"name": "count", "type": "int"}
                ]
            }
        }},
        {"name": "post_time", "type": "long"},
        {"name": "type", "type": "int"},
        {"name": "topics", "type": {
            "type": "array",
            "items": "string"
        }},
        {"name": "currencies", "type": {
            "type": "array",
            "items": {
                "type": "record",
                "name": "PostCurrencies",
                "fields": [
                    {"name": "id", "type": "int"},
                    {"name": "symbol", "type": "string"},
                    {"name": "slug", "type": "string"}
                ]
            }
        }},
        {"name": "bullish", "type": ["boolean", "null"]},
        {"name": "repost_count", "type": "int"},
        {"name": "language_code", "type": "string"}
    ]
})
