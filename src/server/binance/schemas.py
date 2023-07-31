from marshmallow import Schema, fields


class PriceChange(Schema):
    symbol = fields.String()
    last_price = fields.Float()
    price_change_percent = fields.Float()


class Klines(Schema):
    start_time = fields.DateTime()
    open_price = fields.Float()
    high_price = fields.Float()
    low_price = fields.Float()
    close_price = fields.Float()
    base_asset_vol = fields.Float()


class Symbol24HStats(Schema):
    last_price = fields.Float()
    last_price_state = fields.String()
    price_change = fields.Float()
    price_change_percent = fields.Float()
    high_price = fields.Float()
    low_price = fields.Float()
    base_asset_vol = fields.Float()
    quote_asset_vol = fields.Float()


class PriceChangeResponseSchema(Schema):
    models = fields.List(fields.Nested(PriceChange))


class KlinesResponseSchema(Schema):
    models = fields.List(fields.Nested(Klines))


class Symbol24HStatsResponseSchema(Symbol24HStats):
    pass
