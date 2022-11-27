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

    def __str__(self):
        return str(self.id)

class Guess(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    sequence = models.CharField(max_length=4)
    black_pegs = models.IntegerField(default=0)
    white_pegs = models.IntegerField(default=0)

    def __str__(self):
        return "{}->{}".format(self.game.id, self.id)