import numpy as np
import time
from typing import List, Tuple, Optional, Dict, Any

class ConnectFour:
    """ Constructor """
    """ 0 = empty, 1 = player, 2 = AI"""
    def __init__(self, width: int = 7, height: int = 6):
        self.width = width
        self.height = height
        self.board = np.zeros((height, width), dtype=int)
        self.current_player = 1
        self.game_over = False
        self.winner = None
        
    def reset_game(self):
        self.board = np.zeros((self.height, self.width), dtype=int)
        self.current_player = 1
        self.game_over = False
        self.winner = None
    
    def drop_disc(self, column: int) -> bool:
        if column < 0 or column >= self.width:
            return False
            
        for row in range(self.height - 1, -1, -1):
            if self.board[row][column] == 0:
                self.board[row][column] = self.current_player
                return True
            
        return False

    def switch_player(self):
        self.current_player = 3 - self.current_player
    
    def is_valid_move(self, column: int) -> bool:
        return 0 <= column < self.width and self.board[0][column] == 0
    
    def get_valid_moves(self) -> List[int]:
        return [col for col in range(self.width) if self.is_valid_move(col)]
    
    def check_winner(self, player: int) -> bool:
        board = self.board
        
        # Check horizontal wins
        for row in range(self.height):
            for col in range(self.width - 3):
                if (board[row][col] == player and 
                    board[row][col + 1] == player and 
                    board[row][col + 2] == player and 
                    board[row][col + 3] == player):
                    return True
        
        # Check vertical wins
        for row in range(self.height - 3):
            for col in range(self.width):
                if (board[row][col] == player and 
                    board[row + 1][col] == player and 
                    board[row + 2][col] == player and 
                    board[row + 3][col] == player):
                    return True
        
        # Check diagonal wins (positive slope)
        for row in range(3, self.height):
            for col in range(self.width - 3):
                if (board[row][col] == player and 
                    board[row - 1][col + 1] == player and 
                    board[row - 2][col + 2] == player and 
                    board[row - 3][col + 3] == player):
                    return True
                
        for row in range(3, self.height):
            for col in range(3, self.width):
                if (board[row][col] == player and 
                    board[row - 1][col - 1] == player and 
                    board[row - 2][col - 2] == player and 
                    board[row - 3][col - 3] == player):
                    return True

        # Check diagonal wins (negative slope)
        for row in range(self.height - 3):
            for col in range(self.width - 3):
                if (board[row][col] == player and 
                    board[row + 1][col + 1] == player and 
                    board[row + 2][col + 2] == player and 
                    board[row + 3][col + 3] == player):
                    return True
                
        for row in range(self.height - 3):
            for col in range(3, self.width):
                if (board[row][col] == player and 
                    board[row + 1][col - 1] == player and 
                    board[row + 2][col - 2] == player and 
                    board[row + 3][col - 3] == player):
                    return True
                  
        return False
    
    def count_connected_fours(self, player: int) -> int:
        count = 0
        board = self.board
        
        # Horizontal
        for row in range(self.height):
            for col in range(self.width - 3):
                if (board[row][col] == player and 
                    board[row][col + 1] == player and 
                    board[row][col + 2] == player and 
                    board[row][col + 3] == player):
                    count += 1
        
        # Vertical
        for row in range(self.height - 3):
            for col in range(self.width):
                if (board[row][col] == player and 
                    board[row + 1][col] == player and 
                    board[row + 2][col] == player and 
                    board[row + 3][col] == player):
                    count += 1
        
        # Diagonal (positive slope)
        for row in range(3, self.height):
            for col in range(self.width - 3):
                if (board[row][col] == player and 
                    board[row - 1][col + 1] == player and 
                    board[row - 2][col + 2] == player and 
                    board[row - 3][col + 3] == player):
                    count += 1
                
        for row in range(3, self.height):
            for col in range(3, self.width):
                if (board[row][col] == player and 
                    board[row - 1][col - 1] == player and 
                    board[row - 2][col - 2] == player and 
                    board[row - 3][col - 3] == player):
                    count += 1

        # Diagonal (negative slope)
        for row in range(self.height - 3):
            for col in range(self.width - 3):
                if (board[row][col] == player and 
                    board[row + 1][col + 1] == player and 
                    board[row + 2][col + 2] == player and 
                    board[row + 3][col + 3] == player):
                    count += 1
                
        for row in range(self.height - 3):
            for col in range(3, self.width):
                if (board[row][col] == player and 
                    board[row + 1][col - 1] == player and 
                    board[row + 2][col - 2] == player and 
                    board[row + 3][col - 3] == player):
                    count += 1
        
        return count
    
    def is_board_full(self) -> bool:
        return all(self.board[0][col] != 0 for col in range(self.width))
    
    def evaluate_board(self) -> int:
        ai_score = 0
        player_score = 0

        ai_score = self.count_potential_wins(2) * 10 + self.count_connected_fours(2) * 100
        player_score = self.count_potential_wins(1) * 10 + self.count_connected_fours(1) * 100
        
        # Center control bonus
        center_col = self.width // 2
        for row in range(self.height):
            if self.board[row][center_col] == 2:
                ai_score += 3
            elif self.board[row][center_col] == 1:
                player_score += 3
        
        return ai_score - player_score
    
    def count_potential_wins(self, player: int) -> int:
        count = 0
        board = self.board
        
        # Horizontal
        for row in range(self.height):
            for col in range(self.width - 3):
                sequence = [board[row][col], board[row][col + 1], 
                        board[row][col + 2], board[row][col + 3]]
                if sequence.count(player) == 3 and sequence.count(0) == 1:
                    count += 1
        
        # Vertical
        for row in range(self.height - 3):
            for col in range(self.width):
                sequence = [board[row][col], board[row + 1][col], 
                        board[row + 2][col], board[row + 3][col]]
                if sequence.count(player) == 3 and sequence.count(0) == 1:
                    count += 1
        
        # Diagonal (positive slope)
        for row in range(3, self.height):
            for col in range(self.width - 3):
                sequence = [board[row][col], board[row - 1][col + 1], 
                        board[row - 2][col + 2], board[row - 3][col + 3]]
                if sequence.count(player) == 3 and sequence.count(0) == 1:
                    count += 1
        
        for row in range(3, self.height):
            for col in range(3, self.width):
                sequence = [board[row][col], board[row - 1][col - 1], 
                        board[row - 2][col - 2], board[row - 3][col - 3]]
                if sequence.count(player) == 3 and sequence.count(0) == 1:
                    count += 1

        # Diagonal (negative slope)
        for row in range(self.height - 3):
            for col in range(self.width - 3):
                sequence = [board[row][col], board[row + 1][col + 1], 
                        board[row + 2][col + 2], board[row + 3][col + 3]]
                if sequence.count(player) == 3 and sequence.count(0) == 1:
                    count += 1
        
        for row in range(self.height - 3):
            for col in range(3, self.width):
                sequence = [board[row][col], board[row + 1][col - 1], 
                        board[row + 2][col - 2], board[row + 3][col - 3]]
                if sequence.count(player) == 3 and sequence.count(0) == 1:
                    count += 1
        
        return count


class ConnectFourAI:
    """
    AI agent supporting three algorithms:
    1. Minimax without alpha-beta pruning
    2. Minimax with alpha-beta pruning
    3. Expectiminimax (probabilistic)
    """
    def __init__(self, game: ConnectFour, depth: int = 4, use_alpha_beta: bool = True, use_expectiminimax: bool = False):
        self.game = game
        self.depth = depth
        self.use_alpha_beta = use_alpha_beta
        self.use_expectiminimax = use_expectiminimax  # NEW: Expectiminimax flag
        self.nodes_expanded = 0
        self.transposition_table = {}
    
    def get_best_move(self) -> int:
        self.nodes_expanded = 0
        start_time = time.time()
        
        if self.use_expectiminimax:
            best_score = float('-inf')
            best_move = None
            
            print("\n=== Expectiminimax Algorithm ===")
            for move in self.game.get_valid_moves():
                # AI chooses move, then goes through chance node
                expected_value = self.expectiminimax_chance_node(
                    chosen_column=move,
                    depth=self.depth - 1,
                    node_type="min"
                )
                
                print(f"Move {move}: Expected Value = {expected_value:.2f}")
                
                if expected_value > best_score or best_move is None:
                    best_score = expected_value
                    best_move = move
            
            end_time = time.time()
            print(f"\nAI expanded {self.nodes_expanded} nodes in {end_time - start_time:.2f} seconds")
            print(f"Best move: {best_move} with expected value {best_score:.2f}\n")
            
            return best_move
        
        elif self.use_alpha_beta:
            best_score = float('-inf')
            best_move = None
            
            print("\n=== Minimax with Alpha-Beta Pruning ===")
            for move in self.game.get_valid_moves():
                self.game.drop_disc(move)
                self.game.switch_player()
                
                score = self.minimax_alpha_beta(
                    depth=self.depth - 1,
                    alpha=float('-inf'),
                    beta=float('inf'),
                    is_maximizing=False
                )
                
                self.game.switch_player()
                self.undo_move(move)
                
                print(f"Move {move}: Score = {score}")
                
                if score > best_score or best_move is None:
                    best_score = score
                    best_move = move
            
            end_time = time.time()
            print(f"\nAI expanded {self.nodes_expanded} nodes in {end_time - start_time:.2f} seconds")
            print(f"Best move: {best_move} with score {best_score}\n")
            
            return best_move
        
        else:
            best_score = float('-inf')
            best_move = None
            
            print("\n=== Minimax (No Pruning) ===")
            for move in self.game.get_valid_moves():
                self.game.drop_disc(move)
                self.game.switch_player()
                
                score = self.minimax_without(
                    depth=self.depth - 1,
                    is_maximizing=False
                )
                
                self.game.switch_player()
                self.undo_move(move)
                
                print(f"Move {move}: Score = {score}")
                
                if score > best_score or best_move is None:
                    best_score = score
                    best_move = move
            
            end_time = time.time()
            print(f"\nAI expanded {self.nodes_expanded} nodes in {end_time - start_time:.2f} seconds")
            print(f"Best move: {best_move} with score {best_score}\n")
            
            return best_move
    
    
    def expectiminimax_chance_node(self, chosen_column: int, depth: int, node_type: str) -> float:
        """
        Chance node: After choosing a column, disc falls with probability:
        - 60% in chosen column
        - 20% in left column (if available)
        - 20% in right column (if available)
        - 40% to one side if only one neighbor available
        """
        self.nodes_expanded += 1
        
        expected_value = 0.0
        
        left_col = chosen_column - 1
        right_col = chosen_column + 1
        
        # Check validity
        chosen_valid = self.game.is_valid_move(chosen_column)
        left_valid = left_col >= 0 and self.game.is_valid_move(left_col)
        right_valid = right_col < self.game.width and self.game.is_valid_move(right_col)
        
        if not chosen_valid:
            return float('-inf') if node_type == "max" else float('inf')
        
        # Build outcomes with probabilities
        outcomes = []
        
        if chosen_valid and left_valid and right_valid:
            # All three available: 60%, 20%, 20%
            outcomes = [(chosen_column, 0.6), (left_col, 0.2), (right_col, 0.2)]
        elif chosen_valid and left_valid and not right_valid:
            # Only center and left: 60%, 40%
            outcomes = [(chosen_column, 0.6), (left_col, 0.4)]
        elif chosen_valid and right_valid and not left_valid:
            # Only center and right: 60%, 40%
            outcomes = [(chosen_column, 0.6), (right_col, 0.4)]
        else:
            # Only center: 100%
            outcomes = [(chosen_column, 1.0)]
        
        # Calculate expected value
        for column, probability in outcomes:
            self.game.drop_disc(column)
            self.game.switch_player()
            
            value = self.expectiminimax_recursive(depth, node_type)
            
            self.game.switch_player()
            self.undo_move(column)
            
            expected_value += probability * value
        
        return expected_value
    
    def expectiminimax_recursive(self, depth: int, node_type: str) -> float:
        """
        Recursive expectiminimax: MAX and MIN nodes
        """
        self.nodes_expanded += 1
        
        # Terminal checks
        if self.game.check_winner(2):
            return 1000 + depth
        if self.game.check_winner(1):
            return -1000 - depth
        if depth == 0 or self.game.is_board_full():
            return self.game.evaluate_board()
        
        valid_moves = self.game.get_valid_moves()
        
        if node_type == "max":
            # AI maximizes
            best_value = float('-inf')
            for move in valid_moves:
                expected_value = self.expectiminimax_chance_node(move, depth - 1, "min")
                best_value = max(best_value, expected_value)
            return best_value
        
        elif node_type == "min":
            # Player minimizes
            best_value = float('inf')
            for move in valid_moves:
                expected_value = self.expectiminimax_chance_node(move, depth - 1, "max")
                best_value = min(best_value, expected_value)
            return best_value
        
        return 0.0
    
    
    def undo_move(self, column: int):
        for row in range(self.game.height):
            if self.game.board[row][column] != 0:
                self.game.board[row][column] = 0
                break
    
    def minimax_without(self, depth: int, is_maximizing: bool) -> int:
        self.nodes_expanded += 1
        
        if self.game.check_winner(2):
            return 1000 + depth
        if self.game.check_winner(1):
            return -1000 - depth
        if depth == 0 or self.game.is_board_full():
            return self.game.evaluate_board()
        
        if is_maximizing:
            best_score = float('-inf')
            for move in self.game.get_valid_moves():
                self.game.drop_disc(move)
                self.game.switch_player()
                score = self.minimax_without(depth - 1, False)
                self.game.switch_player()
                self.undo_move(move)
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for move in self.game.get_valid_moves():
                self.game.drop_disc(move)
                self.game.switch_player()
                score = self.minimax_without(depth - 1, True)
                self.game.switch_player()
                self.undo_move(move)
                best_score = min(best_score, score)
            return best_score
    
    def minimax_alpha_beta(self, depth: int, alpha: float, beta: float, is_maximizing: bool) -> int:
        self.nodes_expanded += 1
        
        if self.game.check_winner(2):
            return 1000 + depth
        if self.game.check_winner(1):
            return -1000 - depth
        if depth == 0 or self.game.is_board_full():
            return self.game.evaluate_board()
        
        if is_maximizing:
            best_score = float('-inf')
            for move in self.game.get_valid_moves():
                self.game.drop_disc(move)
                self.game.switch_player()
                score = self.minimax_alpha_beta(depth - 1, alpha, beta, False)
                self.game.switch_player()
                self.undo_move(move)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break
            return best_score
        else:
            best_score = float('inf')
            for move in self.game.get_valid_moves():
                self.game.drop_disc(move)
                self.game.switch_player()
                score = self.minimax_alpha_beta(depth - 1, alpha, beta, True)
                self.game.switch_player()
                self.undo_move(move)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if alpha >= beta:
                    break
            return best_score

# # ==================== USAGE EXAMPLES ====================

# if __name__ == "__main__":
    
#     game = ConnectFour(width=7, height=6)
#     gui = ConnectFourGUI(game)
#     gui.run()
    
#     print("Testing all three algorithms:\n")
    
#     # 1. Minimax without pruning
#     print("1. MINIMAX (No Pruning)")
#     print("-" * 50)
#     ai1 = ConnectFourAI(game, depth=3, use_alpha_beta=False, use_expectiminimax=False)
#     move1 = ai1.get_best_move()
    
#     # 2. Minimax with alpha-beta
#     print("\n2. MINIMAX WITH ALPHA-BETA PRUNING")
#     print("-" * 50)
#     ai2 = ConnectFourAI(game, depth=3, use_alpha_beta=True, use_expectiminimax=False)
#     move2 = ai2.get_best_move()
    
#     # 3. Expectiminimax
#     print("\n3. EXPECTIMINIMAX")
#     print("-" * 50)
#     ai3 = ConnectFourAI(game, depth=3, use_alpha_beta=False, use_expectiminimax=True)
#     move3 = ai3.get_best_move()

import tkinter as tk
from tkinter import messagebox
import threading
import time

class ConnectFourGUI(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Connect Four")
        self.resizable(False, False)

        self.game = game
        self.ai = ConnectFourAI(self.game, depth=3, use_alpha_beta=True, use_expectiminimax=False)
        self.cell_size = 70
        self.radius = 30  # for rounded discs
        self.canvas_width = self.game.width * self.cell_size
        self.canvas_height = (self.game.height + 1) * self.cell_size
        self.vs_ai = tk.BooleanVar(value=True)
        self.ai_thinking = False

        # Controls
        control_frame = tk.Frame(self)
        control_frame.pack(padx=6, pady=6, anchor='w')
        tk.Button(control_frame, text="Reset", command=self.reset_game, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=4)
        tk.Checkbutton(control_frame, text="Play vs AI", variable=self.vs_ai, font=("Arial", 10)).grid(row=0, column=1, padx=4)
        tk.Label(control_frame, text="AI Depth:", font=("Arial", 10)).grid(row=0, column=2, padx=(12,0))
        self.depth_spin = tk.Spinbox(control_frame, from_=1, to=6, width=3, font=("Arial", 10), command=self.change_depth)
        self.depth_spin.delete(0, 'end'); self.depth_spin.insert(0, str(self.ai.depth))
        self.depth_spin.grid(row=0, column=3, padx=4)

        # Algorithm choices
        algo_frame = tk.Frame(self)
        algo_frame.pack(padx=6, anchor='w')
        self.algo_var = tk.StringVar(value='alphabeta')
        tk.Label(algo_frame, text="AI Algo:", font=("Arial", 10)).pack(side='left')
        tk.Radiobutton(algo_frame, text='Alpha-Beta', variable=self.algo_var, value='alphabeta', command=self.change_algo).pack(side='left')
        tk.Radiobutton(algo_frame, text='Minimax', variable=self.algo_var, value='minimax', command=self.change_algo).pack(side='left')
        tk.Radiobutton(algo_frame, text='Expecti', variable=self.algo_var, value='expecti', command=self.change_algo).pack(side='left')

        # Canvas
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg="#1A237E", highlightthickness=0)
        self.canvas.pack(padx=6, pady=6)
        self.canvas.bind('<Button-1>', self.on_canvas_click)

        # Status
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(self, textvariable=self.status_var, font=("Arial", 12, "bold"), fg="#FFEB3B")
        self.status_label.pack(pady=(0,6))

        self.draw_board()
        self.update_status()

    # ----------------- DRAW BOARD -----------------
    def draw_board(self):
        self.canvas.delete("all")
        radius = self.cell_size/2 - 5
        
        # Draw background gradient
        for i in range(self.game.height + 1):
            color = f"#{int(26 + i*15):02x}{int(35 + i*15):02x}{int(126 + i*5):02x}"
            self.canvas.create_rectangle(0, i*self.cell_size, self.canvas_width, (i+1)*self.cell_size, fill=color, outline="")

        # Draw discs with rounded style
        for row in range(self.game.height):
            for col in range(self.game.width):
                x = col * self.cell_size + self.cell_size/2
                y = (row+1) * self.cell_size + self.cell_size/2
                color = "white"
                if self.game.board[row][col] == 1:
                    color = "red"
                elif self.game.board[row][col] == 2:
                    color = "yellow"
                self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color, outline="black", width=2)

        # Column numbers (top) - vertical, outside circles
        for col in range(self.game.width):
            x0 = col * self.cell_size
            self.canvas.create_text(x0 + self.cell_size/2, 20, text=str(col), fill='black', font=('Arial', 14, 'bold'))

        # Row numbers (left side) - vertical, outside circles
        for row in range(self.game.height):
            y0 = (row+1) * self.cell_size
            self.canvas.create_text(15, y0 + self.cell_size/2, text=str(row), fill='black', font=('Arial', 12, 'bold'))

    def draw_disc(self, x, y, player):
        if player == 0:
            color = "#ECEFF1"
        elif player == 1:
            color = "#F44336"  # red
        else:
            color = "#FFEB3B"  # yellow

        # Draw circle with slight shadow
        self.canvas.create_oval(x-self.radius, y-self.radius, x+self.radius, y+self.radius, fill=color, outline="#000000", width=2)
        # Add 3D highlight
        self.canvas.create_oval(x-self.radius+5, y-self.radius+5, x+self.radius-5, y+self.radius-5, outline="", fill=color)

    # ----------------- GAME LOGIC -----------------
    def on_canvas_click(self, event):
        if self.game.game_over or self.ai_thinking:
            return
        col = event.x // self.cell_size
        self.player_move(col)

    def player_move(self, col):
        if not self.game.is_valid_move(col):
            return
        self.game.drop_disc(col)
        if self.game.check_winner(self.game.current_player):
            self.game.game_over = True
            self.game.winner = self.game.current_player
        self.game.switch_player()
        self.draw_board()
        self.update_status()

        if self.vs_ai.get() and not self.game.game_over:
            self.ai_thinking = True
            threading.Thread(target=self.ai_move).start()

    def ai_move(self):
        best_move = self.ai.get_best_move()
        time.sleep(0.3)
        if best_move is not None and self.game.is_valid_move(best_move):
            self.game.drop_disc(best_move)
            if self.game.check_winner(self.game.current_player):
                self.game.game_over = True
                self.game.winner = self.game.current_player
            self.game.switch_player()
        self.ai_thinking = False
        self.draw_board()
        self.update_status()

    def update_status(self):
        if self.game.game_over:
            if self.game.winner == 1:
                text = "Player wins! 🎉"
            elif self.game.winner == 2:
                text = "AI wins! 🤖"
            else:
                text = "Draw! 🤝"
        else:
            text = f"Current Turn: {'Player' if self.game.current_player == 1 else 'AI'}"
        self.status_var.set(text)

    def reset_game(self):
        self.game.reset_game()
        self.draw_board()
        self.update_status()

    def change_depth(self):
        try:
            self.ai.depth = int(self.depth_spin.get())
        except ValueError:
            pass

    def change_algo(self):
        algo = self.algo_var.get()
        if algo == 'alphabeta':
            self.ai.use_alpha_beta = True
            self.ai.use_expectiminimax = False
        elif algo == 'minimax':
            self.ai.use_alpha_beta = False
            self.ai.use_expectiminimax = False
        elif algo == 'expecti':
            self.ai.use_alpha_beta = False
            self.ai.use_expectiminimax = True

    def run(self):
        self.mainloop()

# ================== USAGE ==================
if __name__ == "__main__":
    game = ConnectFour(width=7, height=6)
    gui = ConnectFourGUI(game)
    gui.run()
