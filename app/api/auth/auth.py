from flask import request
from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import abort, Resource
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.model.db import User
from app.api.auth.serializer import UserSerializer

serializer = UserSerializer()


def validate_user(username, password):
    """Checks the user's password in the Database and compares it to the one
    given to validate"""
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user

def get_user_id(payload):
    user_id = payload["get_user_id"]
    return User.query.filter_by(id=user_id).first()


class Register(Resource):
    """Defines how a user is registered.
    Username is unique and the password is hashed before being pushed to DB.
    """

    def post(self):
        data = request.get_json()
        user_data, errors = serializer.load(data)

        try:
            password = generate_password_hash(user_data["password"])
            new_user = User(
                username=user_data["username"],
                password=password,
                logged_in=True
            )
            db.session.add(new_user)
            db.session.commit()
            return ("Created.", 201)
        except Exception:
            abort(500, message="An error occurred. Registration failed.")


class LoginUser(Resource):
    """Defines how a user gets logged in. """
    pass
