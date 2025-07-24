import pygame as pg
from ..abstract_handlers import KeyboardInputHandler
from ..audio_utility import SFXPlayer
from ..floor_manager import FloorManager
from .painter_visual import PainterVisual
from .floor_player import FloorPlayer
from .floor_visual import FloorVisual

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

    @staticmethod
    def process_input(cls, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = event.pos
            clicked_pos = FloorVisual.get_coordinates_of_cell_clicked(x, y)
            if clicked_pos is not None:
                adj_cells = FloorPlayer.adjacents_to()
                index_of_pos = None
                for index, pos in enumerate(adj_cells):
                    if pos == clicked_pos:
                        index_of_pos = index
                        break

                if index_of_pos is not None:
                    DIRECTIONS = FloorPlayer.get_directions()
                    direction = DIRECTIONS[index_of_pos]
                    return cls.__do_move(clicked_pos, direction)

        else: return cls._process_keyboard_input(cls, event)

    @classmethod
    def move(cls, direction: int):
        '''Hook that responds to pressing the arrow keys by moving the painter.
        If the painter moved, it checks if the player won the floor,
        and if so, proceeds to the next one.'''
        new_pos = FloorPlayer.painter_position_after_move(direction)
        return cls.__do_move(new_pos, direction)

    @classmethod
    def __do_move(cls, new_pos: tuple, direction: int):
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