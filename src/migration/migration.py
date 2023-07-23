from pymongo import MongoClient

c = MongoClient("mongodb://admin:admin@mongo:27017")

db = c["crypto_hub"]

created_collections = db.list_collection_names()

# Create normal collections
n_collections = [
    "cmc.checkpoints", "cmc.news", "cmc.posts", "cmc.news_assoc",
    "cmc.posts_assoc", "cmc.stream.posts", "cmc.stream.posts_assoc",
    "cmc.stream.news", "cmc.stream.news_assoc"]

for collection in n_collections:
    if collection not in created_collections:
        db.create_collection(collection)

# Create time series collections
ts_collections = [
    {"name": "binance.klines.1m", "timeseries": {"timeField": "start_time", "metaField": "symbol", "granularity": "minutes"}},
    {"name": "binance.klines.1h", "timeseries": {"timeField": "start_time", "metaField": "symbol", "granularity": "hours"}},
    {"name": "binance.klines.1d", "timeseries": {"timeField": "start_time", "metaField": "symbol", "granularity": "hours"}},
    {"name": "binance.klines.1w", "timeseries": {"timeField": "start_time", "metaField": "symbol", "granularity": "hours"}},
    {"name": "binance.klines.1M", "timeseries": {"timeField": "start_time", "metaField": "symbol", "granularity": "hours"}},
    {"name": "binance.24h_ticker", "timeseries": {"timeField": "stats_close_time", "metaField": "symbol", "granularity": "seconds"}},
]

for collection in ts_collections:
    if collection["name"] not in created_collections:
        db.create_collection(collection["name"], timeseries=collection["timeseries"])

# Create index

indexs = [
    {"collection": "cmc.posts", "fields": [("post_time", -1)], "kwargs": {}},
    {"collection": "cmc.posts_assoc", "fields": [("symbol", 1)], "kwargs": {}},
    {"collection": "cmc.posts_assoc", "fields": [("post_time", -1)], "kwargs": {}},
    {"collection": "cmc.stream.posts", "fields": [("post_time", -1)], "kwargs": {"expireAfterSeconds": 604800}},
    {"collection": "cmc.stream.posts_assoc", "fields": [("symbol", 1)], "kwargs": {}},
    {"collection": "cmc.stream.posts_assoc", "fields": [("post_time", -1)], "kwargs": {"expireAfterSeconds": 604800}},
    {"collection": "cmc.news", "fields": [("updated_at", -1)], "kwargs": {}},
    {"collection": "cmc.news_assoc", "fields": [("coin_name", 1)], "kwargs": {}},
    {"collection": "cmc.news_assoc", "fields": [("updated_at", -1)], "kwargs": {}},
    {"collection": "cmc.stream.news", "fields": [("updated_at", -1)], "kwargs": {"expireAfterSeconds": 604800}},
    {"collection": "cmc.stream.news_assoc", "fields": [("coin_name", 1)], "kwargs": {}},
    {"collection": "cmc.stream.news_assoc", "fields": [("updated_at", -1)], "kwargs": {"expireAfterSeconds": 604800}}
]

for index in indexs:
    db[index["collection"]].create_index(index["fields"], **index["kwargs"])
