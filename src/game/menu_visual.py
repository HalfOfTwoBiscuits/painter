import pygame as pg
from math import ceil
from os import path
from .visual_handler_base import VisualHandler

class MenuVisual(VisualHandler):
    '''A visual for menus where the player chooses a numbered option.
    Unlike the other visual handlers an instance is created rather than using the class:
    this is because the options can vary but the logic is the same.'''

    __OPTIONS_PER_PAGE = 5 # Maximum of 9, to correspond with the number keys 1-9
    __PADDING_PX = 4 # Used for option padding and rounding of corners
    __LINE_SIZE = 1 # Size in pixels of lines separating options

    __TEXT_COL = pg.Color(0,0,0)
    __BG_COL = pg.Color(200,200,200)

    __THIS_DIR = path.split(path.abspath(__file__))[0]
    
    # Font data
    __FONT_FILETYPE = '.ttf'
    __FONT_DIR_RELATIVE_PATH = 'font'
    __FONT_FILENAME = 'Gorilla_Black'

    __FONT_PATH = path.join(__THIS_DIR, __FONT_DIR_RELATIVE_PATH, __FONT_FILENAME + __FONT_FILETYPE)

    pg.font.init()
    __FONT = pg.font.Font(__FONT_PATH, 16)
    __TITLE_FONT = pg.font.Font(__FONT_PATH, 20)

    def __init__(self, title: str, options: list[str]):
        self.__title = title
        self.__options = options
        self.__page_index = 0
        self.__num_pages = ceil(len(options) / self.__class__.__OPTIONS_PER_PAGE)

        # Find the width required for the longest line in the menu
        # and height required for the tallest.

        # Use the width and height of the title as a starting point.
        title_w_highest_page_num = self.__append_page_num(title)
        option_width, option_height = self.__class__.__TITLE_FONT.size(title_w_highest_page_num)

        # Iterate over options to check if any are wider or taller
        for index, o in enumerate(options):
            # Prepend with the number key used to select it
            full_o = self.__prepend_key(o, index)

            # If an option is the widest or tallest so far, update width/height
            w, h = self.__class__.__FONT.size(full_o)
            if w > option_width: option_width = w
            if h > option_height: option_height = h

        # Add padding to width to find the menu width
        self.__width = option_width + self.__class__.__PADDING_PX * 2

        # Add padding and the size of a dividing line to height
        # to find height of a row in the menu.
        self.__row_height = option_height + self.__class__.__PADDING_PX * 2 + self.__class__.__LINE_SIZE

        # Find total height: height of all options plus one for the title
        self.__height = self.__row_height * (len(options) + 1)

        # Get window dimensions and subtract the width and height needed,
        # to find the position of the topleft and bottom.
        win_width, win_height = self.__class__._window_dimensions
        self.__left_edge = (win_width - self.__width) // 2
        self.__top_edge = (win_height - self.__height) // 2
        self.__bottom_edge = self.__height - self.__top_edge

    def __prepend_key(self, option: str, index: int):
        '''Add the key pressed to select the option to the front of it.
        Returns the text displayed on the menu for the option.'''
        index_of_page = index // self.__class__.__OPTIONS_PER_PAGE
        key_for_option = index - index_of_page * self.__class__.__OPTIONS_PER_PAGE
        return f'{key_for_option}) {option}'
    
    def __append_page_num(self, title: str, use_highest: bool=False):
        '''Add the page number to the end of the title, unless on page 1.
        If use_highest is true, use the highest page number instead of the current one.'''

        if self.__page_index == 0:
            return title
        else:
            page_num = use_highest and self.__num_pages or self.__page_index + 1
            return f'{title} (Page {page_num})'

    def draw(self):
        # Draw background rect
        pg.draw.rect(self.__class__._window, self.__class__.__BG_COL,
                     (self.__left_edge, self.__top_edge, self.__width, self.__height),
                     border_radius = self.__class__.__PADDING_PX)
        
        # Draw title
        full_title = self.__append_page_num(self.__title)
        self.__draw_menu_row(full_title, self.__top_edge, is_title=True)

        # Find the options being shown on the current page
        cur_options = self.__options[self.__page_index * self.__class__.__OPTIONS_PER_PAGE - 1:]

        # Iterate over options, incrementing top_y by row_height from top to bottom of the menu
        # If we are on the last page and there are fewer options left than OPTIONS_PER_PAGE
        # then zip() will truncate the range of y positions.
        for o, top_y in zip(cur_options,
            range(self.__top_edge + self.__row_height, self.__bottom_edge, self.__row_height)):
            full_o = self.__prepend_key(o)
            self.__draw_menu_row(full_o, top_y)

    def __draw_menu_row(self, content: str, top: int, is_title: bool=False):
        '''Render the given content string, with padding separating it from
        the left edge of the menu and from the given y position for the top.
        If is_title is True, use the larger font.
        Underneath, draw a line.'''

        # Find topleft corner of the option
        left = self.__left_edge + self.__class__.__PADDING_PX
        top += self.__class__.__PADDING_PX

        # Select font to use
        font = is_title and self.__class__.__TITLE_FONT or self.__class__.__FONT        

        text_surf = font.render(content, True, self.__class__.__TEXT_COL)
        self.__class__._window.blit(text_surf, (left, top))

    def option_for_number(self, number_pressed: int):
        '''Given that the options on a page are numbered 1 to __OPTIONS_PER_PAGE,
        return the option on the current page corresponding to the given number.
        If there is no option corresponding to the number then raise ValueError.

        Only used when options may or will use more than one page,
        since the response to a number keypress might change depending on visual state.'''

        if 1 <= number_pressed <= self.__class__.__OPTIONS_PER_PAGE:
            try:
                index_increment = number_pressed - 1
                # Multiply __OPTIONS_PER_PAGE by the page index to find how many along we already are,
                # and add number_pressed - 1
                option_index = index_increment + self.__page_index * self.__class__.__OPTIONS_PER_PAGE
                return self.__options[option_index]
            
            # Raise error if the number isn't within 1 to __OPTIONS_PER_PAGE
            # or the resulting index is past the final option
            except IndexError: raise ValueError        
        else: raise ValueError

    def next_page(self):
        '''Increment the page number to show later options.
        Does nothing if the menu is on the last page.'''
        if self.__page_index < self.__num_pages:
            self.__page_index += 1

    def prev_page(self):
        '''Decrement the page number to show earlier options.
        Does nothing if the menu is on the first page.'''
        if self.__page_index > 0:
            self.__page_index -= 1

    def get_options_per_page(self):
        '''Return the constant number of options per page'''
        return self.__class__.__OPTIONS_PER_PAGE