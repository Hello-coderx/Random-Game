import random
import sys
import tkinter as tk
from tkinter import messagebox


# ---------------------------------------------------------------------------
# Core logic (shared by both console and GUI)
# ---------------------------------------------------------------------------

def generate_secret_number(lower, upper):
    return random.randint(lower, upper)


def evaluate_guess(guess, secret):
    if guess > secret:
        return "Too high"
    if guess < secret:
        return "Too low"
    return "Correct"


# ---------------------------------------------------------------------------
# Console mode
# ---------------------------------------------------------------------------

def get_valid_guess(prompt):
    while True:
        raw = input(prompt)
        try:
            return int(raw)
        except ValueError:
            print(f"Invalid input: '{raw}' is not an integer. Please enter a whole number.")


def display_win(attempts_used):
    print(f"Congratulations! You guessed the number in {attempts_used} attempt(s)!")


def display_game_over(secret):
    print("Game Over")
    print(f"The secret number was {secret}.")


def ask_play_again():
    while True:
        raw = input("Play again? (y/n): ").strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("Please enter 'y' or 'n'.")


def play_round_console(lower, upper, attempt_limit):
    secret = generate_secret_number(lower, upper)
    attempts_used = 0

    for _ in range(attempt_limit):
        guess = get_valid_guess("Enter your guess: ")
        attempts_used += 1
        feedback = evaluate_guess(guess, secret)
        print(feedback)
        if feedback == "Correct":
            display_win(attempts_used)
            return True

    display_game_over(secret)
    return False


def run_console():
    bonus_mode = "--bonus" in sys.argv

    if not bonus_mode:
        play_round_console(1, 100, 7)
        return

    lower = 1
    upper = 100

    while True:
        print(f"Current range: [{lower}, {upper}]")
        play_round_console(lower, upper, 7)
        upper += 50
        if not ask_play_again():
            break


# ---------------------------------------------------------------------------
# GUI mode (tkinter)
# ---------------------------------------------------------------------------

class GameGUI:
    ATTEMPT_LIMIT = 7

    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.resizable(False, False)

        self.bonus_mode = tk.BooleanVar(value=False)
        self.lower = 1
        self.upper = 100
        self.secret = None
        self.attempts_used = 0

        self._build_ui()
        self._new_round()

    def _build_ui(self):
        pad = {"padx": 10, "pady": 6}

        # Range label
        self.range_label = tk.Label(self.root, text="", font=("Arial", 11))
        self.range_label.grid(row=0, column=0, columnspan=2, **pad)

        # Attempts label
        self.attempts_label = tk.Label(self.root, text="", font=("Arial", 11))
        self.attempts_label.grid(row=1, column=0, columnspan=2, **pad)

        # Guess entry
        tk.Label(self.root, text="Your guess:", font=("Arial", 11)).grid(
            row=2, column=0, sticky="e", **pad
        )
        self.entry = tk.Entry(self.root, font=("Arial", 13), width=10)
        self.entry.grid(row=2, column=1, sticky="w", **pad)
        self.entry.bind("<Return>", lambda e: self._submit_guess())

        # Submit button
        self.submit_btn = tk.Button(
            self.root, text="Guess", font=("Arial", 11),
            width=10, command=self._submit_guess
        )
        self.submit_btn.grid(row=3, column=0, columnspan=2, **pad)

        # Feedback label
        self.feedback_label = tk.Label(
            self.root, text="", font=("Arial", 13, "bold"), fg="navy"
        )
        self.feedback_label.grid(row=4, column=0, columnspan=2, **pad)

        # Bonus mode checkbox
        tk.Checkbutton(
            self.root, text="Bonus mode (harder each round)",
            variable=self.bonus_mode, font=("Arial", 10)
        ).grid(row=5, column=0, columnspan=2, **pad)

        # New game button
        tk.Button(
            self.root, text="New Game", font=("Arial", 11),
            width=10, command=self._start_new_game
        ).grid(row=6, column=0, columnspan=2, **pad)

    def _new_round(self):
        self.secret = generate_secret_number(self.lower, self.upper)
        self.attempts_used = 0
        self._update_labels()
        self.feedback_label.config(text="")
        self.entry.config(state="normal")
        self.submit_btn.config(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.focus()

    def _update_labels(self):
        self.range_label.config(
            text=f"Guess a number between {self.lower} and {self.upper}"
        )
        remaining = self.ATTEMPT_LIMIT - self.attempts_used
        self.attempts_label.config(text=f"Attempts remaining: {remaining}")

    def _submit_guess(self):
        raw = self.entry.get().strip()
        try:
            guess = int(raw)
        except ValueError:
            self.feedback_label.config(
                text=f"'{raw}' is not a valid number.", fg="red"
            )
            self.entry.delete(0, tk.END)
            return

        self.attempts_used += 1
        self.entry.delete(0, tk.END)
        feedback = evaluate_guess(guess, self.secret)

        if feedback == "Correct":
            self.feedback_label.config(
                text=f"Correct! You got it in {self.attempts_used} attempt(s)!",
                fg="green"
            )
            self._end_round(won=True)
            return

        self._update_labels()

        if self.attempts_used >= self.ATTEMPT_LIMIT:
            self.feedback_label.config(
                text=f"{feedback} — Game Over! The number was {self.secret}.",
                fg="red"
            )
            self._end_round(won=False)
        else:
            self.feedback_label.config(text=feedback, fg="navy")

    def _end_round(self, won):
        self.entry.config(state="disabled")
        self.submit_btn.config(state="disabled")

        if self.bonus_mode.get():
            play_again = messagebox.askyesno(
                "Play Again?", "Do you want to play another round?"
            )
            if play_again:
                self.upper += 50
                self._new_round()
        else:
            play_again = messagebox.askyesno(
                "Play Again?", "Do you want to play again?"
            )
            if play_again:
                self._start_new_game()

    def _start_new_game(self):
        self.lower = 1
        self.upper = 100
        self._new_round()


def run_gui():
    root = tk.Tk()
    GameGUI(root)
    root.mainloop()


# ---------------------------------------------------------------------------
# Entry point — choose GUI or console
# ---------------------------------------------------------------------------

def main():
    if "--console" in sys.argv:
        run_console()
    else:
        run_gui()


if __name__ == "__main__":
    main()
