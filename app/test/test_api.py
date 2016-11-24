import json
import os
import unittest

from flask import Flask
from flask_testing import TestCase
from faker import Factory

from app.api import api


class TestApi(TestCase):
    """Test crud functions"""
    def create_app(self):
        test_app = Flask(__name__)
        test_app.config["TESTING"] = True
        return test_app

    def setUp(self):
        fakes = Factory.create()
        username = fakes.user_name()
        password = fakes.password()
        self.client.post("/auth/register",
                         data=json.dumps({"username": username,
                                          "password": password}))
        response = self.client.post("auth/login",
                                    data=json.dumps({"username": username,
                                                     "password": password}))
        token = os.environ["SECRET_KEY"]
        self.headers = {"Auth": token}


    def test_create_bucketlist_after_auth(self):
        response = self.client.post("/bucketlists/",
                                    headers=self.headers,
                                    data=json.dumps({"name": "listname"}))
        self.assertEqual(response.status_code, 201)
        self.assertTrue("Bucketlist created." in response.data)

    def test_fail_create_bucketlist_before_auth(self):
        response = self.client.post("/bucketlists/",
                                    data=json.dumps({"name": "listname"}),
                                    headers={})
        self.assertEqual(response.status_code, 401)
        self.assertIn("You have to log in first", response.data)

    def test_fail_create_bucketlist_with_blank_name(self):
        response = self.client.post("/bucketlists/",
                                    data=json.dumps({"name": ""}),
                                    headers=self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn("The name cannot be blank", response.data)

    def test_get_all_bucketlists_after_auth(self):
        response = self.client.get("/bucketlists/", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_fail_to_get_bucket_lists_before_auth(self):
        response = self.client.get("/bucketlists/", headers={})
        self.assertEqual(response.status_code, 401)
        self.assertIn("You have to log in first", response.data)

    def test_get_bucketlist_by_id(self):
        response = self.client.get("/bucketlists/1", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_bucketlist_id_is_not_found(self):
        response = self.client.get("/bucketlists/105", headers=self.headers)
        self.assertEqual(response.status_code, 404)
        # self.assertIn("Id not found.", response.data)

    def test_update_bucketlist(self):
        response = self.client.put("/bucketlists/1",
                                   data=json.dumps({"name": "NewName"}),
                                   headers=self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Updated", response.data)

    def test_delete_bucketlist(self):
        response = self.client.delete("/bucketlists/1", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_create_bucketlist_item(self):
        response = self.client.post("/bucketlists/1/items/",
                                    data=json.dumps({"name": "item1"}),
                                    headers=self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Bucketlist item created.", response.data)

    def test_create_bucketlist_item_fails_if_id_is_invalid(self):
        response = self.client.post("/bucketlists/105/items/",
                                    data=json.dumps({"name": "item2"}),
                                    headers=self.headers)
        self.assertEqual(response.status_code, 404)
        # self.assertIn("The bucketlist ID was not found.", response.data)

    def test_create_bucketlist_item_fails_if_name_is_blank(self):
        response = self.client.post("/bucketlists/1/items/",
                                    data=json.dumps({"name": ""}),
                                    headers=self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Item name cannot be blank.", response.data)

    def test_get_bucket_list_item(self):
        response = self.client.get("/bucketlists/1/items/1",
                                   headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_update_bucketlist_item(self):
        response = self.client.put("/bucketlists/1/items/1",
                                   data=json.dumps({"name": "NewName"}),
                                   headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Item updated", response.data)

    def test_delete_bucketlist_item_by_id(self):
        response = self.client.delete("/bucketlists/1/items/1", headers=self.headers)
        self.assertEqual(response.status_code, 204)
        self.assertIn("Deleted", response.data)

    def test_get_bucketlist_by_name(self):
        response = self.client.get("/bucketlists?q=bucket1", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_it_doesnt_get_bucketlist_name(self):
        response = self.client.get("/bucketlists?q=bucket50", headers=self.headers)
        self.assertEqual(response.status_code, 204)



if __name__ == "__main__":
    unittest.main()
