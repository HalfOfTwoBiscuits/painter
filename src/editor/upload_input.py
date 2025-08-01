import pygame as pg
from ..abstract_handlers import KeyboardInputHandler
from ..error_report import ErrorReportVisual, ErrorReportControl
from ..audio_utility import SFXPlayer
from .upload import FloorpackUploader

class UploadPromptInput(KeyboardInputHandler):
    _ACTIONS = {pg.K_BACKSPACE : ('back',),
                pg.K_ESCAPE : ('back',)}
    
    @staticmethod
    def process_input(cls, event):
        ERR_MSG = \
            "That isn't a valid floorpack.\n"\
            "Please upload a .yaml file that was created by the level editor.\n"\
            "You can download one that you made in the browser\n"\
            "by selecting it and choosing Download All,\n"\
            "or if you downloaded Painter, it will be in the folder resources/floors."
        NEXT_STATE = 'EditFloorpacksState'
        if FloorpackUploader.upload_was_invalid():
            ErrorReportVisual.set_message(ERR_MSG)
            ErrorReportControl.set_state_after_dismiss(NEXT_STATE)
            return 'ErrorState'
        elif FloorpackUploader.has_just_uploaded():
            FloorpackUploader.remove_upload_prompt()
            return NEXT_STATE
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            return cls.back()
        else: return cls._process_keyboard_input(cls, event)

    @staticmethod
    def back():
        FloorpackUploader.remove_upload_prompt()
        FloorpackUploader.abort_upload()
        SFXPlayer.play_sfx('back')
        return 'EditFloorpacksState'