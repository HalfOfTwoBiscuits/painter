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

        self.__game_window = setup_window()
        self.__s = StartupMenu(STARTUP_INITIAL_STATE, self.__game_window)

        game_initial_state = setup_state()
        self.__g = Game(game_initial_state, self.__game_window)

        editor_initial_state = setup_state(editor=True)
        editor_window = setup_window(True)
        self.__e = Editor(editor_initial_state, editor_window)

    def loop(self):
        '''Overrides the usual main loop to delegate to the
        main loops of the StartupMenu, Game, and Editor.
        Forms a menu where the user chooses one to boot.'''
        exit_code = self.__s.main()
        match exit_code:
            case 3 | True:
                # Exit option or closing the window will exit
                return False
            case 1:
                # First option opens the game
                SFXPlayer.play_sfx('menu')
                exit_code = self.__g.main()
                # An exit code of 3 means the ingame exit option was chosen.
                # That means we should continue running, to ask whether to boot
                # the editor or close the window.
                if exit_code != 3: return True
            case 2:
                # Second option opens the editor
                SFXPlayer.play_sfx('menu')
                exit_code = self.__e.main()
                if exit_code != 3: return True