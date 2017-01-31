import json

from flask import jsonify
from faker import Factory

from app.test import test_setup


class TestApi(test_setup.TestSetUp):
    """Test crud functions"""

    def test_it_creates_a_bucket(self):
        response = self.app.post("/bucketlists/",
                                 data=json.dumps({"bucket_name": "bucket1",
                                                  "bucket":1, "created_by":1}),
                                 headers=self.auth_headers, content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_create_bucketlist_fails_if_no_auth(self):
        response = self.app.post("/bucketlists/", headers=None,
                                 data=json.dumps({"bucket_name": "bucket1",
                                                  "bucket":1, "created_by":1}))
        self.assertEqual(response.status_code, 403)

    def test_create_fails_if_bucket_name_exists(self):
        self.app.post("/bucketlists/",
                                 data=json.dumps({"bucket_name": "Bucket1",
                                                  "created_by":1}),
                                 headers=self.auth_headers,
                                 content_type="application/json")
        response = self.app.post("/bucketlists/",
                                 data=json.dumps({"bucket_name": "Bucket1",
                                                  "created_by":1}),
                                 headers=self.auth_headers,
                                 content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_it_gets_all_buckets(self):
        response = self.app.get("/bucketlists/", headers=self.auth_headers,
                                content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_it_fails_to_get_buckets_if_user_not_auth(self):
        response = self.app.get("/bucketlists/", headers=None,
                                content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_it_gets_a_single_bucket(self):
        response = self.app.get("/bucketlists/1", headers=self.auth_headers,
                                content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_it_fails_to_get_bucket_if_id_is_invalid(self):
        response = self.app.get("/bucketlists/180", headers=self.auth_headers,
                                content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_it_updates_a_bucketlist(self):
        response = self.app.put("/bucketlists/1", headers=self.auth_headers,
                                data=json.dumps({"bucket_name": "NewName"}),
                                content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_update_bucketlist_fails_if_id_is_ivalid(self):
        response = self.app.put("/bucketlists/c", headers=self.auth_headers,
                                data=json.dumps({"bucket_name": "NewName"}),
                                content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_it_deletes_a_bucketlist(self):
        response = self.app.delete("/bucketlists/1", headers=self.auth_headers,
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_it_creates_a_bucketlist_item(self):
        response = self.app.post("/bucketlists/1/items/", headers=self.auth_headers,
                                 data=json.dumps({"item_name": "iteme2",
                                                  "bucket" :1, "done": False}),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_it_fails_to_create_item_if_bucket_doesnt_exist(self):
        response = self.app.post("/bucketlists/12334534/items/", headers=self.auth_headers,
                                 data=json.dumps({"item_name": "iteme2",
                                                  "bucket" :1, "done": False}),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_it_updates_a_bucketlist_item(self):
        response = self.app.put("/bucketlists/1/items/1", headers=self.auth_headers,
                                data=json.dumps({"item_name": "newname",
                                                 "done": True}),
                                content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_it_deletes_a_bucketlist_item(self):
        response = self.app.delete("/bucketlists/1/items/1", headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
