import unittest

from game.main import Game

from tcase_states import FloorViewer

class DrawLevelTest(unittest.TestCase):
    def test_leveldraw(self):
        g = Game(FloorViewer)
        self.assertTrue(g.main())