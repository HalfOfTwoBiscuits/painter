import pygame as pg
from painter_visual import PainterVisual
from abc import ABC

class InputHandler(ABC):
    _ACTIONS = {}

    def process_input(self, key):
        action = self._ACTIONS.get(key)
        if action is not None:
            method_to_call = getattr(self,action[0])
            arguments = action[1:]
            method_to_call(arguments)

class PainterControl(InputHandler):
    _ACTIONS = {
        pg.K_RIGHT : ('move',1),
        pg.K_LEFT : ('move',-1),
        pg.K_DOWN : ('move',2),
        pg.K_UP : ('move',-2),
        pg.K_BACKSPACE : ('undo'),
    }

    def __init__(self, level_interface_obj):
        self.__play = level_interface_obj

    def move(self, direction: int):
        new_pos = self.__play.painter_position_after_move(direction)
        could_move = self.__play.move_painter(new_pos)

        if could_move:
            PainterVisual.go_to(new_pos, direction)
        else:
            PainterVisual.shake()

    def undo(self):
        new_pos = self.__play.undo()

        if new_pos is None:
            PainterVisual.shake()
        else:
            # Face up after undoing, same as initial
            PainterVisual.go_to(new_pos, -2)