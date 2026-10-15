# 01. Reason about work before writing code

[Course home](../README.md) · [Next lesson](02-arrays-strings-and-boundary-handling.md) · [Full course](../README.md)

**Prerequisite:** Basic Python functions, loops, lists, and dictionaries.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

An algorithm is a sequence of decisions with a cost. Count how many times an operation can happen as the input grows. A loop nested inside another loop is not automatically quadratic: the question is whether their work multiplies. Big O describes growth rather than a stopwatch result. For Python dictionaries, use expected constant-time lookup under ordinary hashing assumptions; it is not a worst-case guarantee.

## Walk through an example

For values [4, 7, 4, 4], the three 4s form three pairs. Scanning left to right, their contributions are 0, 1, and 2. The 7 contributes 0. A frequency table replaces repeatedly scanning earlier items.

## Your exercise

Implement count_equal_pairs(values). Return the number of index pairs i < j whose values are equal. Values are hashable. Empty input returns 0; do not mutate the input.

Start in [the exercise file](../exercises/01-reason-about-work-before-writing-code.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Before recording the current value, ask how many matching values have already appeared.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def count_equal_pairs(values):
    counts = Counter()
    pairs = 0
    for value in values:
        pairs += counts[value]
        counts[value] += 1
    return pairs
```

### Why it works

Before each iteration, counts describes exactly the processed prefix and pairs counts every matching pair entirely inside it. Adding counts[value] introduces exactly the pairs ending at the new position. No pair is missed or counted twice.

### Time and space

Expected O(n) time and O(u) auxiliary space, where u is the number of distinct values. A direct comparison of all pairs costs O(n²) time and O(1) extra space.

</details>

## A mistake to watch for

Incrementing the frequency before adding its contribution counts each element as a pair with itself. Test [9] and [9, 9] to expose that error.

## Retrieval check

Close the solution and answer: **If every value is equal, what is the result for n elements?**

<details><summary>Check your answer</summary>

n(n − 1) / 2. The output grows quadratically even though the counting algorithm is expected linear time.

</details>

## Optional extension

Write the quadratic version and compare results for every length-5 list over values 0, 1, and 2.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
