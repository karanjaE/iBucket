from flask import Flask

app = Flask(__name__)
# app.config.from_object("config")


from app.api import api
from app.api import auth
