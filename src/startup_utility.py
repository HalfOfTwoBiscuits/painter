from .game.states import LevelSelectState
from .game.visual_handler_base import VisualHandler
from .game.floor_manager import FloorManager
import pygame as pg

def setup_state(editor: bool=False):
    '''Return the initial state used by the game,
    passed to the Game instance during startup.
    To ensure all states can access necessary data,
    also load the game levels
    with FloorManager.load_floors()'''
    initial_state = editor and None or LevelSelectState

    FloorManager.load_floors()

    return initial_state

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