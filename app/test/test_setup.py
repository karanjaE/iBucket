import json
import os

from faker import Factory
from flask import jsonify
from flask_testing import TestCase

from app import app, db, blist_api
from app.model.db import User, Bucket, Item

from app.api.auth import auth
from app.api.bucketlists import api


class TestSetUp(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["TEST_DB_URL"]
        return app

    def setUp(self):
        """Set up testing environment."""
        self.fakes = Factory.create()
        self.username = self.fakes.user_name()
        self.password = self.fakes.password()
        self.bucket_name = self.fakes.word()
        self.item_name = self.fakes.word()
        test_app = self.create_app()
        db.create_all(app=test_app)
        self.app = test_app.test_client()

        # Create a test user
        test_user = User(username=self.username, password=self.password)
        db.session.add(test_user)
        db.session.commit()

        #test bucket
        test_bucket = Bucket(bucket_name="Bucket1", created_by=1)
        test_bucket.save()

        #test item
        test_item = Item(item_name="Item1", bucket=1, done=False)
        test_item.save()

        #headers::
        self.auth_headers = {"access-token": auth.gen_auth_token(test_user)}
        self.headers = auth.gen_auth_token(test_user)
