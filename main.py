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