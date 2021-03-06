import json
from datetime import datetime
import os

import jwt
from flask import Response, abort, request, jsonify, g
from flask_restful import abort, Resource, reqparse

from app import app, bcrypt, db
from app.model.db import User, Bucket, Item

JWT_PASS = os.environ["SECRET_KEY"]
JWT_ALGORITHM = "HS256"

def verify_auth_token(token):
    user = jwt.decode(token, JWT_PASS, JWT_ALGORITHM)
    g.user_id = user.get("user_id", "0")
    return user

def get_buckets(q):
    bucketlists = Bucket.query.filter(Bucket.bucket_name.contains(q))
    return bucketlists.filter_by(created_by=g.user_id)

class BucketLists(Resource):
    """Defines crud for alll bucketlists"""

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("bucket_name", type=str, required=True)
        self.parser.add_argument("date_created", type=datetime)
        self.parser.add_argument("date_modified", type=datetime)
        self.parser.add_argument("created_by", type=int)
        super(BucketLists, self).__init__()

    def post(self):
        """creates a new bucketlist"""
        auth = request.headers.get("access-token")
        if not auth:
            return("Unautorized access. Please log in to continue.", 403)
        user = verify_auth_token(auth)
        user_id = user.get("user_id", None)
        if not user_id:
            abort(401, message="Invalid user.")
        bucket_name = request.json.get("bucket_name")
        if (Bucket.query.filter_by(bucket_name=bucket_name,
                                   created_by=user_id).first() is not None):
            abort(403, message="that name has already been taken.")
        new_bucket = Bucket(bucket_name=bucket_name, created_by=user_id)
        db.session.add(new_bucket)
        db.session.commit()
        return({"Message": "Bucketlist created."}, 201)

    def get(self):
        """Retrievs all bucketlists"""
        auth = request.headers.get("access-token")
        q = request.args.get("q", "")
        page = request.args.get('page', '1')
        limit = request.args.get('limit', '3')
        if not auth:
            return("Unautorized access. Please log in to continue.", 403)
        user = verify_auth_token(auth)
        user_id = user.get("user_id", None)
        if not user_id:
            abort(401, message="Invalid user.")
        all_buckets = get_buckets(q)
        all_buckets.paginate(int(page), int(limit), True).items
        buckets = []
        for bucket in all_buckets:
            buckets.append({
                "bucket name": bucket.bucket_name,
                "created by": bucket.created_by,
                "id": bucket.id,
                "date created": str(bucket.date_created),
                "date_modified": str(bucket.date_modified)
            })
        return Response(json.dumps(buckets), mimetype='application/json')


class BucketList(Resource):
    """Defines CRUD for a single bucketlist"""

    def get(self, id):
        """Retrieves a single BucketList"""
        auth = request.headers.get("access-token")
        if not auth:
            return({"error":"Unautorized access. Please log in to continue."},
                   403)
        user = verify_auth_token(auth)
        bucketlists = Bucket.query.filter_by(id=id, created_by=user["user_id"]).all()
        if not bucketlists:
            return({"message": "That bucket either doesn't exist or doesn't belong to you."})
        items = Item.query.filter_by(bucket=id).all()
        bucketlist_items = []
        buckets = []
        for item in items:
            bucketlist_items.append({
                "id": item.id,
                "item name": item.item_name,
                "description": item.description,
                "date created": str(item.date_created),
                "date modified": str(item.date_modified),
                "done": item.done
            })
        all_items = Response(json.dumps(bucketlist_items), mimetype='application/json')
        for bucket in bucketlists:
            buckets.append({
                "id": bucket.id,
                "bucket name": bucket.bucket_name,
                "owner id": bucket.created_by,
                "items": bucketlist_items,
                "date created": str(bucket.date_created),
                "date modified": str(bucket.date_modified)
            })
        return Response(json.dumps(buckets), mimetype='application/json')

    def put(self, id):
        """Updates a bucketlist"""
        auth = request.headers.get("access-token")
        if not auth:
            return({"error":"Unautorized access. Please log in to continue."},
                   403)
        user = verify_auth_token(auth)
        new_name = request.json.get("bucket_name")
        bucket = Bucket.query.filter_by(id=id, created_by=user["user_id"]).first()
        if not bucket:
            return({"Error": "The ID given is invalid."})
        try:
            bucket.bucket_name = new_name
            bucket.date_modified = datetime.utcnow()
            db.session.commit()
            return({"message": "Success! Bucket updated"}, 200)
        except Exception:
            return({"Error":"Not updated. Please try again."}, 500)

    def delete(self, id):
        """Deletes a given bucket"""
        auth = request.headers.get("access-token")
        if not auth:
            return({"error":"Unautorized access. Please log in to continue."},
                   403)
        user = verify_auth_token(auth)
        bucket = Bucket.query.filter_by(id=id, created_by=user["user_id"]).first()
        if not bucket:
            return({"Error": "The ID givne is invalid."})
        try:
            db.session.delete(bucket)
            db.session.commit()
            return({"Success!": "Deleted"}, 200)
        except Exception:
            return({"Error":"Not deleted. Please try again."}, 500)


class CreateItems(Resource):
    """Creates the post method for bucketlist items"""

    def post(self, bucket_id):
        auth = request.headers.get("access-token")
        if not auth:
            return({"error":"Unautorized access. Please log in to continue."},
                   403)
        user = verify_auth_token(auth)
        item_name = request.json.get("item_name")
        description = request.json.get("description")
        done = request.json.get("done", False)
        if Bucket.query.filter_by(id=bucket_id,
                                  created_by=user["user_id"]).first() is None:
            return({"Error":"The given bucket id is invalid"})
        if Item.query.filter_by(item_name=item_name).first() is not None:
            return({"Error": "Item name has already been taken"})
        new_item = Item(item_name=item_name, bucket=bucket_id, done=done,
                        description=description)
        db.session.add(new_item)
        db.session.commit()
        return({"Success": "Item created successfully."})


class BucketItems(Resource):
    """Creates put and delete functionality for bucketlist items"""

    def  put(self, bucket_id, item_id):
        auth = request.headers.get("access-token")
        if not auth:
            return({"error":"Unautorized access. Please log in to continue."},
                   403)
        user = verify_auth_token(auth)
        item = Item.query.filter_by(id=item_id, bucket=bucket_id).first()
        if not item:
            return({"Error": "Item ID enter is invalid."})
        try:
            item.item_name = request.json.get("item_name")
            item.description = request.json.get("description")
            item.date_modified = datetime.utcnow()
            db.session.commit()
            return({"Success": "Item updated"}, 201)
        except Exception:
            return({"Error":"Not updated. Please try again."}, 500)

    def delete(self, bucket_id, item_id):
        auth = request.headers.get("access-token")
        if not auth:
            return({"error":"Unautorized access. Please log in to continue."},
                   403)
        user = verify_auth_token(auth)
        item = Item.query.filter_by(id=item_id, bucket=bucket_id).first()
        if not item:
            return({"Error": "Item ID enter is invalid."})
        try:
            db.session.delete(item)
            db.session.commit()
            return({"Success": "Item deleted."})
        except Exception:
            return({"Error":"Not deleted. Please try again."}, 500)
