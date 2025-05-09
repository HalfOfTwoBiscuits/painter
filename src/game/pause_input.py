import pygame as pg
from .input_handler_base import InputHandler
from .painter_visual import PainterVisual
from .floor_player import FloorPlayer
from .sound import SFXPlayer

class ExitMenuControl(InputHandler):
    '''A menu with the ability to exit back to the level select.
    Used as a base class for the pause and floor complete menus,
    and instead of the floor complete menu for the last floor.'''
    
    _ACTIONS = {
        pg.K_1 : ('exit',),
        pg.K_RETURN : ('exit',),
        pg.K_ESCAPE : ('exit',),
        pg.K_LCTRL : ('exit',),
        pg.K_RCTRL : ('exit',),
    }
    @staticmethod
    def exit():
        SFXPlayer.play_sfx('menu')
        return 'LevelSelectState'

class PauseMenuControl(ExitMenuControl):
    '''A menu with the ability to resume gameplay, restart the floor,
    or exit back to the level select.'''

    _ACTIONS = {
        pg.K_1 : ('resume',),
        pg.K_LCTRL : ('resume',),
        pg.K_RCTRL : ('resume',),
        pg.K_ESCAPE : ('resume',),
        pg.K_RETURN : ('resume',),
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

class FloorClearMenuControl(ExitMenuControl):
    '''A menu with the ability to proceed to the next floor or
    exit to the level select.'''

    _ACTIONS = {
        pg.K_1 : ('next_floor',),
        pg.K_RETURN : ('next_floor',),
        pg.K_2 : ('exit',),
        pg.K_ESCAPE : ('exit',),
        pg.K_LCTRL : ('exit',),
        pg.K_RCTRL : ('exit',)
    }

    @staticmethod
    def next_floor():
        SFXPlayer.play_sfx('start')
        return 'NewFloorState'