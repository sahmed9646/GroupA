# Standard imports
import sys
import random
from enum import Enum

# Project imports
import console
import display
import player
import rps

## -------------------------------------------------------------------------- ##
## Utility functions
## -------------------------------------------------------------------------- ##

def ordinalName(number):
    if (number <= 8):
        ordinals = ["first", "second", "third", "fourth", "fifth", "sixth", "eight"]
        return ordinals[number]
    else:
        return str(number) + "th"

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
    def __init__(self, demo=False):
        if demo:
            self.type = TournamentType.KNOCKOUT
            self.players = []
            for i in range(4):
                p = player.Player(ordinalName(i) + "_P", player.PlayerDifficulty.HUMAN)
                self.players.append(p)
            for i in range(1):
                a = player.Player(ordinalName(i) + "_A", player.PlayerDifficulty.EASY)
                self.players.append(a)
            for i in range(1):
                a = player.Player(ordinalName(i + 1) + "_A", player.PlayerDifficulty.HARD)
                self.players.append(a)
            for i in range(2):
                a = player.Player(ordinalName(i + 2) + "_A", player.PlayerDifficulty.MEDIUM)
                self.players.append(a)
            return

        done = False
        while not done:
            self.setupType()
            self.setupPlayers()
            self.setupAI()
            choice = console.readAlts(
                self.summary() + "\n"
                "Is this setup ok?",
                console.CLEAR,
                [("y", "Yes", console.GREEN), ("n", "No", console.RED), ("q", "Quit", console.MAGENTA)]
            )
            if choice == "q":
                quitProgram()
            elif choice == "y":
                done = True

    """
    Setup the type of the tournament by asking the user
    """
    def setupType(self):
        choice = console.readAlts(
            "Do you want the type of tournament to be Round-Robin or Knockout?", console.CLEAR,
            [("r", "Round-robin", 166), ("k", "Knockout", 26), ("q", "Quit", console.MAGENTA)]
        )
        if choice == "q":
            quitProgram()
        self.type = TournamentType.ROUND_ROBIN if choice == "r" else TournamentType.KNOCKOUT

    """
    Setup all the human players by asking the user about them
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
                name = console.read("What is the name of the " + ordinalName(i) + " player? (1-12 characters)", i == 0)
                if name.lower() == "q":
                    quitProgram()
                if len(name) > 12:
                    console.write("Name is too long. Please choose a shorter name")
                    continue
                if len(name) < 1:
                    console.write("Name cannot be empty. Please choose another name")
                    continue
                if name not in playerNames:
                    self.players.append(player.Player(name, player.PlayerDifficulty.HUMAN))
                    playerNames.append(name)
                    validName = True
                else:
                    console.write("Name " + name + " is already taken. Please choose a new name")

    """
    Setup the AI players and their difficulty by asking the user
    """
    def setupAI(self):
        # Setup AI players
        aiCount = 8 - len(self.players)
        for i in range(aiCount):
            difficultyChoice = console.readAlts(
                "What difficulty should the " + ordinalName(i) + " AI be at?", console.CLEAR,
                [("e", "Easy", 46), ("m", "Medium", 214), ("h", "Hard", 197), ("q", "Quit", console.MAGENTA)]
            )
            if difficultyChoice == "q":
                quitProgram()
            self.players.append(player.Player("AI#" + str(i + 1), player.PlayerDifficulty.EASY if difficultyChoice == "e" else player.PlayerDifficulty.MEDIUM if difficultyChoice == "m" else player.PlayerDifficulty.HARD))

    """
    Returns a summary of the tournament descriptor
    """
    def summary(self):
        text = "Summary of tournament:\n"
        text = text + "Type: " + getTournamentTypeName(self.type) + "\n" + "Players:\n"
        for p in self.players:
            playerText = "\t" + p.name + " - " + player.getDifficultyName(p.difficulty) + "\n"
            text = text + console.coloredText(playerText, console.CLEAR)
        return text

## -------------------------------------------------------------------------- ##
## Function for handling tie
## -------------------------------------------------------------------------- ##

"""
Resolves a tie between to players. If both players are AI then it's resolved
with a simple random toss. If either or both is a player then a game of Rock-paper-scissor will be used instead.
"""
def handleTie(player0, player1):
    console.write("") #console.clear()
    console.write("There was a tie between players " + player0.name + " and " + player1.name + ". This will be resolved with a game of Rock-paper-scissor")
    return rps.playRPS(player0, player1)

## -------------------------------------------------------------------------- ##
## BracketKO class
## -------------------------------------------------------------------------- ##

"""
Represents a bracket in a Knockout game. The two players are the ones that are competing. The result is represents the result of the bracket.

The first player always has black markers.

Score:
    -1 when the game has not yet been played and there is not result
    0 when the first player suffered a loss
    1 when the first player won
    0.5 when the game tied
"""
class BracketKO:
    def __init__(self, player0, player1):
        self.player0 = player0
        self.player0.blackCount += 1
        self.player1 = player1
        self.player1.whiteCount += 1
        self.result = -1

    def setResult(self, result):
        self.result = result

"""
"""
class MatchRR:
    def __init__(self, player0, player1):
        self.player0 = player0
        self.player1 = player1



"""
Create a new bracket from two other brackets. The bracket contains the winners in the two brackets.
"""
def createSubBracket(bracket0, bracket1):
    # Retrieve winners
    player0 = bracket0.player0 if bracket0.result == 1 else bracket0.player1
    player1 = bracket1.player0 if bracket1.result == 1 else bracket1.player1
    return BracketKO(player0, player1)

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
        if self.desc.type == TournamentType.KNOCKOUT:
            self.startKO()
        else:
            self.startRR()

    """
    Start Knockout tournament
    """
    def startKO(self):
        # Randomize players in first bracket
        allPlayers = self.desc.players
        self.bracketsR0 = []
        for i in range(4):
            i = random.choice(list(range(len(allPlayers))))
            player0 = allPlayers[i]
            del allPlayers[i]
            i = random.choice(list(range(len(allPlayers))))
            player1 = allPlayers[i]
            del allPlayers[i]            
            self.bracketsR0.append(BracketKO(player0, player1))

        # Show brackets
        console.clear()
        console.write("The brackets for the first round of Knockout are:")
        koDisp = display.KO_displayer(self.bracketsR0)
        koDisp.show()

        # Play first 4 games
        console.write("")
        for b in self.bracketsR0:
            # TODO(Filip): PLAY THE REAL GAME
            b.setResult(playGame(b.player0, b.player1))

            # Handle tie
            if b.result == 0.5:
                b.setResult(handleTie(b.player0, b.player1))

        # Setup 2 new brackets
        self.bracketsR1 = []
        for i in range(2):
            # Determine which players won
            bracket0 = self.bracketsR0[i * 2]
            bracket1 = self.bracketsR0[i * 2 + 1]
            self.bracketsR1.append(createSubBracket(bracket0, bracket1))

        # Show brackets
        console.clear() 
        console.write("The brackets for the second round of Knockout are:")
        koDisp.add_bracket(self.bracketsR1)
        koDisp.show()
        # Play both games
        for b in self.bracketsR1:
            # TODO(Filip): PLAY THE REAL GAME
            b.setResult(playGame(b.player0, b.player1))

            # Handle tie
            if b.result == 0.5:
                b.setResult(handleTie(b.player0, b.player1))

        # Setup final brackets
        self.bracketFinal = createSubBracket(self.bracketsR1[0], self.bracketsR1[1])

        # Show brackets
        console.clear() 
        console.write("The bracket for the final round of Knockout is:")
        koDisp.add_bracket(self.bracketFinal)
        koDisp.show()

        # Play final
        # TODO(Filip): PLAY THE REAL GAME
        self.bracketFinal.setResult(playGame(self.bracketFinal.player0, self.bracketFinal.player1))

        # Handle tie
        if self.bracketFinal.result == 0.5:
            self.bracketFinal.setResult(handleTie(self.bracketFinal.player0, self.bracketFinal.player1))

        # Show final result brackets
        winner = self.bracketFinal.player0 if self.bracketFinal.result == 1 else self.bracketFinal.player1
        console.clear() 
        console.write("The winner is " + winner.name)
        koDisp.add_winner(winner)
        koDisp.show()
    """
    Start Round-robin tournament
    """
    def startRR(self):
        # Get all combinations for the players/AI. nCr = 28 different combinations
        players = self.desc.players #all players

        RR_Disp = display.RR_displayer_L(players)

        for i in range(7):
            Matches = []
            Moving =players[0]

            for j in range(7):
                posMoveTo = (j+1) % 7
                nextToMove = players[posMoveTo]
                players[posMoveTo]= Moving
                Moving = nextToMove

            print('Round' + str(i) + ' Schedule:')

            for k in range(3):
                player0 = players[k]
                player1 = players[6-k]
                matchText = console.coloredText(player0.name, RR_Disp.colorSetting[player0.name]) + ' Vs ' + console.coloredText(player1.name, RR_Disp.colorSetting[player1.name])
                Matches.append(MatchRR(player0, player1))
                print(matchText)

            player0 = players[3]
            player1 = players[7]
            Matches.append(MatchRR(player0, player1))
            matchText = console.coloredText(player0.name,RR_Disp.colorSetting[player0.name]) + ' Vs ' + console.coloredText(player1.name, RR_Disp.colorSetting[player1.name])
            Matches.append(MatchRR(player0, player1))
            print(matchText)


            for m in Matches:

                result = playGame(m.player0, m.player1)
                RR_Disp.add_record(result, m.player0, m.player1)

                if result == 1:
                    print("player: " + m.player0.name + " won!")
                    m.player0.score += 1


                elif result == 0.5:
                    print("Tie!")
                    m.player0.score += 0.5
                    m.player1.score += 0.5

                else:
                    print("player: " + m.player1.name + " won!")
                    m.player1.score += 1


            RR_Disp.printRecord()
            RR_Disp.printRanking()

        
        winner =  RR_Disp.ranking[0]

        print(winner.name + " WON with the score of " + str(winner.score) + " points!")
    
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
## Mock functions
## -------------------------------------------------------------------------- ##

"""
Plays a random game and returns the score. This is either 1 for win of first player, 0.5 for tie and 0 for loss of first player
"""
def playGame(player0, player1):
    # Don't play if both players are AI
    if player0.difficulty != player.PlayerDifficulty.HUMAN and player1.difficulty != player.PlayerDifficulty.HUMAN:
        bag = []
        for i in range(player0.difficulty.value[0]):
            bag.append(1)
        for i in range(player1.difficulty.value[0]):
            bag.append(0)
        return random.choice(bag)

    #console.write("Playing game: " + player0.name + " vs " + player1.name)
    return random.choice([0, 0.5, 1])

## -------------------------------------------------------------------------- ##
## Demo driver
## -------------------------------------------------------------------------- ##
if __name__ == '__main__':
    tournamentManager()
