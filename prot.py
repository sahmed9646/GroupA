import sys
import os
from enum import Enum
 
## -------------------------------------------------------------------------- ##
## Config variables
## -------------------------------------------------------------------------- ##

# Config variable for setting whether the console support truecolor, meaning RGB
# color values. If the variable is defined as False then only standard 
# monochrone values are supported.
rgbSupport = True

## -------------------------------------------------------------------------- ##
## Color class
## -------------------------------------------------------------------------- ##

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

## -------------------------------------------------------------------------- ##
## Color constants
## -------------------------------------------------------------------------- ##

CLEAR   = Color(-1, -1, -1)

RED     = Color(255, 0, 0)
GREEN   = Color(0, 255, 0)
BLUE    = Color(0, 0, 255)

CYAN    = Color(0, 255, 255)
MAGENTA = Color(255, 0, 255)
YELLOW  = Color(255, 255, 0)

## -------------------------------------------------------------------------- ##
## Utility functions
## -------------------------------------------------------------------------- ##

def isStringInt(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

## -------------------------------------------------------------------------- ##

def coloredText(text, color):
    if (rgbSupport or color.r < 0 or color.g < 0 or color.b < 0):
        return "\033[38;2;" + str(color.r) + ";" + str(color.g) + ";" + str(color.b) + "m" + text + "\033[0m"
    return text

## -------------------------------------------------------------------------- ##

def consoleWrite(text):
    print(text)
 
## -------------------------------------------------------------------------- ##

def consoleRead(text):
    return input(text).lower()

## -------------------------------------------------------------------------- ##

def consoleReadInt(text, color, min, max, choices):
    text = coloredText(text, color) + "\n"

    # Format message
    validChoices = []
    for (choiceChar, choiceText, choiceColor) in choices:
        text = text + coloredText("[" + str(choiceChar) + "] " + choiceText + "\n", choiceColor)
        validChoices.append(choiceChar)

    # Prompt user until valid choice
    choice = consoleRead(text)
    validNum = isStringInt(choice) and int(choice) >= min and int(choice) <= max
    while choice not in validChoices and not validNum:
        consoleWrite("Invalid choice (" + choice + ")\n")
        choice = consoleRead(text)
        validNum = isStringInt(choice) and int(choice) >= min and int(choice) <= max


    consoleWrite("")
    return choice

## -------------------------------------------------------------------------- ##

def consoleReadAlts(text, color, choices):

    text = coloredText(text, color) + "\n"

    # Format message
    validChoices = []
    for (choiceChar, choiceText, choiceColor) in choices:
        text = text + coloredText("[" + str(choiceChar) + "] " + choiceText + "\n", choiceColor)
        validChoices.append(choiceChar)

    # Prompt user until valid choice
    choice = consoleRead(text)
    while choice not in validChoices:
        consoleWrite("Invalid choice (" + choice + ")\n")
        choice = consoleRead(text)

    consoleWrite("")
    return choice



## -------------------------------------------------------------------------- ##
## Tournament class
## -------------------------------------------------------------------------- ##

"""
"""
class TournamentType(Enum):
    ROUND_ROBIN = 1
    KNOCKOUT = 2

## -------------------------------------------------------------------------- ##

"""
"""
class Tournament:  
    """
    """
    def __init__(self):
        done = False
        while not done:
            self.setupType()
            self.setupPlayers()
            self.setupAI()
            self.setupPlayerNames()
            self.summary()
            choice = consoleReadAlts(
                "Is this setup ok?",
                CLEAR,
                [("y", "Yes", GREEN), ("n", "No", RED), ("q", "Quit", MAGENTA)]
            )
            if choice == "q":
                quitProgram()
            elif choice == "y":
                done = True

        consoleWrite("Tournament has been setup!")

    """
    """
    def setupType(self):
        choice = consoleReadAlts(
            "Do you want the type of tournament to be Round-Robin or Knockout?", CLEAR,
            [("r", "Round-robin", Color(250,128,114)), ("k", "Knockout", Color(102,205,170)), ("q", "Quit", MAGENTA)]
        )
        if choice == "q":
            quitProgram()
        self.type = TournamentType.ROUND_ROBIN if (choice == "r" or choice == "R") else TournamentType.KNOCKOUT

    """
    """
    def setupPlayers(self):
        choice = consoleReadInt(
            "How many players are participating in the tournament? (3 - 8)", CLEAR,
            3, 8,
            [("q", "Quit", MAGENTA)]

        )
        if choice == "q":
            quitProgram()
        self.playerCount = int(choice)

    """
    """
    def setupAI(self):
       
        countChoice = consoleReadInt(
            "How many of those players are represented by AI? (0 - " + str(self.playerCount) + ")", CLEAR,
            0, self.playerCount,
            [("q", "Quit", MAGENTA)]
        )
        if countChoice == "q":
            quitProgram()
        self.aiCount = int(countChoice)

        difficulties = []
        for i in range(self.aiCount):
            difficultyChoice = consoleReadAlts(
                "What difficulty should AI " + str(i+1) + " be?", CLEAR,
                [("e", "Easy", Color(136, 216, 176)), ("m", "Medium", Color(255, 204, 92)), ("h", "Hard", Color(255, 111, 105)), ("q", "Quit", MAGENTA)]
            )
            if difficultyChoice == "q":
                quitProgram()
            difficulties.append(difficultyChoice)
        self.aiDifficulties = difficulties


    """
    """

    def setupPlayerNames(self):
        
        playerNames = []
        for i in range(self.playerCount - self.aiCount):
            choice = consoleRead(
                "Name of player #" + str(i+1) + "?\n"
            )
            if choice == "q":
                quitProgram()
            playerNames.append(choice)
        self.playerNames = playerNames


    """
    """


    def summary(self):
        consoleWrite(
            "\nSummary of tournament:\n" +
            "Type: " + ("Round-robin" if self.type == TournamentType.ROUND_ROBIN else "Knockout") + "\n" +
            "Player count: " + str(self.playerCount) + "\n" +
            "Player names: " + str(self.playerNames) +"\n" +
            "AI count: " + str(self.aiCount) + "\n" + 
            "AI difficulty: " + str(expandDifficultyList(self.aiDifficulties))
        )
    


    
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
    os.system("clear")
    choice = consoleReadAlts(
        "Welcome to the tournament manager!\n\n"
        "What do you want to do?", CLEAR,
        [("c", "Create tournament", CLEAR), ("q", "Quit", MAGENTA)])
    if choice == "q":
        quitProgram()

    tournament = Tournament()


## -------------------------------------------------------------------------- ##

def expandDifficultyList(list):
    result = []
    for difficulty in list:
        result.append("Easy" if difficulty == "e" else "Medium" if difficulty == "m" else "Hard")
    return result


## -------------------------------------------------------------------------- ##
## Demo driver
## -------------------------------------------------------------------------- ##

tournamentManager()
