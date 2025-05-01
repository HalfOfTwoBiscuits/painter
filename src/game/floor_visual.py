from .visual_handler_base import VisualHandler
import pygame as pg

class FloorVisual(VisualHandler):
    __LINE_SIZE = 3
    __LINE_COL = pg.Color(0,0,0)
    __PAINT_COL = pg.Color(150,30,30)

    @classmethod
    def new_floor(cls, floor_obj):
        '''Set up graphical parameters used to draw the grid for a floor.
        Called once when the floor starts.'''

        # Retrieve size of grid (in cells)
        # and dimensions of the game window (in pixels)
        cls.__grid = floor_obj.get_cell_grid()
        grid_w, grid_h = cls.__grid.get_size()
        win_w, win_h = cls._window_dimensions

        # Calculate width and height taken up by lines between cells
        all_lines_w = cls.__LINE_SIZE * grid_w
        all_lines_h = cls.__LINE_SIZE * grid_h
        # Calculate dimension of a cell in pixels.
        # Base it on whichever of width or height is the limiting factor
        cls.__cell_dimens = min(win_w // grid_w - all_lines_w,
                                  win_h // grid_h - all_lines_h)
        
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
        # Draw vertical lines
        for x in range(cls.__left_edge, cls.__right_edge + 1,
                       cls.__cell_dimens):
            
            pg.draw.line(cls._window, cls.__LINE_COL,
                         x, cls.__top_edge,
                         width=cls.__LINE_SIZE)
        
        # Draw horizontal lines
        for y in range(cls.__top_edge, cls.__bottom_edge + 1,
                       cls.__cell_dimens):
            
            pg.draw.line(cls._window, cls.__LINE_COL,
                         cls.__left_edge, y,
                         width=cls.__LINE_SIZE)
        
        # Fill in the painted cells
        for pos in cls.__grid.get_full_cell_positions():
            # Calculate pixel position of the cell
            x, y = cls.__topleft_for(pos)
            # Draw a filled square
            pg.draw.rect(cls._window, cls.__PAINT_COL,
                         (x, y, cls.__cell_dimens, cls.__cell_dimens))

    @classmethod
    def topleft_for(cls, cell_pos: tuple):
        '''Return the pixel position of the top left corner
        of the cell at the given grid position.
        Called in draw() and also PainterVisual.draw()'''
        x, y = cell_pos
        return (cls.__left_edge + cls.__cell_dimens * x,
                cls.__top_edge + cls.__cell_dimens * y)
    
    @classmethod
    def get_cell_dimens(cls):
        '''Return the dimension of a cell.
        Called in FloorFactory.__start_floor'''
        return cls.__cell_dimens