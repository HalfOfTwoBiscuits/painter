from .abstract_states import MenuState
from .startup_utility_handler import StartupMenuControl
from .config import OnlineConfig

class StartupUtilityState(MenuState):
    _TITLE = 'Menu'
    _INPUT_HANDLER = StartupMenuControl
    __MAIN_OPTIONS = ['Play', 'Make Levels']
    __QUIT_OPTION = 'Quit'
    
    @classmethod
    def enter(cls):
        options = cls.__MAIN_OPTIONS
        if OnlineConfig.can_exit(in_startup_menu=True):
            options.append(cls.__QUIT_OPTION)
        cls._setup_menu_visual(options)
        StartupMenuControl.store_menu(cls._menu_visual)
        cls._visual_handlers = (cls._menu_visual,)