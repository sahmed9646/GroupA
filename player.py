from enum import Enum

## -------------------------------------------------------------------------- ##
## Player difficulty enumeration
## -------------------------------------------------------------------------- ##

"""
Player difficulty. Human players have the difficulty of 'HUMAN'.
"""
class PlayerDifficulty(Enum):
    """ Easy sAI """
    easy = 1,
    """ Medium AI """
    medium = 2,
    """ Hard AI """
    hard = 3,
    """ Human player """
    human = 4
    

"""
"""
def getDifficultyName(difficulty):
    return "Human" if difficulty == PlayerDifficulty.human else "Easy" if difficulty == PlayerDifficulty.easy else "Medium" if difficulty == PlayerDifficulty.medium else "Hard"

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
        self.score = 0
        self.blackCount = 0
        self.whiteCount = 0
        self.winCount = 0
        self.loseCount = 0
        self.tieCount = 0

    def isAI(self):
        return self.difficulty != PlayerDifficulty.human
