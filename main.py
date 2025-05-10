from src.game.main import Game, setup_state, setup_window
import asyncio
if __name__ == '__main__':
    InitialState = setup_state()
    window = setup_window()
    g = Game(InitialState, window)
    asyncio.run(g.online_main())