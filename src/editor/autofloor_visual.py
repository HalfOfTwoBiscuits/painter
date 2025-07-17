import pygame as pg
from ..abstract_handlers import VisualHandler
from .floor_auto_player import FloorAutoPlayer
class AutoFloorVisual(VisualHandler):
    __YES_COL = pg.Color(0,200,0)
    __NO_COL = pg.Color(200,0,0)
    __RADIUS = 20
    __possible = False

    @classmethod
    def update(cls, floor_obj):
        cls.__possible = FloorAutoPlayer.is_possible(floor_obj)

    @classmethod
    def draw(cls):
        col = cls.__possible and cls.__YES_COL or cls.__NO_COL
        pg.draw.circle(cls._window, col, (cls.__RADIUS, cls.__RADIUS), cls.__RADIUS)