from ..app import App
from ..game.floor_visual import FloorVisual
from .floor_data import FloorData
import pygame_gui

class Editor(App):
    def loop(self):
        # Process input, draw graphics, etc in the same way as the game
        super().loop()