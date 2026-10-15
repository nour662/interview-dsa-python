# 16. Directed dependencies and topological order

[Previous lesson](15-graphs-components-and-visited-state.md) · [Next lesson](17-heaps-and-keeping-only-the-best-candidates.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Dependency edges have direction. A topological order places each prerequisite before the work that depends on it. Kahn’s algorithm tracks incoming edges remaining in the unprocessed graph. A zero-indegree vertex has no unfinished prerequisite and can be scheduled. If vertices remain but none is ready, a cycle blocks completion.

## Walk through an example

Edges 0 → 2 and 1 → 2 make both 0 and 1 initially ready. Removing each reduces indegree[2]. Only after both are processed does 2 enter the queue. Either [0,1,2] or [1,0,2] is valid.

## Your exercise

Implement dependency_order(n, edges), where (a, b) means a must happen before b. Return any valid ordering of vertices 0..n−1, or None if a cycle exists. Empty graph returns []. Endpoints are valid.

Start in [the exercise file](../exercises/16-directed-dependencies-and-topological-order.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Build outgoing adjacency and an indegree array. Check the number of processed vertices at the end.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def dependency_order(n, edges):
    """(a, b) means a must finish before b; None means a cycle."""
    adjacency = [[] for _ in range(n)]
    incoming = [0] * n
    for a, b in edges:
        adjacency[a].append(b)
        incoming[b] += 1
    queue = deque(i for i in range(n) if incoming[i] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in adjacency[node]:
            incoming[neighbor] -= 1
            if incoming[neighbor] == 0:
                queue.append(neighbor)
    return order if len(order) == n else None
```

### Why it works

Every emitted vertex has zero incoming edges from unfinished work, so all of its prerequisites already precede it. A finite directed acyclic graph always has a zero-indegree vertex. If processing stalls early, the remaining subgraph contains a cycle.

### Time and space

O(V + E) time and O(V + E) space.

</details>

## A mistake to watch for

An undirected cycle detector does not solve directed scheduling. Different correct orders can exist, so tests should verify constraints instead of only one literal order.

## Retrieval check

Close the solution and answer: **What should a self-loop 2 → 2 imply?**

<details><summary>Check your answer</summary>

A cycle, so no topological ordering exists.

</details>

## Optional extension

Return groups of tasks that can begin in parallel, respecting dependency layers.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
