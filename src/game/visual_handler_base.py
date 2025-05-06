from abc import abstractmethod
import pygame as pg

class VisualHandler:
    '''Has access to the window surface to draw graphics onto,
    and implements a draw() method.
    Visual handlers inherit from it.'''

    __BG_COL = pg.Color(10,10,10)
    @classmethod
    def set_window(cls, window_surf):
        '''Set the surface used to draw graphics on'''
        cls._window = window_surf
        cls._window_dimensions = window_surf.get_size()

    @classmethod
    @abstractmethod
    def draw(cls):
        '''Called every frame to draw graphics.
        Implemented by children'''
        ...

    @classmethod
    def get_graphics(cls):
        '''Get the graphics surface so it can be blitted onto the game window'''
        return cls._window
    
    @classmethod
    def start_draw(cls):
        '''Fill the surface with a background to prepare for drawing'''
        cls._window.fill(cls.__BG_COL)