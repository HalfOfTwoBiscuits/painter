import pygame as pg
from .input_handler_base import InputHandler
from .floor_manager import FloorManager
from .sound import SFXPlayer
from abc import abstractmethod, ABC

class ArbitraryOptionsControl(InputHandler, ABC):
    '''Base class for an input handler that uses the MenuVisual
    to prompt the user to choose from an arbitrary list of options.'''
    _menu = None

    def __init__(self, menu_visual_obj):
        '''Store the MenuVisual object and set up number keys
        based on the number of options per page.'''
        self._menu = menu_visual_obj
        NUM_OPTIONS = menu_visual_obj.get_options_per_page()

        actions = {
            # Get key code for the given number key, from 1 to NUM_OPTIONS.
            # When that key is pressed, call select() with the number
            # to choose the option.
            pg.key.key_code(str(num)) : ('select', num)
            for num in range(1, NUM_OPTIONS + 1)
        }

        actions[pg.K_LEFT] = ('prevpage',)
        actions[pg.K_RIGHT] = ('nextpage',)
        self.__class__._variable_actions = actions

    @abstractmethod
    def select(self, number: int):
        '''Hook for when a number key 1-9 is pressed.
        Selects the menu option corresponding to that number,
        if there is one.'''
        ...

    def _find_option_for_number(self, number: int):
        # If the number pressed corresponds to an option, get the
        # string used to describe it on the menu.
        # If it doesn't then play an 'invalid' sfx.
        try:
            option_id = self._menu.option_for_number(number)
        except ValueError:
            SFXPlayer.play_sfx('invalid')
        else:
            SFXPlayer.play_sfx('menu')
            return option_id
        
    def nextpage(self):
        '''Go to the next page on the menu'''
        SFXPlayer.play_sfx('move')
        self._menu.next_page()
    
    def prevpage(self):
        '''Go to the previous page on the menu'''
        SFXPlayer.play_sfx('move')
        self._menu.prev_page()

class LevelSelectControl(ArbitraryOptionsControl):

    def __init__(self, menu_visual_obj):
        super().__init__(menu_visual_obj)

    def select(self, number: int):
        '''Set the floor manager to start from the selected floor,
        and switch to the gameplay state.'''

        option_id = self._find_option_for_number(number)
        if option_id is None: return

        # As dictated by FloorManager.get_floor_names(),
        # the last character in the string is the floor number.
        # Cast to an integer and subtract 1 to find the index of the floor.
        floor_index = int(option_id[-1]) - 1

        # Select the floor and go to gameplay.
        FloorManager.select_floor(floor_index)
        return 'NewFloorState'