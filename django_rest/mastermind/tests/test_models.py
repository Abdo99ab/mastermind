from django.test import TestCase
from mastermind.models import Game, Guess

# Unit test for Game model
class GameTest(TestCase):
    def create_game(self,guess_limit=3,sequence="BBBB",status="off"):
        return Game.objects.create(guess_limit=guess_limit,sequence=sequence,status=status)

    def test_game_creation(self):
        game = self.create_game()
        self.assertTrue(isinstance(game,Game))
        self.assertTrue(isinstance(game.sequence,str))
        self.assertTrue(isinstance(game.status,str))
        self.assertTrue(isinstance(game.guess_limit,int))

# Unit test for Guess model
class GuessTest(TestCase):
    def create_game(self,guess_limit=3,sequence="BBBB",status="off"):
        return Game.objects.create(guess_limit=guess_limit,sequence=sequence,status=status)

    def create_guess(self,sequence="BBBB",black_pegs=0,white_pegs=0):
        game = self.create_game()
        return Guess.objects.create(sequence=sequence,black_pegs=black_pegs,white_pegs=white_pegs,game=game)
    
    def test_guess_creation(self):
        guess = self.create_guess()
        self.assertTrue(isinstance(guess,Guess))
        self.assertTrue(isinstance(guess.game,Game))
        self.assertTrue(isinstance(guess.sequence,str))
        self.assertTrue(isinstance(guess.black_pegs,int))
        self.assertTrue(isinstance(guess.white_pegs,int))