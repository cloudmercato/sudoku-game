from setuptools import setup, find_packages
import sudoku_game


def read_file(name):
    with open(name) as fd:
        return fd.read()

setup(
    name="sudoku-game",
    version=sudoku_game.__version__,
    author=sudoku_game.__author__,
    author_email=sudoku_game.__email__,
    description=sudoku_game.__doc__,
    url=sudoku_game.__url__,
    license=sudoku_game.__license__,
    py_modules=['sudoku_game'],
    packages=find_packages(),
    install_requires=read_file('requirements.txt').splitlines(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        'Operating System :: OS Independent',
        "Programming Language :: Python",
    ],
    long_description=read_file('README.rst'),
    entry_points={'console_scripts': [
        'sudoku = sudoku_game.console:main',
    ]},
)
