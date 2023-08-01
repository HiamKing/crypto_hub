from marshmallow import Schema, fields


class StatisticsResponseSchema(Schema):
    models = fields.List(fields.List(fields.Raw()))


class RelationsResponseSchema(Schema):
    base_series = fields.List(fields.List(fields.Raw()))
    quote_series = fields.List(fields.List(fields.Raw()))


class AnalyticsSearch(Schema):
    symbol = fields.String()
    start_time = fields.String()
    end_time = fields.String()
    granularity = fields.String()
