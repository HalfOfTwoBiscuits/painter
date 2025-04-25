import pygame as pg
from visual_handler_base import VisualHandler

class MenuVisual(VisualHandler):
    '''A visual for menus where the player chooses an option
    with the number keys. PauseMenuVisual and LevelSelectVisual inherit from it.'''

    _options = []

    @classmethod
    def draw(cls):
        win_width, win_height = cls._window_dimensions

        pg.draw.rect()