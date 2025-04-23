from abc import abstractmethod

class VisualHandler:
    '''Has access to the window surface to draw graphics onto,
    and implements a draw() method.
    Visual handlers inherit from it.'''

    @classmethod
    def set_window(cls, window_surf):
        cls._window = window_surf
        cls._window_dimensions = window_surf.get_size()

    @abstractmethod
    @classmethod
    def draw(cls):
        ...