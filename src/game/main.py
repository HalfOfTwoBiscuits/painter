#import asyncio
import pygame as pg
from . import states
from .visual_handler_base import VisualHandler
from .floor_manager import FloorManager

def setup():
    '''Set up the game and return the initial state.
    For now it is LevelSelect and not FloorPackSelect because load_floors()
    only creates one floorpack (and floor) : there are no level files so the
    concept of a floorpack is not useful.'''

    INITIAL_STATE = states.LevelSelectState

    FloorManager.load_floors()
    return INITIAL_STATE

class Game:
    __TITLE = "Painter"
    __WINDOW_SIZE = (960, 680)

    # Create window
    pg.display.set_caption(__TITLE)
    __window = pg.display.set_mode(__WINDOW_SIZE)

    # Pass the window surface to the base VisualHandler
    # so the classes that inherit from it can draw graphics on the window
    VisualHandler.set_window(__window)

    # For frame rate limiting
    __clock = pg.time.Clock()

    def __init__(self, InitialState):
        InitialState.enter()
        self.__state = InitialState

    def main(self):
        while True:
            # Process key press events
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    raise SystemExit
                if e.type == pg.KEYDOWN:
                    # On key press, process input
                    new_state = self.__state.get_input_handler().process_input(e.key)
                    # and if a string value was returned, change to the state with that name
                    if new_state is not None:
                        # For test cases: returning a boolean value indicates success/failure.
                        if isinstance(new_state, bool): return new_state
                        # Change state
                        self.__state = getattr(states, new_state)
                        self.__state.enter()
            
            # Draw graphics
            for visual_handler in self.__state.get_visual_handlers():
                visual_handler.draw()
            pg.display.update()

            # Limit frame rate
            self.__class__.__clock.tick(30)
            # Await asynchronous processing of pygbag needed for web hosting
            #await asyncio.sleep(0)
        

if __name__ == '__main__':
    InitialState = setup()
    #asyncio.run(Game.main())
    g = Game(InitialState)
    g.main()