from django.urls import reverse
from rest_framework.test import APITestCase
from mastermind.views import *
from rest_framework import status

class StatusViewTests(APITestCase):
    statuses_url = reverse("statuses")

    def test_get_statuses(self):
        response = self.client.get(self.statuses_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GameStateViewTests(APITestCase):
    game_state_url = reverse("game-state", args=[1])
    games_url = '/api/v1/games/'

    def setUp(self):
        data = {
            "guess_limit": 1,
        }
        self.client.post(self.games_url, data, format='json')

    def test_get_game_state(self):
        response = self.client.get(self.game_state_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GameViewTests(APITestCase):
    games_url = '/api/v1/games/'
    game_url = "/api/v1/games/1/"
    
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

    def test_post_game(self):
        data = {
            "guess_limit": 1,
        }
        response = self.client.post(self.games_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)
    
    def test_post_game_wrong(self):
        data = {
            "guess_limit": "A",
        }
        response = self.client.post(self.games_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "guess_limit": -7,
        }
        response = self.client.post(self.games_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
        data = {
            "guess_limit": 1.5,
        }
        response = self.client.post(self.games_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "something_else": 2,
        }
        response = self.client.post(self.games_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class GuessViewTests(APITestCase):
    games_url = '/api/v1/games/'
    guesses_url = "/api/v1/games/1/guesses/"
    guess_url = "/api/v1/games/1/guesses/1/"
    
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

    def test_post_guess(self):
        data = {
            "sequence": "BBBB",
        }
        response = self.client.post(self.guesses_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)
    
    def test_post_guess_wrong(self):
        data = {
            "sequence": "AAAA",
        }
        response = self.client.post(self.guesses_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "sequence": "BBB",
        }
        response = self.client.post(self.guesses_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
        data = {
            "sequence": "BBBBB",
        }
        response = self.client.post(self.guesses_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "something_else": "BBBB",
        }
        response = self.client.post(self.guesses_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "sequence": "BBBB",
        }
        response = self.client.post(self.guesses_url, data, format='json')
        data = {
            "sequence": "BBBB",
        }
        response = self.client.post(self.guesses_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)