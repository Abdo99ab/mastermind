# Mastermind Django Rest API
This repository contains a REST API for the Mastermind game owned by [Abderrahmane Hammia](mailto:fa_hammia@esi.dz). The project was initially started based on a technical test created by [Inari.io](htttps://inari.io)
# _Repository content_
This repository contains two RESTful projects, both developed with Python, one with Django Framework and the other with Flask.
Inside each project you'll find also a README file which describe the project.
# Mastermind algorithm
Given the secret sequence and a guess sequence, we can calculate the number of black pegs (The correct guesses in color and position) and the number of white pegs (The correct guesses in color only)
We start by initializing b (black pegs) and w (white pegs) with 0
We create two tables to track down the positions already gone through for secret sequence and guess sequence
We start searching for the black pegs through one loop by incrementing b and adding both positions to the tracker if the color and position matches.
After that, we search for white pegs through two loops, avoiding the positions already gone through by incrementing w and adding position to the tracker if the color matches
Finally we return b and w.
```Python
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
```