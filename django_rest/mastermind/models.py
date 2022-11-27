from django.db import models
import random

COLORS = ["R","B","Y","G","W","O"]
STATUS_CHOICES = ["off", "ongoing", "won", "lost"]

class Game(models.Model):

    def create_sequence():
        result = ""
        for _ in range(4):
            result += random.choice(COLORS)
        return result

    sequence = models.CharField(max_length=4,default=create_sequence)
    guess_limit = models.IntegerField()
    status = models.CharField(default=STATUS_CHOICES[0],max_length=20)

    class Meta:
        verbose_name = "Game"
        verbose_name_plural = "Games"

    def __str__(self):
        return str(self.id)

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

class Guess(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    sequence = models.CharField(max_length=4)
    black_pegs = models.IntegerField(default=0)
    white_pegs = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Guess"
        verbose_name_plural = "Guesses"

    def __str__(self):
        return "{}->{}".format(self.game.id, self.id)