from ..game.painter_input import PainterControl
from ..audio_utility import SFXPlayer

class PlaytestControl(PainterControl):

    @staticmethod
    def open_menu():
        '''Hook that overrides opening the pause menu with returning to the editor.'''
        SFXPlayer.play_sfx('back')
        return 'EditState'
    
    @staticmethod
    def state_after_win():
        '''Hook that causes a return to the editor after winning.'''
        return 'EditState'