# 13. Tree BFS and level boundaries

[Previous lesson](12-tree-dfs-return-one-fact-update-another.md) · [Next lesson](14-binary-search-trees-and-inherited-constraints.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Level-order traversal groups nodes by distance from the root. A queue naturally holds the next nodes to process, but children are added while the current level is being consumed. Capture the queue length at the start of each level; that snapshot separates current-level nodes from children appended for the next level.

## Walk through an example

For root 6 with children 2 and 10, queue width starts at 1 and produces mean 6. The next width is 2 and produces (2 + 10) / 2 = 6. Children of either node belong to the following level.

## Your exercise

Implement level_means(root), returning a list of arithmetic means from root level downward. Use the provided finite Tree structure. Empty input returns []. Floating-point output is acceptable.

Start in [the exercise file](../exercises/13-tree-bfs-and-level-boundaries.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Use width = len(queue) once per outer iteration and pop exactly width nodes.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

@dataclass
class Tree:
    value: int
    left: Optional['Tree'] = None
    right: Optional['Tree'] = None

def level_means(root):
    if root is None:
        return []
    queue, answer = deque([root]), []
    while queue:
        width, total = len(queue), 0
        for _ in range(width):
            node = queue.popleft()
            total += node.value
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        answer.append(total / width)
    return answer
```

### Why it works

At the start of a level, the queue contains precisely that level in order. Processing its captured width consumes all and only those nodes while appending their children. The invariant repeats for the next level.

### Time and space

O(n) time and O(w) queue space for maximum level width w, plus O(h) output. Floating-point arithmetic has ordinary precision limits.

</details>

## A mistake to watch for

Using a queue length that changes inside the inner loop mixes levels. A wide balanced tree can use more BFS memory than DFS.

## Retrieval check

Close the solution and answer: **Which can use O(n) queue space: a chain or a broad tree?**

<details><summary>Check your answer</summary>

A broad tree. A chain has at most one node in its queue at a time.

</details>

## Optional extension

Produce the visible rightmost value of each level using the same level-boundary pattern.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
