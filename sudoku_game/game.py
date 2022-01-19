import numpy as np


class Game:
    def __init__(self, grid=None, keep_history=False):
        self.grid = np.zeros((9, 9)) if grid is None else grid

    def reset(self):
        self.grid = np.zeros((9, 9))
        
    def set_value(self, x, y, value):
        self.grid[x][y] = value

    def game_over(self):
        return self.grid.all()
