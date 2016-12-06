import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEVELOPMENT"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DB_URL"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
blist_api = Api(app)

from app.model.db import Bucket, Item, User

from app.api.auth import auth
from app.api.bucketlists import api


blist_api.add_resource(auth.Register, "/auth/register")
blist_api.add_resource(auth.LoginUser, "/auth/login")
blist_api.add_resource(api.BucketLists, "/bucketlists/")
blist_api.add_resource(api.BucketList, "/bucketlists/<id>")
