import numpy as np
from random import sample

class Generator:
    def generate_solution(self, flatten=False):
        grid = np.zeros((9, 9))

        base = 3
        side = base*base

        def pattern(r, c):
            return (base*(r%base)+r//base+c)%side
        def shuffle(s):
            return sample(s, len(s))

        rBase = range(base)
        rows = [g*base+r for g in shuffle(rBase)
                for r in shuffle(rBase)]
        cols = [g*base+c for g in shuffle(rBase)
                for c in shuffle(rBase)]
        nums = shuffle(range(1, base*base+1))

        solution = np.array([
            [nums[pattern(r, c)] for c in cols]
            for r in rows
        ])
        if flatten:
            return solution.flatten()
        return solution

    def generate_solutions(self, number, flatten=True):
        return (
            self.generate_solution(flatten=True)
            for i in range(number)
        )

    def generate_grid(self, remove=0):
        solution = self.generate_solution()
        grid = solution.copy()
        for i in range(remove):
            x = np.random.choice(np.arange(9))
            y = np.random.choice(np.arange(9))
            grid[x, y] = 0
        return grid, solution
