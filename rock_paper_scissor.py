import tkinter as tk
from tkinter import font, messagebox
import random

class RockPaperScissorsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors Game")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f8ff")
        self.root.resizable(True, True)

        # Custom fonts
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.button_font = font.Font(family="Arial", size=14)
        self.result_font = font.Font(family="Courier", size=16, weight="bold")

        # Game variables
        self.user_score = 0
        self.computer_score = 0
        self.choices = ["Rock", "Paper", "Scissor"]

        self.setup_ui()

    def setup_ui(self):
        # Header frame
        header_frame = tk.Frame(self.root, bg="#4682b4", height=80)
        header_frame.pack(fill="x", padx=10, pady=10)

        title_label = tk.Label(header_frame, text="Rock Paper Scissors",font=self.title_font, bg="#4682b4", fg="white")
        title_label.pack(pady=20)

        # Score display
        score_frame = tk.Frame(self.root, bg="#f0f8ff")
        score_frame.pack(pady=10)

        self.user_score_label = tk.Label(score_frame, text=f"Your Score: {self.user_score}",font=self.button_font, bg="#f0f8ff")
        self.user_score_label.pack(side="left", padx=20)

        self.computer_score_label = tk.Label(score_frame, text=f"Computer Score: {self.computer_score}",font=self.button_font, bg="#f0f8ff")
        self.computer_score_label.pack(side="right", padx=20)

        # Choice buttons
        button_frame = tk.Frame(self.root, bg="#f0f8ff")
        button_frame.pack(pady=20)

        self.rock_btn = tk.Button(button_frame, text="Rock", font=self.button_font,bg="#ff6b6b", fg="white", width=10, height=2,command=lambda: self.play_game("Rock"))
        self.rock_btn.pack(side="left", padx=10)

        self.paper_btn = tk.Button(button_frame, text="Paper", font=self.button_font,bg="#4ecdc4", fg="white", width=10, height=2,command=lambda: self.play_game("Paper"))
        self.paper_btn.pack(side="left", padx=10)

        self.scissor_btn = tk.Button(button_frame, text="Scissor", font=self.button_font,bg="#ffbe76", fg="white", width=10, height=2,command=lambda: self.play_game("Scissor"))
        self.scissor_btn.pack(side="left", padx=10)

        # Result display
        self.result_label = tk.Label(self.root, text="Choose your move!",font=self.result_font, bg="#f0f8ff", fg="#2c3e50")
        self.result_label.pack(pady=20)

        # Choices display
        choices_frame = tk.Frame(self.root, bg="#f0f8ff")
        choices_frame.pack(pady=10)

        self.user_choice_label = tk.Label(choices_frame, text="Your choice: -",font=self.button_font, bg="#f0f8ff")
        self.user_choice_label.pack(side="left", padx=20)

        self.computer_choice_label = tk.Label(choices_frame, text="Computer choice: -",font=self.button_font, bg="#f0f8ff")
        self.computer_choice_label.pack(side="right", padx=20)

        # Reset button
        reset_btn = tk.Button(self.root, text="Reset Game", font=self.button_font,bg="#576574", fg="white", command=self.reset_game)
        reset_btn.pack(pady=10)

    def play_game(self, user_choice):
        computer_choice = random.choice(self.choices)

        # Update choice displays
        self.user_choice_label.config(text=f"Your choice: {user_choice}")
        self.computer_choice_label.config(text=f"Computer choice: {computer_choice}")

        # Determine winner
        if user_choice == computer_choice:
            result = "It's a Tie!"
            color = "#f39c12"  # Orange
        elif (user_choice == "Rock" and computer_choice == "Scissor") or \
             (user_choice == "Paper" and computer_choice == "Rock") or \
             (user_choice == "Scissor" and computer_choice == "Paper"):
            result = "You Win!"
            color = "#2ecc71"  # Green
            self.user_score += 1
        else:
            result = "Computer Wins!"
            color = "#e74c3c"  # Red
            self.computer_score += 1

        # Update UI
        self.result_label.config(text=result, fg=color)
        self.user_score_label.config(text=f"Your Score: {self.user_score}")
        self.computer_score_label.config(text=f"Computer Score: {self.computer_score}")

        # Flash animation for the winning choice
        self.flash_choice(user_choice, computer_choice, result)

    def flash_choice(self, user_choice, computer_choice, result):
        if result == "You Win!":
            button = self.get_button_by_choice(user_choice)
            self.flash_button(button, "#2ecc71")
        elif result == "Computer Wins!":
            button = self.get_button_by_choice(computer_choice)
            self.flash_button(button, "#e74c3c")
        else:  # Tie
            user_button = self.get_button_by_choice(user_choice)
            computer_button = self.get_button_by_choice(computer_choice)
            self.flash_button(user_button, "#f39c12")
            self.flash_button(computer_button, "#f39c12")

    def get_button_by_choice(self, choice):
        if choice == "Rock":
            return self.rock_btn
        elif choice == "Paper":
            return self.paper_btn
        else:
            return self.scissor_btn

    def flash_button(self, button, color):
        original_bg = button.cget("bg")
        button.config(bg=color)
        self.root.after(300, lambda: button.config(bg=original_bg))

    def reset_game(self):
        self.user_score = 0
        self.computer_score = 0
        self.user_score_label.config(text=f"Your Score: {self.user_score}")
        self.computer_score_label.config(text=f"Computer Score: {self.computer_score}")
        self.result_label.config(text="Choose your move!", fg="#2c3e50")
        self.user_choice_label.config(text="Your choice: -")
        self.computer_choice_label.config(text="Computer choice: -")

def main():
    root = tk.Tk()
    game = RockPaperScissorsGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()