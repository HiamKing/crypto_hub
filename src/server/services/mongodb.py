from pymongo import MongoClient

c = MongoClient("mongodb://admin:admin@mongo:27017")

crypto_hub_db = c["crypto_hub"]
