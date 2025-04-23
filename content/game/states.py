from painter_input import PainterControl
from pause_input import PauseMenuControl
from painter_visual import PainterVisual
from floor_visual import FloorVisual
from pause_visual import PauseMenuVisual

class GameplayState:
    INPUT_HANDLER = PainterControl
    VISUAL_HANDLERS = (PainterVisual, FloorVisual)

class PauseMenuState:
    INPUT_HANDLER = PauseMenuControl
    VISUAL_HANDLERS = (PainterVisual, FloorVisual, PauseMenuVisual)