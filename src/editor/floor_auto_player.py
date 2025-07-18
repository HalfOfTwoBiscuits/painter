from ..game.floor_player import FloorPlayer
from copy import deepcopy

class FloorAutoPlayer(FloorPlayer):

    @classmethod
    def is_possible(cls, floor_obj):
        print ('Call')
        cls.new_floor(deepcopy(floor_obj))

        successors = [] # Alternative moves not yet tried
        output = None # Boolean return value

        while output is None:
            print (cls._painter_pos, successors)
            if cls._grid.is_painted():
                output = True
            else:
                # List potential moves from here.
                moves = cls.__valid_moves_from(cls._painter_pos)
                if len(moves) > 0:
                    # Do an arbitrary move (the last).
                    new_pos = moves.pop()
                    cls.move_painter(new_pos)

                    # Store the alternative moves that were possible.
                    successors.append(moves)
                else:
                    # Find alternate move
                    undoing = True
                    while undoing:
                        # Undo
                        if cls.undo() is None:
                            # If nothing to undo, floor is impossible
                            output = False
                            undoing = False
                        else:
                            # Check for alternative moves
                            # in previous list.
                            if len(successors[-1]) == 0:
                                # No alternate move, undo again
                                del successors[-1]
                            else:
                                # Alternate move found, do it
                                new_pos = successors[-1].pop()
                                cls.move_painter(new_pos)
                                undoing = False
        print (output)
        return output

    @classmethod
    def __adjacents_to(cls, pos: tuple[int]=None) -> set:
        DIRECTIONS = {1,-1,2,-2}
        
        return {
            cls.painter_position_after_move(direc, start_pos=pos)
            for direc in DIRECTIONS
        }
    
    @classmethod
    def __empty_cells_only(cls, cell_positions: set[tuple[int]]):
        full_cell_positions = cls._grid.get_full_cell_positions()
        
        return {
            pos for pos in cell_positions
            if pos not in full_cell_positions
        }
    
    @classmethod
    def __valid_moves_from(cls, pos: tuple[int]=None):
        adjacents = cls.__adjacents_to(pos)
        return cls.__empty_cells_only(adjacents)
    
    @classmethod
    def __degree_of(cls, pos: tuple[int]=None):
        return len(cls.__valid_moves_from(pos))