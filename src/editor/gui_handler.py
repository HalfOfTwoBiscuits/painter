import pygame_gui as gui
class GUIHandler:
    @classmethod
    def init(cls, window_size: tuple[int]):
        cls.__ui = gui.UIManager(window_size)
        # Same index links element with ID.
        cls.__elements = []
        cls.__element_ids = []
        cls.__container = gui.elements.UIAutoResizingContainer((0,0,0,0))
        cls.set_topleft(0,0)

    @classmethod
    def update(cls, e):
        cls.__ui.process_events(e)

    @classmethod
    def set_topleft(cls, x: int, y: int):
        cls.__container.set_dimensions((x,y,0,0))

    @classmethod
    def add_button(cls, id: str, location_rect, text: str=None):
        '''Add a button.'''
        if text is None: text = id
        button = gui.elements.UIButton(relative_rect=location_rect,
                                       text=text,
                                       manager=cls.__ui,
                                       container=cls.__container)
        cls.__store_elem(button, id)

    @classmethod
    def add_textinput(cls, id: str, location_rect, placeholder: str=None):
        '''Add a text input field.'''
        inp = gui.elements.UITextEntryLine(relative_rect=location_rect,
                                           placeholder_text=placeholder,
                                           manager=cls.__ui,
                                           container=cls.__container)
        cls.__store_elem(inp)

    @classmethod
    def add_form(cls, id: str, location_rect, questionaire: dict[str:str]):
        '''Add a form. Based on the questionnaire values, fields and a submit
        button are pre-created.'''
        frm = gui.elements.UIForm(relative_rect=location_rect,
                                  questionnaire=questionaire,
                                  manager=cls.__ui_manager,
                                  container=cls.__container)
        cls.__store_elem(frm)
    @classmethod
    def __store_elem(cls, element, id: str):
        cls.__elements.append(element)
        cls.__element_ids.append(id)

    @classmethod
    def id_for(cls, elem_obj):
        index = cls.__elements.index(elem_obj)
        return cls.__element_ids[index]
    
    @classmethod
    def get_element(cls, id: str):
        index = cls.__element_ids.index(id)
        return cls.__elements[index]