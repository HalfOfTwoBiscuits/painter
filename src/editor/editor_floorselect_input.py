from ..abstract_handlers import KeyboardInputHandler, ArbitraryOptionsControl, FloorManagementControl
from ..audio_utility import SFXPlayer
from .editor_floor_manager import EditorFloorManager
import pygame as pg

class EditFloorpacksControl(ArbitraryOptionsControl):
    def __init__(self, menu_visual_obj, CREATE_OPTION_ID: str):
        super().__init__(menu_visual_obj)
        self.__CREATE_OPTION = CREATE_OPTION_ID

    def select(self, number: int):
        '''If the 'Create' option was selected, create a new floorpack.
        Otherwise, set the floor manager to start from the selected floor,
        and switch to selecting a floor.'''

        option_id = self._find_option_for_number(number)
        if option_id is None: return
        
        if option_id == self.__CREATE_OPTION:
            # Create floorpack.
            SFXPlayer.play_sfx('menu')
            return 'CreateFloorpackState'

        # Edit floorpack.
        SFXPlayer.play_sfx('start')
        EditorFloorManager.select_floorpack(option_id)
        return 'EditFloorsState'

class EditFloorsControl(ArbitraryOptionsControl):
    def __init__(self, menu_visual_obj,
                CREATE_OPTION_ID: str, MOVE_OPTION_ID: str, DELETE_OPTION_ID: str, BACK_OPTION_ID: str):
        super().__init__(menu_visual_obj)
        self.__BACK_OPTION = BACK_OPTION_ID
        self.__CREATE_OPTION = CREATE_OPTION_ID
        self.__MOVE_OPTION = MOVE_OPTION_ID
        self.__DELETE_OPTION = DELETE_OPTION_ID

    def select(self, number: int):
        '''If a floor was selected, start editing that floor.
        If the 'Create' option is selected, create a new floor and start editing it.
        If the 'Reorder' option is selected, switch to re-ordering floors.
        If the 'Back' option is selected, return to the floorpack selection.'''

        option_id = self._find_option_for_number(number)
        if option_id is None: return
        
        elif option_id == self.__BACK_OPTION:
            # Return to floorpack selection
            SFXPlayer.play_sfx('menu')
            return 'EditFloorpacksState'
        elif option_id == self.__MOVE_OPTION:
            # Reorder floors
            SFXPlayer.play_sfx('menu')
            return 'SelectFloorToMoveState'
        elif option_id == self.__DELETE_OPTION:
            # Delete a floor
            SFXPlayer.play_sfx('menu')
            return 'SelectFloorToDeleteState'
        
        SFXPlayer.play_sfx('start')
        if option_id == self.__CREATE_OPTION:
            # Create floor
            EditorFloorManager.create_floor()
            # TEMPORARY.
            # Should go to edit, then save option in there will keep the floor.
            EditorFloorManager.save_floorpack()
            return 'EditFloorsState'
        else:
            # Load floor
            floor_index = EditorFloorManager.index_from_floor_name(option_id)
            EditorFloorManager.select_floor(floor_index)

        # Begin editing
        return 'EditState'

class MoveFloorControl(FloorManagementControl):
        
    def select(self, number: int):
        '''If the back option was selected, go back to selecting a floor to edit.
        Otherwise, proceed to selecting the new index for the floor.'''
        try: cancelling = self._check_for_back_option(number)
        except ValueError: return
        if cancelling: return self.back()

        SFXPlayer.play_sfx('menu')
        floor_index = EditorFloorManager.index_from_floor_name(self._option_id)
        EditorFloorManager.select_floor_to_move(floor_index)
        return 'SelectFloorDestinationState'

class FloorDestinationControl(MoveFloorControl):
    
    def select(self, number: int):
        '''If the back options was selected, go back to selecting a floor to edit.
        Otherwise, move the previously selected floor to the new location.'''
        try: cancelling = self._check_for_back_option(number)
        except ValueError: return
        if not cancelling:
            SFXPlayer.play_sfx('move')
            if self._option_id == 'End': floor_index = EditorFloorManager.get_num_floors()
            else: floor_index = EditorFloorManager.index_from_floor_name(self._option_id)
            EditorFloorManager.move_selected_floor(floor_index)
            EditorFloorManager.save_floorpack()

        return self.back()
    
class SelectFloorToDeleteControl(FloorManagementControl):

    def select(self, number: int):
        SFXPlayer.play_sfx('menu')
        try: cancelling = self._check_for_back_option(number)
        except ValueError: return
        if cancelling: return self.back()

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