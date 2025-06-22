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
        '''If the number given corresponds to an option, 
        return the string used to describe it on the menu.
        If it doesn't then play an 'invalid' sfx.'''
        try:
            option_id = self._menu.option_for_number(number)
        except ValueError:
            SFXPlayer.play_sfx('invalid')
        else:
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
    '''Input handler for floor selection.'''
    def __init__(self, menu_visual_obj, BACK_OPTION_ID: str):
        super().__init__(menu_visual_obj)
        self.__BACK_OPTION = BACK_OPTION_ID

    def select(self, number: int):
        '''If the 'Back' option was selected, return to the floorpack select.
        Otherwise, set the floor manager to start from the selected floor,
        and switch to the gameplay state.'''

        option_id = self._find_option_for_number(number)
        if option_id is None: return
        
        elif option_id == self.__BACK_OPTION:
            # Selecting the 'Back' option will return to floorpack selection
            SFXPlayer.play_sfx('back')
            return 'FloorpackSelectState'
        
        floor_index = FloorManager.index_from_floor_name(option_id)

        # Select the floor and go to gameplay.
        FloorManager.select_floor(floor_index)
        SFXPlayer.play_sfx('start')
        return 'NewFloorState'
    
class FloorpackSelectControl(ArbitraryOptionsControl):
    '''Input handler for floorpack selection.'''
    def __init__(self, menu_visual_obj):
        super().__init__(menu_visual_obj)

    def select(self, number: int):
        '''Set the floor manager to use the selected floorpack,
        and switch to the floor select state.'''
        option_id = self._find_option_for_number(number)
        if option_id is None: return

        # Select the floorpack corresponding to the option.
        FloorManager.select_floorpack(option_id)
        SFXPlayer.play_sfx('menu')
        return 'LevelSelectState'