class FloorPlayer:
    '''Interface for the Painter's interactions with the level.'''

    @classmethod
    def setup(cls, level_obj):
        cls.__painter_pos = level_obj.get_initial_painter_position()
        cls.__grid = level_obj.get_cell_grid()
        cls.__position_history = [cls.__painter_pos] # Series of positions occupied

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
            # Paint the old position.
            cell = cls.__grid[cls.__painter_pos]
            cell.paint()
        except ValueError:
            # The move is not possible.
            # The PainterVisual class does a SFX/animation/effect.
            return False
        else:
            # Move painter, add to position history, and end.
            cls.__painter_pos = new_pos
            cls.__position_history.append(new_pos)
            return True
        
    @classmethod
    def undo(cls):
        '''Undo the painter's last move.

        If the undo worked, return the painter's new position.
        Tuple : Move was undone, None : No moves to undo'''
        if len(cls.__position_history) == 1: return None

        cur_pos = cls.__position_history.pop()
        prev_pos = cls.__position_history[-1]

        cur_cell = cls.__grid[cur_pos]
        cur_cell.revert()
        cls.__painter_pos = prev_pos

        return prev_pos
    
    @classmethod
    def undo_all(cls):
        '''Undo all the painter's moves.
        
        If the undo worked, return the painter's initial position.
        Tuple : All moves undone, False : No moves to undo

        May not be used.
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