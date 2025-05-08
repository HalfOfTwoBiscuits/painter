from game.input_handler_base import InputHandler
#from game.visual_handler_base import VisualHandler
from game.floor_visual import FloorVisual
from game.painter_visual import PainterVisual
from game.menu_visual import MenuVisual
from game.floorselect_input import ArbitraryOptionsControl

import pygame as pg

class ViewerControl(InputHandler):
    '''Input handler when testing whether a displayed graphic looks right.'''
    _ACTIONS = {
        pg.K_RETURN : ('good',),
        pg.K_BACKSPACE : ('fail',),
    }

    @classmethod
    def good(cls):
        '''Graphic looks right, test is successful, return True'''
        return True
    
    @classmethod
    def fail(cls):
        '''Graphic looks wrong, test is unsuccessful, return False'''
        return False

class FloorViewerControl(ViewerControl):
    '''Input handler for testing whether a series of floors look right.
    Pressing return moves onto the next one, and they're all checked before stopping.'''
    _ACTIONS = {
        pg.K_RETURN : ('next',),
        pg.K_BACKSPACE : ('fail',),
    }

    __floors = None
    cur_floor = None

    @classmethod
    def use_floors(cls,floors):
        cls.__floors = floors

    @classmethod
    def next(cls):
        '''Display next floor.
        Called at the start and when confirming the graphics look right
        If out of floors, test is successful and True is returned.'''
        try:
            cls.cur_floor = cls.__floors.pop(0)
        except IndexError:
            # No more floors so test is successful.
            return True
        # Display the new floor
        FloorVisual.new_floor(cls.cur_floor)
    
class FloorViewerWithPainterControl(FloorViewerControl):
    '''Input handler for checking whether a series of floors look right with
    the painter displayed on them. In addition to confirming they look right
    the painter can also be rotated or the shake effect used,
    if this is a TestUsingGameLoop.'''
    _ACTIONS = {
        pg.K_RETURN : ('next',),
        pg.K_BACKSPACE : ('fail',),
        pg.K_RIGHT : ('rotate_painter',),
        pg.K_LEFT : ('shake_painter',)
    }

    __painter_pos = None
    __painter_direction = -2

    @classmethod
    def next(cls):
        '''Display next floor and painter.
        Called at the start and when confirming the graphics look right.'''
        test_outcome = FloorViewerControl.next()
        if test_outcome is not None: return test_outcome

        floor = FloorViewerControl.cur_floor
        cell_dimens = FloorVisual.get_cell_dimens_no_line()
        PainterVisual.new_floor(floor, cell_dimens)

        cls.__painter_pos = floor.get_initial_painter_position()
        cls.__painter_direction = -2

    @classmethod
    def rotate_painter(cls):
        '''Rotate the painter graphic'''
        cls.__painter_direction += 1
        if cls.__painter_direction == 0: cls.__painter_direction = 1
        if cls.__painter_direction == 3: cls.__painter_direction = -2
        PainterVisual.go_to(cls.__painter_pos, cls.__painter_direction)

    @staticmethod
    def shake_painter():
        '''Do the shake VFX on the painter graphic'''
        PainterVisual.shake()

class MenuTesterControl(ArbitraryOptionsControl):

    __MOVE_ON_ID = 'Next Test' # Option added to the end, select it to move on    

    def __init__(self, menu_visual_obj):
        super().__init__(menu_visual_obj)
        # Set to True when the move on option is selected
        self.__finished = False

    @classmethod
    def append_moveon_option(cls, options: list[str]):
        options.append(cls.__MOVE_ON_ID)
        return options
    
    def get_finished(self):
        return self.__finished
    
    def select(self, number: int):
        # Find the option string chosen
        option_id = self._find_option_for_number(number)
        print ('Selected:', option_id)
        if option_id == self.__class__.__MOVE_ON_ID:
            self.__finished = True
        elif option_id is not None: self._menu.set_title(option_id)