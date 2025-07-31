import pygame as pg
from ..abstract_handlers import KeyboardInputHandler
from ..audio_utility import SFXPlayer
from .upload import FloorpackUploader

class UploadPromptInput(KeyboardInputHandler):
    _ACTIONS = {pg.K_BACKSPACE : ('back',),
                pg.K_ESCAPE : ('back',)}
    
    @staticmethod
    def process_input(cls, event):
        if FloorpackUploader.has_just_uploaded():
            FloorpackUploader.remove_upload_prompt()
            return 'EditFloorpacksState'
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            return cls.back()
        else: return cls._process_keyboard_input(cls, event)

    @staticmethod
    def back():
        FloorpackUploader.remove_upload_prompt()
        FloorpackUploader.abort_upload()
        SFXPlayer.play_sfx('back')
        return 'EditFloorpacksState'