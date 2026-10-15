# 05. Sliding windows and reversible state

[Previous lesson](04-two-pointers-and-monotone-movement.md) · [Next lesson](06-prefix-sums-for-signed-ranges.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A sliding window represents a contiguous segment. Add the new right item, then remove left items until the segment satisfies a rule. This needs a property that lets boundary movement repair validity. With nonnegative costs, extending cannot decrease a sum and removing cannot increase it. Although a while loop sits inside a for loop, each element enters and leaves at most once.

## Walk through an example

For costs [2, 1, 3, 1] and budget 4, window [2, 1] has length 2. Adding 3 forces removal of 2 and leaves [1, 3]. Adding 1 removes the earlier 1 and leaves [3, 1]. The longest valid length is 2.

## Your exercise

Implement longest_budget_window(costs, budget). Return the longest contiguous segment length with sum at most budget. Costs and budget are nonnegative numbers; reject negative values with ValueError. Empty input returns 0.

Start in [the exercise file](../exercises/05-sliding-windows-and-reversible-state.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Maintain left, total, and best. Update best only after restoring validity.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def longest_budget_window(costs, budget):
    """Nonnegative costs and budget. Return length, not slice."""
    if budget < 0 or any(cost < 0 for cost in costs):
        raise ValueError('costs and budget must be nonnegative')
    left = total = best = 0
    for right, cost in enumerate(costs):
        total += cost
        while total > budget:
            total -= costs[left]
            left += 1
        best = max(best, right - left + 1)
    return best
```

### Why it works

After shrinking, the window is valid. Every removed left endpoint made a sum too large and cannot become useful by extending the right edge with more nonnegative costs. Across the scan, both pointers move only forward.

### Time and space

O(n) time including validation and O(1) auxiliary space.

</details>

## A mistake to watch for

Negative costs destroy the monotonicity argument. For signed values, do not reuse this template without a new proof. Zero-cost entries must still contribute to window length.

## Retrieval check

Close the solution and answer: **Why does the inner loop not imply O(n²) here?**

<details><summary>Check your answer</summary>

The left pointer advances at most n times across all outer iterations, not n times per iteration.

</details>

## Optional extension

Return the half-open indices [start, end) of a longest valid window.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
