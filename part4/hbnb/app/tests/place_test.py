import unittest
from app import create_app


class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_place(self): # basic place creation
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy flat",
            "description": "Perfect for rainy weekends",
            "price": 45.0,
            "latitude": 50.62,
            "longitude": 3.048,
            "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "amenities": "None"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_place_no_descr(self): # place creation without description
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy flat",
            "price": 45.0,
            "description": "None",
            "latitude": 50.62,
            "longitude": 3.048,
            "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "amenities": "None"
        })
        self.assertEqual(response.status_code, 201)

    def test_negative_price(self): # verifying price cannot be a negative number
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy flat",
            "description": "Perfect for rainy weekends",
            "price": -45.0,
            "latitude": 50.62,
            "longitude": 3.048,
            "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(response.status_code, 400)

    def test_outofbounds_latitude(self): # testing response for out of bounds latitude
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy flat",
            "description": "Perfect for rainy weekends",
            "price": 45.0,
            "latitude": 800.62,
            "longitude": 3.048,
            "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(response.status_code, 400)

    def test_outofbounds_longitude(self): # testing response for out of bounds longitude
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy flat",
            "description": "Perfect for rainy weekends",
            "price": 45.0,
            "latitude": 50.62,
            "longitude": -203.048,
            "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(response.status_code, 400)

    def test_title_too_long(self): # testing response when title > 100 characters
        response = self.client.post('/api/v1/places/', json={
            "title": "Taumata­whakatangihanga­koauau­o­tamatea­turi­pukaka­piki­maunga­horo­nuku­pokai­whenua­ki­tana­tahu in North Island, New Zealand",
            "description": "Perfect for a walk",
            "price": 78.0,
            "latitude": 50.62,
            "longitude": -203.048,
            "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(response.status_code, 400)

    def test_no_owner_id(self): # testing response with missing owner id
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy flat",
            "description": "Perfect for rainy weekends",
            "price": 45.0,
            "latitude": 50.62,
            "longitude": -203.048,
            "owner_id": ""
        })
        self.assertEqual(response.status_code, 400)
