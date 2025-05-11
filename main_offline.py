from src.game.game import Game, setup_state, setup_window
if __name__ == '__main__':
    InitialState = setup_state()
    window = setup_window()
    #asyncio.run(Game.main())
    g = Game(InitialState, window)
    g.main()