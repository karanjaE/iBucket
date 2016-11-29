from flask import request, jsonify, abort
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import g

from app import app, db
from app.model.db import Bucket, Item, User

bcrypt  = Bcrypt(app
                 )
@app.route("/auth/register", methods=["POST"])
def register_user():
    """Registers a new user"""
    username = request.json.get("username")
    password = request.json.get("password")
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")

    if username is None or username == " ":
        abort(400, {"message": "Username can't be blank."})
    elif password is None or password == " ":
        abort(400, {"message": "Password cannot be blank!"})
    elif username == password:
        abort(400, {"message": "Username and password can't be the same."})
    elif first_name is None or last_name is None:
        abort(400, {"message": "Name can't be empty."})
    elif User.query.filter_by(username =  username).first() is not None:
        abort(400, {"message": "Username already taken."})

    password_hash = bcrypt.generate_password_hash(password)
    user = User(username=username)
    user.password = password_hash
    user.first_name = first_name
    user.last_name = last_name
    db.session.add(user)
    db.session.commit()
    return (jsonify({"id" :user.id, "username": user.username,
                     "first_name": user.first_name, "last_name": user.last_name}), 201)

@app.route("auth/login", methods=["POST"])
def login():
    """log in the user and generate a token"""
