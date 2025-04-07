from painter import PainterCharacter
import pygame as pg

class PainterControl:
    ACTIONS = {
        pg.K_RIGHT : lambda : PainterCharacter.move(1),
        pg.K_LEFT : lambda : PainterCharacter.move(-1),
        pg.K_DOWN : lambda : PainterCharacter.move(2),
        pg.K_UP : lambda : PainterCharacter.move(-2),
        pg.K_BACKSPACE : lambda : PainterCharacter.undo()
    }