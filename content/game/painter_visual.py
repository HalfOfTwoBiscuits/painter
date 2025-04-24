from visual_handler_base import VisualHandler
from floor_visual import FloorVisual
from sound import SFXPlayer
import pygame as pg

class PainterVisual(VisualHandler):
    __COL = pg.Color(255, 60, 60)
    __PADDING_FRACTION = 8
    __ARROWHEAD = (
        pg.math.Vector2(1,3),
        pg.math.Vector2(-1,-1),
        pg.math.Vector2(-1,1),
        pg.math.Vector2(1,-3)
    )

    __shake_increment = 0
    __current_shake_amount = 0
    __stopping_shake = False

    @classmethod
    def go_to(cls, pos: tuple, dir: int=-2):
        '''Change the cell the painter graphic is shown in
        and the direction that it faces.'''
        cls.__position = pos
        cls.__direction = dir

    @classmethod
    def shake(cls):
        '''Cause the painter graphic to shake from side to side
        in the next few frames, indicating that an action isn't possible.'''
        if cls.__shake_increment == 0:
            cls.__shake_increment = 1

    @classmethod
    def __update_shake_effect(cls, padding: int):
        '''Update the stored values used for the shaking effect
        to respond to the passing of a frame.'''
        cls.__current_shake_amount += cls.__shake_increment

        if cls.__current_shake_amount == padding:
            # Reached maximum positive offset, so go the other way
            cls.__shake_increment = -1
        elif cls.__current_shake_amount == -padding:
            # Reached maximum negative offset, so back to the centre
            cls.__shake_increment = 1
            cls.__stopping_shake = True
        elif cls.__current_shake_amount == 0 and cls.__stopping_shake:
            # Got back to the centre after reaching max negative,
            # so stop the effect.
            cls.__shake_increment = 0
            cls.__stopping_shake = False

    @classmethod
    def draw(cls):
        '''Draw the painter onscreen.
        The painter appears as an arrowhead shape in a cell.'''

        # Get the pixel position of the cell,
        # and dimension of a cell to use for scaling.
        topleft_x, topleft_y = FloorVisual.topleft_for(cls.__position)
        cell_dimens = FloorVisual.get_cell_dimens()

        # Find centre of the cell
        centre_x = topleft_x + cell_dimens // 2
        centre_y = topleft_y + cell_dimens // 2

        # Use a fraction of the space available as padding:
        # subtract the space used on padding from the cell dimension.
        padding = cell_dimens // cls.__PADDING_FRACTION
        dimens = cell_dimens - padding * 2

        cls.__update_shake_effect(padding)
        
        # If the shake effect is in progress, offset from the centre.
        if abs(cls.__direction) == 1:
            # Facing horizontal, so vertical offset
            centre_y += cls.__current_shake_amount
        else:
            # Facing vertical, so horizontal offset
            centre_x += cls.__current_shake_amount

        # Find the vertices of the arrowhead shape,
        # accounting for the direction the painter is facing.
        vertices = cls.__find_vertices(centre_x, centre_y, dimens)

        # Draw
        pg.draw.polygon(cls._window, cls.__COL, vertices)

    # TODO: When LevelSelectState transitions to GameplayState,
    # calculate the __offset once, set shake data, and go_to initial_painter_position
    
    @classmethod
    def __find_vertices(cls, x: int, y: int, space: int):
        '''Return position vectors for the vertices of an
        arrowhead shape centred at the given x,y position
        using the given space, facing in the stored direction.
        Called in draw().'''

        # Facing up by default,
        # find how many degrees to rotate
        # based on the direction integer:
        # 1 : Right, -1 : Left
        # 2 : Down, -2 : Up
        degrees_to_rotate = 0

        if cls.__direction > -2:
            if cls.__direction == -1: rotations = 3
            else: rotations = cls.__direction

            # Multiply by 90 degrees for quarter rotations
            degrees_to_rotate = 90 * rotations

        # Divide the space available by the greatest
        # magnitude used in the scaled-down arrowhead shape,
        # to calculate a scale multiplier that will fill the space.
        scale = space / max(
            [vector.magnitude() for vector in cls.__ARROWHEAD])
        
        # Create a vector used to offset the shape to the centre (of the cell)
        offset_vector = pg.Vector2(x,y)

        # Rotate, scale, and offset the shape to create position vectors for vertices
        vertices = []
        for vector in cls.__ARROWHEAD:
            vector.rotate(degrees_to_rotate)
            vector.scale_to_length(vector.magnitude() * scale)
            vector += offset_vector
            vertices.append(vector)

        return vertices