from datetime import datetime

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
        response = register_user(self, "+421 900 000001", "test1", "test1", "Testinguser1")  # Vytvor user 1 so spravnymi udajmi
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test0002(self):
        response = register_user(self, "+421 900 000002", "test2", "test2", "Testinguser2")  # Vytvor user 2 so spravnymi udajmi
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
        response = login_user(self, "+421 900 000001", "test1")  # Test prihlasenie user 1
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 201)

    def test0012(self):
        response = login_user(self, "+421 900 000002", "test2")  # Test prihlasenie user 2
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 201)

    def test0013(self):
        response = login_user(self, "+421 900 000001", "test2")  # Test prihlasenie user 1 s nespravnym heslom
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 401)

    def test0014(self):
        response = login_user(self, "+421 900 000000", "test1")  # Test prihlasenie s neexistujucim telefonnym cislom
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

        assert res[0]['id'] == 1
        assert res[0]['phone'] == "+421 900 000001"
        assert res[0]['user_name'] == "Testinguser1"
        assert res[0]['time_account'] == 0

        assert res[1]['id'] == 2
        assert res[1]['phone'] == "+421 900 000002"
        assert res[1]['user_name'] == "Testinguser2"
        assert res[1]['time_account'] == 0

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

    def test0021(self):  # Vytvorenie service pre user 1
        login = login_user(self, "+421 900 000001", "test1")
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

    def test0022(self):  # Test na overenie informacii s get all services
        tester = app.test_client(self)
        response = tester.get("/api/v1/services")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")
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

        assert res[0]['id'] == 1
        assert res[0]['title'] == 'Testing'
        assert res[0]['estimate'] == 5
        assert res[0]['avg_rating'] is None

    def test0031(self):  # Test na vytvorenie serviceregister s user 2 na service 1
        login = login_user(self, "+421 900 000002", "test2")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.post("/api/v1/serviceregister-create", headers={'Authorization': 'Bearer ' + token}, data=dict(
            service_id=1,
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")

    def test0032(self):  # Test na vytvorenie serviceregister s user 1 na service 1
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.post("/api/v1/serviceregister-create", headers={'Authorization': 'Bearer ' + token}, data=dict(
            service_id=1,
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0041(self):  # Test na overenie informacii zo serviceregister
        tester = app.test_client(self)
        response = tester.get("/api/v1/serviceregister")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")
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

        assert res[0]['id'] == 1
        assert res[0]['hours'] is None
        assert res[0]['service_status'] == 'inprogress'
        assert res[0]['end_time'] is None
        assert res[0]['rating'] is None

    def test0051(self):  # Test na ukoncenie serviceregister
        login = login_user(self, "+421 900 000002", "test2")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/1/5/3", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")

    def test0052(self):  # Test na overenie informacii zo serviceregister
        tester = app.test_client(self)
        response = tester.get("/api/v1/serviceregister/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")
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

        assert res[0]['id'] == 1
        assert res[0]['hours'] == 5
        assert res[0]['service_status'] == 'ended'
        assert datetime.strptime(str(res[0]['end_time']), "%a, %d %b %Y %H:%M:%S %Z")
        assert res[0]['rating'] == 3






    def test0801(self):
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.delete("/api/v1/serviceregister/1", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 204)
        self.assertEqual(response.content_type, "application/json")

    def test0901(self):
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.delete("/api/v1/service/1", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 204)
        self.assertEqual(response.content_type, "application/json")

    def test1001(self):
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.delete("/api/v1/user/2", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 204)
        self.assertEqual(response.content_type, "application/json")

    def test1002(self):
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.delete("/api/v1/user/1", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 204)
        self.assertEqual(response.content_type, "application/json")


if __name__ == "__main__":
    unittest.main()
