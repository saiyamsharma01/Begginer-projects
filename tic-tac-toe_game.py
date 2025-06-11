import tkinter as tk
from tkinter import messagebox, font


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.configure(bg="#2c3e50")

        # Game variables
        self.current_player = "X"
        self.game_over = False
        self.move_count = 0
        self.x_wins = 0
        self.o_wins = 0
        self.ties = 0

        # Custom fonts
        self.button_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=14)
        self.score_font = font.Font(family="Helvetica", size=12)

        # Colors
        self.bg_color = "#2c3e50"
        self.button_bg = "#34495e"
        self.button_fg = "#ecf0f1"
        self.x_color = "#3498db"
        self.o_color = "#e74c3c"
        self.win_color = "#2ecc71"
        self.label_color = "#ecf0f1"

        # Create main container frame to center everything
        self.main_frame = tk.Frame(root, bg=self.bg_color)
        self.main_frame.pack(expand=True)

        # Create UI
        self.create_widgets()

        # Center the window on screen
        self.center_window()

    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')

    def create_widgets(self):
        # Score display
        self.score_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.score_frame.pack(pady=(10, 20))

        self.x_score_label = tk.Label(self.score_frame,text=f"Player X: {self.x_wins}",font=self.score_font,bg=self.bg_color,fg=self.x_color)
        self.x_score_label.pack(side=tk.LEFT, padx=10)

        self.tie_score_label = tk.Label(self.score_frame,text=f"Ties: {self.ties}",font=self.score_font, bg=self.bg_color, fg=self.label_color )
        self.tie_score_label.pack(side=tk.LEFT, padx=10)

        self.o_score_label = tk.Label(self.score_frame,text=f"Player O: {self.o_wins}",font=self.score_font,bg=self.bg_color,fg=self.o_color)
        self.o_score_label.pack(side=tk.LEFT, padx=10)

        # Game board frame
        self.board_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.board_frame.pack()

        # Game buttons
        self.buttons = []
        for i in range(9):
            button = tk.Button(self.board_frame,text="",font=self.button_font,width=4, height=2,bg=self.button_bg,fg=self.button_fg,activebackground="#7f8c8d",
                         relief=tk.FLAT, bd=0,command=lambda idx=i: self.button_click(idx))
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(button)

        # Status label
        self.status_label = tk.Label(self.main_frame,text=f"{self.current_player}'s Turn",font=self.label_font,bg=self.bg_color,fg=self.label_color)
        self.status_label.pack(pady=(20, 10))

        # Reset button
        self.reset_button = tk.Button(self.main_frame,text="New Game",font=self.label_font,bg="#3498db",fg="#ecf0f1",activebackground="#2980b9",relief=tk.FLAT,command=self.reset_game)
        self.reset_button.pack(pady=(0, 10), padx=10, fill=tk.X)

    def button_click(self, index):
        if not self.game_over and self.buttons[index]["text"] == "":
            self.buttons[index]["text"] = self.current_player
            self.buttons[index]["fg"] = self.x_color if self.current_player == "X" else self.o_color
            self.move_count += 1

            if self.check_winner():
                self.game_over = True
                self.update_score()
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.highlight_winner()
            elif self.move_count == 9:
                self.game_over = True
                self.ties += 1
                self.update_score()
                messagebox.showinfo("Game Over", "It's a tie!")
            else:
                self.toggle_player()

    def check_winner(self):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]  # diagonals
        ]

        for combo in win_combinations:
            if (self.buttons[combo[0]]["text"] ==
                    self.buttons[combo[1]]["text"] ==
                    self.buttons[combo[2]]["text"] != ""):
                return True
        return False

    def highlight_winner(self):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]  # diagonals
        ]

        for combo in win_combinations:
            if (self.buttons[combo[0]]["text"] ==
                    self.buttons[combo[1]]["text"] ==
                    self.buttons[combo[2]]["text"] != ""):
                for index in combo:
                    self.buttons[index]["bg"] = self.win_color
                break

    def toggle_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"
        self.status_label.config(text=f"{self.current_player}'s Turn")

    def update_score(self):
        if self.game_over:
            if self.move_count == 9 and not self.check_winner():
                self.ties += 1
            elif self.current_player == "X":
                self.x_wins += 1
            else:
                self.o_wins += 1

        self.x_score_label.config(text=f"Player X: {self.x_wins}")
        self.o_score_label.config(text=f"Player O: {self.o_wins}")
        self.tie_score_label.config(text=f"Ties: {self.ties}")

    def reset_game(self):
        self.current_player = "X"
        self.game_over = False
        self.move_count = 0

        for button in self.buttons:
            button.config(text="", bg=self.button_bg, fg=self.button_fg)

        self.status_label.config(text=f"{self.current_player}'s Turn")


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()