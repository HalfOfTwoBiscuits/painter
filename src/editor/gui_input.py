import pygame_gui as gui
import pygame as pg

from ..abstract_handlers import KeyboardInputHandler
from ..audio_utility import SFXPlayer
from ..game.floor_visual import FloorVisual
from ..game.painter_visual import PainterVisual
from .editor_floor_manager import EditorFloorManager
from .autofloor_visual import AutoFloorVisual
from .gui_handler import GUIHandler

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