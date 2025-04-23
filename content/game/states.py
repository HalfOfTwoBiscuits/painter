from painter_input import PainterControl
from pause_input import PauseMenuControl
from painter_visual import PainterVisual
from floor_visual import FloorVisual
from pause_visual import PauseMenuVisual

class GameplayState:
    _INPUT_HANDLER = PainterControl
    _VISUAL_HANDLERS = (PainterVisual, FloorVisual)

class PauseMenuState:
    _INPUT_HANDLER = PauseMenuControl
    _VISUAL_HANDLERS = (PainterVisual, FloorVisual, PauseMenuVisual)