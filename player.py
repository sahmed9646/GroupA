from enum import Enum

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
        self.score = 0
        self.blackCount = 0
        self.whiteCount = 0