from ..abstract_handlers import TextDisplayVisualHandler

class UploadPromptVisual(TextDisplayVisualHandler):
    _TEXT =\
        'Select a floorpack file above,\n'\
        'or press backspace/escape/right click to cancel.\n'\
        'If you already chose a file,\n'\
        'you can still cancel the upload before it finishes.'