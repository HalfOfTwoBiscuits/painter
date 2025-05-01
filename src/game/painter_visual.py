from .visual_handler_base import VisualHandler
from .floor_visual import FloorVisual
from .sound import SFXPlayer
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
    def initialise_shakevfx_state(cls):
        '''Set the attributes that track the shaking vfx
        to their initial values. Called when starting a floor.'''
        cls.__shake_increment = 0
        cls.__current_shake_amount = 0
        cls.__stopping_shake = False

    @classmethod
    def __update_shake_effect(cls):
        '''Update the stored values used for the shaking effect
        to respond to the passing of a frame.'''
        cls.__current_shake_amount += cls.__shake_increment

        if cls.__current_shake_amount == cls.__padding:
            # Reached maximum positive offset, so go the other way
            cls.__shake_increment = -1
        elif cls.__current_shake_amount == -cls.__padding:
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

        # Find centre of the cell
        centre_x = topleft_x + cls.__offset
        centre_y = topleft_y + cls.__offset

        cls.__update_shake_effect()
        
        # If the shake effect is in progress, offset from the centre.
        if cls.__shake_increment != 0:
            if abs(cls.__direction) == 1:
                # Facing horizontal, so vertical offset
                centre_y += cls.__current_shake_amount
            else:
                # Facing vertical, so horizontal offset
                centre_x += cls.__current_shake_amount

        # Find the vertices of the arrowhead shape,
        # accounting for the direction the painter is facing.
        vertices = cls.__find_vertices(centre_x, centre_y)

        # Draw
        pg.draw.polygon(cls._window, cls.__COL, vertices)

    @classmethod
    def new_cell_dimens(cls, cell_dimens: int):
        '''Set up visual parameters
        based on the dimension of a cell on the new floor.'''

        # Calculate x/y offset from topleft to the centre of a cell.
        cls.__offset = cell_dimens // 2

        # Use a fraction of the space available as padding.
        cls.__padding = cell_dimens // cls.__PADDING_FRACTION
        # Subtract padding to find the space available.
        graphic_dimens = cell_dimens - cls.__padding * 2

        # Divide the space available by the greatest magnitude
        # used in the scaled-down arrowhead shape, to calculate
        # a scale multiplier that makes the vectors fill the space.
        cls.__scale = graphic_dimens / max(
            [vector.magnitude() for vector in cls.__ARROWHEAD])
    
    @classmethod
    def __find_vertices(cls, x: int, y: int):
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
        
        # Create a vector used to offset the shape to the centre (of the cell)
        offset_vector = pg.Vector2(x,y)

        # Rotate, scale, and offset the shape to create position vectors for vertices
        vertices = []
        for vector in cls.__ARROWHEAD:
            vector.rotate(degrees_to_rotate)
            vector.scale_to_length(vector.magnitude() * cls.__scale)
            vector += offset_vector
            vertices.append(vector)

        return vertices