SYMBOL_LIST = [
    "BTC", "USDT", "LUNA", "ETH", "BNB",
    "SOL", "DOGE", "SHIB", "TRX", "XRP"
]

SYMBOL_ID_MAPPING = {
    "BTC": 1,
    "USDT": 825,
    "LUNA": 20314,
    "ETH": 1027,
    "BNB": 1839,
    "SOL": 5426,
    "DOGE": 74,
    "SHIB": 5994,
    "TRX": 1958,
    "XRP": 52,
}
CRAWL_INTERVAL = 10  # 10 secs
CMC_POSTS_KAFKA_TOPIC = "cmc.posts"
CMC_NEWS_KAFKA_TOPIC = "cmc.news"
