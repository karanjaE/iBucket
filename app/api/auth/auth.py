import os

import jwt
from flask import abort, request, jsonify, g
from flask_restful import abort, Resource

from app import app, bcrypt, db
from app.model.db import User

JWT_PASS = os.environ["SECRET_KEY"]
JWT_ALGORITHM = "HS256"

def verify_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        g.user_id = user.id
        return user

def gen_auth_token(user):
    data = {"user_id": user.id}
    token = jwt.encode(data, JWT_PASS, JWT_ALGORITHM)
    return token.decode('utf-8')


class Register(Resource):
    """Registers a new user."""

    def post(self):
        username = request.json.get("username")
        password = request.json.get('password')
        if username is None  or password is None:
            abort(400, message="Username and password cannot be blank.")
        if User.query.filter_by(username=username).first() is not None:
            abort(409, message="Username already exists. Pick another.")
        hash_pass = bcrypt.generate_password_hash(password)
        user = User(username=username, password=hash_pass)
        db.session.add(user)
        db.session.commit()
        return ("Success! You are regisrered! Please log in.", 201)

class LoginUser(Resource):
    """Logs in the user"""

    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        if username is None  or password is None:
            abort(400, message="Username and password cannot be blank.")
        user = verify_user(username, password)
        if user:
            token = gen_auth_token(user)
            return({"User": user.username, "token": token},200)
        else:
            abort(401, message="Wrong username or password.")
