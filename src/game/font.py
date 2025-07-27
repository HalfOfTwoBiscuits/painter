import pygame as pg
from ..file_utility import FileUtility
class FontManager:
    # Font data
    __FONT_DIRNAME = 'font'
    __FONT_FILENAME = 'Gorilla_Black'

    __FONT_PATH = FileUtility.path_to_resource(__FONT_DIRNAME, __FONT_FILENAME)

    pg.font.init()
    __FONT = pg.font.Font(__FONT_PATH, 17)
    __HEADING_FONT = pg.font.Font(__FONT_PATH, 20)

    @classmethod
    def get_font(cls):
        return cls.__FONT
    
    @classmethod
    def get_heading_font(cls):
        return cls.__HEADING_FONT