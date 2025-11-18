import unittest
from app import create_app


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self): #tests successful use case
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self): #tests invalid input data
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_long_first_name(self): #tests first name longer than 50 characters
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Florm Rox Fey Fenerill-Slam Slitheen of Raxacoricofallapatorius",
            "last_name": "Who",
            "email": "flormrox@drwhomst.co.uk"
        })
        self.assertEqual(response.status_code, 400)

    def test_long_last_name(self): #tests last name longer than 50 characters
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Tim",
            "last_name": "Kist Magg Thek Lutiven-Day Slitheen of Raxacoricofallapatorius",
            "email": "kistmagg@drwhomst.co.uk"
        })
        self.assertEqual(response.status_code, 400)

    def test_names_are_numbers(self): # tests numeric first and last names
        response = self.client.post('/api/v1/users/', json={
            "first_name": 1234,
            "last_name": 5678,
            "email": "numb3rz@email.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_registered_email(self): #tests use of registered email
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Janet",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_email_is_numbers(self): # tests email if @ . format is ok, but everything else is numbers
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Tim",
            "last_name": "Cook",
            "email": "12345@678.910"
        })
        self.assertEqual(response.status_code, 400)

    def test_email_has_two_ats(self): # tests email with two @'s
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Tim",
            "last_name": "Cook",
            "email": "123@45@678.910"
        })
        self.assertEqual(response.status_code, 400)
