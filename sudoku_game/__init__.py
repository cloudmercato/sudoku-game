"""Package for Sudoku Game logic."""
VERSION = (0, 1)
__version__ = '.'.join([str(i) for i in VERSION])
__email__ = 'anthony@cloud-mercato.com'
__author__ = 'Anthony Monthe'
__url__ = 'https://github.com/cloudmercato/sudoku-game'
__license__ = 'BSD'

from .game import Game
