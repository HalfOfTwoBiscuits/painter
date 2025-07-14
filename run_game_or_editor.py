from src.game.game import Game
from src.editor.editor import Editor
from src.startup_utility import setup_state, setup_window, StartupMenu
from src.audio_utility import SFXPlayer

def main():
    running = True
    while running:
        STATE_NAME = 'StartupUtilityState'
        game_window = setup_window()
        s = StartupMenu(STATE_NAME, game_window)
        exit_code = s.main()
        match exit_code:
            case 3 | True:
                # Exit option or closing the window will exit
                running = False
            case 1:
                # First option opens the game
                SFXPlayer.play_sfx('menu')
                initial_state = setup_state()
                g = Game(initial_state, game_window)
                exit_code = g.main()
                if exit_code != 3: running = False
            case 2:
                # Second option opens the editor
                SFXPlayer.play_sfx('menu')
                initial_state = setup_state(editor=True)
                editor_window = setup_window(True)
                e = Editor(initial_state, editor_window)
                exit_code = e.main()
                if exit_code != 3: running = False

if __name__ == '__main__':
    main()