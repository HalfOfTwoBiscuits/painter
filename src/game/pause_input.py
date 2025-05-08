import pygame as pg
from .input_handler_base import InputHandler
from .painter_visual import PainterVisual
from .floor_player import FloorPlayer
from .sound import SFXPlayer

class PauseMenuControl(InputHandler):

    _ACTIONS = {
        pg.K_1 : ('resume',),
        pg.K_LCTRL : ('resume',),
        pg.K_RCTRL : ('resume',),
        pg.K_ESCAPE : ('resume',),
        pg.K_2 : ('undo_all',),
        pg.K_3 : ('exit',)
    }

    @staticmethod
    def resume():
        SFXPlayer.play_sfx('menu')
        return 'GameplayState'
    
    @staticmethod
    def undo_all():
        new_loc = FloorPlayer.undo_all()
        if new_loc is not None:
            new_pos, _ = new_loc
            PainterVisual.go_to(new_pos)
            SFXPlayer.play_sfx('back')
        return 'GameplayState'

    @staticmethod
    def exit():
        SFXPlayer.play_sfx('menu')
        return 'LevelSelectState'