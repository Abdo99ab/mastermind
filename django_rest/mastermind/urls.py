from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.documentation import include_docs_urls
from mastermind.views import StatusView, GameStateView, GameView, GuessView

# Create default router
router = routers.DefaultRouter()
# register games /api/v1/games
router.register(r'games', GameView)
# Create nested default router to make the guesses path appear inside related game path
game_router = routers.NestedDefaultRouter(router, r'games', lookup='game')
game_router.register(r'guesses', GuessView, basename='game-guesses')

urlpatterns = [
    path('', include(router.urls),name="game"),
    path('', include(game_router.urls),name="game-guesses"),
    path('statuses/', StatusView.as_view(), name="statuses"),
    # Create game state path to show customized result for a given game
    path('game-state/<int:pk>/', GameStateView.as_view(),name="game-state"),
    path('docs/', include_docs_urls(title='Mastermind REST'))
]