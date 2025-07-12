from ..abstract_handlers import GUIVisualHandler
from .gui_handler import GUIHandler
class FloorpackCreateVisual(GUIVisualHandler):
    __CANCEL_BUTTON_RECT = (100,100,100,50)
    __CANCEL_BUTTON_TEXT = 'Cancel'
    __DIMENSIONS = (100,100,200,200) # Could base on window size.
    __CREATE_BUTTON_TEXT = 'Create'
    
    @classmethod
    def init(cls, FIELD_ID: str):
        GUIHandler.set_dimensions(*cls.__DIMENSIONS)

        GUIHandler.add_button(cls.__CANCEL_BUTTON_TEXT, cls.__CANCEL_BUTTON_RECT)

        # Don't seem to be able to specify submit button text as 'Create'
        GUIHandler.add_form('frm', '{"%s" : "short_text"}' % FIELD_ID)