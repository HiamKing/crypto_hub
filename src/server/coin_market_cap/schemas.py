from marshmallow import Schema, fields


class PostSchema(Schema):
    _id = fields.Integer()
    text_content = fields.String()
    comment_count = fields.Integer()
    like_count = fields.Integer()
    reactions = fields.List(fields.Raw())
    post_time = fields.DateTime()
    topics = fields.List(fields.String())
    bullish = fields.Boolean()
    repost_count = fields.Integer()
    language_code = fields.String()


class SearchPostsResponseSchema(Schema):
    models = fields.List(fields.Nested(PostSchema))
    count = fields.Integer()


class NewsSchema(Schema):
    _id = fields.String()
    cover = fields.String()
    title = fields.String()
    subtitle = fields.String()
    source_name = fields.String()
    max_char = fields.Integer()
    language = fields.String()
    status = fields.String()
    source_url = fields.String()
    views = fields.Integer()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    released_at = fields.DateTime()


class SearchNewsResponseSchema(Schema):
    models = fields.List(fields.Nested(NewsSchema))
    count = fields.Integer()
