from .floor_data import FloorData # Temporary, this will actually be imported by the level editor

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
        '''Return the next floor in the floorpack.
        Called after completing a floor.
        Assumes the floorpack is not over.'''
        
        # Get next floor
        floorpack = cls.__floor_packs[cls.__current_pack_id]
        floor = floorpack[cls.__next_floor_index]
        
        # Increment progression index
        cls.__next_floor_index += 1
        return floor
    
    @classmethod
    def get_floorpack_names(cls):
        '''Return a list of the names of floorpacks.
        They can then be options in floorpack selection.'''
        return [name for name in cls.__floor_packs.keys()]
    
    @classmethod
    def select_floorpack(cls, pack_name: str):
        '''Floors will be chosen from the floorpack with this name.'''
        cls.__current_pack_id = pack_name
    
    @classmethod
    def get_floor_names(cls):
        '''Return a list of the names of levels in the current floorpack:
        'Floor 1', 'Floor 2', and so on, to be picked from in the level select menu.'''
        floorpack = cls.__floor_packs[cls.__current_pack_id]
        return [f'Floor {index + 1}' for index in range(len(floorpack))]
    
    @classmethod
    def select_floor(cls, floor_index: int):
        '''Start playing floors from this index in the current floorpack,
        setting progression to start from that floor for future next_floor() calls.'''
        cls.__next_floor_index = floor_index