from src.game.game import Game
from src.editor.editor import Editor
from src.startup_utility import setup_state, setup_window, StartupMenu

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
                initial_state = setup_state()
                g = Game(initial_state, game_window)
                g.main()
            case 2:
                # Second option opens the editor
                initial_state = setup_state(editor=True)
                editor_window = setup_window(True)
                e = Editor(initial_state, editor_window)
                e.main()
            

if __name__ == '__main__':
    main()