from ..app import App
from ..game.floor_visual import FloorVisual
from .floor_data import FloorData
from .gui_handler import GUIHandler
from . import editor_states
import pygame as pg


class Editor(App):
    _state_module = editor_states

    def __init__(self, initial_state_name: str, window):
        super().__init__(initial_state_name, window)
        size = window.get_size()
        GUIHandler.init(size)

    def _process_other_event(self, e):
        GUIHandler.process_event(e)
        try: new_state_name = self._state.process_bespoke_input(e)
        except AttributeError: pass
        else: self._change_state(new_state_name)

    def _use_delta(self, dt):
        GUIHandler.update(dt)