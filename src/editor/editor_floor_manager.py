import os
import yaml
from ..floor_manager import FloorManager
from ..file_utility import FileUtility
from .floor_data import FloorData

class EditorFloorManager(FloorManager):
    @classmethod
    def create_floorpack(cls, name: str):
        '''Create a YAML file in the resources/floors directory with the given name,
        containing an empty list.
        Store an empty floorpack by that name, and select it as the current one.
        Raises FileExistsError if there is already a floorpack with that name.'''

        floorpack_dir = FileUtility.path_to_resource_directory('floors')
        path_for_pack = os.path.normpath(floorpack_dir + os.sep + name + '.yaml')

        if os.path.exists(path_for_pack):
            # Equivalent check: if name in cls.get_floorpack_names().
            # This is more foolproof however.
            raise FileExistsError
        
        # Save an empty list to the file.
        # (If the file were completely empty, it would need a special case)
        with open(path_for_pack, 'x') as file:
            yaml.dump([], file)

        cls._floor_packs[name] = []
        cls.select_floorpack(name)

    @classmethod
    def create_floor(cls):
        '''Create a 3x3 floor where the painter starts at 0,0.
        Insert it at the end of the current floorpack,
        and select it.'''
        floor = FloorData(3,3)
        floor.set_initial_painter_position((0,0))
        pack = cls._floor_packs[cls._current_pack_id]
        pack.append(floor)
        cls.select_floor(len(pack) - 1)

    @classmethod
    def __move_floor(cls, from_index: int, to_index: int):
        '''Move the floor at the given index in the pack to a different index.'''
        pack = cls._floor_packs[cls._current_pack_id]
        floor = pack.pop(from_index)
        pack.insert(to_index, floor)

    @classmethod
    def select_floor_to_edit(cls, index: int):
        '''Select a floor index as the current one being edited.
        Its data will be returned by get_floor_being_edited(), and
        after being changed, that data can be passed to edit_floor()
        to put it at this index.'''
        cls.__floor_index_being_edited = index
    
    @classmethod
    def get_floor_being_edited(cls):
        '''Return the floor data at the index previously passed to select_floor_to_edit().'''
        pack = cls._floor_packs[cls._current_pack_id]
        return pack[cls.__floor_index_being_edited]
    
    @classmethod
    def edit_floor(cls, floor_data_obj):
        '''Store the given FloorData object at the index
        previously chosen by select_floor_to_edit().
        Does not actually write the floor data to the floorpack file:
        call save_floorpack() to do that.'''
        cls._floor_packs[cls._current_pack_id][cls.__floor_index_being_edited] = floor_data_obj

    @classmethod
    def select_floor_to_move(cls, index: int):
        '''Store a floor index for later use by move_selected_floor().
        Assumes the index is in the pack.'''
        cls.__floor_index_to_move = index
    
    @classmethod
    def get_floor_index_being_moved(cls):
        return cls.__floor_index_to_move
    
    @classmethod
    def move_selected_floor(cls, to_index: int):
        '''Move the floor at the index previously given to select_floor_to_move()
        to the other index given.'''
        cls.__move_floor(cls.__floor_index_to_move, to_index)

    @classmethod
    def select_floor_to_delete(cls, index: int):
        '''Store a floor index for later use by delete_selected_floor().
        Assumes the index is in the pack.'''
        cls.__floor_index_to_delete = index
    
    @classmethod
    def delete_selected_floor(cls):
        del cls._floor_packs[cls._current_pack_id][cls.__floor_index_to_delete]

    @classmethod
    def save_floorpack(cls):
        '''Save the current floorpack into a YAML file in the resources/floors directory.
        Does not check whether the file exists or not, though,
        in order to have selected the floorpack, the file must exist.'''

        floorpack_dir = FileUtility.path_to_resource_directory('floors')
        pack_path = os.path.normpath(floorpack_dir + os.sep + cls._current_pack_id + '.yaml')

        pack = cls._floor_packs[cls._current_pack_id]
        with open(pack_path, 'w') as file:
            yaml.dump(pack, file)
