from timebank import app
import unittest
import json


def login_user(self, phone, password):
    tester = app.test_client(self)
    response = tester.post("/api/v1/user/login", json={
        'phone': phone,
        'password': password
    })
    return response


def register_user(self, phone, password, password_val, user_name):
    tester = app.test_client(self)
    response = tester.post("/api/v1/user-create", json={
        'phone': phone,
        'password': password,
        'password_val': password_val,
        'user_name': user_name
    })
    return response


class Test(unittest.TestCase):
    def test0001(self):
        response = register_user(self, "+421 900 000000", "test1", "test1", "Testinguser1")  # Vytvor user 1 so spravnymi udajmi
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test0002(self):
        response = register_user(self, "+421 900 000001", "test2", "test2", "Testinguser2")  # Vytvor user 2 so spravnymi udajmi
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test0003(self):
        response = register_user(self, "+421 900 000001", "test2", "test2", "Testinguser3")  # Test o vytvorenie usera s rovnakym telefonnym cislom
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 405)

    def test0004(self):
        response = register_user(self, "+421900000001", "test2", "test2", "Testinguser3")  # Test o vytvorenie usera s nespravnym formatom telefonneho cisla
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

    def test0005(self):
        response = register_user(self, "+421 900 000002", "test2", "test1", "Testinguser3")  # Test o vytvorenie usera s roznymi heslami
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

    def test0011(self):
        response = login_user(self, "+421 900 000000", "test1")  # Test prihlasenie user 1
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 201)

    def test0012(self):
        response = login_user(self, "+421 900 000001", "test2")  # Test prihlasenie user 2
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 201)

    def test0013(self):
        response = login_user(self, "+421 900 000000", "test2")  # Test prihlasenie user 1 s nespravnym heslom
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 401)

    def test0014(self):
        response = login_user(self, "+421 900 000002", "test1")  # Test prihlasenie s neexistujucim telefonnym cislom
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)

    def test0015(self):  # Test na overenie informacii s get all users
        tester = app.test_client(self)
        response = tester.get("/api/v1/users")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")
        res = json.loads(response.data.decode('utf-8'))
        assert type(res[0]) is dict
        assert type(res[1]) is dict
        assert 'id' in res[0]
        assert type(res[0]['id']) is int
        assert 'phone' in res[0]
        assert type(res[0]['phone']) is str
        assert 'user_name' in res[0]
        assert type(res[0]['user_name']) is str
        assert 'time_account' in res[0]
        assert type(res[0]['time_account']) is int

    def test0016(self):  # Overenie existencie user 1
        tester = app.test_client(self)
        response = tester.get("/api/v1/user/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")

    def test0017(self):  # Overenie existencie user 2
        tester = app.test_client(self)
        response = tester.get("/api/v1/user/2")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")

    def test0021(self):
        login = login_user(self, "+421 900 000000", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.post("/api/v1/service-create", headers={'Authorization': 'Bearer ' + token}, data=dict(
            title='Testing',
            user_id=1,
            estimate=5
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")
    #
    # def test_user_login_with_correct_data(self):
    #     response = login_user(self, "+421 999 999999", "testing")
    #     self.assertEqual(response.content_type, "application/json")
    #     statuscode = response.status_code
    #     self.assertEqual(statuscode, 201)
    #
    # def test_user_login_with_incorrect_phone(self):
    #     response = login_user(self, "+421 999 999998", "testing")
    #     self.assertEqual(response.content_type, "text/html; charset=utf-8")
    #     statuscode = response.status_code
    #     self.assertEqual(statuscode, 404)
    #
    # def test_user_login_with_incorrect_password(self):
    #     response = login_user(self, "+421 999 999999", "test")
    #     self.assertEqual(response.content_type, "text/html; charset=utf-8")
    #     statuscode = response.status_code
    #     self.assertEqual(statuscode, 401)
    #
    # def test_put_one_user_index_content(self):
    #     login = login_user(self, "+421 999 999999", "testing")
    #     tester = app.test_client(self)
    #     token = login.json['access_token']
    #     response = tester.put("/api/v1/user/9", headers={'Authorization': 'Bearer ' + token}, data=dict(
    #         phone='+421 999 888888',
    #         user_name='Testname',
    #         password='test'
    #     ))
    #     statuscode = response.status_code
    #     self.assertEqual(statuscode, 204)
    #     self.assertEqual(response.content_type, "text/html; charset=utf-8")
    #
    #




#
# class ServicesTest(unittest.TestCase):
#     def test_get_all_services_index(self):
#         tester = app.test_client(self)
#         response = tester.get("/api/v1/services")
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 200)
#
#     def test_get_all_services_index_content(self):
#         tester = app.test_client(self)
#         response = tester.get("/api/v1/services")
#         self.assertEqual(response.content_type, "application/json")
#     #
#     def test_get_all_services(self):
#         response = app.test_client().get('/api/v1/services')
#         res = json.loads(response.data.decode('utf-8'))
#         assert type(res[0]) is dict
#         assert 'id' in res[0]
#         assert type(res[0]['id']) is int
#         assert 'title' in res[0]
#         assert type(res[0]['title']) is str
#         assert 'estimate' in res[0]
#         if res[0]['estimate'] is not None:
#             assert type(res[0]['estimate']) is int
#         assert 'avg_rating' in res[0]
#         if res[0]['avg_rating'] is not None:
#             assert type(res[0]['avg_rating']) is int
#         print("test_get_all_services finished successfully")
#
#
# class ServiceregisterTest(unittest.TestCase):
#     def test_index_content_index(self):
#         tester = app.test_client(self)
#         response = tester.get("/api/v1/serviceregister")
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 200)
#
#     def test_index_content_index_content(self):
#         tester = app.test_client(self)
#         response = tester.get("/api/v1/serviceregister")
#         self.assertEqual(response.content_type, "application/json")
#
#     def test_get_all_serviceregister(self):
#         response = app.test_client().get('/api/v1/serviceregister')
#         res = json.loads(response.data.decode('utf8'))
#         assert type(res[0]) is dict
#         assert 'id' in res[0]
#         assert type(res[0]['id']) is int
#         assert 'hours' in res[0]
#         if res[0]['hours'] is not None:
#             assert type(res[0]['hours']) is int
#         assert 'service_status' in res[0]
#         assert type(res[0]['service_status']) is str
#         assert 'end_time' in res[0]
#         if res[0]['end_time'] is not None:
#             assert type(res[0]['end_time']) is str
#         assert 'rating' in res[0]
#         if res[0]['rating'] is not None:
#             assert type(res[0]['rating']) is int
#         print("test_get_all_serviceregister finished successfully")

    def test0901(self):
        login = login_user(self, "+421 900 000000", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.delete("/api/v1/service/1", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 204)
        self.assertEqual(response.content_type, "application/json")

    def test1001(self):
        login = login_user(self, "+421 900 000000", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.delete("/api/v1/user/2", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 204)
        self.assertEqual(response.content_type, "application/json")

    def test1002(self):
        login = login_user(self, "+421 900 000000", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.delete("/api/v1/user/1", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 204)
        self.assertEqual(response.content_type, "application/json")

if __name__ == "__main__":
    unittest.main()
