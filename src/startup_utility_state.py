from .abstract_states import FixedOptionsSelectState
from .game.menu_visual import MenuVisual
from .startup_utility_handler import StartupMenuControl

class StartupUtilityState(FixedOptionsSelectState):
    _TITLE = 'Menu'
    _OPTIONS = ['Play', 'Make Levels', 'Quit']
    _INPUT_HANDLER = StartupMenuControl
    
    @classmethod
    def enter(cls):
        # Could put this in a FixedOptionsSelectState method that uses _INPUT_HANDLER.
        # Then, if enter() is overridden, call it with the extra visual handlers.
        cls._setup_menu_visual()
        StartupMenuControl.store_menu(cls._menu_visual)
        cls._visual_handlers = (cls._menu_visual,)