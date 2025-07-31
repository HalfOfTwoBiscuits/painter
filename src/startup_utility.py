import pygame as pg
from .abstract_handlers import VisualHandler
from .floor_manager import FloorManager
from .app import App
from . import startup_utility_state

def setup_state(editor: bool=False):
    '''Return the initial state used by the game,
    passed to the Game instance during startup.
    To ensure all states can access necessary data,
    also load the game levels
    with FloorManager.load_floors()'''
    initial_state_name = editor and "EditorStartState" or "GameStartState"

    return initial_state_name

def setup_window(editor: bool=False):
    '''Create and return the game window object
    passed to the Game instance during startup.'''
    WINDOW_SIZE = (960, 680)

    # Create window
    window = pg.display.set_mode(WINDOW_SIZE)

    draw_surf = pg.Surface(WINDOW_SIZE)

    # Pass the window surface to the base VisualHandler
    # so the classes that inherit from it can draw graphics on the window
    VisualHandler.set_window(draw_surf)
    return window

class StartupMenu(App):
    _state_module = startup_utility_state