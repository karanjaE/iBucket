import json
import os

from flask import Flask, jsonify, request, make_response
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEVELOPMENT"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DB_URL"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
blapi = Api(app)

from app.model.db import Bucket, Item, User

from app.api import api
from app.api import auth

# blapi.add_resource(api.Index, "/index", "/")
blapi.add_resource(auth.RegisterUser, "/auth/register")
blapi.add_resource(auth.LoginUser, "/auth/login")
