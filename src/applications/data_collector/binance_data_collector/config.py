import json
import os

secret_file_path = f"{os.path.dirname(os.path.realpath(__file__))}/secret.json"
data = json.load(open(secret_file_path, "r"))["data"]

BINANCE_API_KEY = data["apiKey"]
BINANCE_SECRET = data["secret"]

KAFKA_CONFIG = {
    "bootstrap.servers": "localhost:19092,localhost:29092,localhost:39092",
    "client.id": "binance_data_collector"
}
