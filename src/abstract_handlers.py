import pygame as pg
from abc import abstractmethod, ABC
from .audio_utility import SFXPlayer

class InputHandler(ABC):
    '''Base for all input processing classes.'''

    @staticmethod
    @abstractmethod
    def process_input(self, event):
        '''Respond to a pygame event. Used for any event other than closing the game.

        For some children an instance is created and for others the class is used,
        so this is a staticmethod and self is passed in manually.'''
        ...

class KeyboardInputHandler(InputHandler, ABC):
    '''A base class for input handlers that specifies the
    _process_keyboard_input() method to respond to key presses,
    and calls that in process_input().
    Child classes that want to process other input too
    can override process_input().'''

    # Constant response to keys being pressed
    _ACTIONS = {}
    # If not None, this variable value will be used instead
    _variable_actions = None

    @staticmethod
    def process_input(self, event):
        '''Delegate to _process_keyboard_input().
        Can be overriden in order to process other input too.'''
        return self._process_keyboard_input(self, event)
    
    @staticmethod
    def _process_keyboard_input(self, event):
        '''Use the actions dictionary to determine
        what to do in response to a key being pressed.
        
        If the key code is a key in the dictionary,
        the first element of the corresponding tuple is the
        string name of a method to call.
        All other elements in that tuple will be passed as arguments.
        
        The return value of that method, if any, is a string
        identifier for a new state. Return it to the main loop.'''
        if event.type == pg.KEYDOWN:
            key = event.key

            actions = self._variable_actions or self._ACTIONS
            a = actions.get(key)
            if a is not None:
                method_name = a[0]
                method_to_call = getattr(self, method_name)
                arguments = a[1:]
                state_change = method_to_call(*arguments)
                return state_change
            
        return None
        
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
        store the ID used for it on the menu as the _option_id attribute.
        If there is no corresponding option then play an 'invalid' sfx
        and raise ValueError.'''
        try:
            self._option_id = self._menu.option_for_number(number)
        except ValueError:
            SFXPlayer.play_sfx('invalid')
            raise ValueError
        
    def nextpage(self):
        '''Go to the next page on the menu'''
        self._menu.next_page()
    
    def prevpage(self):
        '''Go to the previous page on the menu'''
        self._menu.prev_page()

class ArbitraryOptionsControlWithBackButton(ArbitraryOptionsControl, ABC):

    _STATE_AFTER_BACK = None

    def __init__(self, menu_visual_obj, BACK_OPTION_ID: str):
        super().__init__(menu_visual_obj)
        self.__BACK_OPTION = BACK_OPTION_ID
        self.__class__._variable_actions[pg.K_BACKSPACE] = ('back',)
        self.__class__._variable_actions[pg.K_ESCAPE] = ('back',)

    def _find_option_for_number(self, number: int) -> bool:
        '''Like the base _find_option_for_number but also returns
        a boolean for whether the back option was chosen.
        True : back option chosen, False : another option was chosen.
        Will raise ValueError if there is no corresponding option.'''

        super()._find_option_for_number(number)
        return self._option_id == self.__BACK_OPTION
    
    @classmethod
    def back(cls) -> str | int:
        SFXPlayer.play_sfx('back')
        return cls._STATE_AFTER_BACK

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
        