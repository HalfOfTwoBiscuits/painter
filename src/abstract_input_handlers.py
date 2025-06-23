import pygame as pg
from abc import abstractmethod, ABC
from .sound import SFXPlayer

class InputHandler(ABC):
    '''A base class for input handlers that specifies the
    process_input() method to respond to key presses.'''

    # Constant response to keys being pressed
    _ACTIONS = {}
    # If not None, this variable value will be used instead
    _variable_actions = None

    @staticmethod
    def process_input(self, key):
        '''Use the actions dictionary to determine
        what to do in response to a key being pressed.
        
        If the key code is a key in the dictionary,
        the first element of the corresponding tuple is the
        string name of a method to call.
        All other elements in that tuple will be passed as arguments.
        
        The return value of that method, if any, is a string
        identifier for a new state. Return it to the main loop.
        
        For some children an instance is created and for others the class is used,
        so this is a staticmethod and self is passed in manually in the main loop.'''

        actions = self._variable_actions or self._ACTIONS
        a = actions.get(key)
        if a is not None:
            method_name = a[0]
            method_to_call = getattr(self, method_name)
            arguments = a[1:]
            state_change = method_to_call(*arguments)
            return state_change
        
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