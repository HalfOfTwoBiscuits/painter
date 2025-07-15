import pygame as pg
from ..abstract_handlers import KeyboardInputHandler
from ..audio_utility import SFXPlayer
from .painter_visual import PainterVisual
from .floor_player import FloorPlayer
from ..floor_manager import FloorManager

class PainterControl(KeyboardInputHandler):
    '''Input handler for when playing a level.
    Move with the arrows, use backspace to undo,
    and control or escape to open the menu.'''
    _ACTIONS = {
        pg.K_RIGHT : ('move', 1),
        pg.K_LEFT : ('move', -1),
        pg.K_DOWN : ('move', 2),
        pg.K_UP : ('move', -2),
        pg.K_BACKSPACE : ('undo',),
        pg.K_LCTRL : ('open_menu',),
        pg.K_RCTRL : ('open_menu',),
        pg.K_ESCAPE : ('open_menu',)
    }

    @classmethod
    def move(cls, direction: int):
        '''Hook that responds to pressing the arrow keys by moving the painter.
        If the painter moved, it checks if the player won the floor,
        and if so, proceeds to the next one.'''
        new_pos = FloorPlayer.painter_position_after_move(direction)
        could_move = FloorPlayer.move_painter(new_pos, direction)

        if could_move:
            PainterVisual.go_to(new_pos, direction)
            SFXPlayer.play_sfx('move')
        else:
            PainterVisual.shake()
            SFXPlayer.play_sfx('invalid')
        if FloorPlayer.floor_is_over():
            return cls._state_after_win()

    @staticmethod
    def _state_after_win():
        if FloorManager.floorpack_is_over():
            return 'FloorpackOverState'
        else:
            return "FloorClearState"

    @staticmethod
    def undo():
        '''Hook that responds to pressing backspace by undoing.'''
        new_loc = FloorPlayer.undo()

        if new_loc is None:
            PainterVisual.shake()
            SFXPlayer.play_sfx('invalid')
        else:
            new_pos, new_direction = new_loc
            PainterVisual.go_to(new_pos, new_direction)
            SFXPlayer.play_sfx('back')

    @staticmethod
    def open_menu():
        '''Hook that responds to pressing control by opening the menu.'''
        SFXPlayer.play_sfx('menu')
        return 'PauseMenuState'