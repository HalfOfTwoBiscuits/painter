from ..abstract_states import State
from ..game.floor_visual import FloorVisual
from ..game.painter_visual import PainterVisual
from ..game.menu_visual import MenuVisual
from ..editor.floor_data import FloorData
from .tcase_floor_manager import TestFloorManager

from .tcase_handlers import FloorViewerControl, FloorViewerWithPainterControl, ViewerControl, MenuTesterControl

def list_of_floors():
    '''Manually a create a list of FloorData objects for testing.
    
    This could be put into a file, separating the FloorData creation
    from FloorManager.load_floors().
    Consider again when making the level editor - that functionality might
    be part of the editor in some way.'''

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

class MenuTester(State):
    '''Test visuals and controls for menus with different amounts of options.'''
    __input_handler = None
    __visual_handler = None

    __TITLES = ['Pause', 'Floor Select', 'Words']
    __OPTION_LISTS = [
        ['Continue', 'Restart', 'Exit'],
        ['First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh'],
        ['Fish', 'Flan', 'Fries', 'Fillet', 'Frozen',
         'Greater', 'Gaping', 'Green', 'Greed', 'Grasp',
         'Hispanic', 'Hardship', 'Hollow'],
    ]
    __menu_index = 0
    __success = False

    @classmethod
    def enter(cls):
        cls.__new_menu()

    @classmethod
    def get_visual_handlers(cls):
        # Make use of this being called every frame to check if
        # we moved onto the next menu.
        if cls.__input_handler.get_finished():
            cls.__menu_index += 1

            try: cls.__new_menu()
            # No more menus means the test is successful
            except IndexError: cls.__success = True
        return (cls.__visual_handler,)
    
    @classmethod
    def get_input_handler(cls):
        # Returning True finishes test.
        if cls.__success: return True
        return cls.__input_handler
    
    @classmethod
    def __new_menu(cls):
        # Use the index of the current menu in the series to retrieve title and option names
        title = cls.__TITLES[cls.__menu_index]
        options = cls.__OPTION_LISTS[cls.__menu_index]
        options = MenuTesterControl.append_moveon_option(options)
        # update the stored index and visual handler for the menu
        cls.__visual_handler = MenuVisual(title, options)
        cls.__input_handler = MenuTesterControl(cls.__visual_handler)

class GameplayTester(State):
    @classmethod
    def enter(cls):
        # Start gameplay using the test floorpack.
        fpack = list_of_floors()
        TestFloorManager.insert_test_floorpack(fpack)
        return "NewFloorState"