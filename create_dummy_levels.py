from src.game.floor_data import FloorData
from src.file_utility import FileUtility
from os import path
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

    f3 = FloorData(6,3)
    f3.set_initial_painter_position((1,1))

    cells = f3.get_cell_grid()
    cells[(0,0)].start_filled()
    cells[(5,0)].start_filled()
    cells[(2,1)].start_filled()
    return [f1,f2,f3]

def save(floor_objects, packname: str):
    pack_path = FileUtility.path_to_resource('floors', packname)
    with open(pack_path, 'x') as file:
        yaml.dump(floor_objects, file)

if __name__ == '__main__':
    floors = create()
    save(floors, 'dummy')
