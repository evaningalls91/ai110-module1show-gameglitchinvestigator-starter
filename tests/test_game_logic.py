from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


# =====================================================================
# Bug 1: check_guess hint direction was backwards
#   "Too High" used to say "Go HIGHER!" and "Too Low" said "Go LOWER!"
# =====================================================================

def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high_outcome():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low_outcome():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


def test_too_high_hint_says_go_lower():
    # Guess is above the secret -> player must aim LOWER next time
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message.upper()
    assert "HIGHER" not in message.upper()


def test_too_low_hint_says_go_higher():
    # Guess is below the secret -> player must aim HIGHER next time
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()
    assert "LOWER" not in message.upper()


# =====================================================================
# Bug 2: get_range_for_difficulty made Hard EASIER than Normal
#   Hard used to return (1, 50), narrower than Normal's (1, 100).
# =====================================================================

def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 50)


def test_hard_range_is_wider_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high


def test_unknown_difficulty_falls_back_to_normal():
    assert get_range_for_difficulty("???") == get_range_for_difficulty("Normal")


# =====================================================================
# Bug 3: parse_guess crashed / mishandled whitespace-only input
#   "   " should be treated as empty, not parsed as a number.
# =====================================================================

def test_parse_valid_integer():
    assert parse_guess("42") == (True, 42, None)


def test_parse_decimal_rejected():
    # Only whole numbers are valid; a decimal is not a positive integer.
    ok, value, err = parse_guess("3.9")
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None


def test_parse_whitespace_only():
    ok, value, err = parse_guess("   ")
    assert ok is False
    assert value is None


def test_parse_none():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None


def test_parse_non_number():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None


def test_parse_strips_surrounding_whitespace():
    assert parse_guess("  7 ") == (True, 7, None)


# =====================================================================
# Edge cases: only positive integers within the range are valid.
#   parse_guess now takes an optional (low, high) range and rejects
#   zero, negatives, and out-of-range values with a clear message.
# =====================================================================

def test_parse_zero_rejected():
    ok, value, err = parse_guess("0")
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_negative_rejected():
    ok, value, err = parse_guess("-5")
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_within_range_is_valid():
    assert parse_guess("10", 1, 20) == (True, 10, None)


def test_parse_at_range_boundaries_is_valid():
    assert parse_guess("1", 1, 20) == (True, 1, None)
    assert parse_guess("20", 1, 20) == (True, 20, None)


def test_parse_above_range_rejected():
    ok, value, err = parse_guess("21", 1, 20)
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_below_range_rejected():
    ok, value, err = parse_guess("0", 1, 20)
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_without_range_skips_range_check():
    # With no range supplied, any positive whole number is accepted.
    assert parse_guess("999") == (True, 999, None)


# =====================================================================
# Bug 4: update_score rewarded wrong "Too High" guesses and
#        double-penalized the win bonus.
# =====================================================================

def test_wrong_too_high_always_loses_points():
    # Previously +5 on even attempts; should always be a penalty now.
    assert update_score(100, "Too High", 2) == 95
    assert update_score(100, "Too High", 3) == 95


def test_wrong_too_low_loses_points():
    assert update_score(100, "Too Low", 2) == 95


def test_win_on_first_attempt_scores_full_points():
    # attempt_number == 1 should give the full 100 (no +1 double penalty).
    assert update_score(0, "Win", 1) == 100


def test_win_score_decreases_with_more_attempts():
    assert update_score(0, "Win", 2) == 90
    assert update_score(0, "Win", 3) == 80


def test_win_score_never_below_floor():
    # Even a very late win is worth at least 10 points.
    assert update_score(0, "Win", 50) == 10


def test_unknown_outcome_leaves_score_unchanged():
    assert update_score(42, "???", 1) == 42


# =====================================================================
# Note: the remaining fixes (New Game state reset, attempts counter
# init, "between {low} and {high}" banner, removing the secret->str
# glitch, only counting valid guesses) live in app.py and depend on
# Streamlit session_state, so they are verified manually in the app
# rather than in these pure-function unit tests.
# =====================================================================
