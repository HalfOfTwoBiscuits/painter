import pygame as pg
from math import ceil
from os import path
from visual_handler_base import VisualHandler

class MenuVisual(VisualHandler):
    '''A visual for menus where the player chooses a numbered option.
    Unlike the other visual handlers an instance is created rather than using the class:
    this is because the options can vary but the logic is the same.'''

    __OPTIONS_PER_PAGE = 10 # To correspond with the number keys 0-9

    # Font data
    __FONT_FILETYPE = '.ttf'
    __FONT_DIR_RELATIVE_PATH = 'font'
    __FONT_FILENAME = 'Gorilla_Black'

    __FONT_PATH = path.join(__FONT_DIR_RELATIVE_PATH, __FONT_FILENAME + __FONT_FILETYPE)

    __FONT = pg.font.Font(__FONT_PATH, 16)
    __TITLE_FONT = pg.font.Font(__FONT_PATH, 20)
    
    __PADDING = 4

    def __init__(self, title: str, options: list[str]):
        self.__title = title
        self.__options = options
        self.__page = 1
        self.__num_pages = ceil(len(options) / self.__class__.__OPTIONS_PER_PAGE)

        self.__width = self.__option_height = 0
        # Find the width required for the longest option
        # and height required for the tallest.
        for o in options:
            w, h = self.__class__.__FONT.size(o)
            if w > self.__width: self.__width = w
            if h > self.__option_height: self.__option_height = h

        # Also consider the width and height of the title.
        title_w, title_h = self.__class__.__TITLE_FONT.size(title)
        if title_w > self.__width: self.__width = title_w
        if title_h > self.__option_height: self.__option_height = title_h

        # Add padding
        self.__width += self.__class__.__PADDING * 2
        self.__option_height += self.__class__.__PADDING * 2

        # Find total height: height of all options plus one for the title
        self.__height = self.__option_height * (len(options) + 1)

        # Get window dimensions and subtract the width and height needed,
        # to find the position of the topleft.
        win_width, win_height = self.__class__._window_dimensions
        self.__left_edge = (win_width - self.__width) // 2
        self.__top_edge = (win_height - self.__height) // 2

    def draw(self):
        pg.draw.rect()