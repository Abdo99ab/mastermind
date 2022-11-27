from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from mastermind.serializers import *
from mastermind.models import *

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

# Create status view with only get method
class StatusView(APIView):
    def get(self, request):
        return Response(STATUS_CHOICES)

# Create game state view with only get method to get a given game state with customized result (parsed)
class GameStateView(APIView):
    def get(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            return Response(game.parsed())
        except Game.DoesNotExist:
            return Response({"game":"Game with id {} Does not exist".format(pk)}, status=status.HTTP_400_BAD_REQUEST)

# Create game view, to access all games or a given game, and to create a new game
class GameView(viewsets.ModelViewSet):
    queryset = Game.objects.all().annotate(
        # Calculate the number of guesses in each game
        current_guess=Count("guess")
    )
    serializer_class = GameSerializer
    http_method_names = ["get", "post", "head"]
    def get_queryset(self):
        return super().get_queryset()

    def create(self, request, **kwargs):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            guess_limit = request.data.get("guess_limit")
            game = Game.objects.create(guess_limit=guess_limit)
            return Response({"game":game.id,"data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create guess view, to access all guesses or a given guess inside a game, and to create a new guess
class GuessView(viewsets.ModelViewSet):
    queryset = Guess.objects.all()
    serializer_class = GuessSerializer
    http_method_names = ["get", "post", "head"]

    def get_queryset(self):
        return Guess.objects.filter(game=self.kwargs.get('game_pk'))

    def create(self, request, **kwargs):
        serializer = GuessSerializer(data=request.data)
        if serializer.is_valid():
            game_id = self.kwargs.get('game_pk')
            sequence = request.data.get("sequence")
            game = Game.objects.filter(pk=game_id).annotate(
                # Calculate the number of guesses in each game
                current_guess=Count("guess")
            ).first()
            if game is None:
                return Response({"game":"Game with id {} Does not exist".format(game_id)}, status=status.HTTP_400_BAD_REQUEST)
            # if guess limit reached, the new test can't be accepted we return lost status
            if game.guess_limit - game.current_guess <= 0:
                if game.status != STATUS_CHOICES[2]:
                    game.status = STATUS_CHOICES[3]
                    game.save()
                return Response({"status":game.status}, status=status.HTTP_403_FORBIDDEN)
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
        