'''These abstract visual handlers were once part of abstract_handlers.py,
but since the main game code imports from that file,
this caused the main game to depend on pygame_gui, which it doesn't use.
So they are separate.'''

from abc import ABC
from .abstract_handlers import VisualHandler
from .editor.gui_handler import GUIHandler

class GUIVisualHandler(VisualHandler, ABC):
    '''Visual handler that makes use of the GUIHandler to create UI elements
    rather than drawing graphics itself.'''

    @classmethod
    def draw(cls):
        '''This visual handler draws a GUI.'''
        GUIHandler.draw(cls._window)

    @staticmethod
    def _centred_in_dimensions(x_dimens: int, y_dimens: int, elem_w: int, elem_h: int):
        '''Return the x, y position for a GUI element with the given width and height
        so that it is centred inside an area with the given dimensions.'''
        return (x_dimens - elem_w) // 2, (y_dimens - elem_h) // 2

class CentredFixedSizeGUIVisualHandler(GUIVisualHandler, ABC):
    _GUI_WIDTH = 175
    _GUI_HEIGHT = 175

    @classmethod
    def _setup_container(cls):
        '''Set the GUI to be centred in the window,
        given it has the width and height specified.
        Delegates to _centred_in_dimensions() but
        allows reuse of the logic to create a centred GUI window.
        Also clears existing GUI elements.'''

        GUIHandler.clear_elements()
        win_w, win_h = cls._window_dimensions
        x, y = cls._centred_in_dimensions(win_w, win_h, cls._GUI_WIDTH, cls._GUI_HEIGHT)
        GUIHandler.set_container(x, y, cls._GUI_WIDTH, cls._GUI_HEIGHT)