import jwt

from flask import abort, g, jsonify
from flask_restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError

from app import app, bcrypt, db
from app.api import serializer
from app.model.db import User

JWT_SECRET = 'passcode'
JWT_ALGORITHM = 'HS256'

def verify_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        g.user_id = user.id
        return user

def generate_token(user):
    data = {"user_id": user.id}
    token = jwt.encode(data, JWT_SECRET, JWT_ALGORITHM)
    return token

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
        user = verify_user(username, password)
        if not user:
            abort(400, "Username or password are wrong")
        token = generate_token(user)
        return {"message": "Welcome %s" % username,
                "your token": token.decode("ascii")}
