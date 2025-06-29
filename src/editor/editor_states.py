from ..abstract_states import State, GameContentSelectState
from ..game.menu_visual import MenuVisual
from .editor_floor_manager import EditorFloorManager
from .editor_floorselect_input import EditFloorpacksControl, EditFloorsControl, MoveFloorControl, FloorDestinationControl

class EditFloorpacksState(GameContentSelectState):
    _TITLE = 'Select Floor Pack'
    __CREATE_OPTION = 'Create New'

    @classmethod
    def enter(cls):
        '''Create a menu with the floorpack names, plus a 'Create Floorpack' option.'''
        packnames = EditorFloorManager.get_floorpack_names()
        
        options = packnames + [cls.__CREATE_OPTION]
        cls._setup_menu_visual(options)
        cls._menu_input_handler = EditFloorpacksControl(cls._menu_visual, cls.__CREATE_OPTION)

class EditFloorsState(GameContentSelectState):
    _TITLE = 'Select Floor To Edit'
    __CREATE_OPTION = 'Create New'
    __MOVE_OPTION = 'Re-order'
    __BACK_OPTION = 'Another Floorpack'

    @classmethod
    def enter(cls):
        '''Create a menu with the floors, plus a back option, and the options to
        create a new floor or move an existing one.'''
        floornames = EditorFloorManager.get_floor_names()

        options = floornames + [cls.__CREATE_OPTION, cls.__MOVE_OPTION, cls.__BACK_OPTION]
        cls._setup_menu_visual(options)
        cls._menu_input_handler = EditFloorsControl(
            cls._menu_visual, cls.__CREATE_OPTION, cls.__MOVE_OPTION, cls.__BACK_OPTION)
        
class SelectFloorToMoveState(GameContentSelectState):
    _TITLE = 'Select Floor To Move'
    __BACK_OPTION = 'Cancel'

    @classmethod
    def enter(cls):
        floornames = EditorFloorManager.get_floor_names()

        options = floornames + [cls.__BACK_OPTION]
        cls._setup_menu_visual(options)
        cls._menu_input_handler = MoveFloorControl(cls._menu_visual, cls.__BACK_OPTION)

class SelectFloorDestinationState(GameContentSelectState):
    _TITLE = 'Select Destination'
    __BACK_OPTION = 'Cancel'

    @classmethod
    def enter(cls):
        floornames = EditorFloorManager.get_floor_names()
        menu_options = ['Start'] + \
            [f'Between {num} and {num + 1}' for num in range(1, len(floornames))] + \
            ['End'] + [cls.__BACK_OPTION]

        cls._menu_visual = MenuVisual(cls._TITLE, menu_options, option_ids=floornames)
        cls._menu_input_handler = FloorDestinationControl(cls._menu_visual, cls.__BACK_OPTION)