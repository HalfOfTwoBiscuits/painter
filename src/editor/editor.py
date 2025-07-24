from ..app import App
from .gui_handler import GUIHandler
from . import editor_states

class Editor(App):
    _state_module = editor_states

    def __init__(self, initial_state_name: str, window):
        super().__init__(initial_state_name, window)
        size = window.get_size()
        GUIHandler.init(size)

    def _process_other_event(self, e):
        super()._process_other_event(e)
        GUIHandler.process_event(e)

    def _use_delta(self, dt):
        GUIHandler.update(dt)