from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from mastermind.serializers import *
from mastermind.models import *

def mastermind_algo(secret_sequence, guess_sequence):
    b = w = 0
    gone_through = []
    for i,cs in enumerate(secret_sequence):
        if guess_sequence[i] == cs:
            b+=1
            gone_through.append(i)
    for i,cs in enumerate(secret_sequence):
        if i not in gone_through:
            for j,cg in enumerate(guess_sequence):
                if cs == cg:
                    gone_through.append(i)
                    w+=1
    return b,w

class StatusView(APIView):
    def get(self, request):
        return Response(STATUS_CHOICES)

class GameView(viewsets.ModelViewSet):
    queryset = Game.objects.all().annotate(
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
                current_guess=Count("guess")
            ).first()
            if game is None:
                return Response({"game":"Game with id {} Does not exist".format(game_id)}, status=status.HTTP_400_BAD_REQUEST)
            if game.guess_limit - game.current_guess <= 0:
                if game.status != STATUS_CHOICES[2]:
                    game.status = STATUS_CHOICES[3]
                    game.save()
                return Response({"status":game.status}, status=status.HTTP_403_FORBIDDEN)
            guess = Guess.objects.create(game=game, sequence=sequence)
            guess.black_pegs, guess.white_pegs = mastermind_algo(game.sequence, guess.sequence)
            if guess.black_pegs == 4:
                game.status = STATUS_CHOICES[2]
            elif game.guess_limit - (game.current_guess + 1) <= 0:
                game.status = STATUS_CHOICES[3]
            else:
                game.status = STATUS_CHOICES[1]
            guess.save()
            game.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        