class OnlineConfig:
    '''Class that stores whether the web version is being used or not.
    This determines whether the ingame exit option is available,
    and will later determine whether floorpack upload/download are available.'''
    __is_online = False
    __using_startup_menu_online = None

    @classmethod
    def set_using_web(cls, both_game_and_editor: bool):
        '''Set a flag so that states which inherit from this class
        will not include an option to exit the game.
        Used for the web build.'''
        cls.__is_online = True
        cls.__using_startup_menu_online = both_game_and_editor
    
    @classmethod
    def can_exit(cls, in_startup_menu: bool) -> bool:
        if cls.__is_online:
            if in_startup_menu:
                return False
            else:
                return cls.__using_startup_menu_online
        else:
            return True
        
    @classmethod
    def is_online(cls) -> bool:
        return cls.__is_online