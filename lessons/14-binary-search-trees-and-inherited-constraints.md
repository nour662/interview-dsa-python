# 14. Binary search trees and inherited constraints

[Previous lesson](13-tree-bfs-and-level-boundaries.md) · [Next lesson](15-graphs-components-and-visited-state.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A binary search tree imposes constraints from every ancestor, not only the parent. Under strict ordering, every value in a left subtree is smaller than its root and every value in a right subtree is larger. Pass an allowed open interval downward. A missing bound means unbounded; it is not a numeric sentinel that might collide with input.

## Walk through an example

Root 10 has left child 5, and 5 has right child 12. Each local parent-child comparison looks valid, but 12 lies in the left subtree of 10. It violates the inherited upper bound 10.

## Your exercise

Implement valid_bst(root). Use strict ordering, so duplicates are invalid. An empty tree is valid. Node values are integers; assume a finite proper tree.

Start in [the exercise file](../exercises/14-binary-search-trees-and-inherited-constraints.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

When descending left, replace the upper bound with the current value. When descending right, replace the lower bound.

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

def valid_bst(root):
    def visit(node, low, high):
        if node is None:
            return True
        if low is not None and node.value <= low:
            return False
        if high is not None and node.value >= high:
            return False
        return (visit(node.left, low, node.value)
                and visit(node.right, node.value, high))
    return visit(root, None, None)
```

### Why it works

Each call receives exactly the ancestor constraints for its subtree. Rejecting a value outside them detects a violation; narrowing the interval for each child preserves every earlier constraint.

### Time and space

O(n) time and O(h) recursion space. Searching a balanced BST is O(log n), but validating one requires inspecting all its nodes.

</details>

## A mistake to watch for

Checking only immediate children accepts deeply misplaced values. Decide duplicate policy explicitly rather than silently mixing < and <=.

## Retrieval check

Close the solution and answer: **Does sorting a tree’s values prove that the original tree was a BST?**

<details><summary>Check your answer</summary>

No. Sorting discards structure. A strictly increasing inorder traversal would be a valid alternative check.

</details>

## Optional extension

Implement the inorder alternative iteratively, retaining only the previous visited value.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
