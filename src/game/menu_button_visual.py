import pygame as pg
from ..abstract_handlers import VisualHandler
from .font import FontManager

class MenuButtonVisual(VisualHandler):
    __BUTTON_RECT = pg.Rect(0,0,55,60)
    __BUTTON_CORNER_RADIUS = 5
    __BG_COL = pg.Color(200,200,200)
    __TEXT_COL = pg.Color(0,0,0)
    _TEXT = 'Menu\n(Esc)'

    @classmethod
    def draw(cls):
        pg.draw.rect(cls._window, cls.__BG_COL, cls.__BUTTON_RECT, border_radius=cls.__BUTTON_CORNER_RADIUS)
        font = FontManager.get_font()
        text = font.render(cls._TEXT, True, cls.__TEXT_COL)
        cls._window.blit(text, (0,0))

    @classmethod
    def get_button_rect(cls):
        return cls.__BUTTON_RECT