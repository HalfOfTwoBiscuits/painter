from ..abstract_handlers import GUIVisualHandler
from .gui_handler import GUIHandler
class FloorpackCreateVisual(GUIVisualHandler):
    __CANCEL_RECT = (0,175,175,50)
    __DIMENSIONS = (300,300,225,225) # Could base on window size.
    __FORM_DIMENSIONS = (0,0,175,175)
    
    @classmethod
    def init(cls, FIELD_ID: str, CANCEL_ID: str):
        GUIHandler.set_dimensions(*cls.__DIMENSIONS)

        GUIHandler.add_button(CANCEL_ID, cls.__CANCEL_RECT)

        # Don't seem to be able to specify submit button text as 'Create'
        # __CREATE_BUTTON_TEXT = 'Create'
        GUIHandler.add_form('frm', cls.__FORM_DIMENSIONS, {FIELD_ID : "short_text"})