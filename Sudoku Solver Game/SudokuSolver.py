import tkinter as tk
from tkinter import messagebox
from time import time

# TODO: Implement the ability to load puzzles from a file.
from tkinter import filedialog

def load_puzzle():
    """Load a Sudoku puzzle from a file."""
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not file_path:
        return
    
    with open(file_path, "r") as file:
        lines = file.readlines()
    
    for r in range(min(6, len(lines))):
        values = lines[r].strip().split()
        for c in range(min(6, len(values))):
            entries[r][c].delete(0, tk.END)
            if values[c].isdigit():
                entries[r][c].insert(0, values[c])

# TODO: Implement the ability to save solutions to a file.
def save_solution():
    """Save the solved Sudoku puzzle to a file."""
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if not file_path:
        return
    
    board = [[entries[r][c].get() for c in range(6)] for r in range(6)]
    with open(file_path, "w") as file:
        for row in board:
            file.write(" ".join(row) + "\n")


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

def solve_sudoku(board, entries=None, delay=100):
    """Solves the Sudoku puzzle using backtracking."""
    # TODO: Show the solving process visually step-by-step.
    """
    Solves the Sudoku puzzle using backtracking with visual step-by-step display.
    
    Args:
        board: The 6x6 Sudoku board
        entries: List of tkinter Entry widgets representing the grid
        delay: Delay in milliseconds between steps (default 100ms)
    """
    def update_gui(row, col, num, color):
        """Helper function to update GUI with current attempt"""
        if entries:
            entries[row][col].delete(0, tk.END)
            entries[row][col].insert(0, str(num))
            entries[row][col].config(bg=color)
            root.update()
            root.after(delay)  # Add delay to make steps visible
            
    def is_valid(board, row, col, num):
        """Checks if placing num in board[row][col] is valid."""
        # Check row
        for c in range(6):
            if board[row][c] == num:
                return False
                
        # Check column
        for r in range(6):
            if board[r][col] == num:
                return False
                
        # Check 2x3 box
        start_row = (row // 2) * 2
        start_col = (col // 3) * 3
        for r in range(start_row, start_row + 2):
            for c in range(start_col, start_col + 3):
                if board[r][c] == num:
                    return False
        return True

    # Find empty cell
    empty = None
    for row in range(6):
        for col in range(6):
            if board[row][col] == 0:
                empty = (row, col)
                break
        if empty:
            break

    # If no empty cell found, puzzle is solved
    if not empty:
        return True
        
    row, col = empty
    
    # Try digits 1-6
    for num in range(1, 7):
        if is_valid(board, row, col, num):
            # Show attempt
            update_gui(row, col, num, '#e6ffe6')  # Light green for attempts
            
            # Place number
            board[row][col] = num
            
            # Recursively solve rest of puzzle
            if solve_sudoku(board, entries, delay):
                update_gui(row, col, num, '#90EE90')  # Green for correct placement
                return True
                
            # If placement leads to unsolvable puzzle, backtrack
            board[row][col] = 0
            update_gui(row, col, '', '#FFCCCB')  # Light red for backtracking
            
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
    """
    Display solving metrics including recursion depth, steps taken, and timing statistics.
    Requires global variables to track metrics across solving iterations.
    """
    class MetricsTracker:
        def __init__(self):
            self.current_depth = 0
            self.max_depth = 0
            self.steps_taken = 0
            self.backtracks = 0
            self.start_time = None
            self.end_time = None
            self.attempts_by_number = {i: 0 for i in range(1, 7)}  # For 6x6 grid
            self.success_rate = 0
            
        def reset(self):
            """Reset all metrics for new solve attempt"""
            self.__init__()
            
        def start_tracking(self):
            """Start timing the solve attempt"""
            self.start_time = time()
            
        def stop_tracking(self):
            """Stop timing the solve attempt"""
            self.end_time = time()
            
        def increment_depth(self):
            """Track recursion depth"""
            self.current_depth += 1
            self.max_depth = max(self.max_depth, self.current_depth)
            
        def decrement_depth(self):
            """Track backing out of recursion"""
            self.current_depth -= 1
            
        def record_attempt(self, number):
            """Record attempt to place a number"""
            self.steps_taken += 1
            self.attempts_by_number[number] += 1
            
        def record_backtrack(self):
            """Record a backtrack operation"""
            self.backtracks += 1
            
        def calculate_success_rate(self):
            """Calculate placement success rate"""
            total_attempts = sum(self.attempts_by_number.values())
            successful_placements = self.steps_taken - self.backtracks
            self.success_rate = (successful_placements / total_attempts * 100) if total_attempts > 0 else 0
            
        def get_solving_time(self):
            """Calculate total solving time"""
            if self.start_time and self.end_time:
                return self.end_time - self.start_time
            return 0
            
        def display_metrics(self):
            """Create and show metrics window"""
            metrics_window = tk.Toplevel()
            metrics_window.title("Sudoku Solver Metrics")
            metrics_window.geometry("400x500")
            
            style = ttk.Style()
            style.configure("Metric.TLabel", padding=5, font=('Arial', 10))
            
            # Basic Metrics
            ttk.Label(metrics_window, text="Solving Metrics", font=('Arial', 14, 'bold')).pack(pady=10)
            
            metrics_frame = ttk.Frame(metrics_window)
            metrics_frame.pack(fill='x', padx=20)
            
            metrics = [
                ("Maximum Recursion Depth:", f"{self.max_depth}"),
                ("Total Steps Taken:", f"{self.steps_taken}"),
                ("Number of Backtracks:", f"{self.backtracks}"),
                ("Success Rate:", f"{self.success_rate:.1f}%"),
                ("Solving Time:", f"{self.get_solving_time():.3f} seconds")
            ]
            
            for label, value in metrics:
                frame = ttk.Frame(metrics_frame)
                frame.pack(fill='x', pady=2)
                ttk.Label(frame, text=label, style="Metric.TLabel").pack(side='left')
                ttk.Label(frame, text=value, style="Metric.TLabel").pack(side='right')
            
            # Number Attempts Chart
            ttk.Label(metrics_window, text="\nAttempts by Number", font=('Arial', 12, 'bold')).pack(pady=5)
            
            chart_frame = ttk.Frame(metrics_window)
            chart_frame.pack(fill='x', padx=20)
            
            max_attempts = max(self.attempts_by_number.values())
            bar_width = 30
            
            for num, attempts in self.attempts_by_number.items():
                frame = ttk.Frame(chart_frame)
                frame.pack(fill='x', pady=2)
                
                ttk.Label(frame, text=f"{num}:", width=3).pack(side='left')
                bar_length = int((attempts / max_attempts) * 200) if max_attempts > 0 else 0
                canvas = tk.Canvas(frame, width=bar_length + 5, height=20)
                canvas.pack(side='left')
                canvas.create_rectangle(0, 5, bar_length, 15, fill='blue')
                ttk.Label(frame, text=str(attempts)).pack(side='left', padx=5)
                
            # Add close button
            ttk.Button(metrics_window, text="Close", command=metrics_window.destroy).pack(pady=20)
    
    # Show metrics if they exist
    if hasattr(show_metrics, 'tracker') and show_metrics.tracker.steps_taken > 0:
        show_metrics.tracker.calculate_success_rate()
        show_metrics.tracker.display_metrics()
    else:
        messagebox.showinfo("No Metrics", "No solving metrics available. Please solve a puzzle first.")

# Initialize tracker at module level
show_metrics.tracker = MetricsTracker()

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
