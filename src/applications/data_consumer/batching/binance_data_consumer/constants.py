TICKER_INFO_KAFKA_TOPIC = "ticker.24h-info"
KLINES_KAFKA_TOPIC = "klines"
FE_TICKER_INFO_KAFKA_TOPIC = "ticker.24h-info.file_event"
FE_KLINES_KAFKA_TOPIC = "klines.file_event"

FE_TOPIC_MAPPING = {
    TICKER_INFO_KAFKA_TOPIC: FE_TICKER_INFO_KAFKA_TOPIC,
    KLINES_KAFKA_TOPIC: FE_KLINES_KAFKA_TOPIC,
}

MAX_FILE_SIZE = 10485760  # 10 mb

KLINES_FIELDS_MAPPING = {
    "e": {"name": "event_type", "type": "string"},
    "E": {"name": "event_time", "type": "long"},
    "s": {"name": "symbol", "type": "string"},
    "k": {"name": "kline", "type": "dict"},
    "t": {"name": "start_time", "type": "long"},
    "T": {"name": "close_time", "type": "long"},
    "i": {"name": "interval", "type": "string"},
    "f": {"name": "first_trade_id", "type": "long"},
    "L": {"name": "last_trade_id", "type": "long"},
    "o": {"name": "open_price", "type": "double"},
    "c": {"name": "close_price", "type": "double"},
    "h": {"name": "high_price", "type": "double"},
    "l": {"name": "low_price", "type": "double"},
    "v": {"name": "base_asset_vol", "type": "double"},
    "n": {"name": "number_of_trade", "type": "long"},
    "x": {"name": "is_closed", "type": "boolean"},
    "q": {"name": "quote_asset_vol", "type": "double"},
    "V": {"name": "buy_base_asset_vol", "type": "double"},
    "Q": {"name": "buy_quote_asset_vol", "type": "double"}
}

TICKER_INFO_FIELDS_MAPPING = {
    "e": {"name": "event_type", "type": "string"},
    "E": {"name": "event_time", "type": "long"},
    "s": {"name": "symbol", "type": "string"},
    "p": {"name": "price_change", "type": "double"},
    "P": {"name": "price_change_percent", "type": "double"},
    "w": {"name": "weighted_avg_price", "type": "double"},
    "x": {"name": "first_trade_price", "type": "double"},
    "c": {"name": "last_price", "type": "double"},
    "Q": {"name": "last_quantity", "type": "double"},
    "b": {"name": "best_bid_price", "type": "double"},
    "B": {"name": "best_bid_quantity", "type": "double"},
    "a": {"name": "best_ask_price", "type": "double"},
    "A": {"name": "best_ask_quantity", "type": "double"},
    "o": {"name": "open_price", "type": "double"},
    "h": {"name": "high_price", "type": "double"},
    "l": {"name": "low_price", "type": "double"},
    "v": {"name": "base_asset_vol", "type": "double"},
    "q": {"name": "quote_asset_vol", "type": "double"},
    "O": {"name": "stats_open_time", "type": "long"},
    "C": {"name": "stats_close_time", "type": "long"},
    "F": {"name": "first_trade_id", "type": "long"},
    "L": {"name": "last_trade_id", "type": "long"},
    "n": {"name": "number_of_trade", "type": "long"}
}
