import yaml
from copy import deepcopy
from os import walk
from .file_utility import FileUtility
from .error_report import ErrorReportVisual
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
        
        If any floorpacks are invalid, call ErrorReportVisual.set_message_from_invalid_packs()
        to prepare an error message with the names of the invalid packs, and raise TypeError.
        Valid floorpacks will still be loaded.'''
        invalid_floorpack_names = []

        floorpack_dir = FileUtility.path_to_resource_directory('floors')
        # Iterate over files in the directory
        # (this will also load floorpack files in subdirectories,
        # though this is not used)
        for rootpath, _, filenames in walk(floorpack_dir):

            for fname in filenames:
                # Join directory and fname to find the path.
                path = (floorpack_dir / fname)
                # Load floorpack file
                try:
                    cls._load_floorpack(path, fname)
                except TypeError:
                    invalid_floorpack_names.append(fname)
        if len(invalid_floorpack_names) > 0:
            ErrorReportVisual.set_message_from_invalid_packs(invalid_floorpack_names)
            raise TypeError
    
    @classmethod
    def _load_floorpack(cls, path, fname: str=None, floorpack_id: str=None):
        '''Load the floorpack at the given pathlib.Path into memory.
        It will be saved with the given ID.
        
        If the ID is not passed, the ID will be the filename without extention.
        If the filename is not given it will be derived from the path.
        (This is significant because when uploading, the path is different to the original filename)

        If the file doesn't contain a floorpack, raise TypeError.
        
        Called in load_floors() and EditorFloorManager.upload_floorpack().'''

        # Call resolve() to ensure it is absolute,
        # and as_posix() for compatibility with pygbag.
        path = path.resolve()
        posix_path = path.as_posix()

        try:
            with open(posix_path) as file:
                floorpack = yaml.load(file, Loader=yaml.Loader)
        except Exception:
            raise TypeError

        # Check the pack is a list of FloorData
        if not isinstance(floorpack, list) or not all([isinstance(floor, FloorData) for floor in floorpack]):
            raise TypeError
        
        if floorpack_id is None:
            if fname is None: floorpack_id = path.name
            else: floorpack_id = cls.get_packname(fname)

        cls._floor_packs[floorpack_id] = floorpack

    @classmethod
    def get_packname(cls, filename: str):
        '''Retrieve fname without extention: the floorpack ID used as a key'''
        return filename[:filename.index('.')]
    
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