class SudokuError(Exception):
    pass


class InvalidGrid(SudokuError):
    pass


class InvalidSolution(SudokuError):
    pass


class NoAvailableSolution(SudokuError):
    pass
