import pygame as pg
from .abstract_handlers import VisualHandler
from .floor_manager import FloorManager
from .app import App
from . import startup_utility_state
from .audio_utility import SFXPlayer
from .game.game import Game
from .editor.editor import Editor

def setup_state(editor: bool=False):
    '''Return the initial state used by the game,
    passed to the Game instance during startup.
    To ensure all states can access necessary data,
    also load the game levels
    with FloorManager.load_floors()'''
    initial_state_name = editor and "EditFloorpacksState" or "FloorpackSelectState"

    FloorManager.load_floors()

    return initial_state_name

def setup_window(editor: bool=False):
    '''Create and return the game window object
    passed to the Game instance during startup.'''
    GAME_TITLE = "Painter"
    EDITOR_TITLE = "Level Editor"
    WINDOW_SIZE = (960, 680)

    title = editor and EDITOR_TITLE or GAME_TITLE

    # Create window
    pg.display.set_caption(title)
    window = pg.display.set_mode(WINDOW_SIZE)

    draw_surf = pg.Surface(WINDOW_SIZE)

    # Pass the window surface to the base VisualHandler
    # so the classes that inherit from it can draw graphics on the window
    VisualHandler.set_window(draw_surf)
    return window

class StartupMenu(App):
    _state_module = startup_utility_state

class GameAndEditor(App):
    def __init__(self):
        '''Create StartupMenu, Game, and Editor instances
        and store them for later use.'''
        STARTUP_INITIAL_STATE = 'StartupUtilityState'

        self.__game_window = setup_window()
        self.__s = StartupMenu(STARTUP_INITIAL_STATE, self.__game_window)

        game_initial_state = setup_state()
        self.__g = Game(game_initial_state, self.__game_window)

        editor_initial_state = setup_state(editor=True)
        editor_window = setup_window(True)
        self.__e = Editor(editor_initial_state, editor_window)

    def loop(self):
        '''Overrides the usual main loop to delegate to the
        main loops of the StartupMenu, Game, and Editor.
        Forms a menu where the user chooses one to boot.'''
        exit_code = self.__s.main()
        match exit_code:
            case 3 | True:
                # Exit option or closing the window will exit
                return False
            case 1:
                # First option opens the game
                SFXPlayer.play_sfx('menu')
                exit_code = self.__g.main()
                # An exit code of 3 means the ingame exit option was chosen.
                # That means we should continue running, to ask whether to boot
                # the editor or close the window.
                if exit_code != 3: return True
            case 2:
                # Second option opens the editor
                SFXPlayer.play_sfx('menu')
                exit_code = self.__e.main()
                if exit_code != 3: return True