from .audio_utility import SFXPlayer
from .game.game import Game
from .editor.editor import Editor
from .app import App
from .startup_utility import setup_window, setup_state, StartupMenu

class GameAndEditor(App):
    def __init__(self):
        '''Create StartupMenu, Game, and Editor instances
        and store them for later use.'''
        STARTUP_INITIAL_STATE = 'StartupUtilityState'

        game_window = setup_window()
        self.__s = StartupMenu(STARTUP_INITIAL_STATE, game_window)

        game_initial_state = setup_state()
        self.__g = Game(game_initial_state, game_window)

        editor_initial_state = setup_state(editor=True)
        editor_window = setup_window(True)
        self.__e = Editor(editor_initial_state, editor_window)

        self.__app = self.__s
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
                    self.__app = self.__s
                    self.__starting_up = True
            case 1:
                # First option opens the game
                SFXPlayer.play_sfx('menu')
                self.__app = self.__g
                self.__starting_up = False
            case 2:
                # Second option opens the editor
                SFXPlayer.play_sfx('menu')
                self.__app = self.__e
                self.__starting_up = False