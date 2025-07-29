import pygame as pg
from ..abstract_handlers import VisualHandler
from ..file_utility import FileUtility
from ..audio_utility import SFXPlayer
from .floor_auto_player import FloorAutoPlayer
class AutoFloorVisual(VisualHandler):
    __YES_COL = pg.Color(0,200,0)
    __NO_COL = pg.Color(200,0,0)
    __TEXT_COL = pg.Color(0,0,0)
    __BROKEN_COL = pg.Color(200,200,200)
    __RADIUS = 30
    __TOGGLE_RECT = pg.Rect(0,0,__RADIUS * 2,__RADIUS * 2)
    __TEXT_MARGIN = __RADIUS // 2
    __num_solutions = 0

    # Font data
    __FONT_DIRNAME = 'font'
    __FONT_FILENAME = 'Gorilla_Black'

    __FONT_PATH = FileUtility.path_to_resource(__FONT_DIRNAME, __FONT_FILENAME)

    pg.font.init()
    __FONT = pg.font.Font(__FONT_PATH, 18)

    __is_possible = None
    # 1 : checking possibility with heuristic
    # 2 : definite checking of possiblility
    # 3 : checking number of solutions
    __state = 1

    @classmethod
    def update(cls, floor_obj):
        if cls.__state == 3:
            try:
                cls.__num_solutions = FloorAutoPlayer.num_solutions(floor_obj)
            except ValueError:
                cls.__state = 1
            else: cls.__is_possible = cls.__num_solutions > 0
        elif cls.__state == 2:
            try:
                cls.__is_possible = FloorAutoPlayer.is_possible(floor_obj)
            except ValueError:
                cls.__state = 1
        if cls.__state == 1:
            cls.__is_possible = FloorAutoPlayer.is_possible_heuristic(floor_obj)

    @classmethod
    def toggle_solution_count(cls, floor_obj):
        SFXPlayer.play_sfx('menu')
        if cls.__state == 3: cls.__state = 1
        else: cls.__state += 1
        cls.update(floor_obj)

    @classmethod
    def get_toggle_rect(cls):
        return cls.__TOGGLE_RECT

    @classmethod
    def draw(cls):
        if cls.__is_possible is not None:
            col = cls.__is_possible and cls.__YES_COL or cls.__NO_COL
            pg.draw.circle(cls._window, col, (cls.__RADIUS, cls.__RADIUS), cls.__RADIUS)
            if cls.__state == 3:
                text = cls.__FONT.render(str(cls.__num_solutions), False, cls.__TEXT_COL)
                cls._window.blit(text, (cls.__TEXT_MARGIN, cls.__TEXT_MARGIN))
        else: pg.draw.circle(cls._window, cls.__BROKEN_COL, (cls.__RADIUS, cls.__RADIUS), cls.__RADIUS)