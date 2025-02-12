import tkinter as tk
from tkinter import messagebox
from time import time

# TODO: Implement the ability to load puzzles from a file.
# TODO: Implement the ability to save solutions to a file.

def is_valid(board, row, col, num):
    """Checks if placing num in board[row][col] is valid."""
    for c in range(6):
        if board[row][c] == num:
            return False
    for r in range(6):
        if board[r][col] == num:
            return False
    start_row = (row // 2) * 2
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 2):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False
    return True

def solve_sudoku(board, grid_size=9, entries=None, delay=100):
    """
    Solves Sudoku puzzles of different sizes (6x6, 9x9, or 16x16) using backtracking.
    
    Args:
        board: The Sudoku board (can be 6x6, 9x9, or 16x16)
        grid_size: Size of the grid (6, 9, or 16)
        entries: List of tkinter Entry widgets representing the grid
        delay: Delay in milliseconds between steps
        
    Returns:
        bool: True if solution is found, False otherwise
    """
    def get_box_size(grid_size):
        """Determine box dimensions based on grid size"""
        if grid_size == 6:
            return 2, 3  # 2x3 boxes for 6x6 grid
        elif grid_size == 9:
            return 3, 3  # 3x3 boxes for 9x9 grid
        elif grid_size == 16:
            return 4, 4  # 4x4 boxes for 16x16 grid
        else:
            raise ValueError("Unsupported grid size. Use 6, 9, or 16.")

    def update_gui(row, col, num, color):
        """Helper function to update GUI with current attempt"""
        if entries:
            entries[row][col].delete(0, tk.END)
            if num != 0:  # Only display non-zero values
                # Convert numbers > 9 to hex for 16x16 grid
                display_val = hex(num)[2:].upper() if num > 9 else str(num)
                entries[row][col].insert(0, display_val)
            entries[row][col].config(bg=color)
            root.update()
            root.after(delay)

    def is_valid(board, row, col, num):
        """Checks if placing num in board[row][col] is valid"""
        # Check row
        for x in range(grid_size):
            if board[row][x] == num:
                return False
        
        # Check column
        for x in range(grid_size):
            if board[x][col] == num:
                return False
        
        # Check box
        box_height, box_width = get_box_size(grid_size)
        start_row = (row // box_height) * box_height
        start_col = (col // box_width) * box_width
        
        for r in range(start_row, start_row + box_height):
            for c in range(start_col, start_col + box_width):
                if board[r][c] == num:
                    return False
        
        return True

    def find_empty():
        """Find an empty cell in the board"""
        for row in range(grid_size):
            for col in range(grid_size):
                if board[row][col] == 0:
                    return row, col
        return None

    # Main solving logic
    empty = find_empty()
    if not empty:
        return True
    
    row, col = empty
    max_num = grid_size  # Maximum number that can be placed (6, 9, or 16)
    
    for num in range(1, max_num + 1):
        if is_valid(board, row, col, num):
            # Show attempt
            update_gui(row, col, num, '#e6ffe6')  # Light green for attempts
            
            # Place number
            board[row][col] = num
            
            # Recursively solve rest of puzzle
            if solve_sudoku(board, grid_size, entries, delay):
                update_gui(row, col, num, '#90EE90')  # Green for correct placement
                return True
            
            # If placement leads to unsolvable puzzle, backtrack
            board[row][col] = 0
            update_gui(row, col, 0, '#FFCCCB')  # Light red for backtracking
    
    return False

def get_board():
    """Retrieves the current board from the input fields."""
    board = []
    for r in range(6):
        row = []
        for c in range(6):
            val = entries[r][c].get()
            # TODO: Add validation to ensure input is a valid integer between 1 and 6 for 6x6 grid.
            try: #error handling for it to run a block of code
                # Convert the value to an integer
                int_val = int(val)
                
                # Check if it's between 1 and 6
                if 1 <= int_val <= 6:
                    row.append(int_val)
                else:
                    raise ValueError(f"Value out of range: {val}")
            except ValueError: # in case the block isn't executed successfully 
                print(f"Invalid input at row {r + 1}, column {c + 1}: '{val}'. Must be an integer between 1 and 6.")
                return None  # return None if invalid input is found
        board.append(row)
    return board

def solve():
    """Solves the Sudoku puzzle and updates the GUI."""
    board = get_board()
    
    #start timer
    start_time = time.time()

    if board is None:
        messagebox.showinfo("Unsolvable", "Please provide a valid puzzle board")
        return
    if solve_sudoku(board):
        for r in range(6):
            for c in range(6):
                if board[r][c] != 0:
                    entries[r][c].delete(0, tk.END)
                    entries[r][c].insert(0, str(board[r][c]))
    else:
        messagebox.showinfo("Unsolvable", "The puzzle cannot be solved")
    # TODO: Display the time taken to solve the puzzle.
    end_time = time.time()
    time_taken = end_time - start_time
    tk.messagebox.showinfo("Time taken", f"Time taken to solve the puzzle: {time_taken:.2f} seconds")

def classify_puzzle():
    """Classify the puzzle as Easy, Medium, or Hard based on complexity."""
    # TODO: Implement puzzle classification based on number of blanks or complexity.
    board = get_board()
    blank_count = sum(row.count(0) for row in board)

    if blank_count < 10:
        difficulty = "Easy"
    elif 10 <= blank_count <= 20:
        difficulty = "Medium"
    else:
        difficulty = "Hard"

    messagebox.showinfo("Puzzle Classification", f"The puzzle is classified as: {difficulty}")


def clear_grid():
    """Clear the Sudoku grid."""
    # TODO: Add a button to clear the grid and restart.
def clear_grid():
    """Clear the Sudoku grid."""
    for r in range(6):
        for c in range(6):
            entries[r][c].delete(0, tk.END)

clear_button = tk.Button(root, text="Clear Grid", font=('Arial', 20), command=clear_grid)
clear_button.grid(row=6, column=3, columnspan=3)
    

def show_metrics():
    """Display metrics such as recursion depth or steps taken."""
    # TODO: Implement functionality to track and show recursion depth or steps taken.

def provide_hint():
    """Provide a hint for the next move without solving completely."""
    # TODO: Implement hint functionality.

# Create the main window
root = tk.Tk()
root.title("6x6 Sudoku Solver")

# Create a 6x6 grid of entry fields
entries = []
for r in range(6):
    row_entries = []
    for c in range(6):
        entry = tk.Entry(root, width=2, font=('Arial', 24), borderwidth=2, relief="solid")
        entry.grid(row=r, column=c, padx=5, pady=5)
        row_entries.append(entry)
    entries.append(row_entries)

# Create buttons for the functionalities
solve_button = tk.Button(root, text="Solve", font=('Arial', 16), command=solve)
solve_button.grid(row=6, column=0, columnspan=3)

# TODO : Add button to clear grid

# TODO: Add buttons for loading puzzles from a file and saving solutions.

root.mainloop()
