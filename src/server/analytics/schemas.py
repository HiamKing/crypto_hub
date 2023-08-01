from marshmallow import Schema, fields


class PostsStatistics(Schema):
    stats_time = fields.String()
    posts_count = fields.Integer()


class NewsStatistics(Schema):
    stats_time = fields.String()
    news_count = fields.Integer()


class StatisticsResponseSchema(Schema):
    models = fields.List(fields.List(fields.Raw()))


class AnalyticsSearch(Schema):
    symbol = fields.String()
    start_time = fields.String()
    end_time = fields.String()
    granularity = fields.String()
