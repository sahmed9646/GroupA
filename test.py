import unittest

# Project imports
import tournament
import player
import console

## -------------------------------------------------------------------------- ##
## Test classes
## -------------------------------------------------------------------------- ##

"""
Tournament tests
"""
class TestTournament(unittest.TestCase):
    """
    Test ordinal names
    """
    def test_ordinal_name(self):
        self.assertEqual(tournament.ordinalName(0), "first")
        self.assertEqual(tournament.ordinalName(1), "second")
        self.assertEqual(tournament.ordinalName(2), "third")
        self.assertEqual(tournament.ordinalName(3), "fourth")
        self.assertEqual(tournament.ordinalName(4), "fifth")
        self.assertEqual(tournament.ordinalName(5), "sixth")
        self.assertEqual(tournament.ordinalName(6), "seventh")
        self.assertEqual(tournament.ordinalName(7), "eight")
        self.assertEqual(tournament.ordinalName(8), "9th")
        self.assertEqual(tournament.ordinalName(999), "1000th")

    """
    Test tournament type names
    """
    def test_type_name(self):
        self.assertEqual(tournament.getTournamentTypeName(tournament.TournamentType.KNOCKOUT), "Knockout")
        self.assertEqual(tournament.getTournamentTypeName(tournament.TournamentType.ROUND_ROBIN), "Round-robin")

    """
    Test to see if subbrackets are created correctly
    """
    def test_subbracket(self):
        p0 = player.Player("P0", player.PlayerDifficulty.EASY)
        p1 = player.Player("P1", player.PlayerDifficulty.EASY)
        p2 = player.Player("P2", player.PlayerDifficulty.EASY)
        p3 = player.Player("P3", player.PlayerDifficulty.EASY)
        
        b0 = tournament.BracketKO(p0, p1)
        b0.result = 1
        b1 = tournament.BracketKO(p2, p3)
        b1.result = 0

        b2 = tournament.createSubBracket(b0, b1)
        self.assertEqual(b2.player0, p0)
        self.assertEqual(b2.player1, p3)

    """
    Test of conversion from result from platform layer
    """
    def test_result_convert(self):
        self.assertEqual(tournament.platformToTournamentResult(0), 0.5)
        self.assertEqual(tournament.platformToTournamentResult(1), 1)
        self.assertEqual(tournament.platformToTournamentResult(2), 0)
        self.assertEqual(tournament.platformToTournamentResult(-1), -1)
        self.assertEqual(tournament.platformToTournamentResult(100000), 100000)

## -------------------------------------------------------------------------- ##

class TestConsole(unittest.TestCase):
    """
    Test console color codes
    """
    def test_console_color(self):
        t0 = console.coloredText("test", console.MAGENTA)
        self.assertEqual(t0, "\033[38;5;" + str(console.MAGENTA) + "mtest\033[0m")

        t1 = console.coloredText("fox", console.CLEAR)
        self.assertEqual(t1, "fox")

    """
    Test that integer strings are found to be integer strings
    """
    def test_is_string_int(self):
        self.assertTrue(console.isStringInt("1"))
        self.assertFalse(console.isStringInt("fox"))
        self.assertTrue(console.isStringInt("999"))
        self.assertFalse(console.isStringInt("g"))

## -------------------------------------------------------------------------- ##

"""
Rock-paper-scissor tests
"""
class TestRPS(unittest.TestCase):
    def test_something(self):
        pass

## -------------------------------------------------------------------------- ##

"""
Player tests
"""
class TestPlayer(unittest.TestCase):
    def test_player(self):
        testplayer = player.Player("Zlatan", player.PlayerDifficulty.HUMAN)
        self.assertTrue(testplayer.difficulty == player.PlayerDifficulty.HUMAN)
        self.assertEqual(testplayer.name, "Zlatan")
        self.assertEqual(testplayer.score, 0)
        self.assertFalse(testplayer.isAI())
    
## -------------------------------------------------------------------------- ##
## Test runner
## -------------------------------------------------------------------------- ##

unittest.main()