'''This script is intended for the use of pygbag, a tool for
creating web builds of pygame programs. The guidelines said that the
script to create the web build should be called main.py,
so despite the web build not currently working, this file is named in that fashion.
To play the game use offline_main.py'''
# /// script
# dependencies = [
#   "PyYAML",
#   "pygame-ce"
# ]
import asyncio
from src.game.game import Game, setup_state, setup_window

if __name__ == '__main__':
    InitialState = setup_state()
    window = setup_window()
    g = Game(InitialState, window)
    asyncio.run(g.online_main())