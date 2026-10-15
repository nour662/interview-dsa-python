# 04. Two pointers and monotone movement

[Previous lesson](03-hash-maps-remember-what-a-scan-cannot.md) · [Next lesson](05-sliding-windows-and-reversible-state.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Two pointers work when moving a boundary eliminates candidates safely. Sorted input provides an ordering argument. If the sum of the two endpoints is below the target, pairing the left endpoint with any smaller right endpoint cannot improve that below-target sum. After evaluating the current pair, move the left endpoint. Symmetrically, an excessive sum allows moving the right endpoint. Track the best pair before discarding a boundary.

## Walk through an example

With [1, 4, 6, 10] and target 12: (1, 10) gives 11, then (4, 10) gives 14, then (4, 6) gives 10. The best difference is 1, so return (1, 10). An exact match can stop immediately.

## Your exercise

Implement closest_pair(sorted_values, target). Return values at two distinct positions whose sum is closest to target. The input is sorted in nondecreasing order. Any optimal tie is valid; fewer than two values returns None.

Start in [the exercise file](../exercises/04-two-pointers-and-monotone-movement.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Start at both ends. Record the closest pair seen before advancing one pointer.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def closest_pair(sorted_values, target):
    if len(sorted_values) < 2:
        return None
    left, right = 0, len(sorted_values) - 1
    best = (sorted_values[left], sorted_values[right])
    while left < right:
        total = sorted_values[left] + sorted_values[right]
        if abs(total - target) < abs(sum(best) - target):
            best = (sorted_values[left], sorted_values[right])
        if total == target:
            break
        if total < target:
            left += 1
        else:
            right -= 1
    return best
```

### Why it works

When the sum is below target, all other pairs using the left endpoint and a smaller right endpoint are no closer than the current pair. The symmetric statement holds above target. Each discarded boundary therefore cannot hide a better unexplored pair.

### Time and space

O(n) time and O(1) auxiliary space. Sorting arbitrary input first would add O(n log n) time and may change the mutation contract.

</details>

## A mistake to watch for

Using left <= right permits reusing one position. Negative values are allowed, but unsorted input breaks the elimination proof.

## Retrieval check

Close the solution and answer: **Why is this approach unsafe for unsorted input?**

<details><summary>Check your answer</summary>

Moving right or left no longer predicts how the sum changes, so it can discard the optimal pair.

</details>

## Optional extension

Return indices instead of values and define a deterministic tie-breaking rule.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
