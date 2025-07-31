'''This script is for deploying a web build of the editor only.
It is for debugging purposes.'''
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
from src.config import OnlineConfig

def main():
    OnlineConfig.set_using_web(both_game_and_editor=False)
    initial_state = setup_state(True)
    window = setup_window(True)
    e = Editor(initial_state, window)
    asyncio.run(e.online_main())

if __name__ == '__main__':
    main()