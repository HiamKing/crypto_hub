from pymongo import MongoClient

c = MongoClient("mongodb://admin:admin@mongo:27017")

db = c["crypto_hub"]

created_collections = db.list_collection_names()

# Create normal collections
n_collections = ["cmc_checkpoints"]

for collection in n_collections:
    if collection not in created_collections:
        db.create_collection(collection)

# Create time series collections
ts_collections = [
    {"name": "klines_1m", "timeseries": {"timeField": "start_time", "granularity": "minutes"}},
    {"name": "klines_1h", "timeseries": {"timeField": "start_time", "granularity": "hours"}},
    {"name": "klines_1d", "timeseries": {"timeField": "start_time", "granularity": "hours"}},
    {"name": "klines_1w", "timeseries": {"timeField": "start_time", "granularity": "hours"}},
    {"name": "klines_1M", "timeseries": {"timeField": "start_time", "granularity": "hours"}},
]

for collection in ts_collections:
    if collection["name"] not in created_collections:
        db.create_collection(collection["name"], timeseries=collection["timeseries"])
