import asyncio
import pygame as pg
import input_handlers

class Game:
    TITLE = "Painter"
    WINDOW_SIZE = (960, 680)
    pg.display.set_caption(TITLE)
    window = pg.display.set_mode(WINDOW_SIZE)
    handler = input_handlers.PainterControl

    @classmethod
    async def main(cls):
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    raise SystemExit
                if e.type == pg.KEYDOWN:
                    cls.handler.process_input(e.key)

            # pg.display.flip() only called when visual changes occur
            # as a result of input. Still need to work out structure
            # for loading levels.
        

if __name__ == '__main__':
    asyncio.run(Game.main())