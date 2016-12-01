import jwt

from flask import g, Flask, jsonify, request, make_response, abort
from flask_restful import Resource

from app import app, db, api, bcrypt
from app.model.db import User

JWT_SECRET = 'passcode'
JWT_ALGORITHM = 'HS256'

def verify(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        g.user_id = user.id
        return user

def generate_token(user):
    data = {"user_id": user.id}
    token = jwt.encode(data, JWT_SECRET, JWT_ALGORITHM)
    return token


class RegisterUser(Resource):
    """Defines how the user gets registered"""

    def post(self):
        username = request.json.get("username")
        password = request.json.get("password")
        first_name = request.json.get("first_name")
        last_name = request.json.get("last_name")
        if username is None or password is None:
            abort(400, "Username and password can't be empty.")
        elif first_name is None or last_name is None:
            abort(400, "First name and last name can't be empty")
        elif username == password:
            abort(400, "Username and password can't be the same.")
        elif User.query.filter_by(username=username).first() is not None:
            abort(400, "Username already taken.")
        pwd_hash = bcrypt.generate_password_hash(password)
        user = User(username=username, password=pwd_hash, first_name=first_name,
                    last_name=last_name)
        db.session.add(user)
        db.session.commit()
        return ("Success!", 201)


class LoginUser(Resource):
    """Defines how a user logs in and gets an auth token."""

    def post(self):
        username = request.json.get("username")
        password = request.json.get("password")
        if username is None or username == "":
            abort(400, "Username cannot be blank")
        if password is None or password == "":
            abort(400, "Password cannot be blank.")
        user = verify(username, password)
        if not user:
            abort(400, "Username or password are wrong")
        token = generate_token(user)
        return jsonify(message="Welcome", token=str(token))
