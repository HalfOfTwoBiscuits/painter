from abc import ABC
from .game.menu_visual import MenuVisual

class State(ABC):
    _INPUT_HANDLER = None
    _VISUAL_HANDLERS = ()

    @classmethod
    def enter(cls):
        '''Method called when the program enters this state.
        Optional to implement.'''
        ...

    @classmethod
    def process_input(cls, key_pressed):
        '''Respond to a key press. Delegates to InputHandler.process_input().
        Return any string identifier of a new state to change to.'''
        i_handler = cls.get_input_handler()
        # get_input_handler() can return None to end the program
        if i_handler is None: return True

        # Input handler may be a class or an instance, so 'self' is passed manually
        new_state = i_handler.process_input(i_handler, key_pressed)
        return new_state

    @classmethod
    def get_input_handler(cls):
        '''Method that returns the input handler used.
        Defaults to the value of the _INPUT_HANDLER attribute.
        It is public only for unit tests, otherwise it is only called in process_input().
        If it returns None to process_input() then the program ends.'''
        return cls._INPUT_HANDLER
    
    @classmethod
    def get_visual_handlers(cls):
        '''Method that returns the visual handlers used.
        Defaults to the value of the _VISUAL_HANDLERS attribute.'''
        return cls._VISUAL_HANDLERS
    
class GameContentSelectState(State, ABC):
    '''Base class for floor select and floorpack select.'''
    _menu_input_handler = None
    _menu_visual = None
    _TITLE = 'Menu'

    @classmethod
    def _setup_menu_visual(cls, menu_options: list[str]):
        cls._menu_visual = MenuVisual(cls._TITLE, menu_options)

    @classmethod
    def get_visual_handlers(cls):
        '''Return a MenuVisual instance with the levels as options,
        as created when entering this state.'''
        return (cls._menu_visual,)
    
    @classmethod
    def get_input_handler(cls):
        return cls._menu_input_handler