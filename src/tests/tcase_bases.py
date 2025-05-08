import unittest
import pygame as pg

from game.main import Game, setup_window

class TestUsingWindow(unittest.TestCase):
    '''A test that draws graphics on the game window but does not
    use the overall game loop, taking input from input handlers but
    only calling Game.loop() at the start and when input is recieved.'''
    @classmethod
    def setUpClass(cls):
        cls._window = setup_window()

    def _do_test(self, State):
        g = Game(State, self.__class__._window)
        g.loop()
        result = None
        while result is None:
            for e in pg.event.get():
                if e.type == pg.KEYDOWN:
                    result = State.process_input(e.key)
                    g.loop()
                if e.type == pg.QUIT:
                    return True
        return result
        

class TestUsingGameLoop(TestUsingWindow):
    '''A holistic test that utilises the game loop.'''
    def _do_test(self, State):
        g = Game(State, self.__class__._window)
        self.assertTrue(g.main())