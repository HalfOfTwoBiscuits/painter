from ..abstract_handlers import VisualHandler
from .gui_handler import GUIHandler
class FloorpackCreateVisual(VisualHandler):
    __BUTTONS = {{'id' : 'Create', 'location_rect' : (20)},
                {'id' : 'Cancel'}}
    __TOPLEFT_X = 100
    __TOPLEFT_Y = 100
    
    @classmethod
    def init(cls, FIELD_ID: str):
        for button_data in cls.__BUTTONS:
            GUIHandler.add_button(
                button_data['id'], button_data['location_rect'])
        
        GUIHandler.set_topleft(cls.__TOPLEFT_X, cls.__TOPLEFT_Y)

        