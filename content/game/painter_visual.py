import pygame as pg
import sound

class PainterVisual:
    
    @classmethod
    def be_at(cls, pos: tuple, direction: int, sfx_name: str=None):
        cls.__draw_at(pos, direction)
        sound.play_sfx(sfx_name)

    @classmethod
    def __draw_at(cls, pos: tuple, direction: int):
        pg.display.update()