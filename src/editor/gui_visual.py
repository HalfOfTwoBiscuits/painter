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
        # Find position and dimensions of UI container
        win_w, win_h = cls._window_dimensions
        x, y = cls._centred_in_dimensions(win_w, win_h, cls.__GUI_WIDTH, cls.__GUI_HEIGHT)
        GUIHandler.set_container(x, y, cls.__GUI_WIDTH, cls.__GUI_HEIGHT)

        # Add cancel button
        GUIHandler.add_button(CANCEL_ID, cls.__CANCEL_DIMENSIONS)

        # Add form with text field, label, and submit button
        # Don't seem to be able to specify submit button text as 'Create'
        GUIHandler.add_form('frm', cls.__FORM_DIMENSIONS, {FIELD_ID : "short_text"})

class EditorButtonsVisual(GUIVisualHandler):
    __MARGIN_PX = 4
    __EDITOR_HEIGHT_FRAC = 2
    __BUTTON_WIDTH_FRAC = 1.5
    __BUTTON_HEIGHT_FRAC = 4

    @classmethod
    def init(cls, RESIZE_ID: str, SAVE_ID: str, EXIT_ID: str):
        GUIHandler.clear_elements()
        # Find position and dimensions of UI container.
        win_w, win_h = cls._window_dimensions
        available_h = int(win_h / cls.__EDITOR_HEIGHT_FRAC)
        gui_w = win_w - cls.__MARGIN_PX * 2
        gui_h = available_h - cls.__MARGIN_PX * 2
        gui_x, gui_y = cls._centred_in_dimensions(win_w, available_h, gui_w, gui_h)
        gui_y += win_h - available_h
        GUIHandler.set_container(gui_x, gui_y, gui_w, gui_h)

        # There are three buttons, so divide the width into three.
        width_per_button = gui_w // 3

        # Find dimensions of a button.
        button_w = int(width_per_button / cls.__BUTTON_WIDTH_FRAC)
        button_h = int(gui_h / cls.__BUTTON_HEIGHT_FRAC)

        # Centre a button in the dimensions available for it.
        button_x, button_y = cls._centred_in_dimensions(width_per_button, gui_h, button_w, button_h)

        # Add resize, save, and exit buttons.
        GUIHandler.add_button(RESIZE_ID, (button_x, button_y, button_w, button_h))
        # Add the width-per-button to shift to the right.
        GUIHandler.add_button(SAVE_ID, (button_x + width_per_button, button_y, button_w, button_h))
        GUIHandler.add_button(EXIT_ID, (button_x + width_per_button * 2, button_y, button_w, button_h))