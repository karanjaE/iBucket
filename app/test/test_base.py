import json
import os
import unittest

from sqlalchemy import create_engine
from faker import Factory


# def register_and_login_test_user(client):
#     """Create test user and log them in"""
#     fake = Factory.create()
#
#     username = fake.user_name()
#     password = fake.password()
#
#     # register a fake user
#     response = client.post("/auth/register",
#                            data={"username": username, "password": password})
#
#     # log in the created user
#     response = client.post("/auth/login",
#                            data={"username": username, "password": password})
#
#     token = json.loads(response.data).get("token")
#     return token
