from .audio_utility import SFXPlayer
from .floor_manager import FloorManager
from .game.game import Game
from .editor.editor import Editor
from .app import App
from .startup_utility import setup_window, setup_state, StartupMenu

class GameAndEditor(App):
    def __init__(self):
        '''Create StartupMenu, Game, and Editor instances
        and store them for later use.'''
        STARTUP_INITIAL_STATE = 'StartupUtilityState'

        self.__game_window = setup_window()
        self.__game_initial_state = setup_state()
        self.__editor_initial_state = setup_state(editor=True)
        self.__editor_window = setup_window(True)

        self.__startup_menu = StartupMenu(STARTUP_INITIAL_STATE, self.__game_window)
        self.__app = self.__startup_menu
        self.__starting_up = True

    def loop(self):
        '''Overrides the usual main loop to delegate to the
        main loops of the StartupMenu, Game, and Editor.
        Forms a menu where the user chooses one to boot.'''
        exit_code = self.__app.loop()
        match exit_code:
            case True:
                # Closing the window will exit
                return True
            case 3:
                # Choosing ingame exit option will exit
                # or return to game/editor selection.
                if self.__starting_up: return True
                else:
                    self.__app = self.__startup_menu
                    self.__starting_up = True
            case 1:
                # First option opens the game
                self.__start_app()
            case 2:
                # Second option opens the editor
                self.__start_app(editor=True)

    def __start_app(self, editor: bool=False):
        SFXPlayer.play_sfx('menu')
        if editor:
            app = Editor(self.__editor_initial_state, self.__editor_window)
        else:
            app = Game(self.__game_initial_state, self.__game_window)
        self.__app = app
        self.__starting_up = False