import unittest
import json
from src.main import app

class TattooDesignerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_generate_tattoo_success(self):
        response = self.app.post(
            '/api/generate_tattoo',
            data=json.dumps({
                'first_name': 'John',
                'last_name': 'Doe',
                'date_of_birth': '01/01/1990',
                'age': 35
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('symbolic_analysis', data)
        self.assertIn('core_tattoo_theme', data)
        self.assertIn('visual_motif_description', data)
        self.assertIn('placement_suggestion', data)
        self.assertIn('mystical_insight', data)
        self.assertIn('image_prompt', data)

    def test_generate_tattoo_missing_data(self):
        response = self.app.post(
            '/api/generate_tattoo',
            data=json.dumps({
                'first_name': 'John',
                'last_name': 'Doe',
                'age': 35
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Missing input data')

    def test_generate_tattoo_invalid_dob(self):
        response = self.app.post(
            '/api/generate_tattoo',
            data=json.dumps({
                'first_name': 'John',
                'last_name': 'Doe',
                'date_of_birth': 'invalid_date',
                'age': 35
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Invalid date of birth format. Use dd/mm/yyyy')

    def test_generate_tattoo_invalid_first_name(self):
        response = self.app.post(
            '/api/generate_tattoo',
            data=json.dumps({
                'first_name': '',
                'last_name': 'Doe',
                'date_of_birth': '01/01/1990',
                'age': 35
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'First name must be a non-empty string')

    def test_generate_tattoo_invalid_age(self):
        response = self.app.post(
            '/api/generate_tattoo',
            data=json.dumps({
                'first_name': 'John',
                'last_name': 'Doe',
                'date_of_birth': '01/01/1990',
                'age': -5
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Age must be a positive integer')

if __name__ == '__main__':
    unittest.main()


