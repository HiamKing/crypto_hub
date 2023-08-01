from marshmallow import Schema, fields


class PostsStatistics(Schema):
    stats_time = fields.String()
    posts_count = fields.Integer()


class NewsStatistics(Schema):
    stats_time = fields.String()
    news_count = fields.Integer()


class StatisticsResponseSchema(Schema):
    posts_series = fields.List(fields.Nested(PostsStatistics))
    news_series = fields.List(fields.Nested(NewsStatistics))


class AnalyticsSearch(Schema):
    symbol = fields.String()
    start_time = fields.String()
    end_time = fields.String()
    granularity = fields.String()
