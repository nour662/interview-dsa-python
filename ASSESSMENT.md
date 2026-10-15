# Interview practice and assessment

## A 40-minute mock

Use lesson 26 for your first rehearsal. For later mocks, choose an unfamiliar exercise or variant so recall alone cannot carry the session. Work without hints first, but say clearly when you need one.

| Minutes | Action | Evidence |
| --- | --- | --- |
| 0–5 | Clarify the contract | Restate output, ordering, duplicates, empty input, endpoints, and mutation rules |
| 5–10 | Establish a baseline | Give a correct simple approach and its cost |
| 10–17 | Derive an improvement | Name stored state, justify an invariant, and compare time/space |
| 17–30 | Implement | Use clear names; explain boundary updates while coding |
| 30–36 | Test | Trace a normal example, a smallest case, and an assumption-breaking case |
| 36–40 | Reflect | Explain correctness, complexity, limitations, and the first bug you would check |

These are practice allocations; an interviewer’s format may differ. If you are stuck, keep the correct baseline visible and name the unresolved step. Guessing a familiar template without checking its assumptions is not a substitute for reasoning.

## Score the evidence, not confidence

For each category score **0** if missing or incorrect, **1** if completed with a hint or an unresolved gap, and **2** if independently correct and explained.

| Category | A score of 2 means |
| --- | --- |
| Contract | You asked about the boundary that could change the algorithm |
| Baseline | You described a correct starting approach and its real cost |
| Algorithm | You justified why the chosen pattern fits the constraints |
| Implementation | Code matches the intended state and boundary rules |
| Validation | Tests include meaningful edge cases and match the stated contract |
| Explanation | You can give a correctness argument and accurate time/space bounds |

Use the 0–12 total to compare your own practice over time, not as a hiring prediction. Reattempt the weakest category in a later short session. A high score on a memorized exercise is weaker evidence than a solid explanation on an unfamiliar one.

## Milestone checks

**After lesson 06:** Contrast two pointers, windows, and prefix maps. Give one counterexample to using a nonnegative-cost window on signed values.

**After lesson 14:** Trace a recursive return separately from a global result; validate a BST with a violation below the immediate children.

**After lesson 20:** Explain why a directed cycle prevents scheduling, why a heap does not fully sort its contents, and why greedy token choice can fail.

**After lesson 26:** Solve an unfamiliar variant, explain your state before coding, and test a boundary without being prompted. If this still requires substantial hints, review a small number of topics rather than treating the course as failed.
