from .visual_handler_base import VisualHandler
from .floor_visual import FloorVisual
from .sound import SFXPlayer
import pygame as pg

class PainterVisual(VisualHandler):
    __COL = pg.Color(255, 60, 60)
    __PADDING_FRACTION = 8
    '''
    __ARROWHEAD = [
        pg.math.Vector2(1,3),
        pg.math.Vector2(-1,-1),
        pg.math.Vector2(-1,1),
        pg.math.Vector2(1,-3)
    ]
    '''
    __ARROWHEAD = [
        pg.math.Vector2(1,0),
        pg.math.Vector2(2,3),
        pg.math.Vector2(1,2),
        pg.math.Vector2(0,3)
    ]
    __DEBUG_LINE_COLS = (pg.Color(0,0,255), pg.Color(0,255,0), pg.Color(255,255,0), pg.Color(0,255,255))

    @classmethod
    def go_to(cls, pos: tuple, dir: int=-2):
        '''Change the cell the painter graphic is shown in
        and the direction that it faces.
        
        1 : Right, -1 : Left
        2 : Down, -2 : Up'''
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

        # Offset into the cell based on current direction facing
        offsets = cls.__pixel_offsets[cls.__direction]
        centre_x = topleft_x + offsets[0]
        centre_y = topleft_y + offsets[1]

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

        '''
        print ('Output:', [str(v) for v in vertices])
        print ('Inputs:', centre_x, centre_y, '')
        pg.draw.line(cls._window, cls.__DEBUG_LINE_COLS[0], vertices[0], vertices[1], width=5)
        pg.draw.line(cls._window, cls.__COL, vertices[1], vertices[2], width=5)
        for i,c in enumerate(cls.__DEBUG_LINE_COLS):
            if i == len(vertices) - 1: i2 = -1
            else: i2 = i + 1
            pg.draw.line(cls._window, c, vertices[i], vertices[i2], width=5)
        '''

    @classmethod
    def new_cell_dimens(cls, cell_dimens: int):
        '''Set up visual parameters
        based on the dimension of a cell on the new floor.'''

        # Use a fraction of the space available as padding.
        cls.__padding = cell_dimens // cls.__PADDING_FRACTION
        # Subtract padding to find the space available.
        cls.__graphic_dimens = cell_dimens - cls.__padding * 2

        # Divide the space available by the greatest magnitude
        # used in the scaled-down arrowhead shape, to calculate
        # a scale multiplier that makes the vectors fill the space.
        cls.__scale = cls.__graphic_dimens / max(
            [vector.magnitude() for vector in cls.__ARROWHEAD])
        
        cls.__pixel_offsets = {}
        for direction in (1,2):
            vertices = cls.__find_vertices(0,0,direction)
            x_positions, y_positions = [v.x for v in vertices], [v.y for v in vertices]

            offset = cls.__graphic_dimens - abs(max(x_positions) - min(x_positions)),\
                cls.__graphic_dimens - abs(max(y_positions) - min(y_positions))

            cls.__pixel_offsets[direction] = offset
            cls.__pixel_offsets[-direction] = offset
            
    
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
        
        print (f'With direction {direction}, rotation {degrees_to_rotate}, and position {x},{y}')
        # Create a vector used to offset the shape to the centre (of the cell)
        offset_vector = pg.Vector2(x,y)

        # Rotate, scale, and offset the shape to create position vectors for vertices
        vertices = []
        for vector in cls.__ARROWHEAD:
            new_vector = pg.Vector2(vector)
            print ('The abstract: ', str(vector))
            new_vector.rotate_ip(degrees_to_rotate)
            new_vector.scale_to_length(vector.magnitude() * cls.__scale)
            new_vector += offset_vector
            vertices.append(new_vector)
            print ('Becomes: ', str(new_vector))

        return vertices