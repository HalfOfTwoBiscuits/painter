from ..abstract_handlers import ArbitraryOptionsControl
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
        
        SFXPlayer.play_sfx('menu')
        if option_id == self.__CREATE_OPTION:
            # Create floorpack.
            return 'CreateFloorpackState'

        # Edit floorpack.
        EditorFloorManager.select_floorpack(option_id)
        return 'EditFloorsState'

class EditFloorsControl(ArbitraryOptionsControl):
    def __init__(self, menu_visual_obj,
                CREATE_OPTION_ID: str, MOVE_OPTION_ID: str, BACK_OPTION_ID: str):
        super().__init__(menu_visual_obj)
        self.__BACK_OPTION = BACK_OPTION_ID
        self.__CREATE_OPTION = CREATE_OPTION_ID
        self.__MOVE_OPTION = MOVE_OPTION_ID

    def select(self, number: int):
        '''If a floor was selected, start editing that floor.
        If the 'Create' option is selected, create a new floor and start editing it.
        If the 'Reorder' option is selected, switch to re-ordering floors.
        If the 'Save' option is selected, save changes.
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
        
        SFXPlayer.play_sfx('start')
        if option_id == self.__CREATE_OPTION:
            # Create floor
            EditorFloorManager.create_floor()
            # TEMPORARY.
            EditorFloorManager.save_floorpack()
            return 'EditFloorsState'
        else:
            # Load floor
            floor_index = EditorFloorManager.index_from_floor_name(option_id)
            EditorFloorManager.select_floor(floor_index)

        # Begin editing
        return 'EditState'
    
class MoveFloorControl(ArbitraryOptionsControl):
    def __init__(self, menu_visual_obj, BACK_OPTION_ID: str):
        super().__init__(menu_visual_obj)
        self._BACK_OPTION = BACK_OPTION_ID
        self.__class__._variable_actions[pg.K_BACKSPACE] = ('back',)
        self.__class__._variable_actions[pg.K_ESCAPE] = ('back',)

    def _check_for_back_option(self, number: int):
        '''If the back option was selected, return True.
        If another option was selected, return False.
        If the selection was invalid, raise ValueError.'''

        # Small optimisation: make _find_option_for_number raise ValueError.
        self._option_id = self._find_option_for_number(number)
        if self._option_id is None: raise ValueError
        elif self._option_id == self._BACK_OPTION:
            SFXPlayer.play_sfx('back')
            return True
        return False
        
    def select(self, number: int):
        '''If the back option was selected, go back to selecting a floor to edit.
        Otherwise, proceed to selecting the new index for the floor.'''
        try: cancelling = self._check_for_back_option(number)
        except ValueError: return
        if cancelling: return 'EditFloorsState'

        SFXPlayer.play_sfx('menu')
        floor_index = EditorFloorManager.index_from_floor_name(self._option_id)
        EditorFloorManager.select_floor_to_move(floor_index)
        return 'SelectFloorDestinationState'
    
    @staticmethod
    def back():
        return 'EditFloorsState'

class FloorDestinationControl(MoveFloorControl):
    def __init__(self, menu_visual_obj, BACK_OPTION_ID: str):
        super().__init__(menu_visual_obj, BACK_OPTION_ID)
    
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
        return 'EditFloorsState'