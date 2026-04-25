"""
Tests for the Number Guessing Game.

Includes property-based tests (Hypothesis) and example-based unit tests (pytest).
Run with:
    python -m pytest test_game.py
"""

import pytest
from unittest.mock import patch
from hypothesis import given, settings, strategies as st

from game import ask_play_again


# ---------------------------------------------------------------------------
# Smoke test — verifies the test framework is wired up correctly
# ---------------------------------------------------------------------------

def test_smoke():
    """Placeholder smoke test to confirm pytest and hypothesis are available."""
    assert True


# ---------------------------------------------------------------------------
# Example-based unit tests for ask_play_again
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("response", ["y", "Y", "yes", "YES", "Yes"])
def test_ask_play_again_returns_true_for_yes(response):
    """ask_play_again returns True for 'y' and 'yes' (case-insensitive)."""
    with patch("builtins.input", return_value=response):
        assert ask_play_again() is True


@pytest.mark.parametrize("response", ["n", "N", "no", "NO", "No"])
def test_ask_play_again_returns_false_for_no(response):
    """ask_play_again returns False for 'n' and 'no' (case-insensitive)."""
    with patch("builtins.input", return_value=response):
        assert ask_play_again() is False


def test_ask_play_again_reprompts_then_accepts_yes():
    """ask_play_again re-prompts on unrecognised input before accepting 'y'."""
    responses = iter(["maybe", "sure", "y"])
    with patch("builtins.input", side_effect=responses), \
         patch("builtins.print") as mock_print:
        result = ask_play_again()
    assert result is True
    # Should have printed an error for each unrecognised input
    assert mock_print.call_count == 2


def test_ask_play_again_reprompts_then_accepts_no():
    """ask_play_again re-prompts on unrecognised input before accepting 'n'."""
    responses = iter(["what", "n"])
    with patch("builtins.input", side_effect=responses), \
         patch("builtins.print") as mock_print:
        result = ask_play_again()
    assert result is False
    assert mock_print.call_count == 1


# ---------------------------------------------------------------------------
# Property-based test for ask_play_again (Property 8)
# Feature: number-guessing-game, Property 8: ask_play_again re-prompts on unrecognised input
# ---------------------------------------------------------------------------

# Strategy: generate strings that are NOT valid yes/no responses
_invalid_response = st.text(min_size=1).filter(
    lambda s: s.strip().lower() not in ("y", "yes", "n", "no")
)


@given(
    invalid_inputs=st.lists(_invalid_response, min_size=1, max_size=10),
    final_response=st.sampled_from(["y", "yes", "n", "no"]),
)
@settings(max_examples=100)
def test_ask_play_again_reprompts(invalid_inputs, final_response):
    """
    For any non-empty sequence of unrecognised strings followed by a valid
    response, ask_play_again SHALL re-prompt for each unrecognised input and
    only return after receiving the valid response.

    Validates: Requirements 8.4
    """
    # Feature: number-guessing-game, Property 8: ask_play_again re-prompts on unrecognised input
    all_inputs = invalid_inputs + [final_response]
    call_count = 0

    def mock_input(prompt):
        nonlocal call_count
        call_count += 1
        return all_inputs[call_count - 1]

    with patch("builtins.input", side_effect=mock_input), \
         patch("builtins.print"):
        result = ask_play_again()

    # Should have consumed all inputs (re-prompted for each invalid one)
    assert call_count == len(all_inputs)

    expected = final_response.strip().lower() in ("y", "yes")
    assert result is expected


# ---------------------------------------------------------------------------
# Example-based unit tests for main()
# ---------------------------------------------------------------------------

from game import main


def test_main_base_mode_calls_play_round_once(monkeypatch):
    """main() in base mode calls play_round exactly once with (1, 100, 7)."""
    calls = []

    def fake_play_round(lower, upper, attempt_limit):
        calls.append((lower, upper, attempt_limit))
        return True

    monkeypatch.setattr("game.play_round", fake_play_round)
    monkeypatch.setattr("sys.argv", ["game.py"])

    main()

    assert calls == [(1, 100, 7)]


def test_main_bonus_mode_increments_upper(monkeypatch):
    """main() in bonus mode increments upper by 50 each round."""
    play_calls = []
    # Player plays 3 rounds then declines
    play_again_responses = iter([True, True, False])

    def fake_play_round(lower, upper, attempt_limit):
        play_calls.append((lower, upper, attempt_limit))
        return True

    def fake_ask_play_again():
        return next(play_again_responses)

    monkeypatch.setattr("game.play_round", fake_play_round)
    monkeypatch.setattr("game.ask_play_again", fake_ask_play_again)
    monkeypatch.setattr("sys.argv", ["game.py", "--bonus"])

    with patch("builtins.print"):
        main()

    assert play_calls == [
        (1, 100, 7),
        (1, 150, 7),
        (1, 200, 7),
    ]


def test_main_bonus_mode_exits_on_decline(monkeypatch):
    """main() in bonus mode exits cleanly when player declines to play again."""
    play_calls = []

    def fake_play_round(lower, upper, attempt_limit):
        play_calls.append((lower, upper, attempt_limit))
        return False

    def fake_ask_play_again():
        return False

    monkeypatch.setattr("game.play_round", fake_play_round)
    monkeypatch.setattr("game.ask_play_again", fake_ask_play_again)
    monkeypatch.setattr("sys.argv", ["game.py", "--bonus"])

    with patch("builtins.print"):
        main()

    # Only one round played before declining
    assert len(play_calls) == 1


def test_main_bonus_mode_displays_range(monkeypatch):
    """main() in bonus mode prints the current range before each round (Req 7.2)."""
    play_again_responses = iter([True, False])

    def fake_play_round(lower, upper, attempt_limit):
        return True

    def fake_ask_play_again():
        return next(play_again_responses)

    monkeypatch.setattr("game.play_round", fake_play_round)
    monkeypatch.setattr("game.ask_play_again", fake_ask_play_again)
    monkeypatch.setattr("sys.argv", ["game.py", "--bonus"])

    printed = []
    with patch("builtins.print", side_effect=lambda *args, **kwargs: printed.append(" ".join(str(a) for a in args))):
        main()

    range_messages = [m for m in printed if "range" in m.lower() or "[" in m]
    assert len(range_messages) == 2
    assert "1" in range_messages[0] and "100" in range_messages[0]
    assert "1" in range_messages[1] and "150" in range_messages[1]
