from game.input_handler_base import InputHandler
#from game.visual_handler_base import VisualHandler
from game.floor_visual import FloorVisual

import pygame as pg

def FloorViewerControl(InputHandler):
    _ACTIONS = {
        pg.K_RETURN : ('next',),
        pg.K_BACKSPACE : ('stop',),
    }

    __other_floors = []

    @classmethod
    def use_floors(cls,floors):
        cls.__other_floors = floors

    @classmethod
    def next(cls):
        '''Floor looks right, move on to the next one
        If out of floors, test is successful'''
        try:
            next_floor = cls.__other_floors.pop(1)
        except IndexError:
            # No more floors so test is successful.
            return True
        # Display the new floor
        FloorVisual.new_floor(next_floor)

        
    @staticmethod
    def stop():
        '''Floor doesn't look right, test fails'''
        return False