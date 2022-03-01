from multiprocessing import Pool
import numpy as np
from random import sample


def remove(x, removed=1):
    """Remove a random numbers from a grid"""
    for i in range(removed):
        v = np.random.randint(81)
        x[v] = 0


class Generator:
    def generate_solution(self, flatten=False):
        grid = np.zeros((9, 9))

        base = 3
        side = base*base

        def pattern(r, c):
            return (base*(r%base)+r//base+c)%side
        def shuffle(s):
            return sample(s, len(s))

        r_base = range(base)
        rows = [g*base+r for g in shuffle(r_base)
                for r in shuffle(r_base)]
        cols = [g*base+c for g in shuffle(r_base)
                for c in shuffle(r_base)]
        nums = shuffle(range(1, base*base+1))

        solution = np.array([
            [nums[pattern(r, c)] for c in cols]
            for r in rows
        ])
        if flatten:
            return solution.flatten()
        return solution

    def generate_solutions(self, number, flatten=True, processes=4):
        with Pool(processes=processes) as pool:
            results = [
                pool.apply_async(
                    func=self.generate_solution,
                    kwds={'flatten': True},
                )
                for i in np.arange(number)
            ]
            return [r.get() for r in results]

    def generate_grid(self, remove=0):
        if not hasattr(remove, '__getitem__'):
            remove = [remove, remove+1]

        solution = self.generate_solution()
        grid = solution.copy()
        for i in range(max(remove)):
            x = np.random.choice(np.arange(9))
            y = np.random.choice(np.arange(9))
            grid[x, y] = 0
        return grid, solution
