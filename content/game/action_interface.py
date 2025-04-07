class LevelPlayInterface:
    '''Interface for the Painter's interactions with the level.'''
    def __init__(self, level_obj):
        self.__painter_pos = level_obj.get_initial_painter_position()
        self.__grid = level_obj.get_cell_grid()
        self.__position_history = [self.__painter_pos] # Series of positions occupied

    def move_painter(self, direction: int):
        '''Move the painter one cell.

        The direction argument indicates a direction to move.
        1 : Right, -1 : Left
        2 : Down, -2 : Up
        
        Returns a boolean for whether the move worked.
        True : moved, False : blocked by wet paint'''

        # Calculate new position of the painter after moving
        x, y = self.__painter_pos

        if abs(direction) == 1: x += direction
        else: y += direction // 2

        new_pos = (x,y)

        try:
            # Paint the new position.
            # This means a cell will be full when you stand on it.
            # In-story, the painter doesn't stand on the wet paint.
            # Options:
            # - show painter over square contents
            # - paint the old position, not the new one
            # I prefer the first option.
            cell = self.__grid[new_pos]
            cell.paint()
        except ValueError:
            # The move is not possible.
            # The PainterCharacter class does a SFX/animation/effect.
            return False
        else:
            # Move painter, add to position history, and end.
            self.__painter_pos = new_pos
            self.__position_history.append(new_pos)
            return True

    def undo(self):
        '''Undo the painter's last move.

        Returns a boolean for whether the undo worked.
        True : Move was undone, False : No moves to undo'''
        if len(self.__position_history) == 1: return False

        cur_pos = self.__position_history.pop()
        prev_pos = self.__position_history[-1]

        cur_cell = self.__grid[cur_pos]
        cur_cell.revert()
        self.__painter_pos = prev_pos

        return True

    def undo_all(self):
        '''Undo all the painter's moves.
        
        Returns a boolean for whether the undo worked.
        True : All moves undone, False : No moves to undo

        May not be used.
        '''
        
        # Attempt to undo once.
        has_moved = self.undo()

        if has_moved:
            # If the painter moved, repeatedly call undo()
            # until all moves are undone. 
            while self.undo(): pass
            return True
        else:
            return False