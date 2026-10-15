# Sustainable study pacing

The goal is independent reasoning, not finishing pages quickly. Plan **about 13–16 weeks** at two lessons per week, with extra time for unfamiliar prerequisites, DP, and graph reasoning. This is a planning estimate, not a mastery deadline. If Python functions, dictionaries, or classes are unfamiliar, learn those first with the [English Python Companion](https://github.com/nour662/english-python-companion).

## One lesson across three small sessions

1. **Understand, about 20 minutes:** read the idea, trace a new input by hand, and state the invariant without looking.
2. **Attempt, about 20 minutes:** implement the exercise, test a boundary, and use one hint if blocked. Save the next step when time expires.
3. **Review, about 15 minutes:** compare approaches, fix one misunderstanding, then rebuild the core reasoning from memory later.

These sessions may span multiple days. A course exercise can be that day’s coding practice; it does not need to be added on top of another problem. Keep the learner’s existing daily time limit. For a 60-minute learning day, one possible allocation is 5 minutes of recall, 20 minutes of course study, 25 minutes of implementation, and 10 minutes of explanation and notes. If other learning uses part of the hour, shorten this block rather than adding an evening catch-up session.

## Suggested sequence

| Week | Lessons | Observable milestone |
| --- | --- | --- |
| 1 | 01–02 | Compare linear counting with pair enumeration; handle empty and final-run boundaries |
| 2 | 03–04 | Explain map state and justify pointer movement on sorted input |
| 3 | 05–06 | Distinguish monotone windows from signed prefix-sum queries |
| 4 | 07–08 | Use stack and queue invariants; explain the BFS shortest-path assumption |
| 5 | 09–10 | Preserve links while reversing and defend binary-search boundaries |
| 6 | 11–12 | Define recursive returns and combine child facts correctly |
| 7 | 13–14 | Separate tree levels and validate inherited BST constraints |
| 8 | 15–16 | Traverse disconnected graphs and identify dependency cycles |
| 9 | 17–18 | Maintain a heap boundary and explain a greedy exchange argument |
| 10 | 19–20 | Separate enumeration from optimization; derive a DP state |
| 11 | 21–22 | Explain memory-reused DP and a prefix-index count invariant |
| 12 | 23–24 | Distinguish connectivity maintenance from weighted route search |
| 13 | 25–26 | State integer-model assumptions and complete one mock interview |
| 14–16, if useful | Review weak topics | Re-solve unfamiliar variants and improve explanations |

## Retention without overload

- Try retrieval on the next study day, about a week later, and later when the idea feels less fresh. Adjust intervals to difficulty.
- Import the optional `anki/cards.csv` for 52 original recall prompts. Select comma-separated fields, map Front/Back/Tags, and skip the header row if your importer does not do it automatically. Keep new-card intake small; cards supplement coding rather than replace it.
- Keep a private note with date, lesson, confidence 0–3, one mistake, and the next step. Do not put personal logs in a public pull request.
- On a difficult day, spend five minutes explaining one idea and stop. No backlog of missed study minutes.
- During a weekly review, continue only one or two weak ideas rather than restarting the whole course.

Move on when you can explain the main invariant and attempt the exercise independently. Revisit if the reasoning still depends on remembering exact lines. Passing reference tests or reading a solution does not establish that you can solve a fresh interview problem.
