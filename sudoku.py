import numpy as np

class Sudoku:
    def __init__(self, initial_board, help=True) -> None:
        self.help = help
        
        if initial_board is None:
            raise ValueError("Invalid initial board. Initial board cannot be None.")
        else:
            if initial_board.shape == (9, 9) and np.all((0 <= initial_board) & (initial_board <= 9)):
                self.board = initial_board
                self.copy_board = np.copy(initial_board)
                
                if self.solve():
                    # there was a solution for the iniital_board
                    self.initial_board = initial_board
                    self.resolved_board = self.board
                    self.board = self.copy_board
                else:
                    raise ValueError("Invalid initial board. It doesn't have a solution or has multiple solutions.")
            else:
                raise ValueError("Invalid initial board. It must be a 9x9 NumPy array with values between 0 and 9.")          
        
    
    def display(self):
        # Display the sudoky board
        for row in range(0,9):
            if row%3 == 0:
                print("-"*25)
            for col in range(0,9):
                if col%3 == 0:
                    print("|", end=" ")
                print(self.board[row][col], end=" ")
            print("|")
        print("-"*25)
        
    
    def display_solved_board(self):
        # Display the sudoku board
        for row in range(0,9):
            if row%3 == 0:
                print("-"*25)
            for col in range(0,9):
                if col%3 == 0:
                    print("|", end=" ")
                print(self.resolved_board[row][col], end=" ")
            print("|")
        print("-"*25)
        
    
    def is_valid_move(self, row, col, num) -> bool:
        # Checks if the number is already in the row or column
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False
            
        # Check if the numbe is already in the 3x3 grid
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        
        for i in range(3):
            for j in range(3):
                if self.board[box_row + i][box_col + j] == num:
                    return False
                
        return True
    
    
    def __find_empty_cell(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
                
        return None
    
    
    def solve(self) -> bool:
        empty_cell = self.__find_empty_cell()
        if not empty_cell:
            return True
        
        row, col = empty_cell
        
        # Check for that empty position every single number
        for num in range(1, 10):
            if self.is_valid_move(row, col, num):
                self.board[row][col] = num
                
                if self.solve():
                    return True # If this leads to a solution
                
                self.board[row][col] = 0 # this was not a solution, backtrack
                
        return False
                
    
    def restart_sudoku(self):
        # restarts the current sudoku
        self.board = self.initial_board


    def insert(self, row, col, num) -> bool:
        # check if help is on
        if self.help:
            if self.resolved_board[row][col] == num:
                self.board[row][col] = num
                return True
            else:
                return False
        
        # if help is off, checks if it's a valid move in current board
        if self.is_valid_move(row, col, num):
            self.board[row][col] = num
            return True
        
        return False
    
    def change_help_mode(self, mode: bool):
        self.help = mode