# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  The game looked finished however there were many disfunctional elements. Buttons didn't work as intended, hints were wrong, games didn't restart, etc.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  1. Guesses were not logged until after subsequent guess
  2. Difficulty did not change the number of guesses or range correctly

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input            | Expected Behavior | Actual Behavior | Console Output / Error      |
| ---------------- | ----------------- | --------------- | --------------------------- |
| guessed 2        | "go higher"       | "go lower"      | hints lie                   |
| guessed 5        | score go up       | score = 10?     | score cannot be negative?   |
| clicked new game | score resets      | score increased | new game should reset score |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - Claude Code

- ## Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  1. When fixing the difficulty bug, the AI gave the user 20, 100, and 200 guesses for the respective difficulties. I then manually set the guesses number based on log2(range) + buffer.
  2. I asked the AI to update the developer debug info after guesses and it re rendere the section instead

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I created a pytest case and ran the streamlit app to verify

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  I tested that the input number was always an int instead of a string to prevent data mismatch.

- Did AI help you design or understand any tests? How?
  The AI designed the tests and ran them in bash after each edit.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  Streamlit re-runs your whole script top-to-bottom every time you touch a widget, so any value you need to remember between those re-runs has to live in st.session_state instead of an ordinary variable that gets wiped and recreated each time.

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

  I would like to use AI to explain code so that I can make small edits myself. I found that it was unproductive to use AI for this because it was so slow. However, fixing larger logical errors was fine.

- What is one thing you would do differently next time you work with AI on a coding task?

  I would like to give more context in my prompts and be more explicit on how elements should work. Most errors where caused when I did not give enough context and the AI made false assumptions.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

  AI can be an effective tool for debugging when the expected output is thoughroughly described. It is also pretty good at writing and running tests on the edits it makes.
