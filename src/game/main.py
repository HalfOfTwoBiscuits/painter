#import asyncio
import pygame as pg
from . import states
from .visual_handler_base import VisualHandler
from .floor_manager import FloorManager

def setup_state():
    '''Set up the game and return the initial state.
    For now it is LevelSelect and not FloorPackSelect because load_floors()
    only creates one floorpack (and floor) : there are no level files so the
    concept of a floorpack is not useful.'''

    INITIAL_STATE = states.GameplayState

    FloorManager.load_floors()

    return INITIAL_STATE

def setup_window():
    TITLE = "Painter"
    WINDOW_SIZE = (960, 680)

    # Create window
    pg.display.set_caption(TITLE)
    window = pg.display.set_mode(WINDOW_SIZE)

    draw_surf = pg.Surface(WINDOW_SIZE)

    # Pass the window surface to the base VisualHandler
    # so the classes that inherit from it can draw graphics on the window
    VisualHandler.set_window(draw_surf)
    return window

class Game:
    # For frame rate limiting
    __clock = pg.time.Clock()

    def __init__(self, InitialState, window):
        InitialState.enter()
        self.__state = InitialState
        self.__window = window

    def main(self):
        # Allow returning an output True for successful unit test or False for unsucessful
        output = None
        while output is None: output = self.loop()

    def loop(self):
        # Process key press events
        for e in pg.event.get():
            if e.type == pg.QUIT:
                return False
            if e.type == pg.KEYDOWN:
                # On key press, process input
                i_handler = self.__state.get_input_handler()
                new_state = i_handler.process_input(i_handler, e.key)
                # and if a string value was returned, change to the state with that name
                if new_state is not None:
                    # For test cases: returning a boolean value indicates success/failure.
                    if isinstance(new_state, bool): return new_state
                    # Change state
                    self.__state = getattr(states, new_state)
                    self.__state.enter()
        
        # Draw graphics
        VisualHandler.start_draw()
        for visual_handler in self.__state.get_visual_handlers():
            visual_handler.draw()

        graphics_surf = VisualHandler.get_graphics()
        self.__window.blit(graphics_surf,(0,0))
        pg.display.update()

        # Limit frame rate
        self.__class__.__clock.tick(30)
        # Await asynchronous processing of pygbag needed for web hosting
        #await asyncio.sleep(0)