from flask_restful import fields

"""This defines how users, buckets and items are represented."""

user_serializer = {
    "id": fields.Integer,
    "username": fields.String,
}

item_serializer = {
    "id": fields.Integer,
    "item_name": fields.String,
    "description": fields.String,
    "bucket": fields.Integer, # gets the bucketlist ID
    "done": fields.Boolean,
    "date_created": fields.DateTime,
    "date_modified": fields.DateTime,
}

bucket_serializer = {
    "id": fields.Integer,
    "bucket_name": fields.String,
    "created_by": fields.Integer,
    "items": fields.Nested(item_serializer),
    "date_created": fields.DateTime,
    "date_modified": fields.DateTime,
}
