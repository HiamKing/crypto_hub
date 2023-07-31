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


class PriceChangeResponseSchema(Schema):
    models = fields.List(fields.Nested(PriceChange))


class KlinesResponseSchema(Schema):
    models = fields.List(fields.Nested(Klines))
