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
from src.editor.editor import Editor
from src.startup_utility import setup_state, setup_window
from src.config import ExitOptionConfig

def main():
    ExitOptionConfig.disable_exiting_game()
    initial_state = setup_state(True)
    window = setup_window(True)
    e = Editor(initial_state, window)
    asyncio.run(e.online_main())

if __name__ == '__main__':
    main()