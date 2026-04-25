# Requirements Document

## Introduction

A Python command-line number guessing game that exercises loops, conditionals, and user input handling. The player attempts to guess a randomly generated integer within a limited number of attempts, receiving directional feedback after each guess. The game supports invalid input recovery, a congratulatory or game-over outcome, and an optional bonus mode with increasing difficulty and replay capability.

## Glossary

- **Game**: The overall number guessing program.
- **Round**: A single play session in which the player attempts to guess one Secret_Number.
- **Secret_Number**: The randomly generated integer the player is trying to guess.
- **Attempt**: A single valid guess submitted by the player.
- **Attempt_Limit**: The maximum number of Attempts allowed per Round (7 for the base game).
- **Attempts_Used**: The count of valid Attempts the player has submitted in the current Round.
- **Range**: The inclusive integer interval `[lower_bound, upper_bound]` from which the Secret_Number is drawn.
- **Input_Handler**: The component responsible for reading and validating player input.
- **Feedback_Display**: The component responsible for printing outcome messages to the player.

---

## Requirements

### Requirement 1: Generate a Secret Number

**User Story:** As a player, I want the game to pick a random number, so that each round is unpredictable.

#### Acceptance Criteria

1. WHEN a new Round begins, THE Game SHALL generate a Secret_Number as a uniformly random integer within the current Range (inclusive on both bounds).
2. WHEN the base game starts, THE Game SHALL set the Range to [1, 100].
3. WHEN a new Round begins, THE Game SHALL generate a new Secret_Number independently of any previous Round's Secret_Number.

---

### Requirement 2: Limit Attempts per Round

**User Story:** As a player, I want a maximum number of attempts, so that the game presents a meaningful challenge.

#### Acceptance Criteria

1. WHEN a Round begins, THE Game SHALL set the Attempt_Limit to 7.
2. THE Game SHALL track the Attempts_Used during the Round.
3. WHEN the player submits a valid Attempt, THE Game SHALL increment Attempts_Used by 1.
4. WHEN Attempts_Used equals the Attempt_Limit and the player has not guessed correctly, THE Game SHALL end the Round.

---

### Requirement 3: Provide Directional Feedback

**User Story:** As a player, I want to know whether my guess is too high, too low, or correct, so that I can narrow down the Secret_Number.

#### Acceptance Criteria

1. WHEN the player submits a valid Attempt and the guess is greater than the Secret_Number, THE Feedback_Display SHALL output "Too high".
2. WHEN the player submits a valid Attempt and the guess is less than the Secret_Number, THE Feedback_Display SHALL output "Too low".
3. WHEN the player submits a valid Attempt and the guess equals the Secret_Number, THE Feedback_Display SHALL output "Correct".

---

### Requirement 4: Display Win Message

**User Story:** As a player, I want a congratulatory message when I guess correctly, so that I feel rewarded for succeeding.

#### Acceptance Criteria

1. WHEN the player guesses the Secret_Number within the Attempt_Limit, THE Feedback_Display SHALL output a congratulatory message that includes the Attempts_Used count.

---

### Requirement 5: Display Game Over Message

**User Story:** As a player, I want to see the correct answer when I run out of attempts, so that I know what the number was.

#### Acceptance Criteria

1. WHEN the player exhausts all Attempts without guessing correctly, THE Feedback_Display SHALL reveal the Secret_Number value.
2. WHEN the player exhausts all Attempts without guessing correctly, THE Feedback_Display SHALL output "Game Over".

---

### Requirement 6: Handle Invalid Input

**User Story:** As a player, I want the game to recover gracefully when I enter non-numeric text, so that a typo does not cost me an Attempt.

#### Acceptance Criteria

1. WHEN the player enters input that cannot be parsed as an integer, THE Input_Handler SHALL display an error message and prompt the player to enter a valid integer.
2. WHEN the player enters invalid input, THE Game SHALL leave Attempts_Used unchanged.
3. WHILE the player has not provided a valid integer, THE Input_Handler SHALL continue prompting without advancing the Round state.

---

### Requirement 7 (Bonus): Increasing Difficulty Across Rounds

**User Story:** As a player, I want the guessing range to grow harder each round, so that repeated play remains challenging.

#### Acceptance Criteria

1. WHERE the bonus mode is active, WHEN a new Round begins after the first Round, THE Game SHALL increase the upper bound of the Range by 50.
2. WHERE the bonus mode is active, WHEN a Round begins, THE Feedback_Display SHALL display the current Range to the player.

---

### Requirement 8 (Bonus): Play Again Option

**User Story:** As a player, I want to choose whether to play another round after each game ends, so that I can keep playing without restarting the program.

#### Acceptance Criteria

1. WHERE the bonus mode is active, WHEN a Round ends (win or loss), THE Game SHALL ask the player whether they want to play again.
2. WHERE the bonus mode is active, WHEN the player confirms they want to play again, THE Game SHALL start a new Round with the updated Range.
3. WHERE the bonus mode is active, WHEN the player declines to play again, THE Game SHALL exit cleanly.
4. WHERE the bonus mode is active, WHEN the player enters an unrecognised response to the play-again prompt, THE Input_Handler SHALL re-prompt the player for a valid response.
