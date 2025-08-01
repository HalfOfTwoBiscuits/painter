import pygame as pg
from .audio_utility import SFXPlayer
from .abstract_states import State
from .abstract_handlers import InputHandler, TextDisplayVisualHandler

class ErrorReportVisual(TextDisplayVisualHandler):
    __CONTROL_PROMPT_ENDING = '\nPress any key or click anywhere to dismiss'
    _text = 'An error occurred' + __CONTROL_PROMPT_ENDING

    @classmethod
    def set_message(cls, message: str):
        cls._text = message + cls.__CONTROL_PROMPT_ENDING

    @classmethod
    def set_message_from_invalid_packs(cls, invalid_pack_names: list[str]):
        START = 'Some level packs are invalid:\n'
        END = '\nAny valid level packs will still work.'
        cls.set_message(START + '\n'.join(invalid_pack_names) + END)

class ErrorReportControl(InputHandler):
    # By default, close the game after dismissing the error report
    _state_after_dismiss = True

    @staticmethod
    def process_input(cls, event):
        if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONUP:
            return cls.__back()

    @classmethod
    def __back(cls):
        SFXPlayer.play_sfx('back')
        return cls._state_after_dismiss
    
    @classmethod
    def set_state_after_dismiss(cls, state_name: str | bool):
        cls._state_after_dismiss = state_name

class ErrorState(State):
    _VISUAL_HANDLERS = (ErrorReportVisual,)
    _INPUT_HANDLER = ErrorReportControl

    @classmethod
    def enter(cls):
        SFXPlayer.play_sfx('invalid')
        ErrorReportVisual.init()