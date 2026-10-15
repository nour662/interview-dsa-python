# 12. Tree DFS: return one fact, update another

[Previous lesson](11-recursion-as-a-contract-for-smaller-work.md) · [Next lesson](13-tree-bfs-and-level-boundaries.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Trees connect nodes without cycles. In a binary tree each node has up to two children. A depth-first postorder traversal finishes the children before combining their results. Sometimes the fact a parent needs differs from the answer being optimized. For diameter, a parent needs one downward height, but a path passing through a node can combine both child heights.

## Walk through an example

A root with two leaf children receives heights 1 and 1. Its through-root path has 2 edges; it returns height 2. A chain of three nodes also has diameter 2. The longest path need not pass through the overall root.

## Your exercise

Implement tree_diameter(root) using Tree. Return the maximum number of edges on a simple path between any two nodes. Empty and single-node trees return 0. Assume a finite tree with no shared nodes or cycles.

Start in [the exercise file](../exercises/12-tree-dfs-return-one-fact-update-another.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Let height(None) be 0. At each node, left_height + right_height is a candidate diameter.

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

def tree_diameter(root):
    """Number of edges on the longest simple path; empty tree => 0."""
    best = 0
    def height(node):
        nonlocal best
        if node is None:
            return 0
        left, right = height(node.left), height(node.right)
        best = max(best, left + right)
        return 1 + max(left, right)
    height(root)
    return best
```

### Why it works

Every path has a highest node where its two downward portions meet. Postorder computes the longest available downward portion on each side. Taking the maximum of their sums therefore considers an optimal path at its highest node.

### Time and space

O(n) time and O(h) recursion space. A skewed tree has h = n and may exceed Python recursion depth.

</details>

## A mistake to watch for

Returning the diameter to the parent loses the height information needed for combination. Counting nodes rather than edges produces off-by-one answers.

## Retrieval check

Close the solution and answer: **Can the diameter lie entirely in the left subtree?**

<details><summary>Check your answer</summary>

Yes. Updating a global best at every node covers that case.

</details>

## Optional extension

Return the actual endpoint values along with the diameter length.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
