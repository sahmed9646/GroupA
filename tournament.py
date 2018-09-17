import sys
from enum import Enum

import console

## -------------------------------------------------------------------------- ##
## Tournament types
## -------------------------------------------------------------------------- ##

"""
Enumeration of tournament types
"""
class TournamentType(Enum):
    ROUND_ROBIN = 1
    KNOCKOUT = 2

## -------------------------------------------------------------------------- ##
## TournamentDesc class
## -------------------------------------------------------------------------- ##

"""
Tournament descriptor class. This can be set up and then used to start tournaments with these settings.
"""
class TournamentDesc:  
    """
    """
    def __init__(self):
        done = False
        while not done:
            self.setupType()
            self.setupPlayers()
            self.setupAI()
            self.summary()
            choice = console.readAlts(
                "Is this setup ok?",
                console.CLEAR,
                [("y", "Yes", console.GREEN), ("n", "No", console.RED), ("q", "Quit", console.MAGENTA)]
            )
            if choice == "q":
                quitProgram()
            elif choice == "y":
                done = True

    """
    """
    def setupType(self):
        choice = console.readAlts(
            "Do you want the type of tournament to be Round-Robin or Knockout?", console.CLEAR,
            [("r", "Round-robin", console.Color(250,128,114)), ("k", "Knockout", console.Color(102,205,170)), ("q", "Quit", console.MAGENTA)]
        )
        if choice == "q":
            quitProgram()
        self.type = TournamentType.ROUND_ROBIN if choice == "r" else TournamentType.KNOCKOUT

    """
    """
    def setupPlayers(self):
        choice = console.readInt(
            "How many players are participating in the tournament? (3 - 8)", console.CLEAR,
            3, 8,
            [("q", "Quit", console.MAGENTA)]
        )
        if choice == "q":
            quitProgram()
        self.playerCount = int(choice)

    """
    """
    def setupAI(self):
        countChoice = console.readInt(
            "How many of those players are represented by AI? (0 - " + str(self.playerCount) + ")", console.CLEAR,
            0, self.playerCount,
            [("q", "Quit", console.MAGENTA)]
        )
        if countChoice == "q":
            quitProgram()
        self.aiCount = int(countChoice)

        difficulties = []
        for i in range(self.aiCount):
            difficultyChoice = console.readAlts(
                "What difficulty should AI " + str(i) + " be?", console.CLEAR,
                [("e", "Easy", console.Color(136, 216, 176)), ("m", "Medium", console.Color(255, 204, 92)), ("h", "Hard", console.Color(255, 111, 105)), ("q", "Quit", console.MAGENTA)]
            )
            if difficultyChoice == "q":
                quitProgram()
            difficulties.append(difficultyChoice)
        self.aiDifficulties = difficulties

    """
    """
    def summary(self):
        console.write(
            "Summary of tournament:\n" +
            "Type: " + ("Round-robin" if self.type == TournamentType.ROUND_ROBIN else "Knockout") + "\n" +
            "Player count: " + str(self.playerCount) + "\n" +
            "AI count: " + str(self.aiCount) + "\n" + 
            "AI difficulty: " + str(expandDifficultyList(self.aiDifficulties))
        )

## -------------------------------------------------------------------------- ##
## Tournament class
## -------------------------------------------------------------------------- ##

"""
Represents an actual tournament instance. The tournament is set up according to a tournament descriptor.
"""
class Tournament:
    def __init__(self, desc):
        self.desc = desc

    def start(self):
        pass
    
## -------------------------------------------------------------------------- ##
## Tournament manager
## -------------------------------------------------------------------------- ##

"""
"""
def quitProgram():
    quit()

## -------------------------------------------------------------------------- ##

"""
Start the tournament manager
"""
def tournamentManager():
    choice = console.readAlts(
        "Welcome to the tournament manager!\n"
        "What do you want to do?", console.CLEAR,
        [("c", "Create tournament", console.CLEAR), ("q", "Quit", console.MAGENTA)])
    if choice == "q":
        quitProgram()

    tDesc = TournamentDesc()
    t = Tournament(tDesc)


## -------------------------------------------------------------------------- ##

def expandDifficultyList(list):
    result = []
    for difficulty in list:
        result.append("Easy" if difficulty == "e" else "Medium" if difficulty == "m" else "Hard")
    return result


## -------------------------------------------------------------------------- ##
## Demo driver
## -------------------------------------------------------------------------- ##


console.enableWinVT()
tournamentManager()
