# 06. Prefix sums for signed ranges

[Previous lesson](05-sliding-windows-and-reversible-state.md) · [Next lesson](07-stacks-and-unresolved-candidates.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A prefix sum records the total before a position. The sum of values from i through j is prefix[j + 1] − prefix[i]. This turns a range question into a lookup for an earlier total. Unlike the previous window technique, this works with negative values. When counting all qualifying ranges, store how often each prefix occurred rather than only whether it occurred.

## Walk through an example

For [2, -2, 2] and target 2, prefix totals are 0, 2, 0, 2. The last prefix 2 finds two earlier zeros, contributing two ranges. Together with the first 2, the answer is 3.

## Your exercise

Implement count_target_ranges(values, target). Count nonempty contiguous ranges summing to target. Values may be negative or zero. Empty input returns 0.

Start in [the exercise file](../exercises/06-prefix-sums-for-signed-ranges.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Seed the frequency map with prefix zero appearing once. Query prefix − target before recording the new prefix.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def count_target_ranges(values, target):
    seen = Counter({0: 1})
    prefix = answer = 0
    for value in values:
        prefix += value
        answer += seen[prefix - target]
        seen[prefix] += 1
    return answer
```

### Why it works

Before processing each new prefix, seen contains exactly the prefixes at earlier boundaries. Each matching earlier prefix determines one nonempty range ending now. Querying first prevents a zero-length range when target is zero.

### Time and space

Expected O(n) time and O(n) auxiliary space.

</details>

## A mistake to watch for

A set undercounts repeated prefix totals. Forgetting the initial zero loses ranges starting at index 0. Recording before querying adds empty ranges for target 0.

## Retrieval check

Close the solution and answer: **How many target-zero ranges are in [0, 0]?**

<details><summary>Check your answer</summary>

Three: each individual zero and the full two-element range.

</details>

## Optional extension

Return the length of the longest matching range by storing the earliest index of each prefix.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
