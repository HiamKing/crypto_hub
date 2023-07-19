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
