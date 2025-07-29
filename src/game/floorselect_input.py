from ..abstract_handlers import ArbitraryOptionsControlWithBackButton
from ..audio_utility import SFXPlayer
from ..floor_manager import FloorManager

class LevelSelectControl(ArbitraryOptionsControlWithBackButton):
    '''Input handler for floor selection.'''

    # 1 : No back option
    # 2 : Exit game
    # 3 : Back to floorpack select
    __back_option_type = 0

    def __init__(self, menu_visual_obj, back_option_id: str, is_only_one_floorpack: bool):
        super().__init__(menu_visual_obj, back_option_id)
        if back_option_id is None: back_option_type = 1
        elif is_only_one_floorpack: back_option_type = 2
        else: back_option_type = 3
        self.__class__.__back_option_type = back_option_type

    def _choose_option(self):
        '''If a floor was selected,
        set the floor manager to start from that floor,
        and switch to the gameplay state.'''
        
        floor_index = FloorManager.index_from_floor_name(self._option_id)
        # Select the floor and go to gameplay.
        FloorManager.select_floor(floor_index)
        SFXPlayer.play_sfx('start')
        return 'NewFloorState'
    
    @classmethod
    def back(cls):
        if cls.__back_option_type > 1:
            SFXPlayer.play_sfx('back')
            if cls.__back_option_type == 2: return 3
            else: return 'FloorpackSelectState'
    
class FloorpackSelectControl(ArbitraryOptionsControlWithBackButton):
    '''Input handler for floorpack selection.'''

    # If the back option is selected, quit the game,
    # or if using both game and editor, go back to game/editor choice.
    _STATE_AFTER_BACK = 3

    def __init__(self, menu_visual_obj, EXIT_OPTION_ID: str):
        super().__init__(menu_visual_obj, EXIT_OPTION_ID)

    def _choose_option(self):
        '''Set the floor manager to use the selected floorpack,
        and switch to the floor select state.'''

        # Select the floorpack corresponding to the option.
        FloorManager.select_floorpack(self._option_id)
        SFXPlayer.play_sfx('menu')
        return 'LevelSelectState'