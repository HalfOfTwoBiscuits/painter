from src.editor.editor import Editor
from src.startup_utility import setup_state, setup_window

def main():
    initial_state = setup_state(editor=True)
    window = setup_window(True)
    e = Editor(initial_state, window)
    e.main()

if __name__ == '__main__':
    main()