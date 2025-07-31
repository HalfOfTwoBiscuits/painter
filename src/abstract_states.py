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
    def process_input(cls, event):
        '''Respond to any event other than closing the game.
        Delegates to InputHandler.process_input().
        Return any string identifier of a new state to change to.'''
        i_handler = cls.get_input_handler()
        # get_input_handler() can return None for no input or True to end the program
        if i_handler is True or i_handler is None: return i_handler

        # Input handler may be a class or an instance, so 'self' is passed manually
        new_state = i_handler.process_input(i_handler, event)
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

class MenuState(State, ABC):
    '''Base class for all states that use the MenuVisual.'''
    _TITLE = 'Menu'
    
    @classmethod
    def _setup_menu_visual(cls, menu_options: list[str]):
        cls._menu_visual = MenuVisual(cls._TITLE, menu_options)

    _visual_handlers = None
    
    @classmethod
    def get_visual_handlers(cls):
        return cls._visual_handlers

class GameContentSelectState(MenuState, ABC):
    '''Base class for states where the user selects a floor or floorpack.
    Has a variable for an input handler instance to be initialised with the MenuVisual.'''
    _menu_input_handler = None
    _menu_visual = None
    
    @classmethod
    def get_input_handler(cls):
        return cls._menu_input_handler
    
    @classmethod
    def get_visual_handlers(cls):
        '''Currently, all the floor and floorpack selection menus
        display only the menu, and no other graphics.
        Since this is the case, to save setting the visual handlers on all of them,
        just the menu visual is returned.

        If more graphics are added to these menus, I could remove this method
        or override it on a case-by-case basis.'''
        return (cls._menu_visual,)
    
class FixedOptionsSelectState(MenuState, ABC):
    '''Base class for pause menu and post-floor menus.
    The options displayed on the menu are fixed.'''
    _OPTIONS = None
    
    @classmethod
    def _setup_menu_visual(cls):
        '''Create the MenuVisual with fixed menu options.'''
        return super()._setup_menu_visual(cls._OPTIONS)