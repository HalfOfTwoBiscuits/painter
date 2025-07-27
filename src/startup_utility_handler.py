import pygame as pg
from .abstract_handlers import FixedOptionsControl

class StartupMenuControl(FixedOptionsControl):
    '''A menu with the ability to boot the game or level editor.
    Uses numeric exit codes. 1: game, 2: editor, 3: quit.'''
    
    _ACTIONS = {
        pg.K_1 : ('game',),
        pg.K_RETURN : ('game',),
        pg.K_2 : ('editor',),
        pg.K_3 : ('quit',),
        pg.K_ESCAPE : ('quit',),
        pg.K_BACKSPACE : ('quit',),
    }

    @staticmethod
    def game(): return 1
    
    @staticmethod
    def editor(): return 2

    @staticmethod
    def quit(): return 3