import pygame as pg
import pygame_gui as gui

from ..abstract_handlers import KeyboardInputHandler
from ..audio_utility import SFXPlayer

from ..game.floor_visual import FloorVisual
from ..game.painter_visual import PainterVisual

from .autofloor_visual import AutoFloorVisual
from .cursor_visual import CursorVisual
from .gui_visual import EditorButtonsVisual
from .editor_floor_manager import EditorFloorManager

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
        pg.K_RIGHT : ('move_cursor',1),
        pg.K_LEFT : ('move_cursor',-1),
        pg.K_DOWN : ('move_cursor',2),
        pg.K_UP : ('move_cursor',-2),
        pg.K_1 : ('paint',),
        pg.K_2 : ('move_painter',),
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
                        # Left clicks toggle whether the cell starts painted.
                        cls.paint(cell_pos)
                    case 3:
                        # Right clicks set the painter's initial position.
                        cls.move_painter(cell_pos)
                EditorButtonsVisual.set_savebutton_text(just_saved=False)
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
        EditorButtonsVisual.set_savebutton_text(just_saved=True)

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

    @classmethod
    def move_cursor(cls, direction: int):
        CursorVisual.move_cursor(direction)
    
    @classmethod
    def paint(cls, cell_pos: tuple=None):
        cell_pos = cell_pos or CursorVisual.get_pos()
        if cell_pos is not None:
            cell = cls.__grid[cell_pos]
            if cell.get_full():
                # Unpaint cell
                SFXPlayer.play_sfx('back')
                cell.revert()
            elif cls.__grid.get_num_empty_cells() > 2 and \
            cell_pos != cls.__floor.get_initial_painter_position():
                    # Paint cell
                    SFXPlayer.play_sfx('move')
                    cell.start_filled()
            else: SFXPlayer.play_sfx('invalid')

    @classmethod
    def move_painter(cls, cell_pos: tuple=None):
        cell_pos = cell_pos or CursorVisual.get_pos()
        if cell_pos is not None:
            SFXPlayer.play_sfx('start')
            PainterVisual.go_to(cell_pos)
            cls.__floor.set_initial_painter_position(cell_pos)