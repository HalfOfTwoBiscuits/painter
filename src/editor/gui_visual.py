from pygame import Rect
from ..abstract_handlers_gui import GUIVisualHandler, CentredFixedSizeGUIVisualHandler
from .gui_handler import GUIHandler
class FloorpackCreateVisual(CentredFixedSizeGUIVisualHandler):
    _GUI_WIDTH = 175
    __FIELD_HEIGHT = 50
    __BUTTON_HEIGHT = 50
    __LABEL_HEIGHT = GUIHandler.get_label_height()
    __FULL_FIELD_HEIGHT = __FIELD_HEIGHT + __LABEL_HEIGHT
    
    _GUI_HEIGHT = __FULL_FIELD_HEIGHT + __BUTTON_HEIGHT * 2

    __FIELD_RECT = Rect(0,0,_GUI_WIDTH,__FIELD_HEIGHT)
    __SUBMIT_RECT = Rect(0,__FULL_FIELD_HEIGHT,_GUI_WIDTH,__BUTTON_HEIGHT)
    __CANCEL_RECT = Rect(0,__FULL_FIELD_HEIGHT + __BUTTON_HEIGHT,_GUI_WIDTH,__BUTTON_HEIGHT)
    
    @classmethod
    def init(cls, FIELD_ID: str, CANCEL_ID: str, SUBMIT_ID: str):
        cls._setup_container()

        # Add submit and cancel buttons
        GUIHandler.add_button(SUBMIT_ID, cls.__SUBMIT_RECT)
        GUIHandler.add_button(CANCEL_ID, cls.__CANCEL_RECT)

        # Add text input
        GUIHandler.add_textinput(FIELD_ID, cls.__FIELD_RECT)

class EditorButtonsVisual(GUIVisualHandler):
    __MARGIN_PX = 4
    __EDITOR_HEIGHT_FRAC = 3
    __BUTTON_WIDTH_FRAC = 1.5
    __BUTTON_HEIGHT_FRAC = 4

    @classmethod
    def init(cls, RESIZE_ID: str, SAVE_ID: str, EXIT_ID: str, TEST_ID: str):
        GUIHandler.clear_elements()
        # Find position and dimensions of UI container.
        win_w, win_h = cls._window_dimensions
        available_h = int(win_h / cls.__EDITOR_HEIGHT_FRAC)
        gui_w = win_w - cls.__MARGIN_PX * 2
        gui_h = available_h - cls.__MARGIN_PX * 2
        gui_x, gui_y = cls._centred_in_dimensions(win_w, available_h, gui_w, gui_h)
        gui_y += win_h - available_h
        GUIHandler.set_container(gui_x, gui_y, gui_w, gui_h)

        # There are four buttons, so divide the width into four.
        width_per_button = gui_w // 4

        # Find dimensions of a button.
        button_w = int(width_per_button / cls.__BUTTON_WIDTH_FRAC)
        button_h = int(gui_h / cls.__BUTTON_HEIGHT_FRAC)

        # Centre a button in the dimensions available for it.
        button_x, button_y = cls._centred_in_dimensions(width_per_button, gui_h, button_w, button_h)

        # Add resize, test, save, and exit buttons.
        ORDER = (RESIZE_ID, TEST_ID, SAVE_ID, EXIT_ID)
        for id in ORDER:
            GUIHandler.add_button(id, Rect(button_x, button_y, button_w, button_h))
            # Add the width-per-button to shift to the right.
            button_x += width_per_button

class ResizeMenuVisual(CentredFixedSizeGUIVisualHandler):
    _GUI_WIDTH = 175

    __FIELD_HEIGHT = 50
    __BUTTON_HEIGHT = 50
    __LABEL_HEIGHT = GUIHandler.get_label_height()
    __FULL_FIELD_HEIGHT = __FIELD_HEIGHT + __LABEL_HEIGHT

    __WIDTH_FIELD_RECT = Rect(0,0,_GUI_WIDTH,__FIELD_HEIGHT)
    __HEIGHT_FIELD_RECT = Rect(0,__FULL_FIELD_HEIGHT,_GUI_WIDTH,__FIELD_HEIGHT)

    __SUBMIT_RECT = Rect(0,__FULL_FIELD_HEIGHT * 2,_GUI_WIDTH,__BUTTON_HEIGHT)
    __CANCEL_RECT = Rect(0,__FULL_FIELD_HEIGHT * 2 + __BUTTON_HEIGHT,_GUI_WIDTH,__BUTTON_HEIGHT)

    _GUI_HEIGHT = __FULL_FIELD_HEIGHT * 2 + __BUTTON_HEIGHT * 2

    @classmethod
    def init(cls, WIDTH_FIELD_ID: str, HEIGHT_FIELD_ID: str, CANCEL_ID: str, SUBMIT_ID):
        cls._setup_container()

        # Add submit and cancel buttons
        GUIHandler.add_button(SUBMIT_ID, cls.__SUBMIT_RECT)
        GUIHandler.add_button(CANCEL_ID, cls.__CANCEL_RECT)

        # Add text inputs
        GUIHandler.add_textinput(WIDTH_FIELD_ID, cls.__WIDTH_FIELD_RECT)
        GUIHandler.add_textinput(HEIGHT_FIELD_ID, cls.__HEIGHT_FIELD_RECT)