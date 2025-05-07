class FloorPlayer:
    '''Interface for the Painter's interactions with the floor.'''

    @classmethod
    def new_floor(cls, floor_obj):
        '''Initialise the position of the painter, the cell grid to move on,
        and undo history.'''
        cls.__painter_pos = floor_obj.get_initial_painter_position()
        cls.__grid = floor_obj.get_cell_grid()
        cls.__position_history = [] # Series of positions occupied

    @classmethod
    def painter_position_after_move(cls, direction: int):
        '''The direction argument indicates a direction to move.
        1 : Right, -1 : Left
        2 : Down, -2 : Up
        
        Return the position the painter would be in after
        moving in that direction once.'''

        # Calculate new position of the painter after moving
        x, y = cls.__painter_pos

        if abs(direction) == 1: x += direction
        else: y += direction // 2

        return (x,y)
    
    @classmethod
    def move_painter(cls, new_pos: tuple):
        '''Move the painter to the new position.

        Returns a boolean for whether the move worked.
        True : moved, False : blocked by wet paint.'''

        try:
            # Raise ValueError if the position is not on the grid or is full.
            new_cell = cls.__grid[new_pos]
            if new_cell.get_full(): raise ValueError

            # Paint the old position.
            old_cell = cls.__grid[cls.__painter_pos]
            old_cell.paint()
        except ValueError:
            # The move is not possible.
            # The PainterVisual class does a SFX/animation/effect.
            return False
        else:
            # Move painter, add old position to history
            cls.__position_history.append(cls.__painter_pos)
            cls.__painter_pos = new_pos
            return True
        
    @classmethod
    def undo(cls):
        '''Undo the painter's last move.

        If the undo worked, return the painter's new position.
        Tuple : Move was undone, None : No moves to undo'''
        if len(cls.__position_history) == 0: return None

        prev_pos = cls.__position_history.pop()

        prev_cell = cls.__grid[prev_pos]
        prev_cell.revert()
        cls.__painter_pos = prev_pos

        return prev_pos
    
    @classmethod
    def undo_all(cls):
        '''Undo all the painter's moves.
        
        If the undo worked, return the painter's initial position.
        Tuple : All moves undone, False : No moves to undo
        '''
        
        # Attempt to undo once.
        has_moved = cls.undo()

        if has_moved:
            # If the painter moved, repeatedly call undo()
            # until all moves are undone. 
            while cls.undo(): pass
            return cls.__painter_pos
        else:
            return None
        
    @classmethod
    def floor_is_over(cls):
        '''Return a boolean for whether the floor is clear.
        True : Well done, move on, False : More to paint
        Delegates to CellGrid.__is_painted()'''
        return cls.__grid.is_painted()