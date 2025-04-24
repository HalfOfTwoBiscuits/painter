import pygame as pg
from input_handler_base import InputHandler
from painter_visual import PainterVisual
from floor_player import FloorPlayer
from sound import SFXPlayer

class PainterControl(InputHandler):
    '''Input handler for when playing a level.
    Move with the arrows, use backspace to undo,
    and control to open the menu.'''
    _ACTIONS = {
        pg.K_RIGHT : ('move', 1),
        pg.K_LEFT : ('move', -1),
        pg.K_DOWN : ('move', 2),
        pg.K_UP : ('move', -2),
        pg.K_BACKSPACE : ('undo',),
        pg.K_LCTRL : ('open_menu',),
        pg.K_RCTRL : ('open_menu',)
    }

    @staticmethod
    def move(direction: int):
        '''Hook that responds to pressing the arrow keys by moving the painter.'''
        new_pos = FloorPlayer.painter_position_after_move(direction)
        could_move = FloorPlayer.move_painter(new_pos)

        if could_move:
            PainterVisual.go_to(new_pos, direction)
            SFXPlayer.play_sfx('move')
        else:
            PainterVisual.shake()
            SFXPlayer.play_sfx('invalid')

    @staticmethod
    def undo():
        '''Hook that responds to pressing backspace by undoing.'''
        new_pos = FloorPlayer.undo()

        if new_pos is None:
            PainterVisual.shake()
            SFXPlayer.play_sfx('invalid')
        else:
            PainterVisual.go_to(new_pos)
            SFXPlayer.play_sfx('back')

    @staticmethod
    def open_menu():
        '''Hook that responds to pressing control by opening the menu.'''
        return 'PauseMenuState'