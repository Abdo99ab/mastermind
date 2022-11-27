from rest_framework import serializers
from mastermind.models import *

# Game serializer
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id','guess_limit','current_guess','status')

    # Validate guess limit avoid negative or null entries
    def validate_guess_limit(self, value):
        if value <= 0:
            raise serializers.ValidationError("Guess Limit must be positive")
        return value
        
    # Added view field to calculate the current guess number
    current_guess = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)

# Game serializer inside Guess
class GameGuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id',)

# Guess serializer
class GuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guess
        fields = ('id','sequence','game','black_pegs','white_pegs')

    # Validate guess sequence avoid less than 4 chacters and charcters not in COLORS
    def validate_sequence(self, value):
        if len(value) < 4:
            raise serializers.ValidationError('Sequence must have exactly 4 colors')
        for c in value:
            if c not in COLORS:
                raise serializers.ValidationError('Colors used in sequence must be [{}]'.format(', '.join(COLORS)))
        return value

    black_pegs = serializers.IntegerField(read_only=True)
    white_pegs = serializers.IntegerField(read_only=True)
    game = GameGuessSerializer(read_only=True)
