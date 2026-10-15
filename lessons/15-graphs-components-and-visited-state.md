# 15. Graphs: components and visited state

[Previous lesson](14-binary-search-trees-and-inherited-constraints.md) · [Next lesson](16-directed-dependencies-and-topological-order.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A graph generalizes a tree: cycles, disconnected regions, and multiple routes can exist. Use an adjacency list to store neighbors. In an undirected graph add each edge in both directions. A traversal from one unseen vertex reaches exactly its connected component. Restart from every unseen vertex to cover disconnected input, including isolated vertices.

## Walk through an example

With n = 6 and edges (0, 1), (1, 2), (3, 4), the regions are {0,1,2}, {3,4}, and {5}. Starting a fresh traversal at 0, 3, and 5 gives component count 3.

## Your exercise

Implement component_count(n, edges). Vertices are 0 through n − 1; n is nonnegative and endpoints are valid. Edges are undirected. Parallel edges and self-loops are allowed; they do not create extra components.

Start in [the exercise file](../exercises/15-graphs-components-and-visited-state.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Maintain one visited set across all traversal starts. Mark before pushing onto the explicit stack.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def component_count(n, edges):
    adjacency = [[] for _ in range(n)]
    for a, b in edges:
        adjacency[a].append(b)
        adjacency[b].append(a)
    seen, count = set(), 0
    for start in range(n):
        if start in seen:
            continue
        count += 1
        seen.add(start)
        stack = [start]
        while stack:
            for neighbor in adjacency[stack.pop()]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
    return count
```

### Why it works

A traversal follows exactly the edges reachable from its start, so it covers one complete component. No visited vertex starts another traversal. Every component eventually supplies one unseen start.

### Time and space

O(V + E) time and O(V + E) space including adjacency storage; traversal state alone is O(V).

</details>

## A mistake to watch for

Clearing visited between starts overcounts. Ignoring vertices that never appear in the edge list loses isolated components.

## Retrieval check

Close the solution and answer: **How many components does n = 4 with no edges contain?**

<details><summary>Check your answer</summary>

Four: each isolated vertex is its own component.

</details>

## Optional extension

Return the vertices in each component and test that every vertex appears exactly once.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
