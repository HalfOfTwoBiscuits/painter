class FloorData:
    '''Class representing a level. A level consists of a grid of cells
    and an initial position for the painter.'''

    def __init__(self, cell_width: int, cell_height: int):
        self.__grid = CellGrid(cell_width, cell_height)
        self.__initial_painter_position = (0,0)

    def get_initial_painter_position(self):
        return self.__initial_painter_position

    def set_initial_painter_position(self, new_pos):
        self.__grid.ensure_valid_position(new_pos)
        # Painter position doesn't start filled.
        # If this could be called more than once, also need to unfill previous
        cell = self.__grid[new_pos]
        cell.want_fill()
        self.__initial_painter_position = new_pos

    def get_cell_grid(self):
        return self.__grid

class CellGrid:
    '''Class representing a grid of cells, the main part of a level.
    Instances may be indexed to get the cell at a position.'''

    def __init__(self, width: int, height: int):
        self.__w = width
        self.__h = height
        self.__cells = {}

    def ensure_valid_position(self, pos: tuple):
        '''Ensure a tuple represents a position in this cell grid.
        It must contain two integers, the x and y coordinates.
        The coordinates must be within the grid's width and height.
        If these conditions are not met then raise an exception.'''

        try:
            x, y = pos
            x = int(x)
            y = int(y)
        except (ValueError, TypeError):
            raise TypeError (
                f'Cell position {pos} must be a tuple of two integers!')

        if x < 0 or x >= self.__w or y < 0 or y >= self.__h:
            raise ValueError(
                f'Cell position {pos} must be within ({self.__w},{self.__h})!')

    def __getitem__(self, pos: tuple):
        '''Return the cell object at the given position.
        When a position is accessed for the first time,
        the cell object will be created before returning it.
        Raise an exception if the position is not within the level.'''

        self.__ensure_valid_position(pos)

        if pos in self.__cells:
            return self.__cells[pos]

        new_cell = Cell()
        self.__cells[pos] = new_cell
        return new_cell

class Cell:
    '''Class representing a cell that can be blank or coloured in.
    The goal of a level is to colour all cells.'''

    def __init__(self):
        self.__filled = False

    def paint(self):
        '''Set cell to be full.
        Called during play, when moving.
        Raises ValueError if the cell is full already'''
        if self.__filled: raise ValueError
        self.__filled = True
        return True

    def revert(self):
        '''Set cell to be blank.
        Called during play, when undoing.'''
        self.__filled = False

    def start_filled(self):
        '''Set cell to start filled in.
        Called during level setup.'''
        self.__filled = True