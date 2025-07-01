from ..abstract_handlers import VisualHandler
from .gui_handler import GUIHandler
class FloorpackCreateVisual(VisualHandler):
    def __init__(self, BUTTONS: dict):
        for id, gridstyle_position in BUTTONS.items():
            relative_rect = gridstyle_position # Look at documentation to work this out
            GUIHandler.add_button(id, relative_rect)
        # ...and so on for text input. Could be made generic
        # with parameters for grid setup
        # Even an GUIElementDatum object with a type string?
        # and add_element on GUIHandler?