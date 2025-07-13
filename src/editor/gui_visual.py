from ..abstract_handlers import GUIVisualHandler
from .gui_handler import GUIHandler
class FloorpackCreateVisual(GUIVisualHandler):
    __GUI_WIDTH = 175
    __GUI_HEIGHT = 200
    __FORM_DIMENSIONS = (0,0,175,150)
    __CANCEL_DIMENSIONS = (0,150,175,50)
    
    @classmethod
    def init(cls, FIELD_ID: str, CANCEL_ID: str):
        GUIHandler.clear_elements()
        win_w, win_h = cls._window_dimensions
        x, y = (win_w - cls.__GUI_WIDTH) // 2, (win_h - cls.__GUI_HEIGHT) // 2
        GUIHandler.set_container(x, y, cls.__GUI_WIDTH, cls.__GUI_HEIGHT)

        GUIHandler.add_button(CANCEL_ID, cls.__CANCEL_DIMENSIONS)

        # Don't seem to be able to specify submit button text as 'Create'
        # __CREATE_BUTTON_TEXT = 'Create'
        GUIHandler.add_form('frm', cls.__FORM_DIMENSIONS, {FIELD_ID : "short_text"})