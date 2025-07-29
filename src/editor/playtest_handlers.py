from ..game.painter_input import PainterControl
from ..game.menu_button_visual import MenuButtonVisual
from ..audio_utility import SFXPlayer
    
class ReturnToEditorButtonVisual(MenuButtonVisual):
    _TEXT = 'Back\n(Esc)'

class PlaytestControl(PainterControl):
    _BUTTON_VISUAL = ReturnToEditorButtonVisual
    @staticmethod
    def open_menu():
        '''Hook that overrides opening the pause menu with returning to the editor.'''
        SFXPlayer.play_sfx('back')
        return 'EditState'
    
    @staticmethod
    def _state_after_win():
        '''Hook that causes a return to the editor after winning.'''
        return 'EditState'