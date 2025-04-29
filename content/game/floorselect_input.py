import pygame as pg
from input_handler_base import InputHandler
from floor_manager import FloorManager

class SelectMenuControl(InputHandler):
    _ACTIONS = {
        pg.K_1 : ('select',1),
        pg.K_2 : ('select',2),
        pg.K_3 : ('select',3),
        pg.K_4 : ('select',4),
        pg.K_5 : ('select',5),
        pg.K_6 : ('select',6),
        pg.K_7 : ('select',7),
        pg.K_8 : ('select',8),
        pg.K_9 : ('select',9),
    }

    def ___init__(self, menu_visual_obj):
        self.__menu = menu_visual_obj

class LevelSelectControl(SelectMenuControl):
    def select(self, number: int):
        option_id = self.__menu.option_chosen(number)
        floor_index = int(option_id[-1])
        FloorManager.select_floor(floor_index)
        return 'GameplayState'