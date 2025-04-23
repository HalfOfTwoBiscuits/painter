import asyncio
import pygame as pg
import states
from floor_visual import FloorVisual
from floor_player import FloorPlayer
from visual_handler_base import VisualHandler

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
    # Determines visuals shown and inputs possible
    __state = states.GameplayState

    @classmethod
    async def main(cls):
        while True:
            # Process key press events
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    raise SystemExit
                if e.type == pg.KEYDOWN:
                    new_state = cls.__state.INPUT_HANDLER.process_input(e.key)
                    if new_state is not None:
                        cls.__state = getattr(states, new_state)
            
            # Draw graphics
            for visual_handler in cls.__state.VISUAL_HANDLERS:
                visual_handler.draw()
            
            # Limit frame rate
            cls.__clock.tick(30)
            # Await asynchronous processing of pygbag needed for web hosting
            await asyncio.sleep(0)
        

if __name__ == '__main__':
    asyncio.run(Game.main())