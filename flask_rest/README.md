# Mastermind Flask Rest API
This repository contains a Flask REST API for the Mastermind game owned by [Abderrahmane Hammia](mailto:fa_hammia@esi.dz). The project was initially started based on a technical test created by [Inari.io](https://www.inari.io/)
# Get Started
* Make sure you have *docker* and *docker-compose* installed
* Run ```docker-compose up --build```
* Test the endpoints using port 8000
# Content
## mastermind folder
The mastermind folder contains our rest api app for the mastermind game which mainly consists of the next files and folders
```
app.py (app runner and api endpoints)
utils.py (set of functions and variables to use in app.py)
tests.py (testcases)
```
## Endpoints
The main endpoint for the api will be */api/v1/*.
```
/api/v1/statuses/
/api/v1/game-state/{id}/
/api/v1/games/
/api/v1/games/{id}/
/api/v1/games/{id}/guesses/
/api/v1/games/{id}/guesses/{id}/
```
Here are the required endpoints description
```
1. Create a new game: POST /api/v1/games/
    Request body
        guess_limit: must be non null positive integer
2. Create a new guess: POST /api/v1/games/{pk}/guesses/
    pk: ID of the game
    Request body
        sequence: must be non null string with 4 characters from [b,y,w,o,r,g]
3. Get current state of the game: GET /api/v1/game-state/{pk}
    pk: ID of the game
```
To ensure using the right type and format of request data, validators are being used (inside *utils.py*)
## Unit Tests
All the unit tests are created using *unittest*
```
tests.py (StatusTest, GameStateTest, GameViewTest, GuessViewTest)
```