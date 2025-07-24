import pygame_gui as gui
import pygame as pg

from ..abstract_handlers import InputHandler
from ..audio_utility import SFXPlayer
from ..game.floor_visual import FloorVisual
from ..game.painter_visual import PainterVisual
from .editor_floor_manager import EditorFloorManager
from .autofloor_visual import AutoFloorVisual

class EditControl(InputHandler):

    @classmethod
    def init(cls, RESIZE_ID: str, SAVE_ID: str, EXIT_ID: str, TEST_ID: str):
        cls.__floor = EditorFloorManager.get_floor_being_edited()
        cls.__grid = cls.__floor.get_cell_grid()
        FloorVisual.new_floor(cls.__floor, editor=True)
        cell_dimens = FloorVisual.get_cell_dimens_no_line()
        PainterVisual.new_floor(cls.__floor, cell_dimens)
        cls.__changes_made = False

        cls.__RESIZE_ID = RESIZE_ID
        cls.__TEST_ID = TEST_ID
        cls.__SAVE_ID = SAVE_ID
        cls.__EXIT_ID = EXIT_ID

    @staticmethod
    def process_input(cls, event):
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
            cell_pos = FloorVisual.get_coordinates_of_cell_clicked(mouse_x, mouse_y)

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

class FloorpackCreateControl(InputHandler):
    @classmethod
    def init(cls, FIELD_ID: str, CANCEL_ID: str):
        cls.__FIELD_ID = FIELD_ID
        cls.__CANCEL_ID = CANCEL_ID

    @staticmethod
    def process_input(cls, event):
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
            
class ResizeFloorControl(InputHandler):
    @classmethod
    def init(cls, WIDTH_FIELD_ID: str, HEIGHT_FIELD_ID: str, CANCEL_ID: str):
        cls.__WIDTH_FIELD_ID = WIDTH_FIELD_ID
        cls.__HEIGHT_FIELD_ID = HEIGHT_FIELD_ID
        cls.__CANCEL_ID = CANCEL_ID
    
    @staticmethod
    def process_input(cls, event):
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
                AutoFloorVisual.update(floor)
                return 'EditState'