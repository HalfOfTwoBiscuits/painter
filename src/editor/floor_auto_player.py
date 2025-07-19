from ..game.floor_player import FloorPlayer
from copy import deepcopy

class FloorAutoPlayer(FloorPlayer):
    # Maximums on number of empty cells.
    __USE_ONLY_HEURISTIC_ABOVE = 25
    __USE_HEURISTIC_ABOVE = 12
    __NO_SOLUTIONCOUNT_ABOVE = 18

    @classmethod
    def is_possible(cls, floor_obj) -> bool:
        '''Return whether it is possible to clear the floor, using depth-first traversal.
        If the floor has enough empty cells that this would be overly time-consuming, raise ValueError.'''
        empty_cells = floor_obj.get_cell_grid().get_num_empty_cells()
        if empty_cells > cls.__USE_ONLY_HEURISTIC_ABOVE:
            raise ValueError
        
        if empty_cells > cls.__USE_HEURISTIC_ABOVE:
            is_defo_possible = cls.is_possible_heuristic(floor_obj)
            if is_defo_possible: return True

        return cls.__traverse(floor_obj)
    
    @classmethod
    def num_solutions(cls, floor_obj) -> int:
        '''Return the number of solutions for the floor, using depth-first traversal.
        If the floor has enough empty cells that this would be overly time-consuming, raise ValueError.'''
        if floor_obj.get_cell_grid().get_num_empty_cells() > cls.__NO_SOLUTIONCOUNT_ABOVE:
            raise ValueError
        
        #print ('Counting solutions')
        return cls.__traverse(floor_obj, find_all_solutions=True)
    
    @classmethod
    def is_possible_heuristic(cls, floor_obj) -> bool | None:
        '''Return True if it is definitely possible to clear the floor,
        and None if it is uncertain whether it's possible or not.'''
        #print ('Checking heuristic')
        if cls.__is_possible_dirac(floor_obj): return True
        return None
    
    @classmethod
    def __is_possible_dirac(cls, floor_obj) -> bool:
        '''Return whether or not it is possible to clear the floor,
        using Dirac's Theorem.'''
        cls.new_floor(floor_obj)
        width, height = cls._grid.get_size()
        num_cells = (width * height)
        #if num_cells < 3: return True

        half_num_cells = num_cells // 2
        #print (f'Half number of cells: {half_num_cells}')

        for x in range(width):
            for y in range(height):
                degree = cls.__degree_of((x,y))
                #print (f'Degree of {x},{y} : {degree} {degree < half_num_cells}')
                if degree < half_num_cells:
                    return False
        return True

    @classmethod
    def __traverse(cls, floor_obj, find_all_solutions: bool=False) -> int | bool:
        cls.new_floor(deepcopy(floor_obj))

        successors = [] # Alternative moves not yet tried
        running = True
        if find_all_solutions: num_solutions = 0
        else: found_solution = False

        def reverse():
            output = None
            while output is None:
                # Undo
                if cls.undo() is None:
                    # If nothing to undo, floor is impossible
                    output = False
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
                        output = True
            return output

        while running:
            #print (cls._painter_pos, successors)
            if cls._grid.is_painted():
                # Solution found, look for alternative moves
                if find_all_solutions:
                    num_solutions += 1
                    running = reverse()
                else:
                    found_solution = True
                    running = False
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
                    running = reverse()
                    
        #print (output)
        return num_solutions if find_all_solutions else found_solution

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