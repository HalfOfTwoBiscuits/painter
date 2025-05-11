'''This script creates four FloorData objects and saves them as the floorpack dummy.yaml.
It is used to create the levels played in the current version of the game.
In future, I hope to create a level editor that outputs FloorData objects into these yaml floorpacks,
and a game state for a menu used to select which one to play.'''
from src.file_utility import FileUtility
from src.editor.floor_data import FloorData
import yaml

def create():
    f1 = FloorData(4,3) # 4x3 level
    f1.set_initial_painter_position((1,1))

    # Some cells start filled
    cells = f1.get_cell_grid()
    cells[(0,2)].start_filled()
    cells[(2,1)].start_filled()

    f2 = FloorData(3,5) # 3x5 level
    f2.set_initial_painter_position((1,3))

    cells = f2.get_cell_grid()
    cells[(2,2)].start_filled()

    f3 = FloorData(4,4)
    f3.set_initial_painter_position((1,1))

    cells = f3.get_cell_grid()
    cells[(0,2)].start_filled()
    cells[(1,2)].start_filled()
    cells[(2,2)].start_filled()
    cells[(2,3)].start_filled()
    cells[(2,1)].start_filled()
    cells[(2,0)].start_filled()

    f4 = FloorData(6,3)
    f4.set_initial_painter_position((1,1))

    cells = f4.get_cell_grid()
    cells[(0,0)].start_filled()
    cells[(5,0)].start_filled()
    cells[(2,1)].start_filled()
    return [f1,f2,f3,f4]

def save(floor_objects, packname: str):
    pack_path = FileUtility.path_to_resource('floors', packname)
    with open(pack_path, 'w') as file:
        yaml.dump(floor_objects, file)

if __name__ == '__main__':
    floors = create()
    save(floors, 'dummy')
