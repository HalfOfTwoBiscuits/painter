import pygame as pg
from ..abstract_handlers import VisualHandler
from ..direction_utility import DirectionUtility
from ..game.floor_visual import FloorVisual

class CursorVisual(VisualHandler):
    __COL = pg.Color(0,200,0)
    @classmethod
    def init(cls, floor_obj):
        cls.__cursor_pos = None
        cls.__w, cls.__h = floor_obj.get_cell_grid().get_size()
        cell_dimens = FloorVisual.get_cell_dimens_no_line()
        cls.__margin = cell_dimens // 12
        cls.__width = cell_dimens // 14
        cls.__corner_radius = cell_dimens // 8
        cls.__dimens = cell_dimens - cls.__margin * 2

    @classmethod
    def draw(cls):
        if cls.__cursor_pos is not None:
            x, y = FloorVisual.topleft_for(cls.__cursor_pos)
            x += cls.__margin
            y += cls.__margin
            rect = pg.Rect(x,y,cls.__dimens,cls.__dimens)
            pg.draw.rect(cls._window, cls.__COL, rect, width=cls.__width, border_radius=cls.__corner_radius)

    @classmethod
    def move_cursor(cls, direction: int):
        '''Move the cursor in the given direction based on
        an arrow key being pressed. The directions are the same
        as the painter ingame:
        1 : Right, -1 : Left,
        2 : Down, -2 : Up
        If the cursor does not currently have a position,
        will initialise it to the topleft corner.'''
        if cls.__cursor_pos is None: cls.__cursor_pos = (0,0)
        else:
            x, y = cls.__cursor_pos
            cls.__cursor_pos = DirectionUtility.pos_after_move(x,y,cls.__w,cls.__h,direction)

    @classmethod
    def get_pos(cls):
        return cls.__cursor_pos