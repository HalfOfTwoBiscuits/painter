from .visual_handler_base import VisualHandler
from .floor_visual import FloorVisual
from .sound import SFXPlayer
import pygame as pg

class PainterVisual(VisualHandler):
    __COL = pg.Color(255, 60, 60)
    __PADDING_FRACTION = 8
    __SHAKE_FRACTION = 3
    __ARROWHEAD = [
        pg.math.Vector2(1,0),
        pg.math.Vector2(2,3),
        pg.math.Vector2(1,2),
        pg.math.Vector2(0,3)
    ]
    __ARROWHEAD_CENTRE = pg.math.Vector2(1,1.5)
    __SHAKE_PERFRAME = 6

    #__DEBUG_LINE_COLS = (pg.Color(0,0,255), pg.Color(0,255,0), pg.Color(255,255,0), pg.Color(0,255,255))

    @classmethod
    def go_to(cls, pos: tuple, dir: int=-2):
        '''Change the cell the painter graphic is shown in
        and the direction that it faces.
        
        1 : Right, -1 : Left
        2 : Down, -2 : Up
        
        If the direction is not given, up is the default.'''
        cls.__position = pos
        cls.__direction = dir

    @classmethod
    def new_floor(cls, floor_obj, cell_dimens):
        cls.go_to(floor_obj.get_initial_painter_position())
        cls.initialise_shakevfx_state()
        cls.new_cell_dimens(cell_dimens)

    @classmethod
    def shake(cls):
        '''Cause the painter graphic to shake from side to side
        in the next few frames, indicating that an action isn't possible.'''
        if cls.__shake_increment == 0:
            cls.__shake_increment = cls.__SHAKE_PERFRAME

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

        if cls.__current_shake_amount >= cls.__max_shake_offset:
            # Reached maximum positive offset, so go the other way
            cls.__shake_increment = -cls.__SHAKE_PERFRAME
        elif cls.__current_shake_amount <= -cls.__max_shake_offset:
            # Reached maximum negative offset, so back to the centre
            cls.__shake_increment = cls.__SHAKE_PERFRAME
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

        # Offset into the cell based on current direction facing
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
        vertices = cls.__find_vertices(centre_x, centre_y, cls.__direction)

        # Draw
        pg.draw.polygon(cls._window, cls.__COL, vertices)

    @classmethod
    def new_cell_dimens(cls, cell_dimens: int):
        '''Set up visual parameters
        based on the dimension of a cell on the new floor.'''

        # Use a fraction of the space available as padding.
        cls.__padding = cell_dimens // cls.__PADDING_FRACTION
        cls.__max_shake_offset = cls.__padding // cls.__SHAKE_FRACTION
        # Subtract padding to find the space available.
        graphic_dimens = cell_dimens - cls.__padding * 2
        # Find offset into the cell
        cls.__offset = cell_dimens // 2

        # Divide the space available by the greatest magnitude
        # used in the scaled-down arrowhead shape, to calculate
        # a scale multiplier that makes the vectors fill the space.
        cls.__scale = graphic_dimens / max(
            [vector.magnitude() for vector in cls.__ARROWHEAD])
            
    
    @classmethod
    def __find_vertices(cls, x: int, y: int, direction: int):
        '''Return position vectors for the vertices of an
        arrowhead shape centred at the given x,y position
        using the stored scale factor, facing in the stored direction.
        Called in draw().'''

        # Facing up by default,
        # find how many degrees to rotate
        # based on the direction integer:
        # 1 : Right, -1 : Left
        # 2 : Down, -2 : Up
        degrees_to_rotate = 0

        if direction > -2:
            if direction == -1: rotations = 3
            else: rotations = direction

            # Multiply by 90 degrees for quarter rotations
            degrees_to_rotate = 90 * rotations

        def rotated_and_scaled(vector):
            new_vector = pg.Vector2(vector)
            new_vector.rotate_ip(degrees_to_rotate)
            new_vector.scale_to_length(vector.magnitude() * cls.__scale)
            return new_vector

        #print (f'With direction {direction}, rotation {degrees_to_rotate}, and position {x},{y}')

        # Create a vector used to offset the shape to the centre of the cell
        offset_vector = pg.Vector2(x,y)
        # Subtract the vector that leads from the top left to centre of the arrowhead
        offset_vector = offset_vector - rotated_and_scaled(cls.__ARROWHEAD_CENTRE)

        # Rotate, scale, and offset the shape to create position vectors for vertices
        vertices = []
        for vector in cls.__ARROWHEAD:
            new_vector = rotated_and_scaled(vector)
            new_vector += offset_vector
            vertices.append(new_vector)
            #print ('Becomes: ', str(new_vector))

        return vertices