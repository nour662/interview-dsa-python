# 24. Weighted routes and Dijkstra’s frontier

[Previous lesson](23-disjoint-sets-for-growing-connectivity.md) · [Next lesson](25-bits-and-representation-contracts.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

When edges have unequal nonnegative costs, FIFO order no longer settles the cheapest route. Dijkstra’s algorithm expands the smallest tentative distance using a priority queue. Relaxation asks whether a route through the current vertex improves a neighbor. A simple heap implementation inserts improved entries without deleting old ones; discard stale entries when popped.

## Walk through an example

Edges 0 → 1 cost 8, 0 → 2 cost 2, and 2 → 1 cost 1 first propose distance 8 for vertex 1. Expanding vertex 2 improves it to 3. Later the heap entry (8,1) is stale and ignored.

## Your exercise

Implement shortest_costs(n, edges, source). Directed edges are (a,b,cost), endpoints and source are valid, n >= 1, and costs are nonnegative finite integers. Return distances from source, using float("inf") for unreachable vertices. Reject negative edge costs.

Start in [the exercise file](../exercises/24-weighted-routes-and-dijkstra-s-frontier.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Keep a distances array and a min-heap of (distance, vertex). Ignore a popped entry that no longer equals the stored distance.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def shortest_costs(n, edges, source):
    """Directed nonnegative edges (a, b, cost); unreachable => inf."""
    adjacency = [[] for _ in range(n)]
    for a, b, cost in edges:
        if cost < 0:
            raise ValueError('Dijkstra requires nonnegative edge costs')
        adjacency[a].append((b, cost))
    distances = [float('inf')] * n
    distances[source] = 0
    heap = [(0, source)]
    while heap:
        distance, node = heappop(heap)
        if distance != distances[node]:
            continue
        for neighbor, cost in adjacency[node]:
            candidate = distance + cost
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                heappush(heap, (candidate, neighbor))
    return distances
```

### Why it works

When the smallest current tentative distance is popped, an undiscovered shorter route would have to pass through a frontier vertex with no greater distance. Nonnegative edges prevent such a route from appearing later. Relaxing outgoing edges preserves shortest known route costs.

### Time and space

For this lazy-heap implementation, O(V + E log(E + 2)) time and O(V + E) space. Heap storage may be O(E), including stale entries; parallel edges are allowed.

</details>

## A mistake to watch for

BFS can choose a more expensive path with fewer edges. Dijkstra is not correct with negative edges. Marking a vertex final when first enqueued is premature.

## Retrieval check

Close the solution and answer: **Why can a negative edge invalidate a settled distance?**

<details><summary>Check your answer</summary>

A later route could reduce its total after reaching a farther vertex, contradicting the nondecreasing frontier argument.

</details>

## Optional extension

Store predecessors and reconstruct one cheapest route to a selected reachable destination.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
