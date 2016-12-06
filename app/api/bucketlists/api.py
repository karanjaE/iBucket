from datetime import datetime

from flask import abort, jsonify, request
from flask_restful import Resource, reqparse

from app import db
from app.api.bucketlists import actions
from app.api.bucketlists.serializer import BucketItems, BucketListsAll
from app.model.db import User, Bucket, Item

bucket_list_json = BucketListsAll()
bucket_items_json = BucketItems()

class BucketLists(Resource):
    """Defines crud for a single bucketlist"""

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("bucket_name", type=str, required=True)
        self.parser.add_argument("date_created", type=datetime)
        self.parser.add_argument("date_modified", type=datetime)
        self.parser.add_argument("created_by", type=int)
        super(BucketLists, self).__init__()

    def post(self):
        """creates a new bucketlist"""
        bucket_data = self.parser.parse_args()
        auth = request.headers.get("access-token")
        if not auth:
            return("Unautorized access. Please log in to continue.", 403)
        user = actions.verify_auth_token(auth)
        user_id = user.get("user_id", None)
        if not user_id:
            abort(401, message="Invalid user.")
        new_bucket = actions.create_new_bucket(bucket_data, user_id)
        return ({"Success!":"Bucket created."}, 201)

    def get(self):
        """Lists all buckets by a given user."""
        page = request.args.get("page", "1")
        limit = request.args.get("limit", "100")
        q = request.args.get('q', '')
        auth = request.headers.get("access-token")
        if not auth:
            return({"error":"Unautorized access. Please log in to continue."},
                   403)
        user = actions.verify_auth_token(auth)
        buckets = Bucket.query.filter_by(created_by=user["user_id"])
        result = bucket_list_json.dump(buckets)
        # result = jsonify(result)
        return ({"All buckets": type(result)}, 200)


class BucketList(Resource):
    """Defines CRUD for a single bucketlist"""

    def put(self, id):
        """Updates a bucketlist"""
        auth = request.headers.get("access-token")
        if not auth:
            return({"error":"Unautorized access. Please log in to continue."},
                   403)
        user = actions.verify_auth_token(auth)
        new_name = request.json.get("bucket_name")
        bucket = Bucket.query.filter_by(id=id, created_by=user["user_id"]).first()
        if not bucket:
            return({"Error": "The ID givne is invalid."})
        try:
            bucket.bucket_name = new_name
            bucket.date_modified = datetime.utcnow()
            db.session.add(bucket)
            db.session.commit()
            return({"message": "Success! Bucket updated"}, 201)
        except Exception:
            return({"Error":"Not updated. Please try again."}, 500)

    def delete(self, id):
        """Deletes a given bucket"""
        auth = request.headers.get("access-token")
        if not auth:
            return({"error":"Unautorized access. Please log in to continue."},
                   403)
        user = actions.verify_auth_token(auth)
        new_name = request.json.get("bucket_name")
        bucket = Bucket.query.filter_by(id=id, created_by=user["user_id"]).first()
        if not bucket:
            return({"Error": "The ID givne is invalid."})
        try:
            db.session.delete(bucket)
            db.session.commit()
            return({"Success!": "Deleted"}, 200)
        except Exception:
            return({"Error":"Not deleted. Please try again."}, 500)
