from ..app import App
from ..config import OnlineConfig
from .gui_handler import GUIHandler
from .upload import FloorpackUploader
from . import editor_states

class Editor(App):
    _state_module = editor_states

    def __init__(self, initial_state_name: str, window):
        super().__init__(initial_state_name, window)
        size = window.get_size()
        GUIHandler.init(size)
        if OnlineConfig.is_online(): FloorpackUploader.init()

    def _other_event_processing(self, e):
        GUIHandler.process_event(e)

    def _use_delta(self, dt):
        GUIHandler.update(dt)