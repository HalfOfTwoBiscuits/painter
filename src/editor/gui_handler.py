import pygame_gui as gui
class GUIHandler:
    @classmethod
    def init(cls, window_size: tuple[int]):
        cls.__ui = gui.UIManager(window_size)
        cls.__elements = {}
        cls.__ids_pressed = set()

    @classmethod
    def process_event(cls, e):
        if e.type == gui.UI_BUTTON_PRESSED:
            # Add to ids_pressed, or consider using .bind() instead?
            ...
        cls.__ui.process_events(e)

    @classmethod
    def add_button(cls, id: str, location_rect, text: str, command: exec):
        button = gui.elements.UIButton(relative_rect=location_rect,
                                       text=text,
                                       manager=cls.__ui)
        cls.__elements[id] = button