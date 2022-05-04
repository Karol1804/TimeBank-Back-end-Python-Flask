try:
    from timebank import app
    import unittest
    import json
except Exception as e:
    print("Some modules are Missing {}".format(e))


class UsersTest(unittest.TestCase):
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/api/v1/users")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/api/v1/users")
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
        print("test_get_all_users finished successfully")


class ServicesTest(unittest.TestCase):
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/api/v1/services")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_index_content(self):
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
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/api/v1/serviceregister")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_index_content(self):
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