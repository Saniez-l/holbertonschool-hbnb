import unittest
from app import create_app


class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_review(self): # basic review creation
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Even better than the pictures",
            "rating": 5,
            "place_id": "8ga95b64-6412-1523-b4cf-2b873f56baf5",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(response.status_code, 201)

    def test_no_text_review(self): # trying to create an empty review
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 4,
            "place_id": "8ga95b64-6412-1523-b4cf-2b873f56baf5",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(response.status_code, 400)

    def test_no_rating_review(self): # trying to create a review with invalid rating
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Even better than the pictures",
            "rating": 0,
            "place_id": "8ga95b64-6412-1523-b4cf-2b873f56baf5",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(response.status_code, 400)

    def test_no_place_review(self): # trying to create a review unattached to a place
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Even better than the pictures",
            "rating": 0,
            "place_id": "",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(response.status_code, 400)

    def test_no_user_review(self): # trying to create a review not bound to a user
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Even better than the pictures",
            "rating": 5,
            "place_id": "8ga95b64-6412-1523-b4cf-2b873f56baf5",
            "user_id": ""
        })
        self.assertEqual(response.status_code, 400)
