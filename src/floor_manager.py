import yaml
from copy import deepcopy
from os import walk
from .file_utility import FileUtility

# FloorData is not used here: the floors to paint are created beforehand.
# But it must be imported somewhere in the main project for pyinstaller to detect it exists,
# so that when we load the floor yaml in the built version of the project,
# floor_data.py is included in the build.
# It's imported in this file because the floor yaml is loaded in this file.
from .editor.floor_data import FloorData

class FloorManager:
    '''Class responsible for creating and storing floor data.'''

    # Data for floors (levels)
    _floor_packs = {}
    # String ID of the current list of floors
    _current_pack_id = ''
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
        for rootpath, _, filenames in walk(floorpack_dir):

            for fname in filenames:
                # Join directory and fname to find the path.
                # Call resolve() to ensure it is absolute,
                # and as_posix() for compatibility with pygbag.
                path = (floorpack_dir / fname).resolve().as_posix()
                # Load floorpack file
                cls._load_floorpack(path, fname)
    
    @classmethod
    def _load_floorpack(cls, path, fname: str=None) -> str:
        '''Load the floorpack at the given path into memory.
        The filename can be passed if it is already known,
        otherwise it is derived from the path.
        Returns the ID of the new pack, which is the filename
        without extention.
        
        Called in load_floors() and EditorFloorManager.upload_floorpack().'''

        with open(path) as file:
            floorpack = yaml.load(file, Loader=yaml.Loader)
        
        if fname is None: fname = path.name
        # Retrieve fname without extention: the floorpack ID used as a key
        floorpack_id = fname[:fname.index('.')]
        cls._floor_packs[floorpack_id] = floorpack
        return floorpack_id

    @classmethod
    def floorpack_is_over(cls):
        '''Return a boolean indicating whether the floorpack is over.
        True : All floors clear, False : Moving on to the next floor'''
        floorpack = cls._floor_packs[cls._current_pack_id]
        return cls.__next_floor_index == len(floorpack)
    
    @classmethod
    def next_floor(cls):
        '''Return the next floor in the floorpack.
        Called after completing a floor.
        Assumes the floorpack is not over.'''
        
        # Get next floor
        floorpack = cls._floor_packs[cls._current_pack_id]
        print (f'Moving onto {cls.__next_floor_index + 1} of {len(floorpack)}')
        floor = floorpack[cls.__next_floor_index]
        
        # Increment progression index
        cls.__next_floor_index += 1
        return deepcopy(floor)
    
    @classmethod
    def get_floorpack_names(cls):
        '''Return a list of the names of floorpacks.
        They can then be options in floorpack selection.'''
        return [name for name in cls._floor_packs.keys()]
    
    @classmethod
    def get_num_floorpacks(cls):
        '''Return the number of floorpacks.'''
        return len(cls._floor_packs)
    
    @classmethod
    def select_floorpack(cls, pack_name: str):
        '''Floors will be chosen from the floorpack with this name.'''
        cls._current_pack_id = pack_name
    
    @classmethod
    def get_floor_names(cls):
        '''Return a list of the names of levels in the current floorpack:
        'Floor 1', 'Floor 2', and so on, to be picked from in the level select menu.'''
        floorpack = cls._floor_packs[cls._current_pack_id]
        return [f'Floor {index + 1}' for index in range(len(floorpack))]
    
    @classmethod
    def get_num_floors(cls):
        '''Return the number of floors in the current pack.'''
        floorpack = cls._floor_packs[cls._current_pack_id]
        return len(floorpack)
    
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