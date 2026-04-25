# Number Guessing Game

This project is a Python-based application that offers a Number Guessing Game through two distinct interfaces: a Graphical User Interface (GUI) and a Command Line Interface (CLI). It features automated testing with property-based and example-based methodologies.

---

## Technical Specifications

### Core Logic
* **Generation:** Randomized secret number generation within dynamic ranges.
* **Evaluation:** Logical comparison providing feedback of "Too high", "Too low", or "Correct".
* **Validation:** Error handling for non-integer inputs to prevent application crashes.

### Game Modes
* **Standard Mode:** A fixed range of 1 to 100 with a limit of 7 attempts.
* **Bonus Mode:** Progressive difficulty where the upper bound increases by 50 after each round.
* **Interfaces:** Desktop window via Tkinter or terminal-based interaction via sys.argv flags.

---

## Execution Instructions

### Prerequisites
* Python 3.x
* Pytest (for testing)
* Hypothesis (for property-based testing)

### Launching the Application
* **GUI Mode (Default):** `python game.py`
* **Console Mode:** `python game.py --console`
* **Console with Bonus Mode:** `python game.py --console --bonus`

---

## Testing Framework

The application is verified using the following testing strategies:

* **Smoke Testing:** Basic verification of the test environment.
* **Example-Based Testing:** Specific input/output scenarios using `pytest.mark.parametrize` to check "Yes/No" logic and case sensitivity.
* **Mocking:** Use of `unittest.mock` to simulate user input and print statements without requiring manual interaction.
* **Property-Based Testing:** Utilizing the `Hypothesis` library to generate thousands of invalid string sequences to ensure the "Play Again" loop remains robust against any arbitrary input.

### Running Tests
To execute the full test suite, run:
`python -m pytest test_game.py`

---

## File Architecture

* **game.py:** Contains the shared core logic, the `GameGUI` class for the Tkinter interface, and the CLI execution loop.
* **test_game.py:** Contains the comprehensive suite of tests, including unit tests for main game loops and property-based strategies for input validation.
