from game.states import State, GameplayState
from game.floor_visual import FloorVisual
from game.painter_visual import PainterVisual
from game.floor_data import FloorData
from game.floor_manager import FloorManager

from .tcase_handlers import FloorViewerControl, FloorViewerWithPainterControl, ViewerControl

def list_of_floors():
    '''Manually a list of FloorData objects for testing.
    It would be better to use files but that logic isn't done yet.'''

    f1 = FloorData(4,3) # 4x3 level
    f1.set_initial_painter_position((0,1))

    # Some cells start filled
    cells = f1.get_cell_grid()
    cells[(0,2)].start_filled()
    cells[(2,1)].start_filled()

    f2 = FloorData(2,5) # 2x5 level
    f2.set_initial_painter_position((1,3))

    cells = f2.get_cell_grid()
    cells[(0,0)].start_filled()

    return [f1, f2]

class PainterViewer(State):
    _INPUT_HANDLER = ViewerControl
    _VISUAL_HANDLERS = (PainterVisual,)

    @classmethod
    def enter(cls):
        dummy_floor = list_of_floors()[0]
        # Set up FloorVisual so the painter grid position can be interpreted by PainterVisual
        FloorVisual.new_floor(dummy_floor)
        # Give dummy parameter for size and use the start position from the floor (to ensure it's on the grid)
        PainterVisual.new_cell_dimens(50)
        PainterVisual.go_to(dummy_floor.get_initial_painter_position())
        PainterVisual.initialise_shakevfx_state()
        # Painter will be drawn at an arbitrary position onscreen

class FloorViewer(State):
    _INPUT_HANDLER = FloorViewerControl
    _VISUAL_HANDLERS = (FloorVisual,)

    @classmethod
    def enter(cls):
        # Store the list of floors to use in FloorViewerControl
        FloorViewerControl.use_floors(list_of_floors())
        # Call next() to set up the first floor
        # (and the painter graphic too if this is FloorViewerWithPainterControl)
        cls._INPUT_HANDLER.next()

class FloorViewerWithPainter(FloorViewer):
    _INPUT_HANDLER = FloorViewerWithPainterControl
    _VISUAL_HANDLERS = (FloorVisual, PainterVisual)

class GameplayTester(GameplayState):
    @classmethod
    def enter(cls):
        FloorManager.load_floors()
        floor = FloorManager.next_floor()
        cls._start_floor(floor)