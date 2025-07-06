import pygame_gui as gui
from ..abstract_states import State, GameContentSelectState, StateWithGUI
from ..game.menu_visual import MenuVisual
from .editor_floor_manager import EditorFloorManager
from .editor_floorselect_input import EditFloorpacksControl, EditFloorsControl, MoveFloorControl, FloorDestinationControl, \
    SelectFloorToDeleteControl, ConfirmDeleteFloorControl
from .gui_visual import FloorpackCreateVisual
from .gui_handler import GUIHandler

class EditFloorpacksState(GameContentSelectState):
    _TITLE = 'Select Floor Pack'
    __CREATE_OPTION = 'Create New'

    @classmethod
    def enter(cls):
        '''Create a menu with the floorpack names, plus a 'Create Floorpack' option.'''
        # TODO: make this method generic in a parent. Maybe for the ingame floor select too.
        # FLOOR_MANAGER and INPUT_HANDLER_CLASS and OTHER_OPTIONS can be class constants.
        packnames = EditorFloorManager.get_floorpack_names()
        options = packnames + [cls.__CREATE_OPTION]
        cls._setup_menu_visual(options)
        cls._menu_input_handler = EditFloorpacksControl(cls._menu_visual, cls.__CREATE_OPTION)

class EditFloorsState(GameContentSelectState):
    _TITLE = 'Select Floor To Edit'
    __CREATE_OPTION = 'Create New'
    __MOVE_OPTION = 'Re-order'
    __DELETE_OPTION = 'Delete'
    __BACK_OPTION = 'Back'

    @classmethod
    def enter(cls):
        '''Create a menu with the floors, plus a back option, and the options to
        create a new floor or move an existing one.'''
        floornames = EditorFloorManager.get_floor_names()

        options = floornames + [cls.__CREATE_OPTION, cls.__MOVE_OPTION, cls.__DELETE_OPTION, cls.__BACK_OPTION]
        cls._setup_menu_visual(options)
        cls._menu_input_handler = EditFloorsControl(
            cls._menu_visual, cls.__CREATE_OPTION, cls.__MOVE_OPTION, cls.__DELETE_OPTION, cls.__BACK_OPTION)
        
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

class SelectFloorToDeleteState(GameContentSelectState):
    _TITLE = 'Select Floor To Delete'
    __BACK_OPTION = 'Cancel'

    @classmethod
    def enter(cls):
        floornames = EditorFloorManager.get_floor_names()
        options = floornames + [cls.__BACK_OPTION]
        cls._setup_menu_visual(options)
        cls._menu_input_handler = SelectFloorToDeleteControl(cls._menu_visual, cls.__BACK_OPTION)

class ConfirmDeleteFloorState(State):
    __TITLE = 'Are you sure?'
    __OPTION_NAMES = ['Confirm', 'Cancel']
    _INPUT_HANDLER = ConfirmDeleteFloorControl
    __visual_handlers = None
    
    @classmethod
    def get_visual_handlers(cls):
        if cls.__visual_handlers is None:
            cls.__visual_handlers = (MenuVisual(cls.__TITLE, cls.__OPTION_NAMES),)
        return cls.__visual_handlers

class CreateFloorpackState(StateWithGUI):
    _VISUAL_HANDLERS = (FloorpackCreateVisual,)

    __FIELD_ID = 'new_packname'

    @classmethod
    def enter(cls):
        FloorpackCreateVisual.init(cls.__FIELD_ID)

    @classmethod
    def process_bespoke_input(cls, event):
        match event.type:
            case gui.UI_BUTTON_PRESSED:
                '''Proof of concept for multiple buttons. Use form submit event.
                if GUIHandler.id_for(event.ui_element) == "Create":
                    packname = GUIHandler.
                '''
                return 'EditFloorpacksState'
            case gui.UI_FORM_SUBMITTED:
                packname = event.ui_element.get_current_values()[cls.__FIELD_ID]
                EditorFloorManager.create_floorpack(packname)
                return 'EditFloorpacksState'