from flask import g, Flask, jsonify, request, make_response, abort
from flask_restful import Resource

from app import app, db, api, bcrypt
from app.model.db import User


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
