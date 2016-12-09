import json
from flask import jsonify
from faker import Factory
from app.test import test_setup


class TestUser(test_setup.TestSetUp):
    """Test user creation and login."""

    def test_it_creates_a_user(self):
        fakes = Factory.create()
        self.username = fakes.user_name()
        self.password = fakes.password()
        response = self.app.post("/auth/register",
                                 content_type="application/json",
                                 data=json.dumps({"username": self.username,
                                       "password": self.password}))
        self.assertEqual(response.status_code, 201)

    def test_reg_fails_if_username_empty(self):
        fakes = Factory.create()
        self.username = fakes.user_name()
        response = self.app.post("/auth/register",
                                 content_type="application/json",
                                 data=json.dumps({"password": self.password}))
        self.assertEqual(response.status_code, 400)

    def test_reg_fails_if_password_empty(self):
        fakes = Factory.create()
        self.username = fakes.user_name()
        response = self.app.post("/auth/register",
                                 content_type="application/json",
                                 data=json.dumps({"username": self.username}))
        self.assertEqual(response.status_code, 400)

    def test_reg_fails_if_username_already_exists(self):
        response = self.app.post("/auth/register",
                                 content_type="application/json",
                                 data=json.dumps({"username": self.username,
                                       "password": self.password}))
        self.assertEqual(response.status_code, 409)

    def login_succeeds_if_details_are_correct(self):
        response = self.app.post("/auth/login",
                                 content_type="application/json",
                                 data=json.dumps({"username": self.username,
                                       "password": self.password}))
        self.assertEqual(response.status_code, 200)

    def test_login_fails_if_username_blank(self):
        response = self.app.post("/auth/login",
                                 content_type="application/json",
                                 data=json.dumps({"password": self.password}))
        self.assertEqual(response.status_code, 400)

    def test_login_fails_if_password_is_blank(self):
        response = self.app.post("/auth/login",
                                 content_type="application/json",
                                 data=json.dumps({"username": self.username}))
        self.assertEqual(response.status_code, 400)

    def tearown(self):
        db.session.remove()
        db.drop_all()

if __name__ == "__main__":
    unittest.main()
