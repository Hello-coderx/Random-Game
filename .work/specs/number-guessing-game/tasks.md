# Implementation Plan: Number Guessing Game

## Overview

Implement a single-file Python CLI number guessing game (`game.py`) with a companion test file (`test_game.py`). The implementation follows the component separation defined in the design: number generation, input handling, and feedback display. Tasks build incrementally from pure utility functions up through the full game loop, with the bonus mode layered on last.

## Tasks

- [x] 1. Set up project files and testing framework
  - Create `game.py` with module-level docstring and standard library imports (`random`, `sys`)
  - Create `test_game.py` with `pytest` and `hypothesis` imports and a placeholder smoke test
  - Verify `pytest` and `hypothesis` are available (install if needed: `pip install pytest hypothesis`)
  - _Requirements: 1.1, 1.2_

- [x] 2. Implement `generate_secret_number` and `evaluate_guess`
  - [x] 2.1 Implement `generate_secret_number(lower: int, upper: int) -> int`
    - Use `random.randint(lower, upper)` for uniform inclusive sampling
    - No shared state; each call is independent
    - _Requirements: 1.1, 1.2, 1.3_

  - [ ]* 2.2 Write property test for `generate_secret_number` (Property 1)
    - **Property 1: Secret number is always within range**
    - Use `st.integers()` pairs where `lower <= upper`
    - **Validates: Requirements 1.1, 1.2**

  - [x] 2.3 Implement `evaluate_guess(guess: int, secret: int) -> str`
    - Return `"Too high"` when `guess > secret`, `"Too low"` when `guess < secret`, `"Correct"` when equal
    - Pure function, no side effects
    - _Requirements: 3.1, 3.2, 3.3_

  - [ ]* 2.4 Write property test for `evaluate_guess` (Property 2)
    - **Property 2: evaluate_guess feedback is consistent with ordering**
    - Use `st.integers()` for both `guess` and `secret`
    - **Validates: Requirements 3.1, 3.2, 3.3**

- [x] 3. Implement feedback display functions
  - [x] 3.1 Implement `display_win(attempts_used: int) -> None`
    - Print a congratulatory message that includes the `attempts_used` count
    - _Requirements: 4.1_

  - [ ]* 3.2 Write property test for `display_win` (Property 4)
    - **Property 4: Win message contains attempts used**
    - Use `st.integers(min_value=1, max_value=7)` for `attempts_used`
    - Capture stdout and assert the decimal representation of `n` is present
    - **Validates: Requirements 4.1**

  - [x] 3.3 Implement `display_game_over(secret: int) -> None`
    - Print `"Game Over"` and reveal the `secret` value
    - _Requirements: 5.1, 5.2_

  - [ ]* 3.4 Write property test for `display_game_over` (Property 5)
    - **Property 5: Game over message contains secret and "Game Over"**
    - Use `st.integers()` for `secret`
    - Capture stdout and assert both `"Game Over"` and the decimal representation of `secret` are present
    - **Validates: Requirements 5.1, 5.2**

- [x] 4. Checkpoint — Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Implement `get_valid_guess`
  - [x] 5.1 Implement `get_valid_guess(prompt: str) -> int`
    - Print `prompt`, read a line from stdin, attempt `int()` conversion
    - On `ValueError` print an error message and loop without returning; do not increment any counter
    - Return only when a valid integer is obtained
    - _Requirements: 6.1, 6.2, 6.3_

  - [ ]* 5.2 Write property test for `get_valid_guess` (Property 3)
    - **Property 3: Invalid input does not advance attempts**
    - Use `st.lists(st.text(min_size=1))` of non-integer strings followed by one valid integer string; patch `input()` with `unittest.mock`
    - Assert the returned value equals the valid integer and that the function looped over all invalid inputs
    - **Validates: Requirements 6.1, 6.2, 6.3**

- [x] 6. Implement `play_round`
  - [x] 6.1 Implement `play_round(lower: int, upper: int, attempt_limit: int) -> bool`
    - Call `generate_secret_number(lower, upper)` at the start
    - Loop up to `attempt_limit` times: call `get_valid_guess`, then `evaluate_guess`, print the feedback string
    - On a correct guess call `display_win(attempts_used)` and return `True`
    - On exhaustion call `display_game_over(secret)` and return `False`
    - _Requirements: 1.1, 1.3, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 4.1, 5.1, 5.2_

  - [ ]* 6.2 Write unit tests for `play_round`
    - Test win on first guess (mock `input` returns secret immediately)
    - Test loss after 7 failed guesses
    - Test mix of invalid then valid inputs within a round
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 6.1, 6.2, 6.3_

- [x] 7. Checkpoint — Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. Implement `ask_play_again` (bonus mode)
  - [x] 8.1 Implement `ask_play_again() -> bool`
    - Prompt the player with a yes/no question
    - Accept `"y"` / `"yes"` (case-insensitive) → return `True`; `"n"` / `"no"` → return `False`
    - Re-prompt on any other input
    - _Requirements: 8.1, 8.3, 8.4_

  - [ ]* 8.2 Write property test for `ask_play_again` (Property 8)
    - **Property 8: ask_play_again re-prompts on unrecognised input**
    - Use `st.lists(st.text())` of non-y/n strings followed by one valid response; patch `input()`
    - Assert the function re-prompts for each unrecognised input and returns only after the valid response
    - **Validates: Requirements 8.4**

  - [ ]* 8.3 Write unit tests for `ask_play_again`
    - Test returns `True` for `"y"` and `"yes"` (case-insensitive)
    - Test returns `False` for `"n"` and `"no"`
    - Test re-prompts on unrecognised input before accepting a valid response
    - _Requirements: 8.1, 8.3, 8.4_

- [x] 9. Implement `main` and wire everything together
  - [x] 9.1 Implement `main() -> None`
    - Detect bonus mode via `--bonus` CLI flag (`sys.argv`)
    - **Base mode**: call `play_round(1, 100, 7)` once then exit
    - **Bonus mode**: start with `lower=1, upper=100`; display the current range before each round (satisfies Req 7.2); after each round increment `upper` by 50 and call `ask_play_again()`; exit cleanly when player declines
    - Add `if __name__ == "__main__": main()` guard
    - _Requirements: 1.2, 2.1, 7.1, 7.2, 8.1, 8.2, 8.3_

  - [ ]* 9.2 Write property test for bonus range expansion (Property 6)
    - **Property 6: Range expands by exactly 50 each bonus round**
    - Use `st.integers(min_value=2, max_value=20)` for round count; mock `play_round` and `ask_play_again` to control flow
    - Assert upper bound in round `k` equals `100 + (k - 1) * 50`
    - **Validates: Requirements 7.1**

  - [ ]* 9.3 Write property test for bonus round range display (Property 7)
    - **Property 7: Bonus round displays current range**
    - Use `st.integers()` pairs where `lower <= upper`; capture stdout
    - Assert both `lower` and `upper` decimal representations appear in the output before the round starts
    - **Validates: Requirements 7.2**

  - [ ]* 9.4 Write unit tests for `main`
    - Test bonus mode increments upper bound between rounds
    - Test bonus mode exits cleanly when player declines to play again
    - _Requirements: 7.1, 7.2, 8.2, 8.3_

- [x] 10. Final checkpoint — Ensure all tests pass
  - Run `python -m pytest test_game.py` and confirm all tests pass.
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for a faster MVP
- Each task references specific requirements for traceability
- Property tests use Hypothesis with `@settings(max_examples=100)`
- All tests live in `test_game.py`; run with `python -m pytest test_game.py`
- Checkpoints ensure incremental validation at natural boundaries
