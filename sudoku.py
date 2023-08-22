import numpy as np
import pygame

WIDTH = 550     # Width-height of the gui

# Background color
BACKGROUND_COLOR = (251, 247, 245)


class Sudoku:
    def __init__(self, initial_board, help=True, gui=False):
        """
        Initialize a Sudoku puzzle.

        Args:
            initial_board (numpy.ndarray): A 9x9 NumPy array representing the initial Sudoku board.
            help (bool, optional): Enable or disable help mode. Defaults to True.
            gui (bool, optional): Enable or disable GUI. Defaults to False. 
        
        Raises:
            ValueError: If the initial board is invalid.
        """
        self.help = help
        self.gui = gui  # Now 'gui' is a keyword argument that can be set during instantiation.
        
        if initial_board is None:
            raise ValueError("Invalid initial board. Initial board cannot be None.")
        else:
            if initial_board.shape == (9, 9) and np.all((0 <= initial_board) & (initial_board <= 9)):
                self.initial_board = initial_board
                self.board = np.copy(initial_board)
                self.copy_board = np.copy(initial_board)
                
                if self.solve():
                    # there was a solution for the initial_board
                    self.resolved_board = self.board
                    self.board = self.copy_board
                    if self.gui:
                        self.__start_gui()
                else:
                    raise ValueError("Invalid initial board. It doesn't have a solution or has multiple solutions.")
            else:
                raise ValueError("Invalid initial board. It must be a 9x9 NumPy array with values between 0 and 9.")

    
    def display(self):
        """
        Display the current state of the Sudoku board.
        """
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
        """
        Display the solved Sudoku board.
        """
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
        """
        Check if a given number can be placed in a specific cell.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.
            num (int): The number to check.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
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
        """
        Find the first empty cell in the Sudoku board.

        Returns:
            tuple: A tuple (row, col) representing the empty cell's coordinates, or None if the board is full.
        """
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
                
        return None
    
    
    def solve(self) -> bool:
        """
        Solve the Sudoku puzzle using a backtracking algorithm.

        Returns:
            bool: True if a solution is found, False otherwise.
        """
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
        """
        Restart the current Sudoku puzzle.
        """
        self.board = self.initial_board
        print("The current board has been restarted")


    def insert(self, row, col, num) -> bool:
        """
        Insert a number into a cell on the Sudoku board.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.
            num (int): The number to insert.

        Returns:
            bool: True if the insertion is valid, False otherwise.
        """
        # Check if help is on
        if self.help:
            if self.resolved_board[row][col] == num:
                self.board[row][col] = num
                return True
            else:
                return False
        
        # If help is off, checks if it's a valid move in current board
        if self.is_valid_move(row, col, num):
            self.board[row][col] = num
            return True
        
        return False
    
    
    def delete_value(self, row, col) -> int:
        """
        Delete a value from a cell on the Sudoku board.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.

        Returns:
            int: The deleted number, or -1 if the cell is part of the initial board and cannot be deleted.
        """
        if self.initial_board[row][col] != 0:
            print("Can't delete a number from the initial board")
            return -1
        
        num = self.board[row][col]
        self.board[row][col] = 0
        return num
    
    
    def possible_values(self, row, col) -> list:
        """
        Get a list of possible values that can be placed in a specific cell.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.

        Returns:
            list: A list of integers representing possible values.
        """
        possible_values = [0]*9
        
        # Calculate every single number for the cell
        for num in range(1, 10):
            if self.is_valid_move(row, col, num):
                possible_values[num-1] = 1
                
        return possible_values
            
        
    
    def change_help_mode(self, mode: bool):
        """
        Change the help mode, enabling or disabling hints.

        Args:
            mode (bool): True to enable help mode, False to disable it.
        """
        self.help = mode
        
        
    def __insert_gui(self, win, position):
        i, j = position[1], position[0]
        myfont = pygame.font.SysFont('Comic Sans Ms', 35)
        buffer = 5
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if(self.initial_board[i-1][j-1] != 0):
                        return
                    if(event.key == 48):
                        if self.delete_value(i-1, j-1) > 0:
                            pygame.draw.rect(win, BACKGROUND_COLOR, (j*50 + buffer, i*50+ buffer, 50 - 2*buffer, 50 - 2*buffer))
                            pygame.display.update()
                        return
                        
                    elif(0 < event.key - 48 <10):  #We are checking for valid input
                        if self.insert(i-1, j-1, int(event.key - 48)):
                            pygame.draw.rect(win, BACKGROUND_COLOR, (j*50 + buffer, i*50+ buffer, 50 - 2*buffer, 50 - 2*buffer))
                            value = myfont.render(str(event.key-48), True, (0,0,0))
                            win.blit(value, ((j)*50 + 15, (i)*50 + 15))
                            pygame.display.update()
                            
                        return
                    return
        
        
    def __start_gui(self):
        pygame.init()
        win = pygame.display.set_mode((WIDTH, WIDTH))
        pygame.display.set_caption("Sudoku")
        win.fill(BACKGROUND_COLOR)
        initial_font = pygame.font.SysFont('Comic Sans Ms', 35)
        color_initial_font = (52, 31, 151)
        
        # Draw grid
        for i in range(0, 10):
            if i%3 == 0:
                # thicker lines for box separator
                pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), (50 + 50*i, 500), 4)
                pygame.draw.line(win, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 4)
                
            pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), (50 + 50*i, 500), 2)
            pygame.draw.line(win, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 2)
        pygame.display.update()
        
        # Populate grid with board
        for i in range(9):
            for j in range(9):
                if (0 < self.board[i][j] < 10):
                    value = initial_font.render(str(self.board[i][j]), True, color_initial_font)
                    win.blit(value, ((j+1)*50 + 15, (i+1)*50 + 15))
        pygame.display.update()
        
        while True: 
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    self.__insert_gui(win, (pos[0]//50, pos[1]//50))
                    if self.__find_empty_cell() is None:
                        print("You have succesfully finished the game!")
                        pygame.quit()
                        return
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return