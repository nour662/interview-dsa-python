# 23. Disjoint sets for growing connectivity

[Previous lesson](22-tries-organize-information-by-shared-prefixes.md) · [Next lesson](24-weighted-routes-and-dijkstra-s-frontier.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Disjoint-set union tracks which group each vertex belongs to while connections are added. Each group has a representative root. Union joins roots, rather than arbitrary nodes. Union by size attaches the smaller tree under the larger one; path compression shortens later finds. This structure answers connectivity efficiently but does not retain actual graph paths.

## Walk through an example

Start with four groups {0}, {1}, {2}, {3}. union(0,1) leaves three groups. union(2,3) leaves two. union(1,2) leaves one. union(0,3) returns False because those vertices already share a representative.

## Your exercise

Implement DisjointSets(n) with find(node), union(a,b), and groups. Vertices are valid IDs 0..n−1. union returns True only when it merges two distinct groups. Start with groups = n.

Start in [the exercise file](../exercises/23-disjoint-sets-for-growing-connectivity.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Compress paths during find. Decrease groups only after two different representatives are joined.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

class DisjointSets:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.groups = n

    def find(self, node):
        while node != self.parent[node]:
            self.parent[node] = self.parent[self.parent[node]]
            node = self.parent[node]
        return node

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        self.groups -= 1
        return True
```

### Why it works

Each parent tree represents exactly one connected group. Joining representatives merges exactly two groups and cannot create an internal parent cycle. Compression changes a node’s parent only to another ancestor in the same group.

### Time and space

O(n) initialization and O(n) storage. With both heuristics, m operations take O(m α(n)) amortized time beyond initialization, where α grows extremely slowly; an individual operation need not be constant time.

</details>

## A mistake to watch for

Decrementing groups for an already connected pair gives incorrect counts. Standard DSU cannot efficiently undo arbitrary edge deletions.

## Retrieval check

Close the solution and answer: **Can parent pointers reconstruct the original connecting edges?**

<details><summary>Check your answer</summary>

No. Union and compression change the representation; it is not the original graph.

</details>

## Optional extension

Process a stream of connections and report the component count after every addition.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
