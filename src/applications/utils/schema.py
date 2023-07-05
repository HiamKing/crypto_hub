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
                {"name": "buy_quote_asset_vol", "type": "double"},
            ]
        }},
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
        {"name": "number_of_trade", "type": "long"},
    ]
})
