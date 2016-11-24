import json
import os

from flask import Flask
from faker import Factory
from flask_testing import TestCase
from sqlalchemy import create_engine


from app.api import api, auth


class TestUser(TestCase):
    """Test user creation and login."""

    def create_app(self):
        test_app = Flask(__name__)
        test_app.config["TESTING"] = True
        return test_app

    def setUp(self):
        """Set up testing environment."""
        fake = Factory.create()
        self.username = fake.user_name()
        self.password = fake.password()

    def test_register(self):
        response = self.client.post("/auth/register",
                                    data={"username": self.username,
                                          "password": self.password})
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        response = self.client.post("auth/login", data={"username": self.username,
                                                        "password": self.password})
        self.assertEqual(response.status_code, 201)

    def test_reg_fails_if_username_empty(self):
        response = self.client.post("/auth/register",
                                    data={"password": self.password})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Username can't be blank." in response.data)

    def test_reg_fails_username_and_password_are_the_same(self):
        response = self.client.post("/auth/register", data={"username": "foo",
                                                           "password": "foo"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Username and password can't be the same." in response.data)

    def test_reg_fails_if_password_empty(self):
        response = self.client.post("/auth/register",
                                    data={"username": self.username})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Password cannot be blank!" in response.data)

    def test_login_fails_if_username_blank(self):
        response = self.client.post("/auth/login/", data={"password": self.password})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Username cannot be blank" in response.data)

    def test_login_fails_if_bad_password_is_entered(self):
        self.client.post("/auth/register",
                         data={"username": self.username, "password": self.password})
        response = self.client.post("auth/login",
                                    data={"username": self.username, "password": "21323pass"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Wrong password." in response.data)


if __name__ == "__main__":
    unittest.main()
