import random
import sys


def generate_secret_number(lower, upper):
    return random.randint(lower, upper)


def evaluate_guess(guess, secret):
    if guess > secret:
        return "Too high"
    if guess < secret:
        return "Too low"
    return "Correct"


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


def play_round(lower, upper, attempt_limit):
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


def main():
    bonus_mode = "--bonus" in sys.argv

    if not bonus_mode:
        play_round(1, 100, 7)
        return

    lower = 1
    upper = 100

    while True:
        print(f"Current range: [{lower}, {upper}]")
        play_round(lower, upper, 7)
        upper += 50
        if not ask_play_again():
            break


if __name__ == "__main__":
    main()
