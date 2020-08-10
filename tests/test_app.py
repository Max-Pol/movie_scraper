import unittest
from unittest.mock import patch
import requests as r
from app import app

# Fixtures
FIXTURES_FILM = [{
    "title": "Castle in the Sky",
    "url": "id"
}]
FIXTURES_PEOPLE = [{
    "name": "Colonel Muska",
    "films": ["id"]
}]
FIXTURES_EXPECTED_RESPONSE = b'[{"people":["Colonel Muska"],"title":"Castle in the Sky","url":"id"}]\n'


class BasicTests(unittest.TestCase):
    # executed before each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        pass

    # Test the movies endpoint, by mocking the Ghibli API
    @patch('app.get_people')
    @patch('app.get_films')
    def test_movies_success(self, get_films_mock, get_people_mock):
        # Mock API calls with a set of fixtures
        get_people_mock.return_value = FIXTURES_PEOPLE
        get_films_mock.return_value = FIXTURES_FILM

        # Check that we get the expected response
        response = self.app.get('/movies')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, FIXTURES_EXPECTED_RESPONSE)

    # Test the movies endpoint with an exception
    @patch('app.get_films')
    def test_movies_exceptions(self, get_films_mock):
        # Mock API calls with a set of fixtures
        get_films_mock.side_effect = r.Timeout
        # Check that we get the expected response
        response = self.app.get('/movies')
        self.assertEqual(response.status_code, 503)

    # Test the movies endpoint really use the cache instead of API
    def test_movies_caching(self):
        # TODO: Make two consecutive calls, updating the mock response
        # and assert that the two responses are the same
        pass


if __name__ == "__main__":
    unittest.main()
