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
    def set_dimensions(cls, x: int, y: int, w: int=0, h: int=0):
        cls.__container.set_dimensions((x,y,w,h))

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
        cls.__store_elem(inp, id)

    @classmethod
    def add_form(cls, id: str, location_rect, questionaire: dict[str:str]):
        '''Add a form. Based on the questionnaire values, fields and a submit
        button are pre-created.'''
        frm = gui.elements.UIForm(relative_rect=location_rect,
                                  questionnaire=questionaire,
                                  manager=cls.__ui_manager,
                                  container=cls.__container)
        cls.__store_elem(frm, id)

    @classmethod
    def __store_elem(cls, element, id: str):
        '''Store an element in the list of elements.
        The given ID will have the same index in a separate list,
        so that if the ID is stored outside the class, the element
        can be retrieved.
        (I think there's actually a built-in version of this in pygame-gui
        that adds the ID to the event, that might be better in a refactor.)'''
        cls.__elements.append(element)
        cls.__element_ids.append(id)

    @classmethod
    def id_for(cls, elem_obj):
        '''Get the ID corresponding to the element object from an event involving it.'''
        index = cls.__elements.index(elem_obj)
        return cls.__element_ids[index]
    
    @classmethod
    def get_element(cls, id: str):
        '''Get the element with the given ID.
        If there is more than one element with that ID, will go by order created.'''
        index = cls.__element_ids.index(id)
        return cls.__elements[index]