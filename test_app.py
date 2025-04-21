import unittest
from app import app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the app for testing
        app.testing = True
        self.client = app.test_client()

    def test_hello(self):
        # Test the home route
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Hello, World!")

if __name__ == '__main__':
    unittest.main()