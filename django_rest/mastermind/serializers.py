from rest_framework import serializers
from mastermind.models import *

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id','guess_limit','current_guess','status')

    def validate_guess_limit(self, value):
        if value <= 0:
            raise serializers.ValidationError("Guess Limit must be positive")
        return value
        
    current_guess = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)

class GameGuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id',)

class GuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guess
        fields = ('id','sequence','game','black_pegs','white_pegs')

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
