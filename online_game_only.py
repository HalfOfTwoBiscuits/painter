'''This script is for deploying a web build of the game only.
It is for debugging purposes.'''
# /// script
# dependencies = [
#   "pygame-ce",
#   "yaml",
# ]
import asyncio
from src.game.game import Game
from src.startup_utility import setup_state, setup_window
from src.config import OnlineConfig

def main():
    OnlineConfig.set_using_web(both_game_and_editor=False)
    initial_state = setup_state()
    window = setup_window()
    g = Game(initial_state, window)
    asyncio.run(g.online_main())

if __name__ == '__main__':
    main()