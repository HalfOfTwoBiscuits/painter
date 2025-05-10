from ..game.floor_visual import FloorVisual
from ..game.main import Game
from .floor_data import FloorData
import pygame_gui

class Editor(Game):
    def loop(self):
        # Process input, draw graphics, etc in the same way as the game
        super().loop()