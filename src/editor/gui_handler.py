import pygame_gui as gui
class GUIHandler:
    @classmethod
    def init(cls, window_size: tuple[int]):
        cls.__window_size = window_size
        cls.__ui = gui.UIManager(window_size)
        cls.__container = gui.elements.UIAutoResizingContainer((0,0,0,0))

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
    def add_button(cls, id: str, location_rect: tuple[int], text: str=None):
        '''Add a button.'''
        if text is None: text = id
        gui.elements.UIButton(relative_rect=location_rect,
                              text=text,
                              object_id=id,
                              manager=cls.__ui,
                              container=cls.__container)

    @classmethod
    def add_textinput(cls, id: str, location_rect: tuple[int], placeholder: str=None):
        '''Add a text input field. Unused currently, a UIForm is used instead.'''
        gui.elements.UITextEntryLine(relative_rect=location_rect,
                                    placeholder_text=placeholder,
                                    object_id=id,
                                    manager=cls.__ui,
                                    container=cls.__container)

    @classmethod
    def add_form(cls, id: str, location_rect: tuple[int], questionaire: dict[str:str]):
        '''Add a form. Based on the questionnaire values, fields and a submit
        button are pre-created.'''
        gui.elements.UIForm(relative_rect=location_rect,
                            questionnaire=questionaire,
                            object_id=id,
                            manager=cls.__ui,
                            container=cls.__container)