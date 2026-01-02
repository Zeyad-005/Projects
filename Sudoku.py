import random
from collections import deque
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import time
import threading

# -------------------------
# SudokuSolver 
# -------------------------
class SudokuSolver:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.variables = []
        self.domains = {}
        self.arcs = []
        self.neighbors = {}
        self.log_callback = print
        self.log_buffer = []
        self.show_arc_consistency = True
        self.stats = {
            'revisions': 0,
            'domains_pruned': 0,
            'singleton_domains': 0,
            'forward_checks': 0,
            'lcv_orderings': 0,
            'mrv_selections': 0,
            'backtracks': 0
        }
    
    def set_board(self, board):
        self.board = [row[:] for row in board]
        self.initialize_csp()
    
    def get_board(self):
        return [row[:] for row in self.board]
    
    def set_log_callback(self, callback):
        self.log_callback = callback
        
    def set_show_arc_consistency(self, show):
        self.show_arc_consistency = show
        
    def log(self, message):
        # buffer logs then flush where appropriate
        if self.show_arc_consistency:
            self.log_buffer.append(message)
    
    def flush_log_buffer(self):
        if self.log_buffer and self.show_arc_consistency:
            full_log = "\n".join(self.log_buffer)
            try:
                self.log_callback(full_log)
            except Exception:
                # fallback to print if callback fails
                print(full_log)
            self.log_buffer = []
    
    def initialize_csp(self):
        # reset stats and structures
        self.stats = {
            'revisions': 0,
            'domains_pruned': 0,
            'singleton_domains': 0,
            'forward_checks': 0,
            'lcv_orderings': 0,
            'mrv_selections': 0,
            'backtracks': 0
        }
        
        self.variables = [(i, j) for i in range(9) for j in range(9)]
        
        self.domains = {}
        for var in self.variables:
            i, j = var
            if self.board[i][j] != 0:  # pre filled cell
                self.domains[var] = {self.board[i][j]}
            else:  # empty cell
                self.domains[var] = set(range(1, 10))
        
        self.neighbors = {var: set() for var in self.variables}
        
        # row neighbors
        for i in range(9):
            for j in range(9):
                for k in range(9):
                    if j != k:
                        self.neighbors[(i, j)].add((i, k))
        # column neighbors
        for i in range(9):
            for j in range(9):
                for k in range(9):
                    if i != k:
                        self.neighbors[(i, j)].add((k, j))
        # box neighbors
        for i in range(9):
            for j in range(9):
                box_i, box_j = 3 * (i // 3), 3 * (j // 3)
                for bi in range(box_i, box_i + 3):
                    for bj in range(box_j, box_j + 3):
                        if (bi, bj) != (i, j):
                            self.neighbors[(i, j)].add((bi, bj))
        
        self.arcs = []
        for var in self.variables:
            for neighbor in self.neighbors[var]:
                self.arcs.append((var, neighbor))
    
    def is_valid_board(self, board):
        for row in board:
            digits = [d for d in row if d != 0]
            if len(digits) != len(set(digits)):
                return False
        
        for j in range(9):
            col = [board[i][j] for i in range(9)]
            digits = [d for d in col if d != 0]
            if len(digits) != len(set(digits)):
                return False
        
        for box_i in range(0, 9, 3):
            for box_j in range(0, 9, 3):
                box = [board[i][j] for i in range(box_i, box_i + 3) 
                       for j in range(box_j, box_j + 3)]
                digits = [d for d in box if d != 0]
                if len(digits) != len(set(digits)):
                    return False
        
        return True
        
    def is_valid_move(self, row, col, num):
        for j in range(9):
            if self.board[row][j] == num:
                return False
        
        for i in range(9):
            if self.board[i][col] == num:
                return False
        
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num:
                    return False
        
        return True
    
    def revise(self, xi, xj):
        self.stats['revisions'] += 1
        revised = False
        
        self.log(f"Revising arc (X{xi}, X{xj})")
        self.log(f"Current domain of X{xi}: {sorted(list(self.domains[xi]))}")
        self.log(f"Domain of X{xj}: {sorted(list(self.domains[xj]))}")
        
        xi_domain = self.domains[xi].copy()
        
        for x in xi_domain:
            has_support = False
            for y in self.domains[xj]:
                if x != y:
                    has_support = True
                    break
            
            if not has_support and len(self.domains[xj]) > 0:
                self.domains[xi].remove(x)
                revised = True
                self.stats['domains_pruned'] += 1
                self.log(f"Removed value {x} from X{xi} because no supporting value exists in X{xj}")
        
        if revised:
            self.log(f"Updated domain of X{xi}: {sorted(list(self.domains[xi]))}")
        
        return revised
    
    def ac3(self, queue=None):
        if queue is None:
            queue = self.arcs.copy()
        
        total_arcs = len(queue)
        processed_arcs = 0
        
        self.log(f"Starting AC-3 algorithm with {total_arcs} arcs")
        
        while queue:
            (xi, xj) = queue.pop(0)
            processed_arcs += 1
            
            if processed_arcs % 1000 == 0:
                self.log(f"Processed {processed_arcs}/{total_arcs} arcs so far")
            
            if self.revise(xi, xj):
                if len(self.domains[xi]) == 0:
                    self.log(f"Empty domain found for X{xi}. No solution possible.")
                    return False
                
                if len(self.domains[xi]) == 1:
                    value = next(iter(self.domains[xi]))
                    i, j = xi
                    self.board[i][j] = value
                    self.stats['singleton_domains'] += 1
                    self.log(f"Variable X{xi} became singleton with value {value}")
                
                for xk in self.neighbors[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
        
        self.log(f"\n===== Arc Consistency Summary =====")
        self.log(f"Total arcs processed: {processed_arcs}")
        self.log(f"Total revisions: {self.stats['revisions']}")
        self.log(f"Total domains pruned: {self.stats['domains_pruned']}")
        self.log(f"Total singleton domains found: {self.stats['singleton_domains']}")
        return True
    
    def is_complete(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return False
        return True
    
    def solve_with_arc_consistency(self):
        self.log("Starting to solve with arc consistency, MRV, LCV, and Forward Checking...")
        
        if not self.ac3():
            self.log("Initial arc consistency failed - no solution possible")
            self.flush_log_buffer()
            return False, self.stats
        
        if self.is_complete():
            self.log("Puzzle solved with arc consistency alone!")
            self.flush_log_buffer()
            return True, self.stats
        
        self.log("Using backtracking with MRV, LCV, and Forward Checking...")
        result = self.backtrack()
        
        self.log(f"\n===== Heuristics Summary =====")
        self.log(f"MRV selections: {self.stats['mrv_selections']}")
        self.log(f"LCV orderings: {self.stats['lcv_orderings']}")
        self.log(f"Forward checks: {self.stats['forward_checks']}")
        self.log(f"Backtracks: {self.stats['backtracks']}")
        
        self.flush_log_buffer()
        return result, self.stats
    
    def order_domain_values(self, var):
        if len(self.domains[var]) <= 1:
            return list(self.domains[var])
        
        def count_constraints(value):
            count = 0
            for neighbor in self.neighbors[var]:
                if self.board[neighbor[0]][neighbor[1]] == 0:
                    if value in self.domains[neighbor]:
                        count += 1
            return count
        
        ordered_values = sorted(self.domains[var], key=count_constraints)
        
        self.stats['lcv_orderings'] += 1
        self.log(f"LCV ordered domain for {var}: {ordered_values}")
        
        return ordered_values
    
    def forward_check(self, var, value):
        self.stats['forward_checks'] += 1
        
        saved_domains = {}
        conflicts = []
        
        for neighbor in self.neighbors[var]:
            ni, nj = neighbor
            if self.board[ni][nj] == 0:
                if value in self.domains[neighbor]:
                    if neighbor not in saved_domains:
                        saved_domains[neighbor] = self.domains[neighbor].copy()
                    
                    self.domains[neighbor].remove(value)
                    self.log(f"Forward checking: removed {value} from domain of {neighbor}")
                    
                    if not self.domains[neighbor]:
                        self.log(f"Forward checking: domain of {neighbor} became empty")
                        conflicts.append(neighbor)
        
        if conflicts:
            for n, domain in saved_domains.items():
                self.domains[n] = domain
            return False
        
        return True
    
    def backtrack(self):
        if self.is_complete():
            return True
        
        unassigned = self.select_unassigned_variable()
        
        if not unassigned:
            return True
        
        backtrack_count = 0
        total_values = len(self.domains[unassigned])
        
        i, j = unassigned
        
        for value in self.order_domain_values(unassigned):
            backtrack_count += 1
            self.stats['backtracks'] += 1
            
            if backtrack_count % 5 == 0 or backtrack_count == total_values:
                self.log(f"Backtracking progress: tried {backtrack_count}/{total_values} values for cell {unassigned}")
            
            if self.is_valid_move(i, j, value):
                self.board[i][j] = value
                old_domains = {v: self.domains[v].copy() for v in self.variables}
                
                self.domains[unassigned] = {value}
                
                if self.forward_check(unassigned, value):
                    affected_arcs = [(neighbor, unassigned) for neighbor in self.neighbors[unassigned]]
                    if self.ac3(affected_arcs):
                        if self.backtrack():
                            return True
                
                self.board[i][j] = 0
                self.domains = old_domains
        
        return False
    
    def select_unassigned_variable(self):
        unassigned = [var for var in self.variables if self.board[var[0]][var[1]] == 0]
        
        if not unassigned:
            return None
        
        selected_var = min(unassigned, 
                          key=lambda var: (len(self.domains[var]), 
                                         -len([n for n in self.neighbors[var] 
                                               if self.board[n[0]][n[1]] == 0])))
        
        self.stats['mrv_selections'] += 1
        self.log(f"MRV selected variable {selected_var} with domain size {len(self.domains[selected_var])}")
        
        return selected_var

# -------------------------
# SudokuGenerator
# -------------------------
class SudokuGenerator:
    def __init__(self):
        self.solver = SudokuSolver()
        self.board = [[0 for _ in range(9)] for _ in range(9)]
    
    def generate_puzzle(self, cells_to_remove):
        self.generate_solved_board()
        solved_board = [row[:] for row in self.board]
        puzzle_board = [row[:] for row in solved_board]
        
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        # امسح الخلايا بدون check
        for idx in range(cells_to_remove):
            i, j = cells[idx]
            puzzle_board[i][j] = 0
        
        return puzzle_board, solved_board
    
    def generate_solved_board(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        
        for i in range(0, 9, 3):
            self.fill_box(i, i)
        
        self.solve_board()
        
        return self.board
    
    def fill_box(self, row, col):
        nums = list(range(1, 10))
        random.shuffle(nums)
        
        for i in range(3):
            for j in range(3):
                self.board[row + i][col + j] = nums.pop()
    
    def solve_board(self):
        empty_cell = self.find_empty()
        if not empty_cell:
            return True
        
        row, col = empty_cell
        nums = list(range(1, 10))
        random.shuffle(nums)
        
        for num in nums:
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.solve_board():
                    return True
                self.board[row][col] = 0
        
        return False
    
    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None
    
    def is_valid(self, row, col, num):
        for j in range(9):
            if self.board[row][j] == num:
                return False
        
        for i in range(9):
            if self.board[i][col] == num:
                return False
        
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num:
                    return False
        
        return True
    
    def has_unique_solution(self, board):
        board_copy = [row[:] for row in board]
        first_solution = self.find_solution(board_copy)
        if not first_solution:
            return False
        
        second_solution = self.find_second_solution(board, first_solution)
        return not second_solution
    
    def find_solution(self, board):
        solver = SudokuSolver()
        solver.set_board(board)
        solver.set_log_callback(lambda msg: None)
        solver.set_show_arc_consistency(False)
        solved, _ = solver.solve_with_arc_consistency()
        if solved:
            return solver.get_board()
        return None
    
    def find_second_solution(self, original_board, first_solution):
        board = [row[:] for row in original_board]
        solver = SudokuSolver()
        solver.set_board(board)
        solver.set_log_callback(lambda msg: None)
        solver.set_show_arc_consistency(False)
        
        empty_cells = []
        for i in range(9):
            for j in range(9):
                if original_board[i][j] == 0:
                    empty_cells.append((i, j))
        
        if not empty_cells:
            return None
        
        return self.backtrack_for_second_solution(solver, empty_cells, 0, first_solution)
    
    def backtrack_for_second_solution(self, solver, empty_cells, index, first_solution):
        if index >= len(empty_cells):
            current_board = solver.get_board()
            for i in range(9):
                for j in range(9):
                    if current_board[i][j] != first_solution[i][j]:
                        return current_board
            return None
        
        i, j = empty_cells[index]
        board = solver.get_board()
        
        for num in range(1, 10):
            if solver.is_valid_move(i, j, num):
                board[i][j] = num
                result = self.backtrack_for_second_solution(solver, empty_cells, index + 1, first_solution)
                if result:
                    return result
                board[i][j] = 0
        
        return None

# -------------------------
# Small demonstration 
# -------------------------
def print_board(board):
    for i, row in enumerate(board):
        if i % 3 == 0 and i > 0:
            print("-" * 21)
        row_str = ""
        for j, val in enumerate(row):
            if j % 3 == 0 and j > 0:
                row_str += "| "
            row_str += (str(val) if val != 0 else ".") + " "
        print(row_str)

# -------------------------
# Modern Sudoku GUI
# -------------------------
class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku CSP Solver - Alexandria University")
        self.root.geometry("1300x750")
        
        # Modern color scheme
        self.colors = {
            'bg': '#0f1419',
            'card_bg': '#1a1f2e',
            'accent': '#00d9ff',
            'success': '#00ff9f',
            'error': '#ff3366',
            'warning': '#ffd60a',
            'text': '#e6edf3',
            'text_dim': '#8b949e',
            'border': '#30363d',
            'cell_empty': '#0d1117',
            'cell_fixed': '#161b22',
            'btn_hover': '#1f6feb',
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        self.solver = SudokuSolver()
        self.generator = SudokuGenerator()
        self.current_board = [[0 for _ in range(9)] for _ in range(9)]
        self.original_board = [[0 for _ in range(9)] for _ in range(9)]
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.solving = False
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=15, pady=15)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Left panel
        left_panel = tk.Frame(main_frame, bg=self.colors['bg'])
        left_panel.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 15))
        
        # Title
        title_frame = tk.Frame(left_panel, bg=self.colors['card_bg'], relief='flat', bd=0)
        title_frame.grid(row=0, column=0, pady=(0, 10), sticky='ew')
        
        title_label = tk.Label(title_frame, text="🧩 Sudoku CSP Solver", 
                            bg=self.colors['card_bg'],
                            fg=self.colors['accent'],
                            font=('Segoe UI', 16, 'bold'))
        title_label.pack(pady=10)
        
        subtitle = tk.Label(title_frame, text="Arc Consistency • MRV • LCV • Forward Checking",
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_dim'],
                        font=('Segoe UI', 8))
        subtitle.pack(pady=(0, 8))
        
        # Board
        board_container = tk.Frame(left_panel, bg=self.colors['card_bg'], relief='flat', bd=0)
        board_container.grid(row=1, column=0, pady=(0, 10))
        
        self.board_frame = tk.Frame(board_container, bg=self.colors['border'], 
                                    highlightthickness=2,
                                    highlightbackground=self.colors['accent'])
        self.board_frame.pack(padx=15, pady=15)
        self.create_board()
        
        # Controls
        controls_frame = tk.Frame(left_panel, bg=self.colors['card_bg'], relief='flat', bd=0)
        controls_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        controls_inner = tk.Frame(controls_frame, bg=self.colors['card_bg'])
        controls_inner.pack(padx=15, pady=12, fill='both')
        
        # Mode
        mode_label = tk.Label(controls_inner, text="MODE", 
                            bg=self.colors['card_bg'],
                            fg=self.colors['accent'],
                            font=('Segoe UI', 8, 'bold'))
        mode_label.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 5))
        
        mode_frame = tk.Frame(controls_inner, bg=self.colors['card_bg'])
        mode_frame.grid(row=1, column=0, columnspan=2, sticky='w', pady=(0, 10))
        
        self.mode_var = tk.StringVar(value="generate")
        
        tk.Radiobutton(mode_frame, text="🎲 Generate", variable=self.mode_var, 
                    value="generate",
                    bg=self.colors['card_bg'],
                    fg=self.colors['text'],
                    selectcolor=self.colors['bg'],
                    activebackground=self.colors['card_bg'],
                    activeforeground=self.colors['accent'],
                    font=('Segoe UI', 9),
                    highlightthickness=0).pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Radiobutton(mode_frame, text="✏️ User Input", variable=self.mode_var, 
                    value="input",
                    bg=self.colors['card_bg'],
                    fg=self.colors['text'],
                    selectcolor=self.colors['bg'],
                    activebackground=self.colors['card_bg'],
                    activeforeground=self.colors['accent'],
                    font=('Segoe UI', 9),
                    highlightthickness=0).pack(side=tk.LEFT)
        
        # Difficulty
        diff_label = tk.Label(controls_inner, text="DIFFICULTY", 
                            bg=self.colors['card_bg'],
                            fg=self.colors['accent'],
                            font=('Segoe UI', 8, 'bold'))
        diff_label.grid(row=2, column=0, columnspan=2, sticky='w', pady=(0, 5))
        
        diff_frame = tk.Frame(controls_inner, bg=self.colors['card_bg'])
        diff_frame.grid(row=3, column=0, columnspan=2, sticky='w', pady=(0, 12))
        
        self.difficulty_var = tk.StringVar(value="medium")
        
        tk.Radiobutton(diff_frame, text="😊 Easy", variable=self.difficulty_var, 
                    value="easy",
                    bg=self.colors['card_bg'],
                    fg=self.colors['text'],
                    selectcolor=self.colors['bg'],
                    activebackground=self.colors['card_bg'],
                    activeforeground=self.colors['success'],
                    font=('Segoe UI', 9),
                    highlightthickness=0).pack(side=tk.LEFT, padx=(0, 12))
        
        tk.Radiobutton(diff_frame, text="😐 Medium", variable=self.difficulty_var, 
                    value="medium",
                    bg=self.colors['card_bg'],
                    fg=self.colors['text'],
                    selectcolor=self.colors['bg'],
                    activebackground=self.colors['card_bg'],
                    activeforeground=self.colors['warning'],
                    font=('Segoe UI', 9),
                    highlightthickness=0).pack(side=tk.LEFT, padx=(0, 12))
        
        tk.Radiobutton(diff_frame, text="😤 Hard", variable=self.difficulty_var, 
                    value="hard",
                    bg=self.colors['card_bg'],
                    fg=self.colors['text'],
                    selectcolor=self.colors['bg'],
                    activebackground=self.colors['card_bg'],
                    activeforeground=self.colors['error'],
                    font=('Segoe UI', 9),
                    highlightthickness=0).pack(side=tk.LEFT)
        
        # Buttons
        btn_frame = tk.Frame(controls_inner, bg=self.colors['card_bg'])
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(0, 10))
        
        self.generate_btn = self.create_button(btn_frame, "🎲 Generate", 
                                            self.generate_puzzle, self.colors['accent'])
        self.generate_btn.grid(row=0, column=0, padx=2, pady=2, sticky='ew')
        
        self.solve_btn = self.create_button(btn_frame, "⚡ Solve", 
                                            self.solve_puzzle, self.colors['success'])
        self.solve_btn.grid(row=0, column=1, padx=2, pady=2, sticky='ew')
        
        self.clear_btn = self.create_button(btn_frame, "🗑️ Clear", 
                                            self.clear_board, self.colors['error'])
        self.clear_btn.grid(row=1, column=0, padx=2, pady=2, sticky='ew')
        
        self.validate_btn = self.create_button(btn_frame, "✓ Validate", 
                                            self.validate_input, self.colors['warning'])
        self.validate_btn.grid(row=1, column=1, padx=2, pady=2, sticky='ew')
        
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        
        # Checkbox
        self.show_ac_var = tk.BooleanVar(value=True)
        tk.Checkbutton(controls_inner, text="📊 Show Arc Consistency Logs",
                    variable=self.show_ac_var,
                    bg=self.colors['card_bg'],
                    fg=self.colors['text'],
                    selectcolor=self.colors['bg'],
                    activebackground=self.colors['card_bg'],
                    activeforeground=self.colors['accent'],
                    font=('Segoe UI', 9),
                    highlightthickness=0).grid(row=5, column=0, columnspan=2, sticky='w')
        
        # Statistics
        stats_frame = tk.Frame(left_panel, bg=self.colors['card_bg'], relief='flat', bd=0)
        stats_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        stats_header = tk.Label(stats_frame, text="📈 STATISTICS",
                            bg=self.colors['border'],
                            fg=self.colors['accent'],
                            font=('Segoe UI', 9, 'bold'),
                            anchor='w')
        stats_header.pack(fill=tk.X, padx=0, pady=0)
        
        self.stats_text = tk.Text(stats_frame, height=8, width=40, 
                                bg=self.colors['cell_empty'],
                                fg=self.colors['text'],
                                font=('Consolas', 8),
                                relief='flat',
                                borderwidth=0,
                                insertbackground=self.colors['accent'])
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)
        
        # Right panel - Logs
        right_panel = tk.Frame(main_frame, bg=self.colors['bg'])
        right_panel.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_panel.rowconfigure(1, weight=1)
        right_panel.columnconfigure(0, weight=1)
        
        log_frame = tk.Frame(right_panel, bg=self.colors['card_bg'], relief='flat', bd=0)
        log_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.rowconfigure(1, weight=1)
        log_frame.columnconfigure(0, weight=1)
        
        log_header_frame = tk.Frame(log_frame, bg=self.colors['border'])
        log_header_frame.grid(row=0, column=0, sticky='ew')
        
        log_title = tk.Label(log_header_frame, text="📝 SOLUTION LOGS",
                            bg=self.colors['border'],
                            fg=self.colors['accent'],
                            font=('Segoe UI', 9, 'bold'))
        log_title.pack(side=tk.LEFT, padx=12, pady=8)
        
        clear_log_btn = tk.Button(log_header_frame, text="Clear",
                                command=lambda: self.log_text.delete(1.0, tk.END),
                                bg=self.colors['border'],
                                fg=self.colors['text_dim'],
                                font=('Segoe UI', 8),
                                relief='flat',
                                borderwidth=0,
                                padx=12,
                                pady=4,
                                cursor='hand2')
        clear_log_btn.pack(side=tk.RIGHT, padx=12)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD,
                                                bg=self.colors['cell_empty'],
                                                fg=self.colors['text'],
                                                font=('Consolas', 8),
                                                relief='flat',
                                                borderwidth=0,
                                                insertbackground=self.colors['accent'])
        self.log_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=12, pady=10)
    
    def create_board(self):
        for i in range(9):
            for j in range(9):
                border_top = 2 if i % 3 == 0 else 1
                border_left = 2 if j % 3 == 0 else 1
                border_bottom = 2 if i == 8 else 0
                border_right = 2 if j == 8 else 0
                
                frame = tk.Frame(self.board_frame, 
                            highlightbackground=self.colors['border'],
                            highlightthickness=0,
                            bd=0,
                            bg=self.colors['border'])
                frame.grid(row=i, column=j, sticky=(tk.W, tk.E, tk.N, tk.S))
                
                if (i // 3 + j // 3) % 2 == 0:
                    cell_bg = self.colors['cell_empty']
                else:
                    cell_bg = self.colors['cell_fixed']
                
                padx = (border_left, border_right)
                pady = (border_top, border_bottom)
                
                entry = tk.Entry(frame, width=3, 
                            font=('Segoe UI', 16, 'bold'),
                            justify='center',
                            bg=cell_bg,
                            fg=self.colors['accent'],
                            relief='flat',
                            borderwidth=0,
                            insertbackground=self.colors['accent'],
                            disabledbackground=self.colors['cell_fixed'],
                            disabledforeground=self.colors['text_dim'])
                entry.pack(padx=padx, pady=pady, ipady=6)
                entry.bind('<KeyRelease>', lambda e, r=i, c=j: self.on_cell_change(r, c))
                
                self.entries[i][j] = entry
    
    def create_button(self, parent, text, command, color):
        btn = tk.Button(parent, text=text, command=command,
                    bg=color,
                    fg='#000000',
                    font=('Segoe UI', 9, 'bold'),
                    relief='flat',
                    borderwidth=0,
                    padx=15,
                    pady=8,
                    cursor='hand2',
                    activebackground=color,
                    activeforeground='#000000')
        
        def on_enter(e):
            btn['bg'] = self.lighten_color(color)
        
        def on_leave(e):
            btn['bg'] = color
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
    
    def lighten_color(self, hex_color):
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = min(255, int(r * 1.15))
        g = min(255, int(g * 1.15))
        b = min(255, int(b * 1.15))
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def on_cell_change(self, row, col):
        entry = self.entries[row][col]
        value = entry.get().strip()
        
        if (row // 3 + col // 3) % 2 == 0:
            default_bg = self.colors['cell_empty']
        else:
            default_bg = self.colors['cell_fixed']
        
        entry.config(bg=default_bg, fg=self.colors['accent'])
        
        if not value:
            self.current_board[row][col] = 0
            return
        
        if not value.isdigit() or int(value) not in range(1, 10):
            entry.config(bg=self.colors['error'], fg='#ffffff')
            return
        
        num = int(value)
        self.current_board[row][col] = num
        
        temp = self.current_board[row][col]
        self.current_board[row][col] = 0
        
        if self.is_valid_placement(row, col, num):
            entry.config(bg=self.colors['success'], fg='#000000')
        else:
            entry.config(bg=self.colors['error'], fg='#ffffff')
        
        self.current_board[row][col] = temp
    
    def is_valid_placement(self, row, col, num):
        for j in range(9):
            if self.current_board[row][j] == num:
                return False
        
        for i in range(9):
            if self.current_board[i][col] == num:
                return False
        
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.current_board[i][j] == num:
                    return False
        
        return True
    
    def update_board_display(self, board=None):
        if board is None:
            board = self.current_board
        
        for i in range(9):
            for j in range(9):
                entry = self.entries[i][j]
                value = board[i][j]
                
                entry.delete(0, tk.END)
                if value != 0:
                    entry.insert(0, str(value))
                
                if self.original_board[i][j] != 0:
                    entry.config(state='disabled')
                else:
                    entry.config(state='normal')
                    if value != 0:
                        entry.config(fg=self.colors['accent'])
    
    def generate_puzzle(self):
        if self.solving:
            messagebox.showwarning("Busy", "Please wait for current solving to finish")
            return
        
        self.log_text.delete(1.0, tk.END)
        self.log("🎲 Generating puzzle...")
        
        difficulty_map = {'easy': 30, 'medium': 40, 'hard': 50}
        cells_to_remove = difficulty_map[self.difficulty_var.get()]
        
        def generate_thread():
            try:
                puzzle, solution = self.generator.generate_puzzle(cells_to_remove)
                self.root.after(0, lambda: self.finish_generate(puzzle, solution))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Generation failed: {e}"))
        
        threading.Thread(target=generate_thread, daemon=True).start()
    
    def finish_generate(self, puzzle, solution):
        self.current_board = [row[:] for row in puzzle]
        self.original_board = [row[:] for row in puzzle]
        self.update_board_display()
        
        empty_cells = sum(row.count(0) for row in puzzle)
        self.log(f"✓ Puzzle generated with {empty_cells} empty cells ({self.difficulty_var.get()} difficulty)")
        messagebox.showinfo("Success", f"Puzzle generated!\nDifficulty: {self.difficulty_var.get().capitalize()}")
    
    def solve_puzzle(self):
        if self.solving:
            messagebox.showwarning("Busy", "Already solving")
            return
        
        for i in range(9):
            for j in range(9):
                val = self.entries[i][j].get().strip()
                if val.isdigit() and int(val) in range(1, 10):
                    self.current_board[i][j] = int(val)
                else:
                    self.current_board[i][j] = 0
        
        if not self.solver.is_valid_board(self.current_board):
            messagebox.showerror("Invalid Board", "The current board has constraint violations!")
            return
        
        self.log_text.delete(1.0, tk.END)
        self.log("⚡ Starting to solve puzzle...")
        self.solving = True
        
        def solve_thread():
            try:
                self.solver.set_board(self.current_board)
                self.solver.set_log_callback(self.log)
                self.solver.set_show_arc_consistency(self.show_ac_var.get())
                
                solved, stats = self.solver.solve_with_arc_consistency()
                
                self.root.after(0, lambda: self.finish_solve(solved, stats))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Solving failed: {e}"))
                self.solving = False
        
        threading.Thread(target=solve_thread, daemon=True).start()
    
    def finish_solve(self, solved, stats):
        self.solving = False
        
        if solved:
            self.current_board = self.solver.get_board()
            self.update_board_display()
            self.log("\n✓ PUZZLE SOLVED SUCCESSFULLY!")
            
            self.stats_text.delete(1.0, tk.END)
            stats_str = f"""Solve Time: {stats['solve_time']:.4f} seconds
            Revisions: {stats['revisions']}
            Domains Pruned: {stats['domains_pruned']}
            Singleton Domains: {stats['singleton_domains']}
            MRV Selections: {stats['mrv_selections']}
            LCV Orderings: {stats['lcv_orderings']}
            Forward Checks: {stats['forward_checks']}
            Backtracks: {stats['backtracks']}"""
            self.stats_text.insert(1.0, stats_str)
            
            messagebox.showinfo("Success", f"Puzzle solved in {stats['solve_time']:.4f} seconds!")
        else:
            self.log("\n✗ NO SOLUTION FOUND")
            messagebox.showerror("Failed", "No solution exists for this puzzle!")
    
    def clear_board(self):
        if self.solving:
            messagebox.showwarning("Busy", "Cannot clear while solving")
            return
        
        self.current_board = [[0 for _ in range(9)] for _ in range(9)]
        self.original_board = [[0 for _ in range(9)] for _ in range(9)]
        
        for i in range(9):
            for j in range(9):
                entry = self.entries[i][j]
                entry.config(state='normal')
                entry.delete(0, tk.END)
                
                if (i // 3 + j // 3) % 2 == 0:
                    entry.config(bg=self.colors['cell_empty'])
                else:
                    entry.config(bg=self.colors['cell_fixed'])
                entry.config(fg=self.colors['accent'])
        
        self.log_text.delete(1.0, tk.END)
        self.stats_text.delete(1.0, tk.END)
        self.log("🗑️ Board cleared")
    
    def validate_input(self):
        for i in range(9):
            for j in range(9):
                val = self.entries[i][j].get().strip()
                if val.isdigit() and int(val) in range(1, 10):
                    self.current_board[i][j] = int(val)
                else:
                    self.current_board[i][j] = 0
        
        if self.solver.is_valid_board(self.current_board):
            messagebox.showinfo("Valid", "The board is valid! No constraint violations.")
            self.log("✓ Board validation: PASSED")
        else:
            messagebox.showerror("Invalid", "The board has constraint violations!")
            self.log("✗ Board validation: FAILED")
    
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

# -------------------------
# Main Entry Point
# -------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()


