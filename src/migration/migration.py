from pymongo import MongoClient

c = MongoClient("mongodb://admin:admin@mongo:27017")

db = c["crypto_hub"]

created_collections = db.list_collection_names()

# Create normal collections
n_collections = ["cmc.checkpoints", "cmc.news", "cmc.posts", "cmc.news_assoc", "cmc.posts_assoc"]

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
