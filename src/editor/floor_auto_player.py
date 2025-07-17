from ..game.floor_player import FloorPlayer
from copy import deepcopy

class FloorAutoPlayer(FloorPlayer):

    # A score is given to each move, equal to the number of other moves it prevents.
    # The best score is 1, since we paint somewhere hard to reach while still being able to move on.
    # A score of 2, 3, or 4 has lower priority, and a score of 0 means we've nowhere to go, so it's impossible.
    __SCORE_PRIORITY = (1,2,3,4)
    __MAX_COMPROMISE = len(__SCORE_PRIORITY) - 1

    @classmethod
    def is_possible(cls, floor_obj) -> bool:
        '''Return whether or not it is possible to clear the floor.
        True : possible, False : impossible'''
        cls.new_floor(deepcopy(floor_obj))

        # Compromise: the best score leads to an impossible situation,
        # so start from a later index of SCORE_PRIORITY.
        compromises = {cls._painter_pos : 0}
        # Index in the list of moves that we're currently trying.
        move_index = 0

        while not cls.floor_is_over():
            # Give a score to the possible moves. dict[score : list of moves].
            scored_moves = cls.__score(cls._painter_pos)
            if len(scored_moves) == 0: return False

            # Check down the priority from best score to worst.
            # Any scores with no moves will be skipped,
            # as well as good scores that we've already found
            # lead to an impossible situation.
            moves_with_best_score = None

            comprm = compromises[cls._painter_pos]
            #print (f'Checking scores from {cls.__SCORE_PRIORITY[compromise:]}')
            for index, score in enumerate(cls.__SCORE_PRIORITY[comprm:]):
                if score in scored_moves:
                    moves_with_best_score = scored_moves[score]
                    num_moves = len(moves_with_best_score)
                    compromise_on_deadend = index + 1
                    break
            
            #print (f'Moves: {moves_with_best_score}')
            if moves_with_best_score is None:
                # If moves_with_best_score is still None, this is a dead end.
                if move_index + 1 == num_moves:
                    # We tried every move with the best score.
                    # A new list of moves will be tried.
                    #print ('Trying new move list')
                    move_index = 0
                    if comprm == cls.__MAX_COMPROMISE:
                        # If we compromised as much as possible,
                        # then undo a move.
                        #print ('Undoing')
                        cls.undo()

                    else: compromises[cls._painter_pos] = compromise_on_deadend
                
                # If there's still another move we can try with the same score,
                # no need to compromise yet. Try the next in the list.
                else:
                    #print ('Trying next move')
                    move_index += 1
                    
            else:
                # Move to the new position, and reset compromising parameters.
                move = moves_with_best_score[move_index]
                print (f'Moving: {cls._painter_pos} to {move}')
                #input()
                compromises[move] = 0
                cls.move_painter(move)
                move_index = 0

        return True

    @classmethod
    def __score(cls, pos: tuple[int]) -> dict[int:list]:

        moves = cls.__valid_moves_from(pos)
        num_further_moves = {
            move : len(cls.__valid_moves_from(move)) for move in moves
        }
        scored_moves = {
            score : [move for move in moves if num_further_moves[move] == score]
            for score in cls.__SCORE_PRIORITY
            }
        print (f'Possible: {moves}, Scored: {num_further_moves}, Grouped: {scored_moves}')
        scored_moves = {score : moves for score, moves in scored_moves.items() if moves}
        return scored_moves
    
    @classmethod
    def __valid_moves_from(cls, pos: tuple[int]=None) -> set:
        DIRECTIONS = {1,-1,2,-2}

        potential_moves = {
            cls.painter_position_after_move(direc, start_pos=pos)
            for direc in DIRECTIONS
        }

        possible_moves = set()
        for pos in potential_moves:
            if not cls._grid[pos].get_full():
                possible_moves.add(pos)
        
        return possible_moves