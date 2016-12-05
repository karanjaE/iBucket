import jwt
from datetime import datetime

from flask import abort, g, jsonify, request
from flask_restful import marshal_with, Resource, reqparse
from sqlalchemy.exc import IntegrityError

from app import app, bcrypt, db
from app.api.serializer import bucket_serializer, item_serializer
from app.model.db import Bucket, Item, User


class RegisterUser(Resource):
    """It defines how a user is registered."""

    def post(self):
        user_parser = reqparse.RequestParser()
        user_parser.add_argument("username", required=True,
                                 help="Username can't be blank.")
        user_parser.add_argument("password", required=True,
                                 help="Password can't be blank.")
        args = user_parser.parse_args()
        username = args["username"]
        password = args["password"]
        hash_pass = bcrypt.generate_password_hash(password)
        user = User(username=username, password=hash_pass)
        try:
            db.session.add(user)
            db.session.commit()
            return ("Success!", 201)
        except IntegrityError:
            db.session.rollback()
            return ("Username already taken.", 400)

class LoginUser(Resource):
    """Defines how a user logs in"""

    def post(self):
        user_parser = reqparse.RequestParser()
        user_parser.add_argument("username", required=True,
                                 help="Username can't be blank.")
        user_parser.add_argument("password", required=True,
                                 help="Password can't be blank.")
        args = user_parser.parse_args()
        username = args["username"]
        password = args["password"]
        user = User.verify_user(username, password)
        if not user:
            abort(400, "Username or password are wrong")
        token = User.generate_token(user)
        return {"message": "Welcome %s" % username,
                "your token": token.decode("ascii")}
