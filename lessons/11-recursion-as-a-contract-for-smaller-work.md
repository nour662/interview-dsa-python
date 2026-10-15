# 11. Recursion as a contract for smaller work

[Previous lesson](10-binary-search-with-explicit-boundaries.md) · [Next lesson](12-tree-dfs-return-one-fact-update-another.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A recursive function promises to solve the same kind of problem on a smaller input. Identify the returned meaning, a base case, and a measure that decreases. The call stack stores unfinished work. Recursion is not automatically exponential: repeated subproblems and branching determine total work. Deep Python recursion can exceed the interpreter limit even when asymptotic work is linear.

## Walk through an example

For [2, [3, [], [4]], 1], the inner [4] returns 4, then [3, [], [4]] returns 7. The outer call adds 2 + 7 + 1 and returns 10. An empty list contributes zero.

## Your exercise

Implement nested_total(items). Input is a finite, acyclic nesting of Python lists and integers. Return the sum of every integer. Do not mutate input. Empty lists can appear at any depth.

Start in [the exercise file](../exercises/11-recursion-as-a-contract-for-smaller-work.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

For each item, either add its integer value or ask the same function to sum the nested list.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def nested_total(items):
    """Finite, acyclic nested lists containing integers only."""
    total = 0
    for item in items:
        total += nested_total(item) if isinstance(item, list) else item
    return total
```

### Why it works

For an empty list the result is zero. Assuming recursive calls correctly total each smaller nested list, adding those totals and the direct integers counts every integer exactly once.

### Time and space

O(m) time for m visited list entries and O(h) call-stack space for nesting depth h. A very deep input may raise RecursionError.

</details>

## A mistake to watch for

Summing only the outer integers misses nested values. Cycles are outside the contract; do not claim this handles a list that contains itself.

## Retrieval check

Close the solution and answer: **Does two recursive calls always imply exponential time?**

<details><summary>Check your answer</summary>

No. If they visit disjoint portions of a tree, total work can still be linear in the total nodes.

</details>

## Optional extension

Implement an explicit stack version that handles deeply nested acyclic input.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
