import pygame as pg
import pygame_gui as gui
from copy import deepcopy
from ..abstract_states import State, GameContentSelectState, StateWithBespokeInput
from ..audio_utility import SFXPlayer
from ..game.menu_visual import MenuVisual
from ..game.painter_visual import PainterVisual
from ..game.floor_visual import FloorVisual
from ..game.floor_player import FloorPlayer
from .editor_floor_manager import EditorFloorManager
from .gui_handler import GUIHandler
from .editor_floorselect_input import EditFloorpacksControl, EditFloorsControl, MoveFloorControl, FloorDestinationControl, \
    SelectFloorToDeleteControl, ConfirmDeleteFloorControl
from .gui_visual import FloorpackCreateVisual, EditorButtonsVisual, ResizeMenuVisual
from .autofloor_visual import AutoFloorVisual
from .test_floor_input import PlaytestControl

class EditFloorpacksState(GameContentSelectState):
    _TITLE = 'Select Floor Pack'
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

class CreateFloorpackState(StateWithBespokeInput):
    _VISUAL_HANDLERS = (FloorpackCreateVisual,)

    __FIELD_ID = 'New Floorpack Name'
    __CANCEL_ID = 'Cancel'

    @classmethod
    def enter(cls):
        FloorpackCreateVisual.init(cls.__FIELD_ID, cls.__CANCEL_ID)

    @classmethod
    def process_bespoke_input(cls, event):
        match event.type:
            case gui.UI_BUTTON_PRESSED:
                if event.ui_object_id.endswith(cls.__CANCEL_ID):
                    SFXPlayer.play_sfx('back')
                    return 'EditFloorpacksState'
            case gui.UI_FORM_SUBMITTED:
                packname = event.ui_element.get_current_values()[cls.__FIELD_ID]
                EditorFloorManager.create_floorpack(packname)
                SFXPlayer.play_sfx('start')
                return 'EditState'
            
class EditState(StateWithBespokeInput):
    _VISUAL_HANDLERS = (FloorVisual, PainterVisual, EditorButtonsVisual, AutoFloorVisual)
    __RESIZE_ID = 'Resize'
    __TEST_ID = 'Test'
    __SAVE_ID = 'Save'
    __EXIT_ID = 'Exit'
    @classmethod
    def enter(cls):
        EditorButtonsVisual.init(cls.__RESIZE_ID, cls.__SAVE_ID, cls.__EXIT_ID, cls.__TEST_ID)
        cls.__floor = EditorFloorManager.get_floor_being_edited()
        cls.__grid = cls.__floor.get_cell_grid()
        FloorVisual.new_floor(cls.__floor, editor=True)
        cell_dimens = FloorVisual.get_cell_dimens_no_line()
        PainterVisual.new_floor(cls.__floor, cell_dimens)
        cls.__changes_made = False
    
    @classmethod
    def process_bespoke_input(cls, event):
        if event.type == gui.UI_BUTTON_PRESSED:
            # On UI button press, resize floors, save, or exit.
            if event.ui_object_id.endswith(cls.__RESIZE_ID):
                # Store current changes to the floor,
                # so ResizeFloorState can access the right FloorData object.
                EditorFloorManager.edit_floor(cls.__floor)
                return 'ResizeFloorState'
            elif event.ui_object_id.endswith(cls.__TEST_ID):
                SFXPlayer.play_sfx('start')
                return 'FloorPlaytestState'
            elif event.ui_object_id.endswith(cls.__SAVE_ID):
                SFXPlayer.play_sfx('start')
                EditorFloorManager.edit_floor(cls.__floor)
                EditorFloorManager.save_floorpack()
            elif event.ui_object_id.endswith(cls.__EXIT_ID):
                if cls.__changes_made:
                    # Unused currently. __changes_made is never set.
                    return 'ConfirmExitState'
                else: 
                    return 'EditFloorsState'
        elif event.type == pg.MOUSEBUTTONDOWN:
            # Get mouse click position, size of grid, and dimension of a cell.
            mouse_x, mouse_y = event.pos
            cell_dimens = FloorVisual.get_cell_dimens_no_line()
            grid_w, grid_h = cls.__grid.get_size()
            cell_pos = None
            # Iterate through the grid, checking if the click is within a cell.
            for x in range(0, grid_w):
                for y in range(0, grid_h):
                    left_x, top_y = FloorVisual.topleft_for((x, y))
                    if left_x <= mouse_x <= left_x + cell_dimens and \
                    top_y <= mouse_y <= top_y + cell_dimens:
                        cell_pos = (x,y)
                        break

            if cell_pos is None:
                # If it wasn't, it might have been a click
                # on the solution indicator to toggle solution count.
                rect = AutoFloorVisual.get_toggle_rect()
                if rect.collidepoint(mouse_x, mouse_y): AutoFloorVisual.toggle_solution_count(cls.__floor)
            else:
                # If it was, then check whether it was a left or right click.
                match event.button:
                    case 1:
                        cell = cls.__grid[cell_pos]
                        # Left clicks toggle whether the cell starts painted.
                        if cell.get_full():
                            SFXPlayer.play_sfx('back')
                            cell.revert()
                        else:
                            if cell_pos == cls.__floor.get_initial_painter_position():
                                SFXPlayer.play_sfx('invalid')
                            else:
                                SFXPlayer.play_sfx('move')
                                cell.start_filled()
                    case 3:
                        # Right clicks set the painter's initial position.
                        # Initial cell cannot start painted.
                        SFXPlayer.play_sfx('start')
                        PainterVisual.go_to(cell_pos)
                        cls.__floor.set_initial_painter_position(cell_pos)
                AutoFloorVisual.update(cls.__floor)

class ResizeFloorState(StateWithBespokeInput):
    _VISUAL_HANDLERS = (FloorVisual, PainterVisual, ResizeMenuVisual)
    __WIDTH_FIELD_ID = 'Width'
    __HEIGHT_FIELD_ID = 'Height'
    __CANCEL_ID = 'Cancel'

    @classmethod
    def enter(cls):
        ResizeMenuVisual.init(cls.__WIDTH_FIELD_ID, cls.__HEIGHT_FIELD_ID, cls.__CANCEL_ID)

    @classmethod
    def process_bespoke_input(cls, event):
        match event.type:
            case gui.UI_BUTTON_PRESSED:
                # Cancel
                if event.ui_object_id.endswith(cls.__CANCEL_ID):
                    SFXPlayer.play_sfx('back')
                    return 'EditState'
            case gui.UI_FORM_SUBMITTED:
                SFXPlayer.play_sfx('destroy')

                # Get new width and height from the form
                data = event.ui_element.get_current_values()
                new_width = data[cls.__WIDTH_FIELD_ID]
                new_height = data[cls.__HEIGHT_FIELD_ID]

                # Change size of the current floor grid.
                floor = EditorFloorManager.get_floor_being_edited()
                floor.resize(new_width, new_height)
                FloorVisual.new_floor(floor, editor=True)
                cell_dimens = FloorVisual.get_cell_dimens_no_line()
                PainterVisual.new_floor(floor, cell_dimens)

                # Store changes and return to editing
                EditorFloorManager.edit_floor(floor)
                return 'EditState'
            
class FloorPlaytestState(State):
    _INPUT_HANDLER = PlaytestControl
    _VISUAL_HANDLERS = (FloorVisual, PainterVisual)

    @staticmethod
    def enter():
        GUIHandler.clear_elements()
        floor = deepcopy(EditorFloorManager.get_floor_being_edited())
        FloorVisual.new_floor(floor)
        FloorPlayer.new_floor(floor)
        cell_dimens = FloorVisual.get_cell_dimens_no_line()
        PainterVisual.new_floor(floor, cell_dimens)