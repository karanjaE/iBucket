from marshmallow import Schema, fields


class BucketItems(Schema):
    id = fields.Int(dump_only=True)
    item_name = fields.Str(required=True)
    date_created = fields.DateTime()
    date_modified = fields.DateTime()
    done = fields.Bool(required=True)
    bucket = fields.Int()

class BucketListsAll(Schema):
    id = fields.Int(dump_only=True)
    bucket_name = fields.Str(required=True)
    date_created = fields.DateTime()
    date_modified = fields.DateTime()
    created_by = fields.Int()
    items = fields.Nested(BucketItems, key="id", many=True, dump_only=True)
