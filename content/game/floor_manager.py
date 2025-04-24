from floor_data import FloorData
from floor_visual import FloorVisual
from floor_player import FloorPlayer
from painter_visual import PainterVisual

class FloorManager:
    '''Class responsible for creating and storing floor data.'''

    # Data for floors (levels)
    __floor_packs = {}
    # String ID of the current list of floors
    __current_pack_id = ''
    # Index of the floor to play next
    __next_floor_index = 0

    @classmethod
    def load_floors(cls):
        '''Create a dummy floor to play,
        put it in a floor pack and set that pack as the current one.
        This is a temporary solution.'''

        floor = FloorData(4,3) # 4x3 level
        floor.set_initial_painter_position((0,1))

        # Some cells start filled
        cells = floor.get_cell_grid()
        cells[(0,2)].start_filled()
        cells[(2,1)].start_filled()

        # Add it to a floorpack and select that pack.
        # Floor pack selecting won't be in the first prototype.
        cls.__floor_packs['DUMMY'] = [floor]
        cls.select_floorpack('DUMMY')
    
    @classmethod
    def floorpack_is_over(cls):
        '''Return a boolean indicating whether the floorpack is over.
        True : All floors clear, False : Moving on to the next floor'''
        floorpack = cls.__floor_packs[cls.__current_pack_id]
        return cls.__next_floor_index < len(floorpack)
    
    @classmethod
    def next_floor(cls):
        '''Go on to the next floor in the floorpack.
        Called for the first floor at the start, as well.
        Assumes the floorpack is not over.'''
        
        # Get next floor
        floorpack = cls.__floor_packs[cls.__current_pack_id]
        floor = floorpack[cls.__next_floor_index]

        # Start
        cls.__start_floor(floor)
        
        # Increment progression index
        cls.__next_floor_index += 1
        
    @classmethod
    def __start_floor(cls, floor_obj):
        '''Update program state to account for the new floor.'''

        # Set up the new floor graphic.
        FloorVisual.new_floor(floor_obj)
        # Set up painter control logic to interact with the new floor.
        FloorPlayer.new_floor(floor_obj)

        # Set visual parameters of the painter graphic based on
        # the dimension of a cell on the new floor.
        cell_dimens = FloorVisual.get_cell_dimens()
        PainterVisual.new_cell_dimens(cell_dimens)

        # Put the painter graphic at the initial position.
        painter_pos = floor_obj.get_initial_painter_position()
        PainterVisual.go_to(painter_pos)

        # Initialise the shaking vfx
        # (if the painter was shaking when the last floor ended, this will stop it)
        PainterVisual.initialise_shakevfx_state()

    @classmethod
    def select_floorpack(cls, pack_name: str):
        '''Floors will be chosen from this floorpack.
        Sets up behaviour for next_floor()'''
        cls.__current_pack_id = pack_name

    @classmethod
    def select_floor(cls, floor_index: int):
        '''Set up the program to start playing the current floor pack
        starting from the floor with the given index.
        Not used yet.'''

        cls.__next_floor_index = floor_index
        cls.next_floor()