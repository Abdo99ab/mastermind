from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
import random

# list of colors Blue, Red, Yellow, Green, White, Orange
COLORS = ["R","B","Y","G","W","O"]
# list of status
STATUS_CHOICES = ["off", "ongoing", "won", "lost"]


# Mastermind Algorithm
# Given the secret sequence and a guess sequence, we can calculate the number of black pegs (The correct guesses in color and position) and the number of white pegs (The correct guesses in color only).
# We start by initializing b (black pegs) and w (white pegs) with 0.
# We create two tables to track down the positions already gone through for secret sequence and guess sequence.
# We start searching for the black pegs through one loop by incrementing b and adding both positions to the tracker if the color and position matches.
# After that, we search for white pegs through two loops, avoiding the positions already gone through by incrementing w and adding position to the tracker if the color matches
# Finally we return b and w.
def mastermind_algo(secret_sequence, guess_sequence):
    b = w = 0
    gone_through_ss = []
    gone_through_gs = []
    for i,cs in enumerate(secret_sequence):
        if guess_sequence[i] == cs:
            b+=1
            gone_through_ss.append(i)
            gone_through_gs.append(i)
    for i,cs in enumerate(secret_sequence):
        if i not in gone_through_ss:
            for j,cg in enumerate(guess_sequence):
                if j not in gone_through_gs and cs == cg:
                    gone_through_gs.append(j)
                    w+=1
                    break
    return b,w

# Create the secret sequence with 4 colors
def create_sequence():
    result = ""
    for _ in range(4):
        result += random.choice(COLORS)
    return result

def post_create_game(serializer, guess_limit):
    from mastermind.models import Game
    if serializer.is_valid():
        game = Game.objects.create(guess_limit=guess_limit, sequence=create_sequence())
        return Response({"game":game.id,"data":serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def post_create_guess(serializer, game_id, sequence):
    from mastermind.models import Game, Guess
    if serializer.is_valid():
        game = Game.objects.filter(pk=game_id).annotate(
            # Calculate the number of guesses in each game
            current_guess=Count("guess")
        ).first()
        if game is None:
            return Response({"detail":"Not found."}, status=status.HTTP_404_NOT_FOUND)
        # if guess limit reached, the new test can't be accepted we return lost status
        if game.status == STATUS_CHOICES[2]:
            return Response({"game":game.id,"data":{"status":game.status}}, status=status.HTTP_403_FORBIDDEN)
        if game.guess_limit - game.current_guess <= 0:
            if game.status != STATUS_CHOICES[2]:
                game.status = STATUS_CHOICES[3]
                game.save()
            return Response({"game":game.id,"data":{"status":game.status}}, status=status.HTTP_403_FORBIDDEN)
        guess = Guess.objects.create(game=game, sequence=sequence)
        guess.black_pegs, guess.white_pegs = mastermind_algo(game.sequence, guess.sequence)
        # if black pegs is 4 we put status as win
        if guess.black_pegs == 4:
            game.status = STATUS_CHOICES[2]
        # if black pegs is not 4 and guess limit reached we put status as lost
        elif game.guess_limit - (game.current_guess + 1) <= 0:
            game.status = STATUS_CHOICES[3]
        # if black pegs is not 4 and guess limit is not reached we put status as ongoing
        else:
            game.status = STATUS_CHOICES[1]
        guess.save()
        game.save()
        return Response({"game":game.id,"guess":guess.id,"data":serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
