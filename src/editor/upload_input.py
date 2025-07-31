import pygame as pg
from ..abstract_handlers import KeyboardInputHandler
from .upload import FloorpackUploader

class UploadPromptInput(KeyboardInputHandler):
    _ACTIONS = {pg.K_BACKSPACE : ('back',),
                pg.K_ESCAPE : ('back',)}
    
    @staticmethod
    def process_input(cls, event):
        if FloorpackUploader.has_just_uploaded():
            FloorpackUploader.remove_upload_prompt()
            return 'EditFloorpacksState'
        else: return cls._process_keyboard_input(cls, event)

    @staticmethod
    def back():
        FloorpackUploader.remove_upload_prompt()
        FloorpackUploader.abort_upload()
        return 'EditFloorpacksState'