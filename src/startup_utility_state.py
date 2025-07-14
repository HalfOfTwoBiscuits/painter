from .abstract_states import State
from .game.menu_visual import MenuVisual
from .startup_utility_handler import StartupMenuControl

class StartupUtilityState(State):
    __TITLE = 'Menu'
    __OPTION_NAMES = ['Play', 'Make Levels', 'Quit']
    _INPUT_HANDLER = StartupMenuControl
    __visual_handlers = None
    
    @classmethod
    def get_visual_handlers(cls):
        if cls.__visual_handlers is None:
            cls.__visual_handlers = (MenuVisual(cls.__TITLE, cls.__OPTION_NAMES),)
        return cls.__visual_handlers