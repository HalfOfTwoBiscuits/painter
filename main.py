'''This script is for the web version of the game and editor.
To play the game use run_game.py,
use run_editor.py for the editor,
and use run_game_or_editor.py for a choice between both.
The guidelines for pygbag, the tool that creates the web build,
specified the script to do so should be called main.py,
so this file is named in that fashion.'''
# /// script
# dependencies = [
#   "pygame-ce",
#   "yaml",
#   "pygame_gui",
#   "i18n"
# ]
import asyncio
from src.game_and_editor import GameAndEditor
from src.config import OnlineConfig

def main():
    OnlineConfig.set_using_web(both_game_and_editor=True)
    e = GameAndEditor()
    asyncio.run(e.online_main())

if __name__ == '__main__':
    main()