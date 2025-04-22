class FloorVisual:
    @classmethod
    def setup(cls,level_obj):
        cls.__grid = level_obj.get_cell_grid()