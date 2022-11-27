from django.urls import path, include
from rest_framework_nested import routers
from mastermind.views import *

router = routers.DefaultRouter()
router.register(r'games', GameView)
game_router = routers.NestedDefaultRouter(router, r'games', lookup='game')
game_router.register(r'guesses', GuessView, basename='game-guesses')

urlpatterns = [
    path('', include(router.urls),name="game"),
    path('', include(game_router.urls),name="game-guesses"),
    path('statuses/', StatusView.as_view(), name="statuses"),
    path('game-state/<int:pk>/', GameStateView.as_view(),name="game-state"),
]