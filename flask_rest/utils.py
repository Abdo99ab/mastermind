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

def parsed_game_state(game):
    guesses = list(sorted(game.get('guesses'),key=lambda x:x.get('id'),reverse=True))
    if len(guesses) == 0:
        return {
            "id": game.get('id'),
            "guess_limit": game.get('guess_limit'),
            "status": game.get('status'),
        }
    return {
        "id": game.get('id'),
        "guess_limit": game.get('guess_limit'),
        "status": game.get('status'),
        "current_guess": len(guesses),
        "current_guess_id": guesses[0].get('id'),
        "current_guess_sequence": guesses[0].get('sequence'),
        "current_guess_black_pegs": guesses[0].get('black_pegs'),
        "current_guess_white_pegs": guesses[0].get('white_pegs'),
    }

def parsed_game(game):
    guesses = list(sorted(game.get('guesses'),key=lambda x:x.get('id'),reverse=True))
    return {
        "id": game.get('id'),
        "guess_limit": game.get('guess_limit'),
        "status": game.get('status'),
        "current_guess": len(guesses),
    }

def parsed_guess(game,guess):
    return {
        "id":guess.get('id'),
        "sequence":guess.get('sequence'),
        "game":{
            "id":game.get('id')
        },
        "black_pegs":guess.get('black_pegs'),
        "white_pegs":guess.get('white_pegs')
    }

def create_sequence():
    result = ""
    for _ in range(4):
        result += random.choice(COLORS)
    return result

def validate_guess_limit(value):
    if value is None:
        return None, {"guess_limit": ["This field is required."]}
    if not isinstance(value, int):
        return None, {"guess_limit": ["Guess Limit must be integer"]}
    if value <= 0:
        return None, {"guess_limit": ["Guess Limit must be positive"]}
    return value, None

def validate_sequence(value):
    if value is None:
        return None, {"sequence": ["This field is required."]}
    if not isinstance(value, str):
        return None, {"sequence": ["Guess Limit must be string"]}
    if len(value) < 4:
        return None, {"sequence": ['Sequence must have exactly 4 colors']}
    if len(value) > 4:
        return None, {"sequence": ["Ensure this field has no more than 4 characters."]}
    for c in value:
        if c not in COLORS:
            return None, {"sequence": ['Colors used in sequence must be [{}]'.format(', '.join(COLORS))]}
    return value, None