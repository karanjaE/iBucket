from datetime import datetime

from flask import jsonify, request
from flask_restful import Resource, reqparse

from app.api.bucketlists import actions

class Bucket(Resource):
    """Defines crud for a single bucketlist"""

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("bucket_name", type=str, required=True)
        self.parser.add_argument("date_created", type=datetime)
        self.parser.add_argument("date_modified", type=datetime)
        self.parser.add_argument("created_by", type=int)
        super(Bucket, self).__init__()

    def post(self):
        """creates a new bucketlist"""
        bucket_data = self.parser.parse_args()
        auth = request.headers.get("access-token")
        if not auth:
            abort(403, message="Unautorized access. Please log in to continue.")
        user = actions.verify_auth_token(auth)
        user_id = user.get("user_id", None)
        if not user_id:
            abort(401, message="Invalid user.")
        new_bucket = actions.create_new_bucket(bucket_data, user_id)
        return ("Bucket created.", 201)
