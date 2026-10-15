# 08. Queues and shortest routes without weights

[Previous lesson](07-stacks-and-unresolved-candidates.md) · [Next lesson](09-linked-lists-and-safe-pointer-changes.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A queue processes the oldest waiting item first. Breadth-first search explores distance 0, then distance 1, and so on when every edge costs one step. Use deque.popleft rather than list.pop(0). Mark a state visited when enqueuing it so multiple neighbors cannot queue it repeatedly. The definition of a goal matters as much as the traversal.

## Walk through an example

In ["#####", "#...#", "##.##", "##.##"], start (1, 1) reaches (1, 2), (2, 2), then boundary cell (3, 2). The minimum distance is 3. A start already on an open boundary has distance 0 under this exercise contract.

## Your exercise

Implement nearest_exit_steps(grid, start). The rectangular grid uses # for walls and . for open cells. Move up/down/left/right. Return the fewest steps to any boundary cell, or -1 if unreachable. An empty grid, blocked start, or out-of-bounds start returns -1. Ragged input raises ValueError.

Start in [the exercise file](../exercises/08-queues-and-shortest-routes-without-weights.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Store (row, column, distance) in a queue. Check whether a popped cell is a goal.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def nearest_exit_steps(grid, start):
    """Rectangular grid: '#' blocked, '.' open. Any boundary is an exit."""
    if not grid:
        return -1
    rows, cols = len(grid), len(grid[0])
    if any(len(row) != cols for row in grid):
        raise ValueError('grid must be rectangular')
    if cols == 0:
        return -1
    sr, sc = start
    if not (0 <= sr < rows and 0 <= sc < cols) or grid[sr][sc] == '#':
        return -1
    queue = deque([(sr, sc, 0)])
    seen = {(sr, sc)}
    while queue:
        row, col, distance = queue.popleft()
        if row in (0, rows - 1) or col in (0, cols - 1):
            return distance
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = row + dr, col + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and grid[nr][nc] != '#' and (nr, nc) not in seen):
                seen.add((nr, nc))
                queue.append((nr, nc, distance + 1))
    return -1
```

### Why it works

FIFO processing ensures that all distance-d states are processed before distance-(d + 1) states. The first reachable boundary popped has minimum distance. Visited marking bounds each cell to one enqueue.

### Time and space

O(rows × columns) time and auxiliary space in the worst case.

</details>

## A mistake to watch for

Some other maze problems exclude the entrance as an exit; this one includes it. Do not import a different contract. Weighted moves require another shortest-path method.

## Retrieval check

Close the solution and answer: **When is a plain BFS shortest-path guarantee valid?**

<details><summary>Check your answer</summary>

When each traversed edge has the same cost, commonly one step.

</details>

## Optional extension

Track predecessors and reconstruct one shortest route, including the starting cell.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
