import pygame as pg
from abc import abstractmethod, ABC
from .audio_utility import SFXPlayer
from .font_utility import FontManager

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
        '''If the event is a keypress, delegate to _process_keypress().'''
        if event.type == pg.KEYDOWN:
            return self._process_keypress(self, event.key)
        return None
    
    @staticmethod
    def _process_keypress(self, key):
        '''Use the actions dictionary to determine
        what to do in response to a key being pressed.
        
        If the key code is a key in the dictionary,
        the first element of the corresponding tuple is the
        string name of a method to call.
        All other elements in that tuple will be passed as arguments.
        
        The return value of that method, if any, is a string
        identifier for a new state. Return it to the main loop.'''

        actions = self._variable_actions or self._ACTIONS
        a = actions.get(key)
        if a is not None:
            method_name = a[0]
            method_to_call = getattr(self, method_name)
            arguments = a[1:]
            state_change = method_to_call(*arguments)
            return state_change

class MenuControl(KeyboardInputHandler, ABC):
    '''Class that specifies a static method used to
    respond to clicking on a menu with the mouse.'''

    @staticmethod
    def _process_input_with_mouse(self, event, menu_visual_obj):
        '''Allow clicking options to select them
        or clicking the top area of the menu to change page.
        Delegates to select_mouse().'''
        if event.type == pg.MOUSEBUTTONUP:
            x, y = event.pos
            try:
                menu_response = menu_visual_obj.option_for_mouse_location(x, y)
            except ValueError: pass
            else:
                match menu_response:
                    case 1: menu_visual_obj.prev_page()
                    case 2: menu_visual_obj.next_page()
                    case _:
                        return self._select_mouse(self, *menu_response)
        else: return self._process_keyboard_input(self, event)
    
    @staticmethod
    @abstractmethod
    def _select_mouse(self, number: int, option_id: str):
        '''Hook for when an option is clicked with the mouse.'''
        ...

class FixedOptionsControl(MenuControl, ABC):
    '''Base class for an input handler that prompts the user
    to choose between a number of fixed options.
    Since the option that corresponds to a keypress is known,
    input is usually handled independently of the menu graphic:
    except when selecting an option with the mouse,
    which is where this class comes in.'''

    @classmethod
    def store_menu(cls, menu_visual_obj):
        cls.__menu = menu_visual_obj

    @staticmethod
    def process_input(cls, event):
        return cls._process_input_with_mouse(cls, event, cls.__menu)
    
    @staticmethod
    def _select_mouse(cls, num: int, _):
        return cls._process_keypress(cls, pg.key.key_code(str(num)))

class ArbitraryOptionsControl(MenuControl, ABC):
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
            pg.key.key_code(str(num)) : ('select_keyboard', num)
            for num in range(1, NUM_OPTIONS + 1)
        }

        actions[pg.K_LEFT] = ('prevpage',)
        actions[pg.K_RIGHT] = ('nextpage',)
        self.__class__._variable_actions = actions

    @abstractmethod
    def select_keyboard(self, number: int):
        '''Hook for when a number key 1-9 is pressed.
        Selects the menu option corresponding to that number, if there is one.
        Should call _choose_option()'''
        ...

    @abstractmethod
    def _choose_option(self):
        '''Method to call when an option is selected and its ID has been stored.
        Contains the option-selecting code that is common between select_keyboard()
        and select_mouse().'''
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

    @staticmethod
    def process_input(self, event):
        '''In addition to using _process_keyboard_input() to respond to number keys
        being pressed to select options, allow clicking options to select them
        or clicking the top area of the menu to change page.'''
        return self._process_input_with_mouse(self, event, self._menu)

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

    def select_keyboard(self, number: int):
        try: back_option_chosen = self._find_option_for_number(number)
        except ValueError: return
        if back_option_chosen: return self.back()
        return self._choose_option()
    
    @staticmethod
    def _select_mouse(self, _, option_id: str):
        self._option_id = option_id
        if self._option_id == self.__BACK_OPTION: return self.back()
        return self._choose_option()
    
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

    @staticmethod
    def _centred_in_dimensions(x_dimens: int, y_dimens: int, elem_w: int, elem_h: int):
        '''Return the x, y position for a GUI element with the given width and height
        so that it is centred inside an area with the given dimensions.'''
        return (x_dimens - elem_w) // 2, (y_dimens - elem_h) // 2
    
class TextDisplayVisualHandler(VisualHandler, ABC):
    __FONT = FontManager.get_heading_font()
    __COL = pg.Color(255,255,255)
    _TEXT = 'This message should not appear'

    @classmethod
    def init(cls):
        win_w, win_h = cls._window_dimensions
        text_w, text_h = cls.__FONT.size(cls._TEXT)

        # New lines aren't counted in size calculation
        # so divide width by number of new lines
        # and multiply height.
        num_lines = cls._TEXT.count('\n')
        text_w //= num_lines
        text_h *= num_lines

        text_x, text_y = cls._centred_in_dimensions(win_w, win_h, text_w, text_h)
        cls.__pos = (text_x, text_y)
        cls.__text_surf = cls.__FONT.render(cls._TEXT, False, cls.__COL)

    @classmethod
    def draw(cls):
        cls._window.blit(cls.__text_surf, cls.__pos)