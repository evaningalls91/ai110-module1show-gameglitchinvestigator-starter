def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        # Fix: "Hard had a narrower range than Normal, making it easier; widen it"
        return 1, 100
    return 1, 50


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # Fix: "Treat None and whitespace-only input as empty so they don't crash/parse"
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        # Fix: "Strip surrounding whitespace so ' 7 ' parses correctly"
        text = raw.strip()
        if "." in text:
            value = int(float(text))
        else:
            value = int(text)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # Fix: "Hint direction was backwards (too-high told you to go higher); inverted"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number.

    A win earns more points the fewer attempts it took. A wrong guess
    costs a small, consistent penalty regardless of which attempt it was.
    """
    if outcome == "Win":
        # Fix: "Win bonus used attempt_number + 1, double-penalizing; use - 1 so a first-try win scores 100"
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    # Fix: "A wrong 'Too High' on even attempts used to ADD points; penalize all wrong guesses equally"
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
