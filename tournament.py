# Standard imports
import sys
import random
from enum import Enum

# Project imports
import console

## -------------------------------------------------------------------------- ##
## Player difficulty enumeration
## -------------------------------------------------------------------------- ##

"""
Player difficulty. Human players have the difficulty of 'HUMAN'.
"""
class PlayerDifficulty(Enum):
    """ Human player """
    HUMAN = 1,
    """ Easy AI """
    EASY = 2,
    """ Medium AI """
    MEDIUM = 3,
    """ Hard AI """
    HARD = 4

"""
"""
def getDifficultyName(difficulty):
    return "Human" if difficulty == PlayerDifficulty.HUMAN else "Easy" if difficulty == PlayerDifficulty.EASY else "Medium" if difficulty == PlayerDifficulty.MEDIUM else "Hard"

## -------------------------------------------------------------------------- ##
## Player class
## -------------------------------------------------------------------------- ##

"""
Represents a player in a tournament
"""
class Player:
    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty

## -------------------------------------------------------------------------- ##
## Tournament type enumeration
## -------------------------------------------------------------------------- ##

"""
Enumeration of tournament types
"""
class TournamentType(Enum):
    """ Round-robin tournament type """
    ROUND_ROBIN = 1
    """ Knockout tournament type """
    KNOCKOUT = 2

def getTournamentTypeName(type):
    return "Round-robin" if type == TournamentType.ROUND_ROBIN else "Knockout"

## -------------------------------------------------------------------------- ##
## TournamentDesc class
## -------------------------------------------------------------------------- ##

"""
Tournament descriptor class. This can be set up and then used to start tournaments with these settings.
"""
class TournamentDesc:  
    """
    Initialize a tournament description by setting up all the settings.
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
        # Read number of players
        choice = console.readInt(
            "How many players are participating in the tournament? (3 - 8)", console.CLEAR,
            3, 8,
            [("q", "Quit", console.MAGENTA)]
        )
        if choice == "q":
            quitProgram()
        playerCount = int(choice)

        # Setup player names
        playerNames = []
        self.players = []
        for i in range(playerCount):
            validName = False
            while not validName:
                name = console.read("What is the name of player" + str(i + 1) + "? ")
                if name.lower() == "q":
                    quitProgram()
                if name not in playerNames:
                    self.players.append(Player(name, PlayerDifficulty.HUMAN))
                    playerNames.append(name)
                    validName = True
                else:
                    console.write("Name " + name + " is already taken. Please choose a new name")

    """
    """
    def setupAI(self):
        # Setup AI players
        aiCount = 8 - len(self.players)
        for i in range(aiCount):
            difficultyChoice = console.readAlts(
                "What difficulty should AI " + str(i) + " be?", console.CLEAR,
                [("e", "Easy", console.Color(136, 216, 176)), ("m", "Medium", console.Color(255, 204, 92)), ("h", "Hard", console.Color(255, 111, 105)), ("q", "Quit", console.MAGENTA)]
            )
            if difficultyChoice == "q":
                quitProgram()
            self.players.append(Player("AI#" + str(i + 1), PlayerDifficulty.EASY if difficultyChoice == "e" else PlayerDifficulty.MEDIUM if difficultyChoice == "m" else PlayerDifficulty.HARD))

    """
    """
    def summary(self):
        text = "Summary of tournament:\n"
        text = text + "Type: " + getTournamentTypeName(self.type) + "\n" + "Players:\n"
        for player in self.players:
            playerText = "\t" + player.name + " - " + getDifficultyName(player.difficulty) + "\n"
            text = text + console.coloredText(playerText, console.CLEAR)

        console.write(text)

## -------------------------------------------------------------------------- ##
## BracketKO class
## -------------------------------------------------------------------------- ##

"""
Represents a bracket in a Knockout game. The two players are the ones that are competing. The result is represents the result of the bracket.

Score:
    -1 when the game has not yet been played and there is not result
    0 when the first player suffered a loss
    1 when the first player won
    0.5 when the game tied
"""
class BracketKO:
    def __init__(self, player0, player1):
        self.player0 = player0
        self.player1 = player1
        self.result = -1

    def setResult(self, result):
        self.result = result

## -------------------------------------------------------------------------- ##
## Tournament class
## -------------------------------------------------------------------------- ##

"""
Represents an actual tournament instance. The tournament is set up according to a tournament descriptor.
"""
class Tournament:
    def __init__(self, desc):
        self.desc = desc

    """
    Start the tournament
    """
    def start(self):
        console.write("Starting tournament...")
        if self.desc.type == TournamentType.KNOCKOUT:
            self.startKO()
        else:
            self.startRR()

    """
    Start Knockout tournament
    """
    def startKO(self):
        # Randomize first bracket
        freePlayers = self.desc.players
        self.bracketsR0 = []
        for i in range(4):
            i = random.choice(list(range(len(freePlayers))))
            player0 = freePlayers[i]
            del freePlayers[i]
            i = random.choice(list(range(len(freePlayers))))
            player1 = freePlayers[i]
            del freePlayers[i]            
            self.bracketsR0.append(BracketKO(player0, player1))

        # Play all 4 games
        for b in self.bracketsR0:
            # TODO(Filip): PLAY THE REAL GAME
            console.write("Playing game (r0): " + b.player0.name + " vs " + b.player1.name)
            b.setResult(playGameKO())

            # TODO(Filip): HANDLE TIE
            if b.result == 0.5:
                b.setResult(1)

        # Setup 2 new brackets
        self.bracketsR1 = []
        for i in range(2):
            bracket0 = self.bracketsR0[i * 2]
            bracket1 = self.bracketsR0[i * 2 + 1]
            player0 = bracket0.player0 if bracket0.result == 1 else bracket0.player1
            player1 = bracket1.player0 if bracket1.result == 1 else bracket1.player1
            self.bracketsR1.append(BracketKO(player0, player1))

        # Play both games
        for b in self.bracketsR1:
            # TODO(Filip): PLAY THE REAL GAME
            console.write("Playing game (r1): " + b.player0.name + " vs " + b.player1.name)
            b.setResult(playGameKO())

            # TODO(Filip): HANDLE TIE
            if b.result == 0.5:
                b.setResult(1)

        # Setup final brackets
        player0 = self.bracketsR1[0].player0 if self.bracketsR1[0].result == 1 else self.bracketsR1[0].player1
        player1 = self.bracketsR1[1].player0 if self.bracketsR1[1].result == 1 else self.bracketsR1[1].player1
        self.bracketFinal = BracketKO(player0, player1)

        # Play final
        # TODO(Filip): PLAY THE REAL GAME
        console.write("Playing game (final): " + self.bracketFinal.player0.name + " vs " + self.bracketFinal.player1.name)
        self.bracketFinal.setResult(playGameKO())

        # TODO(Filip): HANDLE TIE
        if self.bracketFinal.result == 0.5:
            self.bracketFinal.setResult(1)

        # Present winner!
        winner = self.bracketFinal.player0 if self.bracketFinal.result == 1 else self.bracketFinal.player1
        console.write("Winner is: " + winner.name + "!")


    """
    Start Round-robin tournament
    """
    def startRR(self):
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
    t.start()


## -------------------------------------------------------------------------- ##

def expandDifficultyList(list):
    result = []
    for difficulty in list:
        result.append("Easy" if difficulty == "e" else "Medium" if difficulty == "m" else "Hard")
    return result


## -------------------------------------------------------------------------- ##
## Mock functions
## -------------------------------------------------------------------------- ##

"""
Plays a random game of Knockout tournament and returns the score. This is either 1 for win of first player, 0.5 for tie and 0 for loss of first player
"""
def playGameKO():
    return random.choice([0, 0.5, 1])

## -------------------------------------------------------------------------- ##
## Demo driver
## -------------------------------------------------------------------------- ##


console.enableWinVT()
tournamentManager()
