from timebank import app
import unittest
import json


def login_user(self, phone, testing):
    tester = app.test_client(self)
    response = tester.post("/api/v1/user/login", json={
        'phone': phone,
        'password': testing
    })
    return response


class UsersTest(unittest.TestCase):
    def test_get_all_users_index(self):
        tester = app.test_client(self)
        response = tester.get("/api/v1/users")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")


    def test_get_all_users(self):
        response = app.test_client().get('/api/v1/users')
        res = json.loads(response.data.decode('utf-8'))
        assert type(res[0]) is dict
        assert 'id' in res[0]
        assert type(res[0]['id']) is int
        assert 'phone' in res[0]
        assert type(res[0]['phone']) is str
        assert 'user_name' in res[0]
        assert type(res[0]['user_name']) is str
        assert 'time_account' in res[0]
        assert type(res[0]['time_account']) is int

    def test_get_one_user_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/api/v1/user/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")

    def test_user_login_with_correct_data(self):
        response = login_user(self, "+421 999 999999", "testing")
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 201)

    def test_user_login_with_incorrect_phone(self):
        response = login_user(self, "+421 999 999998", "testing")
        self.assertEqual(response.content_type, "text/html; charset=utf-8")
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)

    def test_user_login_with_incorrect_password(self):
        response = login_user(self, "+421 999 999999", "test")
        self.assertEqual(response.content_type, "text/html; charset=utf-8")
        statuscode = response.status_code
        self.assertEqual(statuscode, 401)

    def test_put_one_user_index_content(self):
        login = login_user(self, "+421 999 999999", "testing")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/user/2", headers={'Authorization': 'Bearer ' + token}, data=dict(
            phone='+421 999 888888',
            password='test'
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 204)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    def test_delete_one_user_index_content(self):
        login = login_user(self, "+421 999 999999", "testing")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.delete("/api/v1/user/2", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 204)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")





class ServicesTest(unittest.TestCase):
    def test_get_all_services_index(self):
        tester = app.test_client(self)
        response = tester.get("/api/v1/services")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_get_all_services_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/api/v1/services")
        self.assertEqual(response.content_type, "application/json")
    #
    def test_get_all_services(self):
        response = app.test_client().get('/api/v1/services')
        res = json.loads(response.data.decode('utf-8'))
        assert type(res[0]) is dict
        assert 'id' in res[0]
        assert type(res[0]['id']) is int
        assert 'title' in res[0]
        assert type(res[0]['title']) is str
        assert 'estimate' in res[0]
        if res[0]['estimate'] is not None:
            assert type(res[0]['estimate']) is int
        assert 'avg_rating' in res[0]
        if res[0]['avg_rating'] is not None:
            assert type(res[0]['avg_rating']) is int
        print("test_get_all_services finished successfully")


class ServiceregisterTest(unittest.TestCase):
    def test_index_content_index(self):
        tester = app.test_client(self)
        response = tester.get("/api/v1/serviceregister")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_index_content_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/api/v1/serviceregister")
        self.assertEqual(response.content_type, "application/json")

    def test_get_all_serviceregister(self):
        response = app.test_client().get('/api/v1/serviceregister')
        res = json.loads(response.data.decode('utf8'))
        assert type(res[0]) is dict
        assert 'id' in res[0]
        assert type(res[0]['id']) is int
        assert 'hours' in res[0]
        if res[0]['hours'] is not None:
            assert type(res[0]['hours']) is int
        assert 'service_status' in res[0]
        assert type(res[0]['service_status']) is str
        assert 'end_time' in res[0]
        if res[0]['end_time'] is not None:
            assert type(res[0]['end_time']) is str
        assert 'rating' in res[0]
        if res[0]['rating'] is not None:
            assert type(res[0]['rating']) is int
        print("test_get_all_serviceregister finished successfully")


if __name__ == "__main__":
    unittest.main()
