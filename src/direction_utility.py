class DirectionUtility:
    @classmethod
    def pos_after_move(cls, x: int, y: int,
                       grid_w: int, grid_h: int, direction: int):
        '''Given an x, y position on a grid with the given width and height,
        and a direction indicated using an integer,
        return the new x, y position after moving in that direction.
        Will wrap round the grid if at the edges.
        Directions:
        1 : Right, -1 : Left,
        2 : Down, -2 : Up'''
        if abs(direction) == 1:
            x += direction
            x = cls.__loop_round(x, grid_w)
        else:
            y += direction // 2
            y = cls.__loop_round(y, grid_h)
        return (x,y)

    @staticmethod
    def __loop_round(co_ordinate: int, dimension: int):
        '''Given a x or y co-ordinate and the corresponding width or height of the grid,
        check if the co-ordinate is outside the grid and if so, loop round to the other side.
        Return the new co-ordinate.'''
        if co_ordinate >= dimension: co_ordinate = 0
        elif co_ordinate < 0: co_ordinate = dimension - 1
        return co_ordinate