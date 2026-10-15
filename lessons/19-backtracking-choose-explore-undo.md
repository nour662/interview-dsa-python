# 19. Backtracking: choose, explore, undo

[Previous lesson](18-greedy-choices-need-an-exchange-argument.md) · [Next lesson](20-dynamic-programming-on-one-dimension.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Backtracking explores a tree of partial decisions. A path holds the current candidate; a recursive call explores its extensions; undo restores the exact prior state. Generate combinations in increasing input-index order so the same selection is not produced in multiple orders. Pruning skips branches that cannot fill the remaining slots.

## Walk through an example

From [a, b, c] choose 2. Start with a, extend with b and then c, producing [a,b] and [a,c]. Undo a, start b, extend c, producing [b,c]. Never start the second choice before the first choice’s index.

## Your exercise

Implement choose_tags(tags, k). Input tags are distinct. Return all size-k selections as lists, preserving input order inside each selection. Any output order is valid. k = 0 returns [[]]; k outside 0..n returns [].

Start in [the exercise file](../exercises/19-backtracking-choose-explore-undo.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Pass the next allowed start index. Append path.copy() at a complete selection, not the mutable path itself.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def choose_tags(tags, k):
    """Unique input tags; retain input order within each size-k selection."""
    if not 0 <= k <= len(tags):
        return []
    answer, path = [], []
    def search(start):
        if len(path) == k:
            answer.append(path.copy())
            return
        needed = k - len(path)
        for index in range(start, len(tags) - needed + 1):
            path.append(tags[index])
            search(index + 1)
            path.pop()
    search(0)
    return answer
```

### Why it works

Each selection has one unique increasing index sequence. The recursion follows exactly those sequences and cannot repeat them. Pruning only skips a suffix with fewer available items than remaining slots.

### Time and space

For valid k, O((k + 1) × C(n,k)) time and output space; O(k) recursion/path space excluding output. Enumeration cannot be polynomial for all k because output itself can be exponential.

</details>

## A mistake to watch for

Appending path without copying makes saved results change during undo. Forgetting to pop contaminates sibling branches.

## Retrieval check

Close the solution and answer: **Why does k = 0 have one selection rather than zero?**

<details><summary>Check your answer</summary>

There is exactly one way to select nothing: the empty selection.

</details>

## Optional extension

Support repeated input tags while returning unique selections; explain where duplicate branches are skipped.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
