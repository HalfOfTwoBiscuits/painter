import pygame as pg
from input_handler_base import InputHandler
from painter_visual import PainterVisual
from floor_player import FloorPlayer

class PauseMenuControl(InputHandler):

    _ACTIONS = {
        pg.K_1 : ('resume',),
        pg.K_LCTRL : ('resume',),
        pg.K_RCTRL : ('resume',),
        pg.K_2 : ('undo_all',),
        #pg.K_3 : ('exit',)
    }

    @staticmethod
    def resume():
        return 'GameplayState'
    
    @staticmethod
    def undo_all():
        new_pos = FloorPlayer.undo_all()
        if new_pos is not None:
            PainterVisual.go_to(new_pos)
        return 'GameplayState'

    @staticmethod
    def exit():
        return 'LevelSelectState'