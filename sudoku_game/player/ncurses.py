import time
import curses
from curses.textpad import rectangle
import argparse

from sudoku_game.game import Game
from sudoku_game import handlers
from sudoku_game import solvers

MOVES = {
    curses.KEY_LEFT: (0, -1),
    curses.KEY_UP: (-1, 0),
    curses.KEY_RIGHT: (0, 1),
    curses.KEY_DOWN: (1, 0),
}
ACTIONS = {
    113: 'quit',
    114: 'redo',
    115: 'solve',
    117: 'undo',
}
NUMBERS = list(range(49, 57))
ACTION_KEYS = list(MOVES) + list(ACTIONS) + NUMBERS

TEMP_ROW = ' '.join(["%s"] * 9)
RAW_NUMBERS = range(1, 10)


def curses_main(stdscr, seed=None, solver=None, keep_history=True):
    stdscr.clear()

    cursor_x, cursor_y = 0, 0

    if solver is not None:
        stdscr.addstr(9, 23, '(s)olve')
    if keep_history:
        stdscr.addstr(2, 13, '(u)ndo')
        stdscr.addstr(3, 13, '(r)edo')
    stdscr.addstr(10, 23, '(q)uit')

    handler = handlers.Handler()
    grid, solution = handler.generate_grid(60)
    game = Game(grid=grid, keep_history=keep_history)
    rectangle(stdscr, 0, 0, 1+9, 2+18)

    while 1:
        box_cursor_y, box_cursor_x = cursor_y // 3, cursor_x // 3
        stdscr.addstr(1, 23, 'Cursor: %s,%s %s,%s' % (cursor_y, cursor_x, box_cursor_y, box_cursor_x))
        stdscr.addstr(3, 23, 'Posibilities:')
        ## line
        line_nums = game.grid[cursor_x][game.grid[cursor_x] != 0]
        line_pos = list(set(RAW_NUMBERS) - set(line_nums))
        stdscr.addstr(4, 24, 'Line: %s' % sorted(line_pos))
        ## col
        col_nums = game.grid[:, cursor_y][game.grid[:, cursor_y] != 0]
        col_pos = list(set(RAW_NUMBERS) - set(col_nums))
        stdscr.addstr(5, 24, 'Cols: %s' % sorted(col_pos))
        ## box
        box_x, box_y = box_cursor_x * 3, box_cursor_y * 3
        box = game.grid[box_x:box_x+3, box_y:box_y+3]
        box_nums = box[game.grid[box_x:box_x+3, box_y:box_y+3] != 0]
        box_pos = list(set(RAW_NUMBERS) - set(box_nums))
        stdscr.addstr(6, 24, 'Box: %s' % sorted(box_pos))
        ## cursor location
        cursor_pos = []
        if not game.grid[cursor_x, cursor_y]:
            cursor_pos += list(
                set(line_pos) &
                set(col_pos) &
                set(box_pos)
            )
        stdscr.addstr(7, 24, 'Loc: %s' % sorted(cursor_pos))

        # Write grid
        for i, raw_row in enumerate(game.grid):
            row = [(str(i) if i else ' ')
                   for i in raw_row]
            stdscr.addstr(i+1, 2, TEMP_ROW % tuple(row))
        val = game.grid[cursor_x, cursor_y] or ' '
        stdscr.addstr(
            1+cursor_x,
            2+cursor_y*2,
            str(val),
            curses.A_REVERSE
        )

        reward = 0
        while 1:
            key = stdscr.getch()
            stdscr.addstr(1, 13, str(key))
            if key in ACTION_KEYS:
                break

        if key in MOVES:
            mov_x, mov_y = MOVES[key]
            cursor_x += mov_x
            cursor_x = min(8, max(cursor_x, 0))
            cursor_y += mov_y
            cursor_y = min(8, max(cursor_y, 0))
        elif key == 113:
            raise KeyboardInterrupt()
        elif key in NUMBERS:
            value = key - 48
            game.set_value(cursor_x, cursor_y, value)
        elif key == 114 and keep_history:
            game.redo()
        elif key == 117 and keep_history:
            game.undo()
        elif key == 115:
            pos = solver.solve_location(grid, cursor_x, cursor_y)
            if len(pos) == 0:
                continue
            elif len(pos) > 1:
                continue
            else:
                grid[cursor_x, cursor_y] = pos[0]

        if reward:
            stdscr.addstr(8, 6, '+%d' % reward)
        else:
            stdscr.addstr(8, 6, ' '*10)

        if game.game_over():
            stdscr.addstr(9, 0, 'GAME OVER')
            stdscr.getch()
            time.sleep(3)
            break

        stdscr.refresh()

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--seed', type=int)

def main(**kwargs):
    try:
        curses.wrapper(
            curses_main,
            seed=kwargs.get('seed'),
            solver=kwargs.get('solver') or solvers.get_solver()(),
            keep_history=kwargs.get('keep_history'),
        )
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    args = parser.parse_args()
    main(
        seed=args.seed,
    )
