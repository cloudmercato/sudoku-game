import numpy as np
from sudoku_game import generators


class Handler:

    def generate_grid(self, remove=0):
        generator = generators.Generator()
        grid, solution = generator.generate_grid(remove=remove)
        return grid, solution

    def solve_grid(self, grid):
        # while np.count_nonzero(grid != 0):
        #     x = np.random.choice(np.arange(9))
        #     y = np.random.choice(np.arange(9))
        #     self._find_value(grid, x, y)

        # for i in np.arange(9):
        #     x = y = i
        #     self._find_value(grid, x, y)

        # squares = [
        #     (i, j) for i in np.arange(3)
        #     for j in np.arange(3)
        # ] + [
        #     (i, j) for i in np.arange(3, 6)
        #     for j in np.arange(3, 6)
        # ] + [
        #     (i, j) for i in np.arange(6, 9)
        #     for j in np.arange(6, 9)
        # ]
        # for x, y in squares:
        #     self._find_value(grid, x, y)

        # for i in np.arange(9):
        #     rows = np.arange(9)[::-1]
        #     cols = np.arange(i, 9+i)
        #     for x, y in list(zip(rows, cols))[:-i]:
        #         print(grid)
        #         self._find_value(grid, x, y)

        rows = np.arange(9)
        np.random.shuffle(rows)
        cols = np.arange(9)
        np.random.shuffle(cols)
        for x in rows:
            for y in cols:
                self._find_value(grid, x, y)
        return grid

        # rows = np.arange(9)
        # # np.random.shuffle(rows)
        # cols = np.arange(9)
        # # np.random.shuffle(cols)
        # for x in rows:
        #     for y in cols:
        #         print(grid)
        #         self._find_value(grid, x, y)
