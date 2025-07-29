class ExitOptionConfig:
    '''Class that stores whether the game can be exited or not,
    based on the web build.
    Could potentially be adapted to store other config information
    for access by game or editor states.'''
    __can_exit_game = True

    @classmethod
    def disable_exiting_game(cls):
        '''Set a flag so that states which inherit from this class
        will not include an option to exit the game.
        Used for the web build.'''
        cls.__can_exit_game = False
    
    @classmethod
    def can_exit_game(cls):
        return cls.__can_exit_game