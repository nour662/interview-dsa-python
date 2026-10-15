# 09. Linked lists and safe pointer changes

[Previous lesson](08-queues-and-shortest-routes-without-weights.md) · [Next lesson](10-binary-search-with-explicit-boundaries.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A linked list stores each value with a link to the next node. Moving to index k costs traversal, but relinking a node is constant work once its predecessor is known. Reversal is about preserving access while changing direction. Before overwriting current.next, save the following node. Otherwise the unprocessed suffix can become unreachable.

## Walk through an example

For A → B → C, save B, set A.next to None, then advance. Save C, set B.next to A, then advance. Finally set C.next to B. The new head is C; the old head A is now the tail.

## Your exercise

Implement reverse_chain(head) using the provided Node class. Reverse a finite acyclic singly linked list in place and return its new head. None returns None. Preserve node identities; do not create replacement nodes.

Start in [the exercise file](../exercises/09-linked-lists-and-safe-pointer-changes.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Keep three references: previous, current, and a temporary following reference.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

@dataclass
class Node:
    value: int
    next: Optional['Node'] = None

def reverse_chain(head):
    previous = None
    current = head
    while current is not None:
        following = current.next
        current.next = previous
        previous, current = current, following
    return previous
```

### Why it works

At every iteration, previous is the head of the reversed processed prefix and current is the untouched suffix head. Saving following preserves the suffix before relinking. When current becomes None, the entire list is the reversed prefix.

### Time and space

O(n) time and O(1) auxiliary space. The input nodes are reused.

</details>

## A mistake to watch for

Advancing through current.next after overwriting it follows the reversed link. A cyclic input violates this exercise precondition and needs separate cycle handling.

## Retrieval check

Close the solution and answer: **Why should the original head eventually point to None?**

<details><summary>Check your answer</summary>

It becomes the new tail. Keeping its old next link could create a cycle.

</details>

## Optional extension

Reverse only the first k nodes and reconnect the suffix; define behavior when k exceeds length.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
