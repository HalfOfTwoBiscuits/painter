from ..abstract_handlers import ArbitraryOptionsControl
from ..audio_utility import SFXPlayer
from ..floor_manager import FloorManager

class LevelSelectControl(ArbitraryOptionsControl):
    '''Input handler for floor selection.'''
    def __init__(self, menu_visual_obj, BACK_OPTION_ID: str, EXIT_OPTION_ID: str):
        super().__init__(menu_visual_obj)
        self.__BACK_OPTION = BACK_OPTION_ID
        self.__EXIT_OPTION = EXIT_OPTION_ID

    def select(self, number: int):
        '''If the 'Back' option was selected, return to the floorpack select.
        Otherwise, set the floor manager to start from the selected floor,
        and switch to the gameplay state.'''

        option_id = self._find_option_for_number(number)
        if option_id is None: return
        
        elif option_id == self.__BACK_OPTION:
            # Selecting the 'Back' option will return to floorpack selection
            SFXPlayer.play_sfx('back')
            return 'FloorpackSelectState'
        elif option_id == self.__EXIT_OPTION:
            # Choosing the exit option will quit the game,
            # or if using both game and editor, go back to game/editor choice.
            SFXPlayer.play_sfx('back')
            return 3
        
        floor_index = FloorManager.index_from_floor_name(option_id)

        # Select the floor and go to gameplay.
        FloorManager.select_floor(floor_index)
        SFXPlayer.play_sfx('start')
        return 'NewFloorState'
    
class FloorpackSelectControl(ArbitraryOptionsControl):
    '''Input handler for floorpack selection.'''
    def __init__(self, menu_visual_obj, EXIT_OPTION_ID: str):
        super().__init__(menu_visual_obj)
        self.__EXIT_OPTION = EXIT_OPTION_ID

    def select(self, number: int):
        '''Set the floor manager to use the selected floorpack,
        and switch to the floor select state.'''
        option_id = self._find_option_for_number(number)
        if option_id is None: return
        elif option_id == self.__EXIT_OPTION:
            # Choosing the exit option will quit the game,
            # or if using both game and editor, go back to game/editor choice.
            return 3
        # Select the floorpack corresponding to the option.
        FloorManager.select_floorpack(option_id)
        SFXPlayer.play_sfx('menu')
        return 'LevelSelectState'