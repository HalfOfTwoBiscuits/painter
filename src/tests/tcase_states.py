from game.states import State
from game.floor_visual import FloorVisual
from game.floor_data import FloorData

from .tcase_handlers import FloorViewerControl

def list_of_floors(self):
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

    return [f1, f2]

class FloorViewer(State):
    _INPUT_HANDLER = FloorViewerControl
    _VISUAL_HANDLERS = (FloorVisual,)

    @classmethod
    def enter(cls):
        first, *rest = list_of_floors()
        FloorVisual.new_floor(first)
        FloorViewerControl.use_floors(rest)