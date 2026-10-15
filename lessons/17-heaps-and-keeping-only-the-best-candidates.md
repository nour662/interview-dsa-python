# 17. Heaps and keeping only the best candidates

[Previous lesson](16-directed-dependencies-and-topological-order.md) · [Next lesson](18-greedy-choices-need-an-exchange-argument.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A heap exposes the smallest item efficiently without sorting the entire collection. Python heapq implements a min-heap. To retain the k largest values, keep a heap of size at most k: when it grows, remove its smallest member. The root then marks the weakest surviving candidate, which is exactly the kth largest once enough items have arrived.

## Walk through an example

For [6, 2, 9, 4] and k = 2, retain {6}, then {2,6}. Adding 9 ejects 2; adding 4 ejects 4. The final retained values are 6 and 9, so the answer is 6.

## Your exercise

Implement kth_largest(values, k). Count duplicates as separate positions in descending order. Do not mutate the input. Reject k outside 1..len(values) with ValueError.

Start in [the exercise file](../exercises/17-heaps-and-keeping-only-the-best-candidates.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Push each value, and pop whenever the heap contains more than k values.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def kth_largest(values, k):
    if not 1 <= k <= len(values):
        raise ValueError('k must be between 1 and len(values)')
    heap = []
    for value in values:
        heappush(heap, value)
        if len(heap) > k:
            heappop(heap)
    return heap[0]
```

### Why it works

After each input, the heap contains the largest min(k, processed_count) values seen so far. A newly pushed value can only displace the smallest retained candidate. At completion the root is the kth largest.

### Time and space

O(n log(k + 1)) time and O(k) auxiliary space. For k = 1 this is linear; sorting instead costs O(n log n).

</details>

## A mistake to watch for

The heap’s list representation is not fully sorted. The maximum is not necessarily the last item. Duplicates matter unless the contract asks for distinct values.

## Retrieval check

Close the solution and answer: **For [5, 5, 2] with k = 2, what is the answer?**

<details><summary>Check your answer</summary>

5. The two 5s occupy the first and second positions.

</details>

## Optional extension

Adapt this into a streaming class that supports add(value) and reports the current kth largest after at least k observations.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
