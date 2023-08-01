from marshmallow import Schema, fields


class Statistics(Schema):
    stats_time = fields.DateTime()
    news_count = fields.Integer()
    post_count = fields.Integer()


class StatisticsResponseSchema(Schema):
    models = fields.List(fields.Nested(Statistics))


class AnalyticsSearch(Schema):
    symbol = fields.String()
    start_time = fields.String()
    end_time = fields.String()
    granularity = fields.String()
