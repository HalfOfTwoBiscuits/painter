import pygame as pg
from os import path

class SFXPlayer:
    __SFX_DIR_RELATIVE_PATH = 'sfx'
    __FILE_TYPE = '.ogg'
    __sfx = {}

    @classmethod
    def play_sfx(cls, sfx_name: str):
        '''Play a sound effect with the given filename.'''

        # Lazy initialisation:
        # if the sfx hasn't been played before, load the file and store it.
        if sfx_name not in cls.__sfx:
            cls.__load_sfx(sfx_name)
        # Play stored SFX
        cls.__sfx[sfx_name].play()

    @classmethod
    def __load_sfx(cls, sfx_name: str):
        '''Method used to load SFX files with the given filename.'''

        # Create path to the file
        sfx_path = path.join(cls.__SFX_DIR_RELATIVE_PATH, sfx_name + cls.__FILE_TYPE)
        # Create and store SFX object.
        # Assumes file exists, because the sfx_name argument is always explicitly specified in the code
        sfx_obj = pg.mixer.Sound(sfx_path)
        cls.__sfx[sfx_name] = sfx_obj