from sudoku import Sudoku
import numpy as np


# Create an instance of the SudokuBoard class with a custom initial board
custom_board = np.array([
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
], dtype=int)

custom_board2 = np.array([
    [5, 0, 0, 4, 6, 7, 3, 0, 9],
    [9, 0, 3, 8, 1, 0, 4, 2, 7],
    [1, 7, 4, 2, 0, 3, 0, 0, 0],
    [2, 3, 1, 9, 7, 6, 8, 5, 4],
    [8, 5, 7, 1, 2, 4, 0, 9, 0],
    [4, 9, 6, 3, 0, 8, 1, 7, 2],
    [0, 0, 0, 0, 8, 9, 2, 6, 0],
    [7, 8, 2, 6, 4, 1, 0, 0, 5],
    [0, 1, 0, 0, 0, 0, 7, 0, 8]
], dtype=int)

sudoku = Sudoku(custom_board)

sudoku.display()

sudoku.display_solved_board()