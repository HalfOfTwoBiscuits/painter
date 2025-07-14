'''This script runs the game. It can be executed with python,
and is also specified in the pyinstaller command used to create the
executable build.'''
from src.game.game import Game
from src.startup_utility import setup_state, setup_window

def main():
    initial_state = setup_state()
    window = setup_window()
    g = Game(initial_state, window)
    g.main()

if __name__ == '__main__':
    main()