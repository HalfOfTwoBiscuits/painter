from ..abstract_handlers import KeyboardInputHandler, ArbitraryOptionsControlWithBackButton
from ..audio_utility import SFXPlayer
from .editor_floor_manager import EditorFloorManager
import pygame as pg

class EditFloorpacksControl(ArbitraryOptionsControlWithBackButton):
    _STATE_AFTER_BACK = 3

    def __init__(self, menu_visual_obj, CREATE_OPTION_ID: str, EXIT_OPTION_ID: str):
        super().__init__(menu_visual_obj, EXIT_OPTION_ID)
        self.__CREATE_OPTION = CREATE_OPTION_ID

    def select(self, number: int):
        '''If the 'Create' option was selected, create a new floorpack.
        Otherwise, set the floor manager to start from the selected floor,
        and switch to selecting a floor.'''
        try: back_option_chosen = self._find_option_for_number(number)
        except ValueError: return
        if back_option_chosen: return self.back()
        
        if self._option_id == self.__CREATE_OPTION:
            # Create floorpack.
            SFXPlayer.play_sfx('menu')
            return 'CreateFloorpackState'

        # Edit floorpack.
        SFXPlayer.play_sfx('start')
        EditorFloorManager.select_floorpack(self._option_id)
        return 'EditFloorsState'

class EditFloorsControl(ArbitraryOptionsControlWithBackButton):
    _STATE_AFTER_BACK = 'EditFloorpacksState'
    def __init__(self, menu_visual_obj,
                CREATE_OPTION_ID: str, MOVE_OPTION_ID: str, DELETE_OPTION_ID: str, BACK_OPTION_ID: str):
        super().__init__(menu_visual_obj, BACK_OPTION_ID)

        self.__CREATE_OPTION = CREATE_OPTION_ID
        self.__MOVE_OPTION = MOVE_OPTION_ID
        self.__DELETE_OPTION = DELETE_OPTION_ID

    def select(self, number: int):
        '''If a floor was selected, start editing that floor.
        If the 'Create' option is selected, create a new floor and start editing it.
        If the 'Reorder' option is selected, switch to re-ordering floors.
        If the 'Back' option is selected, return to the floorpack selection.'''

        try: back_option_chosen = self._find_option_for_number(number)
        except ValueError: return
        if back_option_chosen: return self.back()
        
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
    _STATE_AFTER_BACK = 'EditFloorsState'
        
    def select(self, number: int):
        '''If the back option was selected, go back to selecting a floor to edit.
        Otherwise, proceed to selecting the new index for the floor.'''
        try: back_option_chosen = self._find_option_for_number(number)
        except ValueError: return
        if back_option_chosen: return self.back()
 
        SFXPlayer.play_sfx('menu')
        floor_index = EditorFloorManager.index_from_floor_name(self._option_id)
        EditorFloorManager.select_floor_to_move(floor_index)
        return 'SelectFloorDestinationState'

class FloorDestinationControl(ArbitraryOptionsControlWithBackButton):
    _STATE_AFTER_BACK = 'SelectFloorToMoveState'

    def __init__(self, menu_visual_obj, BACK_OPTION_ID: str, CANCEL_OPTION_ID: str):
        super().__init__(menu_visual_obj, BACK_OPTION_ID)
        self.__CANCEL_OPTION = CANCEL_OPTION_ID

    def select(self, number: int):
        '''If the back options was selected, go back to selecting a floor to edit.
        Otherwise, move the previously selected floor to the new location.'''

        try: back_option_chosen = self._find_option_for_number(number)
        except ValueError: return
        if back_option_chosen: return self.back()

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
    _STATE_AFTER_BACK = 'EditFloorsState'
    def select(self, number: int):
        try: back_option_chosen = self._find_option_for_number(number)
        except ValueError: return
        if back_option_chosen: return self.back()

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