from copy import deepcopy

from ..abstract_states import State, GameContentSelectState
from ..game.menu_visual import MenuVisual
from ..game.painter_visual import PainterVisual
from ..game.floor_visual import FloorVisual
from ..game.floor_player import FloorPlayer
from .editor_floor_manager import EditorFloorManager
from .gui_handler import GUIHandler
from .editor_floorselect_input import EditFloorpacksControl, EditFloorsControl, MoveFloorControl, FloorDestinationControl, \
    SelectFloorToDeleteControl, ConfirmDeleteFloorControl
from .gui_visual import FloorpackCreateVisual, EditorButtonsVisual, ResizeMenuVisual
from .edit_input import EditControl
from .gui_input import FloorpackCreateControl, ResizeFloorControl
from .autofloor_visual import AutoFloorVisual
from .cursor_visual import CursorVisual
from .playtest_handlers import PlaytestControl, ReturnToEditorButtonVisual

class EditFloorpacksState(GameContentSelectState):
    _TITLE = 'Select Pack To Edit'
    __CREATE_OPTION = 'Create New'
    __EXIT_OPTION = 'Exit Editor'

    @classmethod
    def enter(cls):
        '''Create a menu with the floorpack names, plus a 'Create Floorpack' option.'''
        # TODO: make this method generic in a parent. Maybe for the ingame floor select too.
        # FLOOR_MANAGER and INPUT_HANDLER_CLASS and OTHER_OPTIONS can be class constants.
        packnames = EditorFloorManager.get_floorpack_names()
        options = packnames + [cls.__CREATE_OPTION, cls.__EXIT_OPTION]
        cls._setup_menu_visual(options)
        cls._menu_input_handler = EditFloorpacksControl(cls._menu_visual, cls.__CREATE_OPTION, cls.__EXIT_OPTION)

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
    __BACK_OPTION = 'Move A Different Floor'
    __CANCEL_OPTION = "Don't Move Floors"

    @classmethod
    def enter(cls):
        floornames = EditorFloorManager.get_floor_names()
        num_moving = EditorFloorManager.get_floor_index_being_moved() + 1
        title = f'Select Destination for Floor {num_moving}'
        menu_options = ['Start'] + \
            [f'After Floor {num}' for num in range(1, len(floornames) + 1) if num != num_moving] \
            + [cls.__BACK_OPTION, cls.__CANCEL_OPTION]

        cls._menu_visual = MenuVisual(title, menu_options, option_ids=floornames)
        cls._menu_input_handler = FloorDestinationControl(cls._menu_visual, cls.__BACK_OPTION, cls.__CANCEL_OPTION)

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

class CreateFloorpackState(State):
    _VISUAL_HANDLERS = (FloorpackCreateVisual,)
    _INPUT_HANDLER = FloorpackCreateControl

    __FIELD_ID = 'New_Floorpack_Name'
    __CANCEL_ID = 'Cancel'
    __SUBMIT_ID = 'Create'

    @classmethod
    def enter(cls):
        FloorpackCreateVisual.init(cls.__FIELD_ID, cls.__CANCEL_ID, cls.__SUBMIT_ID)
        FloorpackCreateControl.init(cls.__FIELD_ID, cls.__CANCEL_ID, cls.__SUBMIT_ID)
            
class EditState(State):
    _INPUT_HANDLER = EditControl
    _VISUAL_HANDLERS = (FloorVisual, PainterVisual, EditorButtonsVisual, AutoFloorVisual, CursorVisual)
    # (R) (T) (S) (E) ?
    __RESIZE_ID = 'Resize'
    __TEST_ID = 'Test'
    __SAVE_ID = 'Save'
    __SAVED_TEXT = 'Floor saved!'
    __EXIT_ID = 'Exit'

    @classmethod
    def enter(cls):
        EditorButtonsVisual.init(cls.__RESIZE_ID, cls.__SAVE_ID, cls.__EXIT_ID, cls.__TEST_ID, cls.__SAVED_TEXT)
        EditControl.init(cls.__RESIZE_ID, cls.__SAVE_ID, cls.__EXIT_ID, cls.__TEST_ID)
        CursorVisual.init(EditorFloorManager.get_floor_being_edited())

class ResizeFloorState(State):
    _VISUAL_HANDLERS = (FloorVisual, PainterVisual, ResizeMenuVisual)
    _INPUT_HANDLER = ResizeFloorControl
    __WIDTH_FIELD_ID = 'Width'
    __HEIGHT_FIELD_ID = 'Height'
    __CANCEL_ID = 'Cancel'
    __SUBMIT_ID = 'Resize'

    @classmethod
    def enter(cls):
        ResizeMenuVisual.init(cls.__WIDTH_FIELD_ID, cls.__HEIGHT_FIELD_ID, cls.__CANCEL_ID, cls.__SUBMIT_ID)
        ResizeFloorControl.init(cls.__WIDTH_FIELD_ID, cls.__HEIGHT_FIELD_ID, cls.__CANCEL_ID, cls.__SUBMIT_ID)

class FloorPlaytestState(State):
    _INPUT_HANDLER = PlaytestControl
    _VISUAL_HANDLERS = (FloorVisual, PainterVisual, ReturnToEditorButtonVisual)

    @staticmethod
    def enter():
        GUIHandler.clear_elements()
        floor = deepcopy(EditorFloorManager.get_floor_being_edited())
        FloorVisual.new_floor(floor)
        FloorPlayer.new_floor(floor)
        cell_dimens = FloorVisual.get_cell_dimens_no_line()
        PainterVisual.new_floor(floor, cell_dimens)