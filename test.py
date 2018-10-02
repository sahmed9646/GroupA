import unittest

# Project imports
import tournament

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

## -------------------------------------------------------------------------- ##
## Test runner
## -------------------------------------------------------------------------- ##

unittest.main()