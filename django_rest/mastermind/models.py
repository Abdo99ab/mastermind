from django.db import models
import random

# list of colors Blue, Red, Yellow, Green, White, Orange
COLORS = ["R","B","Y","G","W","O"]
# list of status
STATUS_CHOICES = ["off", "ongoing", "won", "lost"]

# Game model
class Game(models.Model):

    # Create the secret sequence with 4 colors
    def create_sequence():
        result = ""
        for _ in range(4):
            result += random.choice(COLORS)
        return result

    # Game fields
    sequence = models.CharField(max_length=4,default=create_sequence)
    guess_limit = models.IntegerField()
    status = models.CharField(default=STATUS_CHOICES[0],max_length=20)

    # Meta class with verbose names
    class Meta:
        verbose_name = "Game"
        verbose_name_plural = "Games"

    # Game instance name appearance
    def __str__(self):
        return str(self.id)

    # customized parser to send in a response
    def parsed(self):
        guesses = Guess.objects.filter(game=self.pk).order_by('-pk')
        if len(guesses) == 0:
            return {
                "id": self.pk,
                "guess_limit": self.guess_limit,
                "status": self.status,
            }
        return {
            "id": self.pk,
            "guess_limit": self.guess_limit,
            "status": self.status,
            "current_guess": len(guesses),
            "current_guess_id": guesses.first().pk,
            "current_guess_sequence": guesses.first().sequence,
            "current_guess_black_pegs": guesses.first().black_pegs,
            "current_guess_white_pegs": guesses.first().white_pegs,
        }

# Guess model
class Guess(models.Model):

    # Guess fields
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    sequence = models.CharField(max_length=4)
    black_pegs = models.IntegerField(default=0)
    white_pegs = models.IntegerField(default=0)

    # Meta class with verbose names
    class Meta:
        verbose_name = "Guess"
        verbose_name_plural = "Guesses"

    # Guess instance name appearance
    def __str__(self):
        return "{}->{}".format(self.game.id, self.id)