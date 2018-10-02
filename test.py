import unittest

# Project imports
import tournament
import player

## -------------------------------------------------------------------------- ##
## Test classes
## -------------------------------------------------------------------------- ##

"""
Tournament tests
"""
class TestTournament(unittest.TestCase):
    def test_ordinal_name(self):
        self.assertEqual(tournament.ordinalName(0), "first")

## -------------------------------------------------------------------------- ##

"""
Rock-paper-scissor tests
"""
class TestRPS(unittest.TestCase):
    def test_something(self):
        pass


"""
Player tests
"""
class TestPlayer(unittest.TestCase):
    def test_player(self):
        testplayer = player.Player("Zlatan", 4)
        self.assertTrue(testplayer.difficulty == 4)
        self.assertEqual(testplayer.name, "Zlatan")
        self.assertEqual(testplayer.score, 0)
    
## -------------------------------------------------------------------------- ##
## Test runner
## -------------------------------------------------------------------------- ##

unittest.main()