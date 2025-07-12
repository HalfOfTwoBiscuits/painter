import asyncio
import pygame as pg
from abc import ABC

from .abstract_handlers import VisualHandler

class App(ABC):
    '''An instance of this class manages the main loop for the game,
    editor, and unit tests.'''

    # For frame rate limiting
    __clock = pg.time.Clock()

    # Source file for states:
    # game_states.py, editor_states.py, tcase_states.py, or all_states.py
    # Specified by children.
    _state_module = None

    def __init__(self, initial_state_name: str, window):
        '''Store window, enter initial state.'''
        self._change_state(initial_state_name)
        self.__window = window

    def main(self):
        '''Run game loop.
        Allow returning an output:
        True for successful unit test or False for unsucessful.'''
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
                new_state = self._state.process_input(e.key)
                # For test cases: returning a boolean value indicates success/failure.
                if isinstance(new_state, bool): return new_state

                self._change_state(new_state)
            self._process_other_event(e)
        
        # Draw graphics
        VisualHandler.start_draw()
        handlers = self._state.get_visual_handlers()
        for visual_handler in handlers:
            visual_handler.draw()

        graphics_surf = VisualHandler.get_graphics()
        self.__window.blit(graphics_surf,(0,0))
        pg.display.update()

        # Limit frame rate
        delta_time = self.__class__.__clock.tick(30) / 1000
        self._use_delta(delta_time)
    
    def _change_state(self, state_name: str):
        '''Retrieve the given state, a class,
        from the module specified where states are contained
        (e.g. game_states.py, editor_states.py).
        Set up the state with the enter() classmethod and store it for later use.
        The enter() method may forward onto a different state to the one specified.'''

        while state_name is not None:
            # Change state
            print ('New state:', state_name)
            self._state = getattr(self.__class__._state_module, state_name)
            # Call the enter() method, which can *also* cause a change of state:
            # for temporary states that do processing before moving on
            state_name = self._state.enter()

    def _process_other_event(self, event):
        '''Respond to other events than keyboard presses
        or closing the game.
        Overridden by the editor.'''
        ...
    
    def _use_delta(self, dt: float):
        '''Respond to the delta time since the last frame.
        Overridden by the editor.'''
        ...