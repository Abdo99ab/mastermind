from utils import games
from app import app
import unittest

# Unit test for status view
class StatusTest(unittest.TestCase):
    def test_get_status(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/statuses/')
        self.assertEqual(response.status_code, 200)

# Unit test for game state view
class GameStateTest(unittest.TestCase):
    # Create a new game
    @classmethod
    def setUpClass(cls):
        games.append({
            "id":1,
            "guess_limit":3,
            "sequence": "BYOB",
            "status":"off",
            "guesses": []
        })

    def test_get_game_state(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/game-state/1/')
        self.assertEqual(response.status_code, 200)
    
# Unit test for game view
class GameTest(unittest.TestCase):
    # Create a new game
    @classmethod
    def setUpClass(cls):
        games.append({
            "id":1,
            "guess_limit":3,
            "sequence": "BYOB",
            "status":"off",
            "guesses": []
        })

    def test_get_games(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/games/')
        self.assertEqual(response.status_code, 200)
    
    def test_get_game(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/games/1/')
        self.assertEqual(response.status_code, 200)

    # Test create a game correctly
    def test_post_game(self):
        data = {
            "guess_limit": 1,
        }
        tester = app.test_client(self)
        response = tester.post('/api/v1/games/',json=data)
        self.assertEqual(response.status_code, 201)
    
    # Test create a game wrongly
    def test_post_game_wrong(self):
        # post a string
        data = {
            "guess_limit": "A",
        }
        tester = app.test_client(self)
        response = tester.post('/api/v1/games/',json=data)
        self.assertEqual(response.status_code, 400)

        # post a negative value
        data = {
            "guess_limit": -7,
        }
        tester = app.test_client(self)
        response = tester.post('/api/v1/games/',json=data)
        self.assertEqual(response.status_code, 400)

        # post a float value
        data = {
            "guess_limit": 1.5,
        }
        tester = app.test_client(self)
        response = tester.post('/api/v1/games/',json=data)
        self.assertEqual(response.status_code, 400)

        # post another attribute
        data = {
            "something_else": 2,
        }
        tester = app.test_client(self)
        response = tester.post('/api/v1/games/',json=data)
        self.assertEqual(response.status_code, 400)

# Unit test for guess view
class GuessTest(unittest.TestCase):
    # Create a new game and new guess
    @classmethod
    def setUpClass(cls):
        games.append({
            "id":2,
            "guess_limit":2,
            "sequence": "BYOB",
            "status":"ongoing",
            "guesses": [
                {
                    "id":1,
                    "sequence":"RBOB",
                    "black_pegs":1,
                    "white_pegs":2
                }
            ]
        })

    def test_get_guesses(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/games/2/guesses/')
        self.assertEqual(response.status_code, 200)

    def test_get_guess(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/games/2/guesses/1/')
        self.assertEqual(response.status_code, 200)

    # Test create a game correctly
    def test_post_guess(self):
        data = {
            "sequence": "BBOO",
        }
        tester = app.test_client(self)
        response = tester.post('/api/v1/games/2/guesses/',json=data)
        self.assertEqual(response.status_code, 201)

    # Test create a game wrongly
    def test_post_guess_wrong(self):
        # post not existed colors
        data = {
            "sequence": "AAAA",
        }
        tester = app.test_client(self)
        response = tester.post('/api/v1/games/2/guesses/',json=data)
        self.assertEqual(response.status_code, 400)

        # post 3 characters string
        data = {
            "sequence": "BBB",
        }
        tester = app.test_client(self)
        response = tester.post('/api/v1/games/2/guesses/',json=data)
        self.assertEqual(response.status_code, 400)

        # post 5 characters string
        data = {
            "sequence": "BBBBB",
        }
        tester = app.test_client(self)
        response = tester.post('/api/v1/games/2/guesses/',json=data)
        self.assertEqual(response.status_code, 400)

        # post another attribute
        data = {
            "something_else": "BBOO",
        }
        tester = app.test_client(self)
        response = tester.post('/api/v1/games/2/guesses/',json=data)
        self.assertEqual(response.status_code, 400)

        # post guesses to pass guess limit
        data = {
            "sequence": "BBOO",
        }
        tester = app.test_client(self)
        response = tester.post('/api/v1/games/2/guesses/',json=data)
        data = {
            "sequence": "BBOO",
        }
        tester = app.test_client(self)
        response = tester.post('/api/v1/games/2/guesses/',json=data)
        self.assertEqual(response.status_code, 403)


# Run tests
if __name__=="__main__":
    unittest.main()