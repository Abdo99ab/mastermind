from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from mastermind.serializers import GuessSerializer, GameSerializer
from mastermind.models import Game, Guess
from mastermind.utils import STATUS_CHOICES, mastermind_algo, post_create_game, post_create_guess

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
            return Response({"detail":"Not found."}, status=status.HTTP_404_NOT_FOUND)

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
        post_create_game(serializer, request.data.get("guess_limit"))

# Create guess view, to access all guesses or a given guess inside a game, and to create a new guess
class GuessView(viewsets.ModelViewSet):
    queryset = Guess.objects.all()
    serializer_class = GuessSerializer
    http_method_names = ["get", "post", "head"]

    def get_queryset(self):
        return Guess.objects.filter(game=self.kwargs.get('game_pk'))

    def create(self, request, **kwargs):
        serializer = GuessSerializer(data=request.data)
        return post_create_guess(serializer, self.kwargs.get('game_pk'), request.data.get("sequence"))
        