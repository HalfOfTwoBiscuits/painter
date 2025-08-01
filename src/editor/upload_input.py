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
        
        DUPLICATE_MSG = \
            "You tried to upload a floorpack called:\n" \
            "{}\n"\
            "but there's already one with that name.\n" \
            "Please rename the floorpack file to something different."
        
        NEXT_STATE = 'EditFloorpacksState'
        if FloorpackUploader.has_just_uploaded():
            FloorpackUploader.remove_upload_prompt()
            return NEXT_STATE
        
        elif FloorpackUploader.upload_was_invalid():
            ErrorReportVisual.set_message(ERR_MSG)
            ErrorReportControl.set_state_after_dismiss(NEXT_STATE)
            return 'ErrorState'
        
        else:
            # Check if the user uploaded a floorpack with a name that already exists
            duplicate_name = FloorpackUploader.duplicate_name()
            if duplicate_name is not None:
                duplicate_name_msg = DUPLICATE_MSG.format(duplicate_name)
                ErrorReportVisual.set_message(duplicate_name_msg)
                ErrorReportControl.set_state_after_dismiss(NEXT_STATE)
                return 'ErrorState'

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            return cls.back()
        else: return cls._process_keyboard_input(cls, event)

    @staticmethod
    def back():
        FloorpackUploader.remove_upload_prompt()
        FloorpackUploader.abort_upload()
        SFXPlayer.play_sfx('back')
        return 'EditFloorpacksState'