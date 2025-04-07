import pygame as pg

class PainterCharacter:
    @classmethod
    def be_on_level(cls, level_play_interface_obj):
        cls.__play_interface = level_play_interface_obj

    @classmethod
    def move(cls, direction: int):
        cls.__play_interface.move_painter(direction)

    @classmethod
    def undo(cls):
        cls.__play_interface.undo()