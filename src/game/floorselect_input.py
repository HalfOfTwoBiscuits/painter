from ..abstract_handlers import ArbitraryOptionsControlWithBackButton
from ..audio_utility import SFXPlayer
from ..floor_manager import FloorManager

class LevelSelectControl(ArbitraryOptionsControlWithBackButton):
    '''Input handler for floor selection.'''

    __back_option_is_exit_game = False

    def __init__(self, menu_visual_obj, back_option_id: str, is_only_one_floorpack: bool):
        super().__init__(menu_visual_obj, back_option_id)
        self.__class__.__back_option_is_exit_game = is_only_one_floorpack

    def select(self, number: int):
        '''If the 'Back' option was selected, return to the floorpack select.
        Otherwise, set the floor manager to start from the selected floor,
        and switch to the gameplay state.'''

        try: back_option_chosen = self._find_option_for_number(number)
        except ValueError: return
        if back_option_chosen: return self.back()
        
        floor_index = FloorManager.index_from_floor_name(self._option_id)
        # Select the floor and go to gameplay.
        FloorManager.select_floor(floor_index)
        SFXPlayer.play_sfx('start')
        return 'NewFloorState'
    
    @classmethod
    def back(cls):
        SFXPlayer.play_sfx('back')
        if cls.__back_option_is_exit_game: return 3
        else: return 'FloorpackSelectState'
    
class FloorpackSelectControl(ArbitraryOptionsControlWithBackButton):
    '''Input handler for floorpack selection.'''
    # Choosing the exit option will quit the game,
    # or if using both game and editor, go back to game/editor choice.
    _STATE_AFTER_BACK = 3

    def __init__(self, menu_visual_obj, EXIT_OPTION_ID: str):
        super().__init__(menu_visual_obj, EXIT_OPTION_ID)

    def select(self, number: int):
        '''Set the floor manager to use the selected floorpack,
        and switch to the floor select state.'''
        try: back_option_chosen = self._find_option_for_number(number)
        except ValueError: return
        if back_option_chosen: return self.back()

        # Select the floorpack corresponding to the option.
        FloorManager.select_floorpack(self._option_id)
        SFXPlayer.play_sfx('menu')
        return 'LevelSelectState'