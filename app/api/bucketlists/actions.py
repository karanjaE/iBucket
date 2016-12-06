from datetime import datetime
import os

import jwt
from flask import abort, request, jsonify, g
from flask_restful import abort, Resource

from app import app, bcrypt, db
from app.model.db import User, Bucket, Item

JWT_PASS = os.environ["SECRET_KEY"]
JWT_ALGORITHM = "HS256"

def verify_auth_token(token):
    user = jwt.decode(token, JWT_PASS, JWT_ALGORITHM)
    g.user_id = user.get("user_id", "0")
    return user

def create_new_bucket(bucket_name, creator):
    bucket_name = request.json.get("bucket_name")
    if not bucket_name:
        abort(400, message="Bucket name cannot be empty.")
    user_buckets = Bucket.query.filter_by(created_by=creator).all()
    for each_bucket in user_buckets:
        if each_bucket.bucket_name == bucket_name:
            abort(409, message="A bucket with that name already exists.")
    user = User.query.filter_by(id=creator).first()
    bucket = Bucket(bucket_name=bucket_name, created_by=creator).save()
    return bucket

def get_all_buckets(q):
    buckets = Bucket.query.filter(Bucket.bucket_name.contains(q))
    return buckets.filter_by(created_by=g.user_id)
