import pygame as pg
import platform

from ..abstract_handlers import KeyboardInputHandler, ArbitraryOptionsControlWithBackButton
from ..audio_utility import SFXPlayer
from .editor_floor_manager import EditorFloorManager
from .upload import FloorpackUploader

class EditFloorpacksControl(ArbitraryOptionsControlWithBackButton):
    # If the back option is selected, quit the game,
    # or if using both game and editor, go back to game/editor choice.

    def __init__(self, menu_visual_obj, CREATE_OPTION_ID: str, exit_option_id: str | None, upload_option_id: str | None):
        super().__init__(menu_visual_obj, exit_option_id)
        self.__CREATE_OPTION = CREATE_OPTION_ID
        self.__can_upload = upload_option_id is not None
        if self.__can_upload: self.__upload_option = upload_option_id
        self.__class__.__can_go_back = exit_option_id is not None

    def _choose_option(self):
        '''If the 'Create' option was selected, create a new floorpack.
        Otherwise, set the floor manager to start from the selected floor,
        and switch to selecting a floor.'''
        
        if self._option_id == self.__CREATE_OPTION:
            # Create floorpack.
            SFXPlayer.play_sfx('menu')
            return 'CreateFloorpackState'
        elif self.__can_upload and self._option_id == self.__upload_option:
            SFXPlayer.play_sfx('menu')
            FloorpackUploader.allow_upload()
            return 'UploadPromptState'

        # Edit floorpack.
        SFXPlayer.play_sfx('start')
        EditorFloorManager.select_floorpack(self._option_id)
        return 'EditFloorsState'
    
    @classmethod
    def back(cls):
        if cls.__can_go_back:
            SFXPlayer.play_sfx('back')
            return 3

class EditFloorsControl(ArbitraryOptionsControlWithBackButton):
    # If the back option is selected, go back to editing floorpacks.
    _STATE_AFTER_BACK = 'EditFloorpacksState'

    def __init__(self, menu_visual_obj,
                CREATE_OPTION_ID: str, MOVE_OPTION_ID: str, DELETE_OPTION_ID: str, BACK_OPTION_ID: str,
                download_option_id: str | None):
        super().__init__(menu_visual_obj, BACK_OPTION_ID)

        self.__CREATE_OPTION = CREATE_OPTION_ID
        self.__MOVE_OPTION = MOVE_OPTION_ID
        self.__DELETE_OPTION = DELETE_OPTION_ID

        self.__can_download = download_option_id is not None
        if self.__can_download: self.__download_option = download_option_id

    def _choose_option(self):
        '''If a floor was selected, start editing that floor.
        If the 'Create' option is selected, create a new floor and start editing it.
        If the 'Reorder' option is selected, switch to re-ordering floors.'''
        
        if self.__can_download and self._option_id == self.__download_option:
            SFXPlayer.play_sfx('menu')
            pack_path = EditorFloorManager.save_floorpack()
            platform.window.MM.download(pack_path)
            return
        match self._option_id:
            case self.__MOVE_OPTION:
                # Reorder floors
                SFXPlayer.play_sfx('menu')
                return 'SelectFloorToMoveState'
            case self.__DELETE_OPTION:
                # Delete a floor
                SFXPlayer.play_sfx('menu')
                return 'SelectFloorToDeleteState'
            case self.__CREATE_OPTION:
                # Create floor
                SFXPlayer.play_sfx('start')
                EditorFloorManager.create_floor()
                return 'EditState'
            case _:
                # Load floor
                SFXPlayer.play_sfx('start')
                floor_index = EditorFloorManager.index_from_floor_name(self._option_id)
                EditorFloorManager.select_floor_to_edit(floor_index)
                return 'EditState'

class MoveFloorControl(ArbitraryOptionsControlWithBackButton):
    # If the back option is selected, go back to selecting a floor to edit.
    _STATE_AFTER_BACK = 'EditFloorsState'
        
    def _choose_option(self):
        '''Proceed to selecting the new index for the selected floor.'''
 
        SFXPlayer.play_sfx('menu')
        floor_index = EditorFloorManager.index_from_floor_name(self._option_id)
        EditorFloorManager.select_floor_to_move(floor_index)
        return 'SelectFloorDestinationState'

class FloorDestinationControl(ArbitraryOptionsControlWithBackButton):
    # If the back option is selected, go back to selecting a floor to move.
    _STATE_AFTER_BACK = 'SelectFloorToMoveState'

    def __init__(self, menu_visual_obj, BACK_OPTION_ID: str, CANCEL_OPTION_ID: str):
        super().__init__(menu_visual_obj, BACK_OPTION_ID)
        self.__CANCEL_OPTION = CANCEL_OPTION_ID

    def _choose_option(self):
        '''If the 'Cancel' option was selected, go back to selecting a floor.
        Otherwise, move the previously selected floor to the new location.'''

        if self._option_id == self.__CANCEL_OPTION:
            SFXPlayer.play_sfx('back')
        else:
            SFXPlayer.play_sfx('move')
            if self._option_id == 'End': floor_index = EditorFloorManager.get_num_floors()
            else: floor_index = EditorFloorManager.index_from_floor_name(self._option_id)
            EditorFloorManager.move_selected_floor(floor_index)
            EditorFloorManager.save_floorpack()

        return 'EditFloorsState'
    
class SelectFloorToDeleteControl(ArbitraryOptionsControlWithBackButton):
    # If the back option is selected, go back to selecting a floor to edit.
    _STATE_AFTER_BACK = 'EditFloorsState'

    def _choose_option(self):
        '''Proceed to the confirmation on whether to delete the floor.'''

        SFXPlayer.play_sfx('menu')
        floor_index = EditorFloorManager.index_from_floor_name(self._option_id)
        EditorFloorManager.select_floor_to_delete(floor_index)
        return 'ConfirmDeleteFloorState'
    
class ConfirmDeleteFloorControl(KeyboardInputHandler):
    _ACTIONS = {
        pg.K_1 : ('delete',),
        pg.K_RETURN : ('delete',),
        pg.K_2 : ('cancel',),
        pg.K_BACKSPACE : ('cancel',),
        pg.K_ESCAPE : ('cancel',),
    }
    @staticmethod
    def delete():
        SFXPlayer.play_sfx('destroy')
        EditorFloorManager.delete_selected_floor()
        EditorFloorManager.save_floorpack()
        return 'EditFloorsState'
    
    @staticmethod
    def cancel():
        return 'EditFloorsState'