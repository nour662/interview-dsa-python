# 18. Greedy choices need an exchange argument

[Previous lesson](17-heaps-and-keeping-only-the-best-candidates.md) · [Next lesson](19-backtracking-choose-explore-undo.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Greedy algorithms commit to a locally favorable choice without revisiting it. This requires proof, not intuition. For maximizing the count of nonoverlapping meetings with equal value, choosing the earliest finishing available meeting leaves at least as much room as any alternative first choice. That argument fails when meetings carry different rewards.

## Walk through an example

For meetings (0,4), (1,2), (2,3), (3,5), sort by finish and choose (1,2), then (2,3), then (3,5). Choosing the earliest starting meeting (0,4) would leave room for fewer meetings.

## Your exercise

Implement max_meetings(intervals). Return a maximum-size compatible subset of positive-duration half-open intervals [start, end). Touching endpoints do not overlap. Equal-value meetings, arbitrary input order, and negative times are allowed. Invalid duration raises ValueError.

Start in [the exercise file](../exercises/18-greedy-choices-need-an-exchange-argument.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Sort by end time and accept a meeting when its start is at least the last accepted end.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def max_meetings(intervals):
    """Half-open [start, end); all intervals must have start < end."""
    if any(start >= end for start, end in intervals):
        raise ValueError('each meeting needs positive duration')
    selected, last_end = [], None
    for start, end in sorted(intervals, key=lambda interval: interval[1]):
        if last_end is None or start >= last_end:
            selected.append((start, end))
            last_end = end
    return selected
```

### Why it works

Take an optimal solution’s first meeting. Replace it with the earliest finishing meeting; the replacement cannot overlap any later meeting that the original first meeting allowed. Repeat this exchange on the remaining compatible suffix.

### Time and space

O(n log n) time and O(n) additional space for sorting and output. Input is not mutated.

</details>

## A mistake to watch for

Sorting by start time or shortest duration lacks this guarantee. If meetings have different values, maximizing their count is a different objective from maximizing reward.

## Retrieval check

Close the solution and answer: **Are (1, 3) and (3, 4) compatible here?**

<details><summary>Check your answer</summary>

Yes. Half-open intervals do not include their ending point.

</details>

## Optional extension

Give a counterexample to the rule “always take the shortest available meeting.”

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
