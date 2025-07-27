import pygame_gui as gui
class GUIHandler:
    @classmethod
    def init(cls, window_size: tuple[int]):
        cls.__window_size = window_size
        cls.__ui = gui.UIManager(window_size)
        cls.__container = gui.elements.UIAutoResizingContainer((0,0,0,0))
        cls.__element_lookup = {}

    @classmethod
    def clear_elements(cls):
        del cls.__ui
        cls.__ui = gui.UIManager(cls.__window_size)

    @classmethod
    def process_event(cls, e):
        cls.__ui.process_events(e)

    @classmethod
    def update(cls, time_delta: float):
        cls.__ui.update(time_delta)

    @classmethod
    def draw(cls, window):
        cls.__ui.draw_ui(window)

    @classmethod
    def set_container(cls, x: int, y: int, w: int=0, h: int=0):
        cls.__container.set_dimensions((w,h))
        cls.__container.set_position((x,y))

    @classmethod
    def add_button(cls, id: str, location_rect, text: str=None):
        '''Add a button.'''
        if text is None: text = id.replace('_',' ')
        cls.__element_lookup[id] = \
        gui.elements.UIButton(relative_rect=location_rect,
                              text=text,
                              object_id=id,
                              manager=cls.__ui,
                              container=cls.__container)

    @classmethod
    def add_textinput(cls, id: str, location_rect, label: str=None, placeholder: str=None):
        '''Add a text input field and label beside it.'''
        label = label or id.replace('_',' ')
        x, y, w, h = location_rect
        LABEL_HEIGHT = cls.get_label_height()
        gui.elements.UILabel((x, y, w, LABEL_HEIGHT),label,
                             manager=cls.__ui, container=cls.__container)
        y += LABEL_HEIGHT

        cls.__element_lookup[id] = \
        gui.elements.UITextEntryLine(relative_rect=(x,y,w,h),
                                    placeholder_text=placeholder,
                                    object_id=id,
                                    manager=cls.__ui,
                                    container=cls.__container)
        
    @classmethod
    def get_elem(cls, id: str):
        return cls.__element_lookup[id]
    
    @classmethod
    def get_label_height(cls):
        return 30
    
    @classmethod
    def set_focus(cls, elem_id: str):
        cls.__ui.set_focus_set(cls.get_elem(elem_id))