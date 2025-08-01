from ..abstract_states import State, GameContentSelectState
from ..config import OnlineConfig
from ..abstract_states import State, FixedOptionsSelectState, GameContentSelectState
from ..error_report import ErrorState, ErrorReportControl
from ..floor_manager import FloorManager
from .painter_input import PainterControl
from .pause_input import PauseMenuControl, RestartExitMenuControl, FloorClearMenuControl
from .floorselect_input import LevelSelectControl, FloorpackSelectControl
from .painter_visual import PainterVisual
from .floor_visual import FloorVisual
from .menu_button_visual import MenuButtonVisual
from .floor_player import FloorPlayer

class GameStartState(State):
    @classmethod
    def enter(cls):
        NEXT_STATE = 'FloorpackSelectState'
        try:
            FloorManager.load_floors()
        except TypeError:
            ErrorReportControl.set_state_after_dismiss(NEXT_STATE)
            return 'ErrorState'
        return NEXT_STATE

class NewFloorState(State):
    '''The player has chosen to start a new floor.
    Set it up before moving onto GameplayState.'''
    @classmethod
    def enter(cls):
        '''Get the next floor object and use the program to set it up.'''
        floor_obj = FloorManager.next_floor()
        cls.__start_floor(floor_obj)
        return "GameplayState"

    @classmethod
    def __start_floor(cls, floor_obj):
        '''Update program state to account for the new floor.'''

        # Set up the new floor graphic.
        FloorVisual.new_floor(floor_obj)
        # Set up painter control logic to interact with the new floor.
        FloorPlayer.new_floor(floor_obj)

        # Set visual parameters of the painter graphic based on
        # the dimension of a cell on the new floor.
        cell_dimens = FloorVisual.get_cell_dimens_no_line()
        PainterVisual.new_cell_dimens(cell_dimens)

        # Put the painter graphic at the initial position.
        painter_pos = floor_obj.get_initial_painter_position()
        PainterVisual.go_to(painter_pos)

        # Initialise the shaking vfx
        # (if the painter was shaking when the last floor ended, this will stop it)
        PainterVisual.initialise_shakevfx_state()

class GameplayState(State):
    '''The player is painting the floor in gameplay.'''

    _INPUT_HANDLER = PainterControl
    _VISUAL_HANDLERS = (FloorVisual, PainterVisual, MenuButtonVisual)

class PauseMenuState(FixedOptionsSelectState):
    '''The player is playing a floor and has pressed CTRL to pause.
    They can choose to continue, restart the floor, or return to the level select.'''

    _OPTIONS = ['Continue', 'Restart', 'Exit']
    _INPUT_HANDLER = PauseMenuControl

    @classmethod
    def enter(cls):
        cls._setup_menu_visual()
        PauseMenuControl.store_menu(cls._menu_visual)
        cls._visual_handlers = (FloorVisual, PainterVisual, cls._menu_visual)

class LevelSelectState(GameContentSelectState):
    '''The player is choosing a floor to play from a floorpack.
    Any floor can be chosen regardless of which have been finished already.'''

    _TITLE = 'Select Level'
    __BACK_OPTION = 'Another Levelpack'
    __EXIT_OPTION = 'Exit Game'

    @classmethod
    def enter(cls):
        '''If there's only one floor, skip to gameplay.
        Otherwise, create a MenuVisual instance with the floors from the pack.
        If there's more than one floorpack, add to the menu a 'Back' option which
        will return to the floorpack select.'''

        options = FloorManager.get_floor_names()
        
        # If there's only one floor, select it
        if len(options) == 1:
            FloorManager.select_floor(0)
            return 'NewFloorState'

        # If there's only one floorpack, include an exit option.
        # If there's more than one, include a back option.
        last_option = None
        only_one_floorpack = FloorManager.get_num_floorpacks() == 1
        if only_one_floorpack:
            if OnlineConfig.can_exit(in_startup_menu=False):
                last_option = cls.__EXIT_OPTION
                options.append(cls.__EXIT_OPTION)
        else:
            last_option = cls.__BACK_OPTION
            options.append(cls.__BACK_OPTION)

        cls._setup_menu_visual(options)
        cls._menu_input_handler = LevelSelectControl(cls._menu_visual, last_option, only_one_floorpack)

class FloorpackSelectState(GameContentSelectState):
    '''The player is choosing a floorpack to play.
    Skipped if there is only one floorpack.'''

    _TITLE = 'Select Level Pack'
    __EXIT_OPTION = 'Exit Game'

    @classmethod
    def enter(cls):
        '''If there's only one floorpack, skip to the floor select.
        Otherwise, create a MenuVisual instance with floor packs.'''
        packnames = FloorManager.get_floorpack_names()

        # If there's only one floorpack, select it
        if len(packnames) == 1:
            FloorManager.select_floorpack(packnames[0])
            return 'LevelSelectState'
        
        options = packnames
        if OnlineConfig.can_exit(in_startup_menu=False):
            options.append(cls.__EXIT_OPTION)
        
        cls._setup_menu_visual(options)
        cls._menu_input_handler = FloorpackSelectControl(cls._menu_visual, cls.__EXIT_OPTION)
    
class FloorClearState(FixedOptionsSelectState):
    '''The player has painted the floor and is choosing whether to
    continue or return to the level select.'''

    _TITLE = 'Well done!'
    _OPTIONS = ['Next Floor', 'Restart', 'Exit']
    _INPUT_HANDLER = FloorClearMenuControl
    
    @classmethod
    def enter(cls):
        cls._setup_menu_visual()
        FloorClearMenuControl.store_menu(cls._menu_visual)
        cls._visual_handlers = (FloorVisual, cls._menu_visual)
    
class FloorpackOverState(FloorClearState):
    '''The player has painted the last floor in the pack,
    and can only choose to return to the floor select.'''
    
    _INPUT_HANDLER = RestartExitMenuControl
    _OPTIONS = ['Restart', 'Exit']

    @classmethod
    def enter(cls):
        if FloorManager.get_num_floors() == FloorManager.get_num_floorpacks() == 1:
            return 'SingleFloorClearState'
        
        cls._setup_menu_visual()
        RestartExitMenuControl.store_menu(cls._menu_visual)
        cls._visual_handlers = (FloorVisual, cls._menu_visual)