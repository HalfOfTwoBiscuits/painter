import pygame_gui as gui
class GUIHandler:
    @classmethod
    def init(cls, window_size: tuple[int]):
        cls.__ui = gui.UIManager(window_size)
        cls.__elements = {}

    @classmethod
    def update(cls, e):
        cls.__ui.process_events(e)

    @classmethod
    def add_button(cls, id: str, location_rect, text: str=None):
        if text is None: text = id
        button = gui.elements.UIButton(relative_rect=location_rect,
                                       text=text,
                                       manager=cls.__ui)
        cls.__elements[id] = button

    @classmethod
    def get_element(cls, id: str):
        return cls.__elements[id]
    
class GUIElementDatum():
    ...