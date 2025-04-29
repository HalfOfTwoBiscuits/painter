import pygame as pg
from input_handler_base import InputHandler

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
        pg.K_0 : ('select',10)
    }