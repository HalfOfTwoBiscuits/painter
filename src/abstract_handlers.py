import pygame as pg
from abc import abstractmethod, ABC
from .audio_utility import SFXPlayer
from .editor.gui_handler import GUIHandler

class KeyboardInputHandler(ABC):
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
        
class ArbitraryOptionsControl(KeyboardInputHandler, ABC):
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

class ArbitraryOptionsControlWithBackButton(ArbitraryOptionsControl, ABC):
    def __init__(self, menu_visual_obj, BACK_OPTION_ID: str):
        super().__init__(menu_visual_obj)
        self._BACK_OPTION = BACK_OPTION_ID
        self.__class__._variable_actions[pg.K_BACKSPACE] = ('back',)
        self.__class__._variable_actions[pg.K_ESCAPE] = ('back',)

    def _check_for_back_option(self, number: int):
        '''If the back option was selected, return True.
        If another option was selected, return False.
        If the selection was invalid, raise ValueError.
        Store option ID for later reference so find_option_for_number
        doesn't have to be called again.'''

        # Small optimisation: make _find_option_for_number raise ValueError.
        self._option_id = self._find_option_for_number(number)
        if self._option_id is None: raise ValueError
        elif self._option_id == self._BACK_OPTION:
            SFXPlayer.play_sfx('back')
            return True
        return False
    
    @staticmethod
    @abstractmethod
    def back():
        ...

class FloorManagementControl(ArbitraryOptionsControlWithBackButton, ABC):
    @staticmethod
    def back():
        return 'EditFloorsState'

class VisualHandler:
    '''Has access to the window surface to draw graphics onto,
    and implements a draw() method.
    Visual handlers inherit from it.'''

    __BG_COL = pg.Color(10,10,10)
    @classmethod
    def set_window(cls, window_surf):
        '''Set the surface used to draw graphics on'''
        cls._window = window_surf
        cls._window_dimensions = window_surf.get_size()

    @classmethod
    @abstractmethod
    def draw(cls):
        '''Called every frame to draw graphics.
        Implemented by children'''
        ...

    @classmethod
    def get_graphics(cls):
        '''Get the graphics surface so it can be blitted onto the game window'''
        return cls._window
    
    @classmethod
    def start_draw(cls):
        '''Fill the surface with a background to prepare for drawing'''
        cls._window.fill(cls.__BG_COL)

class GUIVisualHandler(VisualHandler, ABC):
    '''Visual handler that makes use of the GUIHandler to create UI elements
    rather than drawing graphics itself.'''

    @classmethod
    def draw(cls):
        '''This visual handler draws a GUI.'''
        GUIHandler.draw(cls._window)

    @staticmethod
    def _centred_in_dimensions(x_dimens: int, y_dimens: int, elem_w: int, elem_h: int):
        '''Return the x, y position for a GUI element with the given width and height
        so that it is centred inside an area with the given dimensions.'''
        return (x_dimens - elem_w) // 2, (y_dimens - elem_h) // 2