from src.editor.editor import Editor
from src.startup_utility import setup_state, setup_window
if __name__ == '__main__':
    InitialState = setup_state(editor=True)
    window = setup_window(True)
    e = Editor(InitialState, window)
    e.main()