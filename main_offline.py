'''This script runs the game. It can be executed with python,
and is also specified in the pyinstaller command used to create the
executable build.'''
from src.game.game import Game, setup_state, setup_window
if __name__ == '__main__':
    InitialState = setup_state()
    window = setup_window()
    g = Game(InitialState, window)
    g.main()