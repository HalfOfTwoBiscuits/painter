import pygame as pg
from math import ceil
from ..abstract_handlers import VisualHandler
from ..file_utility import FileUtility
from ..audio_utility import SFXPlayer

class MenuVisual(VisualHandler):
    '''A visual for menus where the player chooses a numbered option.
    Unlike the other visual handlers an instance is created rather than using the class:
    this is because the options can vary but the logic is the same.'''

    __OPTIONS_PER_PAGE = 9 # Maximum of 9, to correspond with the number keys 1-9
    __PADDING_PX = 4 # Used for option padding and rounding of corners
    __SIDE_PADDING = 10 # Added to pad the edge

    __TEXT_COL = pg.Color(0,0,0)
    __BG_COL = pg.Color(200,200,200)
    
    # Font data
    __FONT_DIRNAME = 'font'
    __FONT_FILENAME = 'Gorilla_Black'

    __FONT_PATH = FileUtility.path_to_resource(__FONT_DIRNAME, __FONT_FILENAME)

    pg.font.init()
    __FONT = pg.font.Font(__FONT_PATH, 17)
    __TITLE_FONT = pg.font.Font(__FONT_PATH, 20)

    def __init__(self, title: str, options: list[str], option_ids: list[str]=[]):
        self.__title = title
        self.__options = options
        self.__option_ids = option_ids
        self.__page_index = 0
        self.__num_pages = ceil(len(options) / self.__class__.__OPTIONS_PER_PAGE)
        self.__is_multi_page = self.__num_pages > 1

        # Find the width required for the longest line in the menu
        # and height required for the tallest.

        # Use the width and height of the title as a starting point.
        title_w_highest_page_num = self.__append_page_info(title)
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
        self.__width = option_width + self.__class__.__PADDING_PX * 2 + self.__class__.__SIDE_PADDING * 2

        # Find string containing ASCII arrows with space between them,
        # indicating multiple pages. Amount of space between depends on menu width
        if self.__is_multi_page:
            self.__arrows_string = self.__arrows_at_edges(self.__width)

        # Add padding to height to find height of a row in the menu
        self.__row_height = option_height + self.__class__.__PADDING_PX * 2

        # Find total height: height of all options on a page,
        # plus one for the title, and another one for the arrows if there's more than one page.
        self.__extra_rows = self.__is_multi_page and 2 or 1
        options_on_page = self.get_options_per_page()
        self.__height = self.__row_height * (options_on_page + self.__extra_rows)

        # Get window dimensions and subtract the width and height needed,
        # to find the position of the topleft and bottom.
        win_width, win_height = self.__class__._window_dimensions
        self.__left_edge = (win_width - self.__width) // 2
        self.__top_edge = (win_height - self.__height) // 2
        self.__bottom_edge = self.__height + self.__top_edge

    def __prepend_key(self, option: str, index: int):
        '''Add the key pressed to select the option to the front of it.
        Returns the text displayed on the menu for the option.'''
        index_of_page = index // self.__class__.__OPTIONS_PER_PAGE
        key_for_option = index - index_of_page * self.__class__.__OPTIONS_PER_PAGE + 1
        return f'{key_for_option}) {option}'
    
    def __append_page_info(self, title: str):
        '''If there is more than one page,
        add the page number and total number of pages in brackets.'''

        output = title
        if self.__is_multi_page:
            page_num = self.__page_index + 1
            output += f' ({page_num}/{self.__num_pages})'
        return output
    
    def __arrows_at_edges(self, menu_width: int):
        '''Given the width of the menu, return a string with ASCII arrows
        separated by space so that they would be at the left and right edges of the width.
        This string is used to draw a graphic indicating the user can change pages.
        The user can change pages by clicking the graphic or using the arrow keys.'''
        LEFT_ARROW = '<-'
        RIGHT_ARROW = '->'
        ARROW_WIDTH, _ = self.__class__.__TITLE_FONT.size(LEFT_ARROW)
        return LEFT_ARROW + ' ' * (menu_width // ARROW_WIDTH - 1) + RIGHT_ARROW

    def draw(self):
        # Draw background rect
        pg.draw.rect(self.__class__._window, self.__class__.__BG_COL,
                     (self.__left_edge, self.__top_edge, self.__width, self.__height),
                     border_radius = self.__class__.__PADDING_PX)
        
        # Draw title
        full_title = self.__append_page_info(self.__title)
        self.__draw_menu_row(full_title, self.__top_edge, heading=True)

        # Draw arrows: clicked to change page
        if self.__is_multi_page:
            self.__draw_menu_row(self.__arrows_string, self.__top_edge + self.__row_height, heading=True)

        # Find the options being shown on the current page
        cur_options = self.__options[self.__first_option_index(self.__page_index):
                                     self.__first_option_index(self.__page_index + 1)]

        # Iterate over options, incrementing top_y by row_height from top to bottom of the menu
        # If we are on the last page and there are fewer options left than OPTIONS_PER_PAGE
        # then zip() will truncate the range of y positions.
        for index, option_info in enumerate(zip(cur_options,
            range(self.__top_edge + self.__row_height * self.__extra_rows,
                  self.__bottom_edge, self.__row_height))):

            option, top_y = option_info
            full_option = self.__prepend_key(option, index)
            self.__draw_menu_row(full_option, top_y)

    def __first_option_index(self, page_index: int):
        '''Return the index of the first option on the given page index.'''
        return page_index * self.__class__.__OPTIONS_PER_PAGE
    
    def __draw_menu_row(self, content: str, top: int, heading: bool=False):
        '''Render the given content string, with padding separating it from
        the left edge of the menu and from the given y position for the top.
        If heading is True, use the larger font and centre the text.'''

        # Find topleft corner of the option
        left = self.__left_edge + self.__class__.__PADDING_PX
        top += self.__class__.__PADDING_PX

        # Select font to use
        font = heading and self.__class__.__TITLE_FONT or self.__class__.__FONT

        # If title, centre
        if heading:
            text_w, _ = font.size(content)
            left += (self.__width - text_w) // 2     

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
                option_index = index_increment + self.__first_option_index(self.__page_index)
                try:
                    id = self.__option_ids[option_index]
                    if id is None: raise IndexError
                except IndexError:
                    return self.__options[option_index]
                else:
                    return id
            
            # Raise error if the number isn't within 1 to __OPTIONS_PER_PAGE
            # or the resulting index is past the final option
            except IndexError: raise ValueError        
        else: raise ValueError

    def next_page(self):
        '''Increment the page number to show later options.
        Does nothing if the menu is on the last page.'''
        if self.__page_index + 1 < self.__num_pages:
            SFXPlayer.play_sfx('move')
            self.__page_index += 1
        else: SFXPlayer.play_sfx('invalid')

    def prev_page(self):
        '''Decrement the page number to show earlier options.
        Does nothing if the menu is on the first page.'''
        if self.__page_index > 0:
            SFXPlayer.play_sfx('move')
            self.__page_index -= 1
        else: SFXPlayer.play_sfx('invalid')

    def get_options_per_page(self):
        '''Return the number of options per page, either the __OPTIONS_PER_PAGE constant
        or less if there aren't enough options for a page'''
        return min(self.__class__.__OPTIONS_PER_PAGE, len(self.__options))
    
    def set_title(self, new_title: str):
        '''Change the title of the menu.
        Called during unit tests to visually indicate a chosen option.
        Because this is only for testing it will not resize the menu to properly contain the title.'''
        self.__title = new_title

    def get_title(self):
        '''Return the title of this menu. Used to identify it for debugging.'''
        return self.__title