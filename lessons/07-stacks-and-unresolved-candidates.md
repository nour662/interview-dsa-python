# 07. Stacks and unresolved candidates

[Previous lesson](06-prefix-sums-for-signed-ranges.md) · [Next lesson](08-queues-and-shortest-routes-without-weights.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A stack removes the most recently added item first. It can represent unfinished parsing, nested work, or candidates awaiting a future event. A monotonic stack keeps candidates in a useful order and removes those settled by the current item. Store indices when distance matters. Equal values need careful handling because strictly greater and greater-or-equal are different conditions.

## Walk through an example

For [20, 18, 21], day 0 waits on the stack, then day 1 joins it. Day 2 is warmer than both: pop day 1 and record 1, then pop day 0 and record 2. Day 2 never sees a warmer future day, so its answer remains 0.

## Your exercise

Implement next_warmer_wait(temperatures). For each day return the number of days until a strictly warmer temperature. Use 0 when no such future day exists.

Start in [the exercise file](../exercises/07-stacks-and-unresolved-candidates.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Keep unresolved day indices. The current day resolves every smaller temperature at the stack top.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def next_warmer_wait(temperatures):
    waits = [0] * len(temperatures)
    pending = []
    for day, temperature in enumerate(temperatures):
        while pending and temperatures[pending[-1]] < temperature:
            earlier = pending.pop()
            waits[earlier] = day - earlier
        pending.append(day)
    return waits
```

### Why it works

The stack temperatures are nonincreasing. Popping a prior day at the first warmer incoming day gives its nearest qualifying future day: any earlier warmer day would already have popped it. Every index is pushed once and popped at most once.

### Time and space

O(n) time and O(n) auxiliary space, plus the O(n) answer.

</details>

## A mistake to watch for

Use < rather than <= when resolving candidates. Equal temperatures do not satisfy strictly warmer. A stack of values alone loses the original day indices.

## Retrieval check

Close the solution and answer: **What is the answer for [5, 5, 6]?**

<details><summary>Check your answer</summary>

[2, 1, 0]. The second 5 does not resolve the first.

</details>

## Optional extension

Find the next strictly smaller value instead. State the new stack invariant.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
