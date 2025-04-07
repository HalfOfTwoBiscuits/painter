import pickle

class Level:
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
    Some cells want to be coloured in, and the others want to be blank.
    The goal of a level is to satisfy all wants.'''

    def __init__(self):
        self.__filled = False
        self.__wants_fill = False

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

    def want_fill(self):
        '''Set cell as wanting to be filled in.
        Called during level setup.'''
        self.__wants_fill = True

    def start_filled(self):
        '''Set cell to start filled in.
        Called during level setup.
        Since a cell that starts full cannot be unfilled,
        also set it to want to be full
        (otherwise the level would be impossible)'''
        self.__filled = True
        self.__wants_fill = True

class LevelPlayInterface:
    '''Interface for the Painter's interactions with the level.'''
    def __init__(self, level_obj):
        self.__painter_pos = level_obj.get_initial_painter_position()
        self.__grid = level_obj.get_cell_grid()
        self.__position_history = [self.__painter_pos]

    def move_painter(self, direction: int):
        '''Move the painter one cell.
        The direction argument indicates a direction to move.
        1 : Right, -1 : Left
        2 : Down, -2 : Up'''

        x, y = self.__painter_pos

        if abs(direction) == 1: x += direction
        else: y += direction // 2

        # Alternate (arbitrary dimensions): pos = list(self.__painter_pos)
        # axis = abs(direction)
        # pos[axis - 1] += direction // axis

        new_pos = (x,y)

        try:
            # This means a cell will be full when you stand on it.
            # Options: show painter over square contents, no wet paint under
            # Change this to paint the one behind: have to move one further
            # in order to paint the last one in the image.
            # Could there be a goal to end on?
            cell = self.__grid[new_pos]
            cell.paint()
        except ValueError:
            pass
            # Move is not possible.
            # SFX/animation/effect goes here.
        else:
            self.__painter_position = new_pos
            self.__position_history.append(new_pos)

    def undo(self):
        '''Undo a movement'''
        if len(self.__position_history) == 1: return True

        cur_pos = self.__position_history.pop()
        prev_pos = self.__position_history[-1]

        cur_cell = self.__grid[cur_pos]
        cur_cell.revert()
        self.__painter_pos = prev_pos


    def undo_all(self):
        while self.undo() is None: pass
