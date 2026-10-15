# 10. Binary search with explicit boundaries

[Previous lesson](09-linked-lists-and-safe-pointer-changes.md) · [Next lesson](11-recursion-as-a-contract-for-smaller-work.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Binary search repeatedly discards half a sorted search space. The reliable version begins by stating what each boundary means. For a lower bound, positions before left are known to contain values smaller than target; positions at or after right are known to contain values at least target. Search the half-open interval [left, right). A length-n input has n + 1 insertion boundaries.

## Walk through an example

For [2, 4, 4, 9] and target 4, start [0, 4). Middle 2 qualifies, so right becomes 2. Middle 1 qualifies, so right becomes 1. Middle 0 is too small, so left becomes 1. Both meet at the first 4.

## Your exercise

Implement lower_bound(values, target). Return the first index whose value is at least target in sorted nondecreasing input. Return len(values) if no value qualifies; empty input returns 0.

Start in [the exercise file](../exercises/10-binary-search-with-explicit-boundaries.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Use right = len(values). A qualifying middle stays a possible answer, so set right = middle.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def lower_bound(values, target):
    left, right = 0, len(values)
    while left < right:
        middle = (left + right) // 2
        if values[middle] < target:
            left = middle + 1
        else:
            right = middle
    return left
```

### Why it works

Both updates preserve the boundary claims. Each update strictly shrinks the unresolved interval. When left equals right, every earlier element is too small and that boundary is the first possible qualifying index.

### Time and space

O(log n) time and O(1) auxiliary space for random-access input.

</details>

## A mistake to watch for

right = middle − 1 belongs to a different boundary convention. Mixing conventions causes missed answers or infinite loops. The returned index can equal n.

## Retrieval check

Close the solution and answer: **What does lower_bound([3, 3], 4) return?**

<details><summary>Check your answer</summary>

2, the insertion boundary after the last item.

</details>

## Optional extension

Search for the smallest feasible capacity in a monotone feasibility predicate instead of searching stored values.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
