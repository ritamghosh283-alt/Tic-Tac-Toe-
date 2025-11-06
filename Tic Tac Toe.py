import tkinter as tk
import random
import math

class TicTacToeAI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Tic Tac Toe")
        self.root.resizable(False, False)
        self.bg_color = "#2C3E50"
        self.btn_color = "#ECF0F1"
        self.x_color = "#E74C3C"
        self.o_color = "#3498DB"

        self.board = ['' for _ in range(9)]
        self.current_player = 'X'  # Human starts first by default
        self.game_over = False

        # Score tracking
        self.x_score = 0
        self.o_score = 0
        self.draw_score = 0

        self.create_ui()

    def create_ui(self):
        self.root.configure(bg=self.bg_color)

        # Title
        tk.Label(
            self.root,
            text="AI Tic Tac Toe",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg="white",
            pady=10
        ).grid(row=0, column=0, columnspan=3)

        # Turn indicator
        self.turn_label = tk.Label(
            self.root,
            text="Your Turn (X)",
            font=("Arial", 14),
            bg=self.bg_color,
            fg="white"
        )
        self.turn_label.grid(row=1, column=0, columnspan=3, pady=5)

        # Board Buttons
        self.buttons = []
        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    self.root, text='', font=('Arial', 36, 'bold'),
                    width=5, height=2, bg=self.btn_color,
                    command=lambda idx=i*3+j: self.player_move(idx)
                )
                btn.grid(row=i+2, column=j, padx=5, pady=5)
                self.buttons.append(btn)

        # Score Label
        self.score_label = tk.Label(
            self.root,
            text=f"X Wins: {self.x_score}  |  O Wins: {self.o_score}  |  Draws: {self.draw_score}",
            font=("Arial", 14),
            bg=self.bg_color,
            fg="white",
            pady=10
        )
        self.score_label.grid(row=5, column=0, columnspan=3)

        # Control Buttons
        control_frame = tk.Frame(self.root, bg=self.bg_color)
        control_frame.grid(row=6, column=0, columnspan=3, pady=10)

        new_game_btn = tk.Button(
            control_frame, text="New Game",
            font=("Arial", 12, "bold"),
            bg="#27AE60", fg="white",
            width=12, height=1,
            command=self.reset_game, cursor="hand2"
        )
        new_game_btn.pack(side=tk.LEFT, padx=5)

        reset_score_btn = tk.Button(
            control_frame, text="Reset Score",
            font=("Arial", 12, "bold"),
            bg="#E67E22", fg="white",
            width=12, height=1,
            command=self.reset_score, cursor="hand2"
        )
        reset_score_btn.pack(side=tk.LEFT, padx=5)

        quit_btn = tk.Button(
            control_frame, text="Quit",
            font=("Arial", 12, "bold"),
            bg="#C0392B", fg="white",
            width=12, height=1,
            command=self.root.quit, cursor="hand2"
        )
        quit_btn.pack(side=tk.LEFT, padx=5)

    # Player move
    def player_move(self, idx):
        if self.board[idx] == '' and not self.game_over:
            self.board[idx] = 'X'
            self.buttons[idx].config(text='X', fg=self.x_color, state=tk.DISABLED)
            if self.check_winner('X'):
                self.turn_label.config(text="🎉 You Win! Restarting...", fg="#F1C40F")
                self.game_over = True
                self.x_score += 1
                self.update_score()
                self.next_starter = 'X'
                self.root.after(2000, self.reset_game)
                return
            elif self.is_draw():
                self.turn_label.config(text="It's a Draw! Restarting...", fg="#F1C40F")
                self.game_over = True
                self.draw_score += 1
                self.update_score()
                self.next_starter = 'O' if self.current_player == 'X' else 'X'  # alternate start
                self.root.after(2000, self.reset_game)
                return
            else:
                self.turn_label.config(text="AI's Turn...", fg=self.o_color)
                self.root.after(600, self.ai_move)

    # AI move using Minimax algorithm
    def ai_move(self):
        best_score = -math.inf
        best_move = None

        for i in range(9):
            if self.board[i] == '':
                self.board[i] = 'O'
                score = self.minimax(self.board, 0, False)
                self.board[i] = ''
                if score > best_score:
                    best_score = score
                    best_move = i

        self.board[best_move] = 'O'
        self.buttons[best_move].config(text='O', fg=self.o_color, state=tk.DISABLED)

        if self.check_winner('O'):
            self.turn_label.config(text="🤖 AI Wins! Restarting...", fg="#E67E22")
            self.game_over = True
            self.o_score += 1
            self.update_score()
            self.next_starter = 'O'
            self.root.after(2000, self.reset_game)
        elif self.is_draw():
            self.turn_label.config(text="It's a Draw! Restarting...", fg="#F1C40F")
            self.game_over = True
            self.draw_score += 1
            self.update_score()
            self.next_starter = 'X' if self.current_player == 'O' else 'O'
            self.root.after(2000, self.reset_game)
        else:
            self.turn_label.config(text="Your Turn (X)", fg="white")

    # Minimax algorithm for AI
    def minimax(self, board, depth, is_maximizing):
        if self.check_winner('O'):
            return 1
        elif self.check_winner('X'):
            return -1
        elif self.is_draw():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for i in range(9):
                if board[i] == '':
                    board[i] = 'O'
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ''
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(9):
                if board[i] == '':
                    board[i] = 'X'
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ''
                    best_score = min(score, best_score)
            return best_score

    # Check winner
    def check_winner(self, player):
        win_patterns = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        for pattern in win_patterns:
            if all(self.board[i] == player for i in pattern):
                for i in pattern:
                    self.buttons[i].config(bg="#27AE60")
                return True
        return False

    # Check draw
    def is_draw(self):
        return all(cell != '' for cell in self.board)

    # Reset for new game
    def reset_game(self):
        self.board = ['' for _ in range(9)]
        self.game_over = False
        for btn in self.buttons:
            btn.config(text='', state=tk.NORMAL, bg=self.btn_color)

        # Set next starter
        if hasattr(self, 'next_starter'):
            self.current_player = self.next_starter
        else:
            self.current_player = 'X'

        if self.current_player == 'X':
            self.turn_label.config(text="Your Turn (X)", fg="white")
        else:
            self.turn_label.config(text="AI Starts...", fg=self.o_color)
            self.root.after(100,self.ai_move)

    # Reset full score
    def reset_score(self):
        self.x_score = 0
        self.o_score = 0
        self.draw_score = 0
        self.update_score()
        self.reset_game()

    # Update score label
    def update_score(self):
        self.score_label.config(
            text=f"X Wins: {self.x_score}  |  O Wins: {self.o_score}  |  Draws: {self.draw_score}"
        )

def main():
    root = tk.Tk()
    TicTacToeAI(root)
    root.mainloop()

if __name__ == "__main__":
    main()