import json
import os
import unittest

from sqlalchemy import create_engine
from faker import Factory

from app.api import app


class TestApi(unittest.TestCase):
    """Test crud functions"""
    def setUp(self):
        pass

    def test_create_bucketlist_after_auth(self):
        response = self.client.post("/bucketlists/", data={})
        self.assertEqual(response.status_code, 201)
        self.assertTrue("Bucketlist created." in response.data)

    def test_fail_create_bucketlist_before_auth(self):
        response = self.client.post("/bucketlists/", data={})
        self.assertEqual(response.status_code, 401)
        self.assertIn("You have to log in first", response.data)

    def test_fail_create_bucketlist_with_blank_name(self):
        response = self.client.post("/bucketlists/", data={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("The name cannot be blank", response.data)

    def test_get_all_bucketlists_after_auth(self):
        response = self.client.get("/bucketlists/", data={})
        self.assertEqual(response.status_code, 200)

    def test_fail_to_get_bucket_lists_before_auth(self):
        response = self.client.get("/bucketlists/", data={})
        self.assertEqual(response.status_code, 401)
        self.assertIn("You have to log in first", response.data)

    def test_get_bucketlist_by_id(self):
        response = self.client.get("/bucketlists/<id>", data-{})
        self.assertEqual(response.status_code, 200)

    def test_bucketlist_id_is_not_found(self):
        response = self.client.get("/bucketlists/<id>", data-{})
        self.assertEqual(response.status_code, 404)
        self.assertIn("Id not found.", response.data)

    def test_update_bucketlist(self):
        response = self.client.put("/bucketlists/<id>", data-{})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Updated", response.data)

    def test_delete_bucketlist(self):
        pass

    def test_create_bucketlist_item(self):
        response = self.client.post("/bucketlists/<id>/items/", data={})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Bucketlist item created.", response.data)

    def test_create_bucketlist_item_fails_if_id_is_invalid(self):
        response = self.client.post("/bucketlists/<id>/items/", data={})
        self.assertEqual(response.status_code, 404)
        self.assertIn("The bucketlist ID was not found.")

    def test_create_bucketlist_item_fails_if_name_is_blank(self):
        response = self.client.post("/bucketlists/<id>/items/", data={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Item name cannot be blank.", response.data)

    def test_get_bucket_list_item(self):
        response = self.client.get("/bucketlists/<id>/items/", data={})
        self.assertEqual(response.status_code, 200)

    def test_update_bucketlist_item(self):
        response = self.client.put("/bucketlists/<id>/items/<item_id>", data={})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Item updated", response.data)

    def test_delete_bucketlist_item_by_id(self):
        response = self.client.delete("/bucketlists/<id>/items/<item_id>", data={})
        self.assertEqual(response.status_code, 204)
        self.assertIn("Deleted", response.data)

    def test_get_bucketlist_by_name(self):
        response = self.client.get()
        self.assertEqual(response.status_code, 200)

    def test_it_doesnt_get_bucketlist_name(self):
        pass

    def test_paginate(self):
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
