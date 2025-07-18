from ..abstract_handlers import VisualHandler
import pygame as pg

class FloorVisual(VisualHandler):
    '''Class that draws graphics for an ingame level (floor)'''
    __LINE_SIZE = 4
    __LINE_COL = pg.Color(255,255,255)
    __WRAP_LINE_COL = pg.Color(60,60,60)
    __PAINT_COL = pg.Color(150,30,30)
    __WRAP_PAINT_COL = pg.Color(75,15,15)
    __BG_COL = pg.Color(0,0,0)
    __EDITOR_HEIGHT_FRAC = 1.25

    @classmethod
    def new_floor(cls, floor_obj, editor: bool=False):
        '''Set up graphical parameters used to draw the grid for a floor.
        Called once when the floor starts.'''
        cls._window.fill(cls.__BG_COL)

        # Retrieve size of grid (in cells)
        # and dimensions of the game window (in pixels)
        cls.__grid = floor_obj.get_cell_grid()
        grid_w, grid_h = cls.__grid.get_size()
        win_w, win_h = cls._window_dimensions
        if editor: win_h = int(win_h / cls.__EDITOR_HEIGHT_FRAC)

        # Calculate width and height taken up by lines between cells
        all_lines_w = cls.__LINE_SIZE * (grid_w + 1)
        all_lines_h = cls.__LINE_SIZE * (grid_h + 1)
        # Calculate dimension of a cell in pixels.
        # Base it on whichever of width or height is the limiting factor
        cls.__cell_dimens = min(
            win_w // grid_w - all_lines_w,
            win_h // grid_h - all_lines_h
            )
        
        # Calculate dimensions of the grid in pixels
        all_cells_w = cls.__cell_dimens * grid_w
        all_cells_h = cls.__cell_dimens * grid_h

        # Determine positions of grid edges when it is centred on the screen
        cls.__left_edge = (win_w - all_cells_w) // 2
        cls.__right_edge = win_w - cls.__left_edge
        cls.__top_edge = (win_h - all_cells_h) // 2
        cls.__bottom_edge = win_h - cls.__top_edge

    @classmethod
    def draw(cls):
        '''Draw the floor on the screen,
        with lines to show the grid and painted cells filled in.'''
        win_w, win_h = cls._window_dimensions

        # Draw vertical lines
        for x in range(cls.__left_edge, cls.__right_edge + 1,
                       cls.__cell_dimens):
            
            cls.__draw_line((x, cls.__top_edge), (x, cls.__bottom_edge))
            cls.__draw_line((x, 0), (x, cls.__top_edge), faded=True)
            cls.__draw_line((x, cls.__bottom_edge), (x, win_h), faded=True)
        
        # Draw horizontal lines
        for y in range(cls.__top_edge, cls.__bottom_edge + 1,
                       cls.__cell_dimens):
            
            cls.__draw_line((cls.__left_edge, y), (cls.__right_edge, y))
            cls.__draw_line((0, y), (cls.__left_edge, y), faded=True)
            cls.__draw_line((cls.__right_edge, y), (win_w, y), faded=True)
        
        grd_w, grd_h = cls.__grid.get_size()
        
        # Fill in the painted cells
        for cell_pos in cls.__grid.get_full_cell_positions():

            # Add paint
            cls.__draw_paint(cell_pos)

            # If the cell is on the edge of the grid,
            # also draw paint outside the grid to indicate
            # the painter can't go to the opposite side.
            x, y = cell_pos
            
            if x == 0 or x == grd_w - 1:
                cls.__draw_paint((grd_w, y), extend=2)
                cls.__draw_paint((-1, y), extend=1)

            if y == 0 or y == grd_h - 1:
                cls.__draw_paint((x, grd_h), extend=4)
                cls.__draw_paint((x, -1), extend=3)

    @classmethod
    def __draw_paint(cls, cell_pos: tuple, extend: int=0):
        '''Draw paint in the cell with the given position.
        The position doesn't have to be on the grid - paint off the grid
        is used to indicate you can't go to the opposite side.
        
        The extend argument indicates a direction in which the paint
        should extend to the edge of the window, used for the off-grid paint.
        0 : normal, 1 : left, 2 : right,
        3 : top, 4 : bottom.
        Any value other than 0 means a more faded red will be used.'''

        # Calculate pixel position of the cell
        pixel_x, pixel_y = cls.topleft_for(cell_pos)
        x_dimens = y_dimens = cls.get_cell_dimens_no_line()

        # Alter colour, position and dimensions based on
        # any specified extention to the edge of the window.
        if extend == 0:
            colour = cls.__PAINT_COL
        else:
            # Get window dimensions
            win_w, win_h = cls._window_dimensions
            colour = cls.__WRAP_PAINT_COL
            if extend == 1:
                x_dimens += pixel_x
                pixel_x = 0
            elif extend == 2:
                x_dimens = (win_w - pixel_x)
            elif extend == 3:
                y_dimens += pixel_y
                pixel_y = 0
            elif extend == 4:
                y_dimens = (win_h - pixel_y)

        # Draw a filled square
        pg.draw.rect(cls._window, colour,
                    (pixel_x, pixel_y, x_dimens, y_dimens))
        
    @classmethod
    def __draw_line(cls, start: tuple, end: tuple, faded: bool=False):
        '''Private method used to shorten the call to pg.draw.line().
        Faded argument indicates the faded colour used for the lines
        that indicate the ability to wrap around from one edge to the other.'''
        col = faded and cls.__WRAP_LINE_COL or cls.__LINE_COL
        pg.draw.line(cls._window, col, start, end, width=cls.__LINE_SIZE)

    @classmethod
    def topleft_for(cls, cell_pos: tuple):
        '''Return the pixel position of the top left corner
        of the cell at the given grid position.
        Called in draw() and also PainterVisual.draw()'''
        x, y = cell_pos
        # Add line size to go over the cell border, and subtract 1 because
        # coordinates start from 0,0
        return (cls.__left_edge + cls.__cell_dimens * x + cls.__LINE_SIZE - 1,
                cls.__top_edge + cls.__cell_dimens * y + cls.__LINE_SIZE - 1)
    
    @classmethod
    def get_cell_dimens_no_line(cls):
        '''Return the dimension of a cell minus the pixels used for the line.'''
        return cls.__cell_dimens - cls.__LINE_SIZE