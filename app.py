import math
import random
import streamlit as st

# Fix: "Refactored the game logic out of app.py into logic_utils.py so it can be unit-tested"
from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

low, high = get_range_for_difficulty(difficulty)

# Fix: "Attempt limits were hardcoded (Hard was unwinnable); derive them from the range"
# A perfect binary-search player needs ceil(log2(N)) guesses to corner any
# number in a range of N values. We add a buffer so reasonable (imperfect)
# play can still win.
GUESS_BUFFER = 2
optimal_guesses = math.ceil(math.log2(high - low + 1))
attempt_limit = optimal_guesses + GUESS_BUFFER

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")


# Fix: "New Game left score/status/history stale and drew the secret from 1-100; reset the whole round here"
def start_new_game():
    """Reset per-round state for a fresh round using the current difficulty.
    The per-game score resets; the cumulative total_score carries over."""
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.game_score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_hint = None


if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

# Fix: "attempts started at 1, making 'attempts left' off by one"
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

# Fix: "Track the per-game score and the cumulative all-games total separately"
if "game_score" not in st.session_state:
    st.session_state.game_score = 0

if "total_score" not in st.session_state:
    st.session_state.total_score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

if "last_hint" not in st.session_state:
    st.session_state.last_hint = None

# Fix: "Changing difficulty did nothing mid-game; now it starts a fresh game with the new range"
if st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    start_new_game()

st.subheader("Make a guess")

# Fix: "Banner/debug showed stale state and the debug expander collapsed on every guess; render them in fixed slots filled after the state updates"
# Reserve fixed slots up front so the banner and debug panel always render at
# the same position in the layout. Because that position is stable across
# reruns, the expander keeps its open/closed state instead of collapsing — we
# just refill the slots with fresh values once the guess has been processed.
status_slot = st.container()
debug_slot = st.container()


def render_status_banner():
    """Show the range and remaining attempts, reflecting the latest state."""
    # Fix: "Clamp so 'Attempts left' can't display a negative number"
    attempts_left = max(0, attempt_limit - st.session_state.attempts)
    # Fix: "Banner hardcoded 'between 1 and 100'; use the actual difficulty range"
    st.info(
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempts_left}"
    )


def render_score_summary():
    """Show this game's score and the cumulative total, side by side."""
    col_game, col_total = st.columns(2)
    col_game.metric("This game", st.session_state.game_score)
    col_total.metric("Total (all games)", st.session_state.total_score)


def render_debug_info():
    """Render current game state, reflecting the latest guess / new game."""
    with st.expander("Developer Debug Info"):
        st.write("Secret:", st.session_state.secret)
        st.write("Attempts:", st.session_state.attempts)
        st.write("Game score:", st.session_state.game_score)
        st.write("Total score:", st.session_state.total_score)
        st.write("Difficulty:", difficulty)
        st.write("History:", st.session_state.history)


raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# Fix: "Show hint now shows/hides the hint immediately on toggle, not only after the next guess"
# Reserve a fixed slot for the hint so toggling "Show hint" updates it in place,
# without waiting for the next guess.
hint_slot = st.container()

if new_game:
    start_new_game()
    st.success("New game started.")
    st.rerun()

# Fix: "Ignore Submit once the game is over (was still processing guesses after win/loss)"
if st.session_state.status == "playing" and submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.error(err)
    else:
        # Fix: "Count an attempt only for a valid guess, so invalid input no longer burns one"
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # Fix: "Removed the secret->str glitch that corrupted comparisons on even attempts"
        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        # Fix: "Persist the hint so the Show hint checkbox can re-show/hide it on demand"
        st.session_state.last_hint = message

        st.session_state.game_score = update_score(
            current_score=st.session_state.game_score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        # Fix: "Add the finished game's score to the cumulative total exactly once"
        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.session_state.total_score += st.session_state.game_score
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.session_state.total_score += st.session_state.game_score

# Fix: "On win/loss, show this game's score and the all-games total as separate values"
if st.session_state.status == "won":
    st.success(f"🎉 You won! The secret was {st.session_state.secret}.")
    render_score_summary()
    st.caption("Start a new game to play again.")
elif st.session_state.status == "lost":
    st.error(f"💥 Out of attempts! The secret was {st.session_state.secret}.")
    render_score_summary()
    st.caption("Start a new game to try again.")

# Fill the reserved slots last so they show post-guess state, in place.
with hint_slot:
    if show_hint and st.session_state.last_hint:
        st.warning(st.session_state.last_hint)
with status_slot:
    render_status_banner()
with debug_slot:
    render_debug_info()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
