from app.test import test_setup
from app.api.bucketlists import api


class TestApi(test_setup.TestSetUp):
    """Test crud functions"""

    def test_create_bucketlist_after_auth(self):
        # Tests that a bucketlist creates successfully after user is logged in.
        response = self.client.post("/bucketlists/",
                                    headers=self.headers,
                                     data=({"name": "listname"}))
        self.assertEqual(response.status_code, 201)
        self.assertTrue("Bucketlist created." in response.data)

    def test_fail_create_bucketlist_before_auth(self):
        # Fails to create a bucketlist if the user is not logged in.
        response = self.client.post("/bucketlists/",
                                     data=({"name": "listname"}),
                                    headers={})
        self.assertEqual(response.status_code, 403)
        self.assertIn("You have to log in first", response.data)

    def test_fail_create_bucketlist_with_blank_name(self):
        # Test that you cant create a bucketlist without a name.
        response = self.client.post("/bucketlists/",
                                     data=({"name": ""}),
                                    headers=self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn("The name cannot be blank", response.data)

    def test_get_all_bucketlists_after_auth(self):
        # Gets all bucketlists as long as the user is logged in.
        response = self.client.get("/bucketlists/", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_fail_to_get_bucket_lists_before_auth(self):
        # Fails to get bucketlists if the user is not logged in
        response = self.client.get("/bucketlists/", headers={})
        self.assertEqual(response.status_code, 403)
        self.assertIn("You have to log in first", response.data)

    def test_get_bucketlist_by_id(self):
        # Gets bucketlist with a given ID
        response = self.client.get("/bucketlists/1", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_bucketlist_id_is_not_found(self):
        # Returns an error if the bucket list ID is not found.
        response = self.client.get("/bucketlists/105", headers=self.headers)
        self.assertEqual(response.status_code, 204)

    def test_update_bucketlist(self):
        # Updates the bucketlist
        response = self.client.put("/bucketlists/1",
                                    data=({"name": "NewName"}),
                                   headers=self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Updated", response.data)

    def test_delete_bucketlist(self):
        # Deletes a bucketlist
        self.client.post("/bucketlists/",
                                     data=({"name": "NewName"}),
                                    headers=self.headers)
        self.client.get("/bucketlists/1", headers=self.headers)
        self.client.delete("/bucketlists/1", headers=self.headers)
        response = self.client.get("/bucketlists/1", headers=self.headers)
        self.assertEqual(response.status_code, 204)

    def test_create_bucketlist_item(self):
        # Creates a bucketlist item
        response = self.client.post("/bucketlists/1/items/",
                                     data=({"name": "item1"}),
                                    headers=self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Bucketlist item created.", response.data)

    def test_create_bucketlist_item_fails_if_id_is_invalid(self):
        response = self.client.post("/bucketlists/105/items/",
                                     data=({"name": "item2"}),
                                    headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_create_bucketlist_item_fails_if_name_is_blank(self):
        response = self.client.post("/bucketlists/1/items/",
                                     data=({"name": ""}),
                                    headers=self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Item name cannot be blank.", response.data)

    def test_get_bucket_list_item(self):
        response = self.client.get("/bucketlists/1/items/1",
                                   headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_update_bucketlist_item(self):
        response = self.client.put("/bucketlists/1/items/1",
                                    data=({"name": "NewName"}),
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
