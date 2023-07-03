SYMBOL_LIST = [
    "btcusdt", "lunausdt", "ethusdt", "bnbusdt", "xrpusdt",
    "dogeusdt", "ethbtc", "bnbbtc", "dogebtc", "solbtc",
    "shibusdt", "trxbtc", "solusdt"
]

SUBCRIBE_CHANNELS = ['ticker', 'kline_1m', 'kline_1h', 'kline_1d', 'kline_1w', 'kline_1M']

CRAWL_INTERVAL = 5  # 5 secs
TICKER_INFO_EVENT_TYPE = "24hrTicker"
KLINES_EVENT_TYPE = "kline"
TICKER_INFO_KAFKA_TOPIC = "ticker.24h-info"
KLINES_KAFKA_TOPIC = "klines"
