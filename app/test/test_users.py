from app.test import test_setup
from app.api import auth


class TestUser(test_setup.TestSetUp):
    """Test user creation and login."""

    def test_register(self):
        response = self.client.post("/auth/register",
                                    data={"username": self.username,
                                          "password": self.password})
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        response = self.client.post("auth/login",
                                    data={"username": self.username,
                                          "password": self.password})
        self.assertEqual(response.status_code, 200)

    def test_reg_fails_if_username_empty(self):
        response = self.client.post("/auth/register",
                                    data={"password": self.password})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Username can't be blank." in response.data)

    def test_reg_fails_username_and_password_are_the_same(self):
        response = self.client.post("/auth/register", data={"username": "foo",
                                                           "password": "foo"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Username and password can't be the same."
                        in response.data)

    def test_reg_fails_if_password_empty(self):
        response = self.client.post("/auth/register",
                                    data={"username": self.username})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Password cannot be blank!" in response.data)

    def test_login_fails_if_username_blank(self):
        response = self.client.post("/auth/login/",
                                    data={"password": self.password})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Username cannot be blank" in response.data)

    def test_login_fails_if_password_is_blank(self):
        # Fails to log in user if the password is blank.
        response = self.client.post("/auth/login",
                                    data=({"username": self.username,
                                                     "password": ""}))
        self.assertEqual(response.status_code, 204)
        self.assertIn("Password cannot be blank.", response.data)

    def test_login_fails_if_bad_password_is_entered(self):
        self.client.post("/auth/register",
                         data={"username": self.username,
                               "password": self.password})
        response = self.client.post("auth/login",
                                    data={"username": self.username,
                                          "password": "21323pass"})
        self.assertEqual(response.status_code, 204)
        self.assertTrue("Wrong password." in response.data)


if __name__ == "__main__":
    unittest.main()
