from marshmallow import Schema, fields


class PriceChange(Schema):
    symbol = fields.String()
    last_price = fields.Float()
    price_change_percent = fields.Float()


class PriceChangeResponseSchema(Schema):
    models = fields.List(fields.Nested(PriceChange))
