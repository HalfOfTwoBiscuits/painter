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
        # (If the file was empty, it would need a special case)
        with open(path_for_pack, 'x') as file:
            yaml.dump([], file)

        cls._floor_packs[name] = []
        cls.select_floorpack(name)

    @classmethod
    def create_floor(cls):
        '''Create a 3x3 floor where the painter starts at 0,0
        and insert it at the end of the current floorpack.'''
        floor = FloorData(0,0)
        floor.set_initial_painter_position((0,0))
        pack = cls._floor_packs[cls._current_pack_id]
        pack.append(floor)

    @classmethod
    def move_floor(cls, from_index: int, to_index: int):
        '''Move the floor at the given index in the pack to a different index.
        By the behaviour of list.pop(),
        will raise IndexError if from_index is outside the pack.'''
        pack = cls._floor_packs[cls._current_pack_id]
        floor = pack.pop(from_index)
        pack.insert(to_index, floor)

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
