from django.urls import reverse
from rest_framework.test import APITestCase
from mastermind.views import *
from rest_framework import status

# Unit test for status view
class StatusViewTests(APITestCase):
    statuses_url = reverse("statuses")

    def test_get_statuses(self):
        response = self.client.get(self.statuses_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Unit test for game state view
class GameStateViewTests(APITestCase):
    game_state_url = reverse("game-state", args=[1])
    games_url = '/api/v1/games/'

    # Create a new game
    def setUp(self):
        data = {
            "guess_limit": 1,
        }
        self.client.post(self.games_url, data, format='json')

    def test_get_game_state(self):
        response = self.client.get(self.game_state_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Unit test for game view
class GameViewTests(APITestCase):
    games_url = '/api/v1/games/'
    game_url = "/api/v1/games/1/"
    
    # Create a new game
    def setUp(self):
        data = {
            "guess_limit": 1,
        }
        self.client.post(self.games_url, data, format='json')

    def test_get_games(self):
        response = self.client.get(self.games_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_game(self):
        response = self.client.get(self.game_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test create a game correctly
    def test_post_game(self):
        data = {
            "guess_limit": 1,
        }
        response = self.client.post(self.games_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # Test create a game wrongly
    def test_post_game_wrong(self):
        # post a string
        data = {
            "guess_limit": "A",
        }
        response = self.client.post(self.games_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # post a negative value
        data = {
            "guess_limit": -7,
        }
        response = self.client.post(self.games_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
        # post a float value
        data = {
            "guess_limit": 1.5,
        }
        response = self.client.post(self.games_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # post another attribute
        data = {
            "something_else": 2,
        }
        response = self.client.post(self.games_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# Unit test for guess view
class GuessViewTests(APITestCase):
    games_url = '/api/v1/games/'
    guesses_url = "/api/v1/games/1/guesses/"
    guess_url = "/api/v1/games/1/guesses/1/"
    
    # Create a new game and new guess
    def setUp(self):
        data = {
            "guess_limit": 2,
        }
        self.client.post(self.games_url, data, format='json')
        data = {
            "sequence": "BBBB",
        }
        self.client.post(self.guesses_url, data, format='json')

    def test_get_guesss(self):
        response = self.client.get(self.guesses_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_guess(self):
        response = self.client.get(self.guess_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test create a game correctly
    def test_post_guess(self):
        data = {
            "sequence": "BBBB",
        }
        response = self.client.post(self.guesses_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # Test create a game wrongly
    def test_post_guess_wrong(self):
        # post not existed colors
        data = {
            "sequence": "AAAA",
        }
        response = self.client.post(self.guesses_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # post 3 characters string
        data = {
            "sequence": "BBB",
        }
        response = self.client.post(self.guesses_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
        # post 5 characters string
        data = {
            "sequence": "BBBBB",
        }
        response = self.client.post(self.guesses_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # post another attribute
        data = {
            "something_else": "BBBB",
        }
        response = self.client.post(self.guesses_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # post guesses to pass guess limit
        data = {
            "sequence": "BBBB",
        }
        response = self.client.post(self.guesses_url, data, format='json')
        data = {
            "sequence": "BBBB",
        }
        response = self.client.post(self.guesses_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)