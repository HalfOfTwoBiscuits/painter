import unittest
import pygame as pg

from ..app import App
from ..startup_utility import setup_window
from . import tcase_states
from . import all_states

class UnitTester(App):
    _state_module = tcase_states

class IntegrationTester(App):
    _state_module = all_states

class TestUsingWindow(unittest.TestCase):
    '''A test that draws graphics on the game window but does not
    use the overall game loop, taking input from input handlers but
    only calling Game.loop() at the start and when input is recieved.'''
    @classmethod
    def setUpClass(cls):
        cls._window = setup_window()

    def _do_test(self, State):
        g = UnitTester(State.__name__, self.__class__._window)
        g.loop()
        result = None
        while result is None:
            for e in pg.event.get():
                if e.type == pg.KEYDOWN:
                    result = State.process_input(e.key)
                    g.loop()
                if e.type == pg.QUIT:
                    return True
        self.assertTrue(result)
        

class TestUsingGameLoop(TestUsingWindow):
    '''A holistic test that utilises the game loop.'''
    def _do_test(self, State):
        g = IntegrationTester(State.__name__, self.__class__._window)
        self.assertTrue(g.main())