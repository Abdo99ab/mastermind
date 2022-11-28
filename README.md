# Mastermind Rest API
This repository contains a REST API for the Mastermind game owned by [Abderrahmane Hammia](mailto:fa_hammia@esi.dz). The project was initially started based on a technical test created by [Inari.io](https://www.inari.io/)
The REST API is developed using two frameworks in python, Django and Flask, the implementation you should pat attention to is the one developed with Django, I just saw this as an oppurtunity to test my persnoal knowledge in Flask and maybe get a feedback about it 😊.
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
## Requirements
Here are the requirements to build the REST API for the mastermind game:
The user introduces a guess code in the form of a string like “RRBB” and then this guess is compared against the secret solution and the feedback is returned. Need at least the following endpoints:
* Endpoint#1: A POST endpoint to create a new game.
* Endpoint#2: A GET endpoint to retrieve the current state of the game, with the information that would be required for a frontend client to render the board appropriately.
* Endpoint#3: A POST endpoint to create a new guess for an on-going game.

# Answers to the questionnaire
## 1. Favourite package manager
Nowadays every software developer uses at least 1 package manager at work. That means you define the software libraries (dependencies) you want to use in your project in a project file.
There are two package managers which I use very often depending on with what I am developing, NPM and PyPI, both of them are very useful and rich in packages. NPM is the main package manager for Node.js, all of the packages are centralized. PyPI is the main package manager for Python. However If I need to choose one it would be Python because it's really easy to work with, the terminology of the packages is simple and effective, we can install packages with different methods (using terminal, file, virtual environment, Pipefile ...).
## 2. Followed architecture
In order to build a solid, reliable and simple REST API, we first need to design a good solution based on the analysis of needs for that, it is necessary to follow an architecture.
The architecture followed in this project is microservices architecture, I find it to match Django framework logic, however in this particular test we can only consider one component.
## 3. UML
To answer the question about UML, I have studied UML in university so I know and understand UML or Unified Modeling Language. For many previous projects the most diagrams I worked with are:
* Class diagram
* Component diagram
* Use case diagram
* Sequence diagram
* Activity diagram
* State diagram
* Package diagram
* Deployment diagram

I imagine that a simple class diagram for the mastermind game would have 3 classes, player, guess and game, the player is related to both guess and game because he can create them both, the game is composed of many guesses and each time it calculate their black and white pegs
![Class Diagram](https://abdoh-gitlab.s3.us-east-2.amazonaws.com/Capture.PNG)
## 4. Formatting tools
In each programming language There are some tools that help styling the code, formatting and typing.
Among the tools that I find very intersting and useful are
* Eslint (consitency): it is used for javascript code to ensure good quality and check various code issues.
* Stylelint (consitency): for CSS and SCSS.
* Prettier (formatting): it edits the javascript code and format it.
* Black and autopep8 (formatting): python formatters.
* For typing codes there are many good code editors that have bultin functions to help with errors, auto-completion and indentation for example: I use VSCode often but I tried Atom, Notepad++, Sublime, and I've also worked with Jetbrains IDEs and Android Studio.
 

## 5.Comments
First of all, I would like to thank you for considering my application with this test, I liked the content of the test and how is production oriented. The game concept is explained very well and  rich of examples. The requirements are also well explained and they show the necessity of production oriented architecture. The use of the programming language / framework is not specified, which give more freedom to the developer to focus on the developement.
I had a fun sunday working on this project, and I had the oppurtunity to code it with two frameworks. I dealt with this project as any other project I used to work on in my previous jobs. I believe that every good developer has its own coding habits so I hope that you like mine 😊.