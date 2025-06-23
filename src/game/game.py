from . import game_states
from .visual_handler_base import VisualHandler
import asyncio
import pygame as pg

class Game:
    '''An instance of this class manages the game loop.'''

    # For frame rate limiting
    __clock = pg.time.Clock()

    def __init__(self, InitialState, window):
        '''Store game window, set up and store initial state.'''
        
        new_state_name = 'maybe'

        # The initial state may be temporary and forward on to a new one.
        # Repeatedly call enter() until it doesn't return another state name to change to.
        while new_state_name is not None:
            self.__state = InitialState
            new_state_name = InitialState.enter()
            if new_state_name is not None:
                InitialState = getattr(game_states, new_state_name)
        self.__window = window

    def main(self):
        '''Run game loop.
        Allow returning an output True for successful unit test or False for unsucessful.'''
        output = None
        while output is None: output = self.loop()
        return output
    
    async def online_main(self):
        '''A version of the main function intended to be used with a pygbag
        web build. That web build doesn't currently work (see README.md)'''
        while True:
            self.loop()
            # Await asynchronous processing of pygbag needed for web hosting
            await asyncio.sleep(0)

    def loop(self):
        '''One iteration of the game loop.
        Called in main(), online_main(), and also independently
        to process one frame, during unit tests.'''

        # Process input events
        for e in pg.event.get():
            if e.type == pg.QUIT:
                # Closing the window ends the program
                return True
            if e.type == pg.KEYDOWN:
                # Process input: make stuff actually happen
                new_state = self.__state.process_input(e.key)
                # and if a string value was returned, change to the state with that name
                # input may result in repeated state change
                while new_state is not None:
                    # For test cases: returning a boolean value indicates success/failure.
                    if isinstance(new_state, bool): return new_state
                    # Change state
                    print ('New state:', new_state)
                    self.__state = getattr(game_states, new_state)
                    # Call the enter() method, which can *also* cause a change of state:
                    # for temporary states that do processing before moving on
                    new_state = self.__state.enter()
        
        # Draw graphics
        VisualHandler.start_draw()
        handlers = self.__state.get_visual_handlers()
        for visual_handler in handlers:
            visual_handler.draw()

        graphics_surf = VisualHandler.get_graphics()
        self.__window.blit(graphics_surf,(0,0))
        pg.display.update()

        # Limit frame rate
        self.__class__.__clock.tick(30)