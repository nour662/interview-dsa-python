# 22. Tries: organize information by shared prefixes

[Previous lesson](21-grid-dp-and-careful-memory-reuse.md) · [Next lesson](23-disjoint-sets-for-growing-connectivity.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A trie is a tree whose edges represent successive symbols. Words sharing a prefix share a traversal path. Hash maps answer exact-key questions; a trie makes prefix navigation explicit. Store a count at each node to answer how many inserted entries share that prefix without traversing the whole subtree. Dictionary child maps avoid allocating an entire alphabet at every node.

## Walk through an example

Insert "map", "math", and "map" again. The path m → a has count 3, while m → a → p has count 2. Query "mat" returns 1. Query "z" returns 0. The empty prefix matches all three inserted entries.

## Your exercise

Implement PrefixIndex with add(word) and count_prefix(prefix). Inputs are Python strings. Count duplicate inserts separately. Empty words are valid, and querying the empty prefix returns the total number of inserted entries.

Start in [the exercise file](../exercises/22-tries-organize-information-by-shared-prefixes.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Give the root its own count, and increment counts along every inserted path.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

class PrefixIndex:
    """Trie with duplicate inserts counted as separate entries."""
    def __init__(self):
        self.root = {'count': 0, 'children': {}}

    def add(self, word):
        node = self.root
        node['count'] += 1
        for char in word:
            node = node['children'].setdefault(char, {'count': 0, 'children': {}})
            node['count'] += 1

    def count_prefix(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node['children']:
                return 0
            node = node['children'][char]
        return node['count']
```

### Why it works

Each insertion increments precisely the nodes corresponding to its prefixes, including the empty prefix at the root. Therefore a reached node’s count equals the number of entries matching that prefix. A missing edge means zero matches.

### Time and space

Expected O(L) per insertion and O(P) per prefix query for lengths L and P. Total storage is O(total inserted characters) in the worst case, with substantial Python object overhead.

</details>

## A mistake to watch for

Without the root counter, empty-prefix queries fail. A terminal-word flag alone cannot count duplicate entries or all descendants.

## Retrieval check

Close the solution and answer: **Does a prefix count of 2 prove the prefix itself was inserted?**

<details><summary>Check your answer</summary>

No. Two longer strings may share that prefix without the prefix being a complete inserted word.

</details>

## Optional extension

Add exact-word counts and then support deletion without making any counters negative.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
