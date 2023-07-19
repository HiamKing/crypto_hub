from marshmallow import Schema, fields

DEFAULT_SEARCH_SIZE = 30


class SearchSchema(Schema):
    filters = fields.List(fields.List(fields.Raw()), missing=[])
    limit = fields.Integer(missing=DEFAULT_SEARCH_SIZE)
    offset = fields.Integer(missing=0)
    with_count = fields.Boolean(missing=False)
    sort_by = fields.String(missing="")
