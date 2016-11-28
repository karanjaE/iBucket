import json
import os

from faker import Factory
from flask import Flask
from flask_testing import TestCase


class TestSetUp(TestCase):

    def create_app(self):
        test_app = Flask(__name__)
        test_app.config["TESTING"] = True
        return test_app

    def setUp(self):
        """Set up testing environment."""
        fake = Factory.create()
        self.username = fake.user_name()
        self.password = fake.password()
        self.client.post("/auth/register",
                         data=json.dumps({"username": username,
                                          "password": password}))
        response = self.client.post("auth/login",
                                    data=json.dumps({"username": username,
                                                     "password": password}))
        token = os.environ["SECRET_KEY"]
        self.headers = {"Auth": token}
