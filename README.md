# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: _"How do I keep a variable from resetting in Streamlit when I click a button?"_
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
- [ ] Detail which bugs you found.
- [ ] Explain what fixes you applied.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User Selects a difficulty from left menu. This adjusts range and alotted guesses.
2. User guesses the number in the text box and hits submit guess.
3. User makes more guesses based upon hints feedback (optional).
4. Once guesses are exhausted or number is guessed the game is over.
5. User receives 10 points for a correct guess and negative points for each wrong guess.

**Screenshot** _(optional)_:

![Screenshot](Game%20Glitch%20Investigator%20Finished.png)

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
======================================================== test session starts ================================================
platform win32 -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Evan\Documents\Game Glitch Investigator
plugins: anyio-4.13.0
collected 22 items

ai110-module1show-gameglitchinvestigator-starter\tests\test_game_logic.py ......................
# ========================= 22 passed in 0.12s =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
