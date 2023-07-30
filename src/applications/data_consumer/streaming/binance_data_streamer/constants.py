TICKER_INFO_KAFKA_TOPIC = "ticker.24h-info"
KLINES_KAFKA_TOPIC = "klines"

KLINES_INTERVAL = ["1m", "1h", "1d", "1w", "1M"]

KLINES_COLS_NORMALIZED_COLS = {
    "t": {"name": "start_time", "type": "long"},
    "T": {"name": "close_time", "type": "long"},
    "s": {"name": "symbol", "type": "string"},
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

TICKER_INFO_COLS_NORMALIZED_COLS = {
    "s": {"name": "symbol", "type": "string"},
    "p": {"name": "price_change", "type": "double"},
    "P": {"name": "price_change_percent", "type": "double"},
    "c": {"name": "last_price", "type": "double"},
    "h": {"name": "high_price", "type": "double"},
    "l": {"name": "low_price", "type": "double"},
    "v": {"name": "base_asset_vol", "type": "double"},
    "q": {"name": "quote_asset_vol", "type": "double"},
    "O": {"name": "stats_open_time", "type": "long"},
    "C": {"name": "stats_close_time", "type": "long"},
}
