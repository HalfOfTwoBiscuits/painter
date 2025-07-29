'''This script is intended for the use of pygbag, a tool for
creating web builds of pygame programs. The guidelines said that the
script to create the web build should be called main.py,
so despite the web build not currently working, this file is named in that fashion.
To play the game use run_game.py'''
# /// script
# dependencies = [
#   "pygame-ce",
#   "yaml",
#   "pygame_gui",
#   "i18n"
# ]
import asyncio
from src.game_and_editor import GameAndEditor
from src.config import ExitOptionConfig

def main():
    ExitOptionConfig.disable_exiting_game()
    e = GameAndEditor()
    asyncio.run(e.online_main())

if __name__ == '__main__':
    main()