# 21. Grid DP and careful memory reuse

[Previous lesson](20-dynamic-programming-on-one-dimension.md) · [Next lesson](22-tries-organize-information-by-shared-prefixes.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Two-dimensional DP often represents progress along two coordinates. For right/down grid movement, each cell can be reached only from above or from the left. A full table makes this clear. A one-row optimization reuses memory: before updating column c, dp[c] means “from above,” while dp[c − 1] already means “from the left in this row.” Update direction therefore carries meaning.

## Walk through an example

For [[2, 9, 1], [1, 3, 2]], the first row’s totals are [2, 11, 12]. The next row becomes [3, 6, 8]. The cheapest path costs 8, including both start and destination.

## Your exercise

Implement minimum_grid_cost(grid). Grid is a nonempty rectangular matrix of integers, which may be negative. Start top-left and move only right or down to bottom-right. Include every visited cell’s cost. Empty or ragged input raises ValueError.

Start in [the exercise file](../exercises/21-grid-dp-and-careful-memory-reuse.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Initialize dp[0] = 0 and other entries to infinity. At each cell add its cost to min(above, left).

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def minimum_grid_cost(grid):
    """Nonempty rectangular integer grid; move right/down, include endpoints."""
    if not grid or not grid[0] or any(len(row) != len(grid[0]) for row in grid):
        raise ValueError('grid must be nonempty and rectangular')
    cols = len(grid[0])
    dp = [float('inf')] * cols
    dp[0] = 0
    for row in grid:
        for col, cost in enumerate(row):
            dp[col] = cost + min(dp[col], dp[col - 1] if col else float('inf'))
    return dp[-1]
```

### Why it works

Every route into a cell has a final move from above or left. Minimizing over those optimal prefixes gives the best route to that cell. Row-major order solves both dependencies before their values are needed.

### Time and space

O(rows × columns) time and O(columns) auxiliary space.

</details>

## A mistake to watch for

Negative cells are safe here because the movement graph has no cycles. A negative-weight general graph would require different reasoning. One-row costs alone do not retain a reconstructable path.

## Retrieval check

Close the solution and answer: **Why can updating columns right-to-left break this implementation?**

<details><summary>Check your answer</summary>

The left neighbor would still contain the previous row’s value rather than the current row’s solved cost.

</details>

## Optional extension

Build the full table and a predecessor table to return both minimum cost and a path.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
