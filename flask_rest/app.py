from flask import Flask, jsonify, request
from games import games
from utils import *

app = Flask(__name__)

@app.route('/api/v1/statuses/', methods=['GET'])
def getStatuses():
    return jsonify(STATUS_CHOICES)

# Testing Route
@app.route('/api/v1/game-state/<int:pk>/', methods=['GET'])
def getGameState(pk):
    for game in games:
        if game.get('id') == pk:
            return jsonify(parsed_game_state(game))
    return jsonify({"detail":"Not found."}), 404

@app.route('/api/v1/games/', methods=['GET'])
def getGames():
    parsed_games = []
    for game in games:
            parsed_games.append(parsed_game(game))
    return jsonify(parsed_games)

@app.route('/api/v1/games/<int:pk>/', methods=['GET'])
def getGame(pk):
    for game in games:
        if game.get('id') == pk:
            return jsonify(parsed_game(game))
    return jsonify({"detail":"Not found."}), 404

@app.route('/api/v1/games/<int:pk>/guesses/', methods=['GET'])
def getGuesses(pk):
    parsed_guesses = []
    for game in games:
        if game.get('id') == pk:
            for guess in game.get('guesses'):
                parsed_guesses.append(parsed_guess(game,guess))
            return jsonify(parsed_guesses)
    return jsonify({"detail":"Not found."}), 404

@app.route('/api/v1/games/<int:pk>/guesses/<int:pk2>/', methods=['GET'])
def getGuess(pk,pk2):
    for game in games:
        if game.get('id') == pk:
            for guess in game.get('guesses'):
                if guess.get('id') == pk2:
                    return jsonify(parsed_guess(game,guess))
    return jsonify({"detail":"Not found."}), 404

@app.route('/api/v1/games/', methods=['POST'])
def addGame():
    new_id = list(sorted(games,key=lambda x:x.get('id'),reverse=True))[0].get('id')+1
    guess_limit, validator = validate_guess_limit(request.json.get('guess_limit'))
    if guess_limit is None:
        return jsonify(validator), 400
    new_game = {
        'id':new_id,
        'guess_limit': guess_limit,
        'sequence': create_sequence(),
        'status': STATUS_CHOICES[0],
        "guesses": []
    }
    games.append(new_game)
    return jsonify({"game":new_id,"data":{"guess_limit":guess_limit}}), 201

@app.route('/api/v1/games/<int:pk>/guesses/', methods=['POST'])
def addGuess(pk):
    for game in games:
        if game.get('id') == pk:
            guesses = game.get('guesses')
            if len(guesses) > 0:
                new_id = list(sorted(guesses,key=lambda x:x.get('id'),reverse=True))[0].get('id')+1
            else:
                new_id = 1
            sequence, validator = validate_sequence(request.json.get('sequence'))
            if sequence is None:
                return jsonify(validator), 400
            if game.get('status') == STATUS_CHOICES[2]:
                return jsonify({"game":game.get('id'),"data":{"status":game.get('status')}}), 403
            if game.get('guess_limit') - len(guesses) <= 0:
                if game.get('status') != STATUS_CHOICES[2]:
                    game['status'] = STATUS_CHOICES[3]
                return jsonify({"game":game.get('id'),"data":{"status":game.get('status')}}), 403
            b, w = mastermind_algo(game.get('sequence'), sequence)
            new_guess = {
                'id':new_id,
                'sequence': sequence,
                "black_pegs": b,
                "white_pegs": w
            }
            if b == 4:
                game['status'] = STATUS_CHOICES[2]
            elif game.get('guess_limit') - len(guesses) + 1 <= 0:
                game['status'] = STATUS_CHOICES[3]
            else:
                game['status'] = STATUS_CHOICES[1]
            guesses.append(new_guess)
            game['guesses'] = guesses
            return jsonify({"game":game.get('id'),"guess":new_id,"data":{"sequence":sequence}}), 201
    return jsonify({"detail":"Not found."}), 404

if __name__ == '__main__':
    app.run(debug=True, port=4000)
