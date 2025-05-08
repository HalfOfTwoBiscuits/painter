from .painter_input import PainterControl
from .pause_input import PauseMenuControl
from .floorselect_input import LevelSelectControl
from .painter_visual import PainterVisual
from .floor_visual import FloorVisual
from .menu_visual import MenuVisual
from .floor_player import FloorPlayer
from .floor_manager import FloorManager

class State:
    _INPUT_HANDLER = None
    _VISUAL_HANDLERS = ()

    @classmethod
    def enter(cls):
        '''Method called when the program enters this state.
        Optional to implement.'''
        ...

    @classmethod
    def process_input(cls, key_pressed):
        '''Respond to a key press. Delegates to InputHandler.process_input().
        Return any string identifier of a new state to change to.'''
        i_handler = cls.get_input_handler()
        # get_input_handler() can return None to end the program
        if i_handler is None: return True

        # Input handler may be a class or an instance, so 'self' is passed manually
        new_state = i_handler.process_input(i_handler, key_pressed)
        return new_state

    @classmethod
    def get_input_handler(cls):
        '''Method that returns the input handler used.
        Defaults to the value of the _INPUT_HANDLER attribute.
        It is public only for unit tests, otherwise it is only called in process_input().
        If it returns None to process_input() then the program ends.'''
        return cls._INPUT_HANDLER
    
    @classmethod
    def get_visual_handlers(cls):
        '''Method that returns the visual handlers used.
        Defaults to the value of the _VISUAL_HANDLERS attribute.'''
        return cls._VISUAL_HANDLERS

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
    _VISUAL_HANDLERS = (FloorVisual, PainterVisual)

class PauseMenuState(State):
    '''The player is playing a floor and has pressed CTRL to pause.
    They can choose to continue, restart the floor, or return to the level select.'''

    __TITLE = 'Pause'
    __OPTION_NAMES = ['Continue', 'Restart', 'Exit']
    _INPUT_HANDLER = PauseMenuControl
    __visual_handlers = None
    
    @classmethod
    def get_visual_handlers(cls):
        if cls.__visual_handlers is None:
            cls.__visual_handlers = (FloorVisual, PainterVisual, MenuVisual(cls.__TITLE, cls.__OPTION_NAMES))
        return cls.__visual_handlers

class LevelSelectState(State):
    '''The player is choosing a floor to play from a floorpack.
    Any floor can be chosen regardless of which have been finished already.'''

    __TITLE = 'Select Level'
    __input_handler = None
    __menu_visual = None

    @classmethod
    def enter(cls):
        '''Create a MenuVisual instance with the floors from the pack.'''
        floornames = FloorManager.get_floor_names()
        cls.__menu_visual = MenuVisual(cls.__TITLE, floornames)
        cls.__input_handler = LevelSelectControl(cls.__menu_visual)

    @classmethod
    def get_visual_handlers(cls):
        '''Return a MenuVisual instance with the levels as options,
        as created when entering this state.'''
        return (cls.__menu_visual,)
    
    @classmethod
    def get_input_handler(cls):
        return cls.__input_handler
    
class FloorPackSelect(State):
    '''The player is choosing a floorpack to play.'''

    __TITLE = 'Select Level Pack'
    _INPUT_HANDLER = LevelSelectControl
    __menu_visual = None

    @classmethod
    def enter(cls):
        '''Create a MenuVisual instance with floor packs.'''
        packnames = FloorManager.get_floorpack_names()
        cls.__menu_visual = MenuVisual(cls.__TITLE, packnames)

    @classmethod
    def get_visual_handlers(cls):
        '''Return a MenuVisual instance with the floorpacks as options,
        as created when entering this state.'''
        return (cls.__menu_visual,)