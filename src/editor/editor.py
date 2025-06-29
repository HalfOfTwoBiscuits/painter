from ..app import App
from ..game.floor_visual import FloorVisual
from .floor_data import FloorData
from . import editor_states
import pygame as pg
import pygame_gui as gui

class Editor(App):
    _state_module = editor_states

    def __init__(self, initial_state_name: str, window):
        super().__init__(initial_state_name, window)
        size = window.get_size()
        self.__ui = gui.UIManager(size)

    def _process_other_event(self, e):
        if e.type == gui.UI_BUTTON_PRESSED:
            ...
        self.__ui.process_events(e)