from menu_visual import MenuVisual

class PauseMenuVisual(MenuVisual):
    '''A menu where the player can restart the floor or quit to the floor select.'''

    # Options are constant.
    __PAUSE_OPTIONS = ['Continue', 'Restart Level', 'Exit (Not Implemented)']
    _options = __PAUSE_OPTIONS