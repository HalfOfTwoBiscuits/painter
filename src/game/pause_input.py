import pygame as pg
from ..abstract_handlers import FixedOptionsControl
from ..audio_utility import SFXPlayer
from .painter_visual import PainterVisual
from .floor_player import FloorPlayer
from ..floor_manager import FloorManager
    
class RestartExitMenuControl(FixedOptionsControl):
    '''A menu with the ability to exit or restart the floor.
    The exit option will go to the floor select
        - unless there is only one floor, in which case it goes to the floorpack select
        - unless there is only one floorpack, in which case it quits the game
        - unless the player is using the combined game+editor, in which case it goes to the game/editor select.

    Used as a base class for the pause and floor complete menus,
    and on completing the last floor in a pack.'''

    _ACTIONS = {
        pg.K_1 : ('restart',),
        pg.K_BACKSPACE : ('restart',),
        pg.K_2 : ('exit',),
        pg.K_RETURN : ('exit',),
        pg.K_ESCAPE : ('exit',),
    }

    @staticmethod
    def restart():
        SFXPlayer.play_sfx('back')
        new_loc = FloorPlayer.undo_all()
        if new_loc is not None:
            new_pos, _ = new_loc
            PainterVisual.go_to(new_pos)
        return 'GameplayState'
    
    @staticmethod
    def exit():
        SFXPlayer.play_sfx('menu')
        if FloorManager.get_num_floors() == 1:
            if FloorManager.get_num_floorpacks() == 1:
                # If there's only one floor and one floorpack, exit game,
                # or if using the game and editor combination,
                # go back to choosing which to use.
                return 3
            else:
                # Select a floorpack if there's only one floor.
                return 'FloorpackSelectState'
        # Otherwise select a floor.
        return 'LevelSelectState'

class PauseMenuControl(RestartExitMenuControl):
    '''A menu with the ability to resume gameplay, restart the floor,
    or exit back to the level select.'''

    _ACTIONS = {
        pg.K_1 : ('resume',),
        pg.K_LCTRL : ('resume',),
        pg.K_RCTRL : ('resume',),
        pg.K_ESCAPE : ('resume',),
        pg.K_RETURN : ('resume',),
        pg.K_BACKSPACE : ('resume',),
        pg.K_2 : ('restart',),
        pg.K_3 : ('exit',),
    }

    @staticmethod
    def resume():
        SFXPlayer.play_sfx('menu')
        return 'GameplayState'

class FloorClearMenuControl(RestartExitMenuControl):
    '''A menu with the ability to proceed to the next floor, restart the floor,
    or exit to the level select. The usual menu on clearing a floor.'''

    _ACTIONS = {
        pg.K_1 : ('next_floor',),
        pg.K_RETURN : ('next_floor',),
        pg.K_2 : ('restart',),
        pg.K_BACKSPACE : ('restart',),
        pg.K_3 : ('exit',),
        pg.K_ESCAPE : ('exit',),
    }

    @staticmethod
    def next_floor():
        SFXPlayer.play_sfx('start')
        return 'NewFloorState'