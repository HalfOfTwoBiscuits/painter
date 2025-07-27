import pygame_gui as gui
import pygame as pg

from ..abstract_handlers import KeyboardInputHandler
from ..audio_utility import SFXPlayer
from ..game.floor_visual import FloorVisual
from ..game.painter_visual import PainterVisual
from .editor_floor_manager import EditorFloorManager
from .autofloor_visual import AutoFloorVisual
from .gui_handler import GUIHandler

class EditControl(KeyboardInputHandler):
    _ACTIONS = {
        pg.K_RETURN : ('save',),
        pg.K_s : ('save',),
        pg.K_t : ('playtest',),
        pg.K_r : ('resize',),
        pg.K_e : ('exit',),
        pg.K_ESCAPE : ('exit',),
        pg.K_BACKSPACE : ('exit',),
        pg.K_a : ('toggle_autosolve',),
    }

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
                return cls.resize()
            elif event.ui_object_id.endswith(cls.__TEST_ID):
                return cls.playtest()
            elif event.ui_object_id.endswith(cls.__SAVE_ID):
                cls.save()
            elif event.ui_object_id.endswith(cls.__EXIT_ID):
                return cls.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            # Get mouse click position, size of grid, and dimension of a cell.
            mouse_x, mouse_y = event.pos
            cell_pos = FloorVisual.get_coordinates_of_cell_clicked(mouse_x, mouse_y)

            if cell_pos is None:
                # If it wasn't, it might have been a click
                # on the solution indicator to toggle solution count.
                rect = AutoFloorVisual.get_toggle_rect()
                if rect.collidepoint(mouse_x, mouse_y): cls.toggle_autosolve()
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
        else:
            return cls._process_keyboard_input(cls, event)

    @classmethod
    def resize(cls):
        # Store current changes to the floor,
        # so ResizeFloorState can access the right FloorData object.
        EditorFloorManager.edit_floor(cls.__floor)
        return 'ResizeFloorState'
    
    @classmethod
    def playtest(cls):
        SFXPlayer.play_sfx('start')
        return 'FloorPlaytestState'
    
    @classmethod
    def save(cls):
        SFXPlayer.play_sfx('start')
        EditorFloorManager.edit_floor(cls.__floor)
        EditorFloorManager.save_floorpack()

    @classmethod
    def exit(cls):
        SFXPlayer.play_sfx('back')
        if cls.__changes_made:
            # Unused currently. __changes_made is never set.
            return 'ConfirmExitState'
        else: 
            return 'EditFloorsState'
        
    @classmethod
    def toggle_autosolve(cls):
        AutoFloorVisual.toggle_solution_count(cls.__floor)

class FloorpackCreateControl(KeyboardInputHandler):
    _ACTIONS = {
        pg.K_RETURN : ('submit',),
        pg.K_ESCAPE : ('back',),
        pg.K_BACKSPACE : ('back_if_unfocussed',),
        pg.K_UP : ('focus',),
        pg.K_DOWN : ('focus',),
        pg.K_TAB : ('focus',),
    }

    @classmethod
    def init(cls, FIELD_ID: str, CANCEL_ID: str, SUBMIT_ID: str):
        cls.__FIELD_ID = FIELD_ID
        cls.__CANCEL_ID = CANCEL_ID
        cls.__SUBMIT_ID = SUBMIT_ID
        cls.focus()

    @staticmethod
    def process_input(cls, event):
        match event.type:
            case gui.UI_BUTTON_PRESSED:
                id = event.ui_object_id
                if id.endswith(cls.__CANCEL_ID):
                    return cls.back()
                elif id.endswith(cls.__SUBMIT_ID):
                    return cls.submit()
            case _:
                return cls._process_keyboard_input(cls, event)
    
    @staticmethod
    def back():
        print ('Back')
        SFXPlayer.play_sfx('back')
        return 'EditFloorpacksState'
    
    @classmethod
    def submit(cls):
        print ('Submit')
        # Get pack name from the form
        field = GUIHandler.get_elem(cls.__FIELD_ID)
        packname = field.get_text()
        EditorFloorManager.create_floorpack(packname)

        SFXPlayer.play_sfx('start')
        return 'EditState'
    
    @classmethod
    def focus(cls):
        print ('Focus')
        GUIHandler.set_focus(cls.__FIELD_ID)

    @classmethod
    def back_if_unfocussed(cls):
        if not GUIHandler.get_elem(cls.__FIELD_ID).is_focused:
            return cls.back()
    
class ResizeFloorControl(KeyboardInputHandler):
    _ACTIONS = {
        pg.K_RETURN : ('submit',),
        pg.K_ESCAPE : ('back',),
        pg.K_BACKSPACE : ('back_if_unfocussed',),
        pg.K_UP : ('focus',),
        pg.K_DOWN : ('focus',),
        pg.K_TAB : ('focus',),
    }

    @classmethod
    def init(cls, WIDTH_FIELD_ID: str, HEIGHT_FIELD_ID: str, CANCEL_ID: str, SUBMIT_ID: str):
        cls.__WIDTH_FIELD_ID = WIDTH_FIELD_ID
        cls.__HEIGHT_FIELD_ID = HEIGHT_FIELD_ID
        cls.__CANCEL_ID = CANCEL_ID
        cls.__SUBMIT_ID = SUBMIT_ID
    
    @staticmethod
    def process_input(cls, event):
        match event.type:
            case gui.UI_BUTTON_PRESSED:
                id = event.ui_object_id
                if id.endswith(cls.__CANCEL_ID):
                    return cls.back()
                elif id.endswith(cls.__SUBMIT_ID):
                    return cls.submit()
            case _:
                return cls._process_keyboard_input(cls, event)
            
    @staticmethod
    def back():
        SFXPlayer.play_sfx('back')
        return 'EditState'
    
    @staticmethod
    def __retrieve_from_field(field_id: str) -> int | None:
        field = GUIHandler.get_elem(field_id)
        contents = field.get_text()
        try: contents = int(contents)
        except ValueError: return None
        return contents

    @classmethod
    def submit(cls):
        SFXPlayer.play_sfx('destroy')

        # Get new width and height from the form
        new_width = cls.__retrieve_from_field(cls.__WIDTH_FIELD_ID)
        new_height = cls.__retrieve_from_field(cls.__HEIGHT_FIELD_ID)

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
    
    @classmethod
    def focus(cls):
        if GUIHandler.get_elem(cls.__WIDTH_FIELD_ID).is_focused:
            GUIHandler.set_focus(cls.__HEIGHT_FIELD_ID)
        else: GUIHandler.set_focus(cls.__WIDTH_FIELD_ID)

    @classmethod
    def back_if_unfocussed(cls):
        if not (GUIHandler.get_elem(cls.__WIDTH_FIELD_ID).is_focused
                or GUIHandler.get_elem(cls.__HEIGHT_FIELD_ID).is_focused):
            return cls.back()