import importlib
import numpy as np
from sudoku_game import constants
from sudoku_game import exceptions


class BaseSolver:
    def is_valid_value(self, grid, value):
        return np.count_nonzero(grid == value) != 9

    def is_valid_row(self, grid, x, value):
        if grid[x].all():
            return False
        return not (grid[x] == value).any()

    def is_valid_col(self, grid, y, value):
        if grid[:, y].all():
            return False
        return not (grid[:, y] == value).any()

    def is_valid_location(self, grid, x, y, value):
        return not grid[x, y]

    def is_valid_square(self, grid, x, y, value):
        row = (x // 3) * 3
        col = (y // 3) * 3
        square = grid[row:row+3, col:col+3]
        if square.all():
            return False
        return not (square == value).any()

    def is_valid_location_value(self, grid, x, y, value):
        return all((
            self.is_valid_value(grid, value),
            self.is_valid_location(grid, x, y, value),
            self.is_valid_row(grid, x, value),
            self.is_valid_col(grid, y, value),
            self.is_valid_square(grid, x, y, value),
        ))

    def solve_location(self, grid, x, y):
        if grid[x, y]:
            return []

        pos_numbers = []

        numbers = constants.NUMBERS.copy()
        np.random.shuffle(numbers)
        for value in numbers:
            is_valid = self.is_valid_location_value(
                grid, x, y, value)
            if is_valid:
                pos_numbers.append(value)
        return pos_numbers


class Solver(BaseSolver):
    pass


DEFAULT_SOLVER = Solver


def get_solver(path=None):
    if path is None:
        return DEFAULT_SOLVER
    class_name = path.split('.')[-1]
    module_path = '.'.join([i for i in path.split('.')][:-1])
    solvers = importlib.import_module(module_path)
    solver = getattr(solvers, class_name)
    return solver
