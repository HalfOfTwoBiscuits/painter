import unittest
import pygame as pg

from game.main import Game, setup_window

class TestUsingWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._window = setup_window()

    def _do_test(self, State):
        g = Game(State, self.__class__._window)
        g.loop()
        ih = State.get_input_handler()
        result = None
        while result is None:
            for e in pg.event.get():
                if e.type == pg.KEYDOWN:
                    result = ih.process_input(ih, e.key)
                    g.loop()
                if e.type == pg.QUIT:
                    return False
        return result
        

class TestUsingGameLoop(TestUsingWindow):

    def _do_test(self, State):
        g = Game(State, self.__class__._window)
        self.assertTrue(g.main())