from marshmallow import fields, Schema, ValidationError


class UserSerializer(Schema):
    id =  fields.Int(dump_only=True)
    username = fields.Str(required=True, load_only=True)
    password = fields.Str(required=True, load_only=True)
    logged_in = fields.Str(required=True, load_only=True)
