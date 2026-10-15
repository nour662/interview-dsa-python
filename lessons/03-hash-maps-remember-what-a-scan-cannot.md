# 03. Hash maps: remember what a scan cannot

[Previous lesson](02-arrays-strings-and-boundary-handling.md) · [Next lesson](04-two-pointers-and-monotone-movement.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A hash map associates keys with information. A set remembers presence; a map can remember counts, positions, or accumulated results. The stored value must answer the future question. If the question asks whether something occurs exactly once in the entire input, a first encounter cannot settle it: a duplicate might appear later. Separate global counting from ordered selection.

## Walk through an example

For [8, 3, 8, 5, 3], the count map is {8: 2, 3: 2, 5: 1}. A second scan in original order first finds count 1 at index 3. Map order is irrelevant because the input scan determines the answer.

## Your exercise

Implement earliest_unique(values). Return the earliest index whose value occurs exactly once, or -1 if none exists. Values are hashable. Preserve the input.

Start in [the exercise file](../exercises/03-hash-maps-remember-what-a-scan-cannot.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Use one pass to count and a second pass to select. Returning from the first pass is premature.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def earliest_unique(values):
    counts = Counter(values)
    return next((i for i, value in enumerate(values) if counts[value] == 1), -1)
```

### Why it works

After counting, each map entry is the exact frequency of its key. Scanning indices in increasing order means the first frequency-one item has no earlier qualifying item.

### Time and space

Expected O(n) time and O(u) auxiliary space. A count map may store up to n distinct keys.

</details>

## A mistake to watch for

Do not return the value when the contract asks for an index. Empty input and input containing only repeated values must return -1.

## Retrieval check

Close the solution and answer: **Can a set alone distinguish one occurrence from three?**

<details><summary>Check your answer</summary>

No. Both produce one membership entry. You need counts or another structure that records repeated membership.

</details>

## Optional extension

Return all unique-value indices while preserving input order. What extra space is output space?

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
