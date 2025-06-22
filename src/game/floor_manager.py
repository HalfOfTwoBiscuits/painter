from ..file_utility import FileUtility
import copy
import os
import yaml

# FloorData is not used here: the floors to paint are created beforehand.
# But it must be imported somewhere in the main project for pyinstaller to detect it exists,
# so that when we load the floor yaml in the built version of the project,
# floor_data.py is included in the build.
# It's imported in this file because the floor yaml is loaded in this file.
from ..editor.floor_data import FloorData

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
        '''Iterate through the yaml files in the resources/floors directory,
        deserialising a list of FloorData objects from each.
        These 'floorpacks' will be stored so they can be played later.

        Currently only one floorpack will be used due to the input handler
        for floor pack selection, and the editor program to create floorpacks,
        not being done yet.'''

        floorpack_dir = FileUtility.path_to_resource_directory('floors')
        # Iterate over files in the directory
        # (this will also load floorpack files in subdirectories,
        # though this is not used)
        for rootpath, _, filenames in os.walk(floorpack_dir):

            for fname in filenames:
                # Join directory and fname to find the path
                path = os.path.join(rootpath, fname)
                # Load floorpack file
                with open(path) as file:
                    floorpack = yaml.load(file, Loader=yaml.Loader)
                
                # Retrieve fname without extention: the floorpack ID used as a key
                floorpack_id = fname[:fname.index('.')]
                cls.__floor_packs[floorpack_id] = floorpack
    
    @classmethod
    def floorpack_is_over(cls):
        '''Return a boolean indicating whether the floorpack is over.
        True : All floors clear, False : Moving on to the next floor'''
        floorpack = cls.__floor_packs[cls.__current_pack_id]
        return cls.__next_floor_index == len(floorpack)
    
    @classmethod
    def next_floor(cls):
        '''Return the next floor in the floorpack.
        Called after completing a floor.
        Assumes the floorpack is not over.'''
        
        # Get next floor
        floorpack = cls.__floor_packs[cls.__current_pack_id]
        print (f'Moving onto {cls.__next_floor_index + 1} of {len(floorpack)}')
        floor = floorpack[cls.__next_floor_index]
        
        # Increment progression index
        cls.__next_floor_index += 1
        return copy.deepcopy(floor)
    
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

    @staticmethod
    def index_from_floor_name(floor_name: str):
        '''Given the name for a floor returned from get_floor_names(),
        return the index of that floor in the floorpack.'''
        
        # As dictated by get_floor_names(),
        # the last character in the string is the floor number.
        # Cast to an integer and subtract 1 to find the index of the floor.
        return int(floor_name[-1]) - 1