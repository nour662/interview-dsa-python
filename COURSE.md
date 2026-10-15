# Interview DSA in Python — complete reading guide

Original independent educational material. Work one lesson at a time.

# 01. Reason about work before writing code

[Course home](README.md) · [Next lesson](lessons/02-arrays-strings-and-boundary-handling.md) · [Full course](README.md)

**Prerequisite:** Basic Python functions, loops, lists, and dictionaries.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

An algorithm is a sequence of decisions with a cost. Count how many times an operation can happen as the input grows. A loop nested inside another loop is not automatically quadratic: the question is whether their work multiplies. Big O describes growth rather than a stopwatch result. For Python dictionaries, use expected constant-time lookup under ordinary hashing assumptions; it is not a worst-case guarantee.

## Walk through an example

For values [4, 7, 4, 4], the three 4s form three pairs. Scanning left to right, their contributions are 0, 1, and 2. The 7 contributes 0. A frequency table replaces repeatedly scanning earlier items.

## Your exercise

Implement count_equal_pairs(values). Return the number of index pairs i < j whose values are equal. Values are hashable. Empty input returns 0; do not mutate the input.

Start in [the exercise file](exercises/01-reason-about-work-before-writing-code.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Before recording the current value, ask how many matching values have already appeared.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def count_equal_pairs(values):
    counts = Counter()
    pairs = 0
    for value in values:
        pairs += counts[value]
        counts[value] += 1
    return pairs
```

### Why it works

Before each iteration, counts describes exactly the processed prefix and pairs counts every matching pair entirely inside it. Adding counts[value] introduces exactly the pairs ending at the new position. No pair is missed or counted twice.

### Time and space

Expected O(n) time and O(u) auxiliary space, where u is the number of distinct values. A direct comparison of all pairs costs O(n²) time and O(1) extra space.

</details>

## A mistake to watch for

Incrementing the frequency before adding its contribution counts each element as a pair with itself. Test [9] and [9, 9] to expose that error.

## Retrieval check

Close the solution and answer: **If every value is equal, what is the result for n elements?**

<details><summary>Check your answer</summary>

n(n − 1) / 2. The output grows quadratically even though the counting algorithm is expected linear time.

</details>

## Optional extension

Write the quadratic version and compare results for every length-5 list over values 0, 1, and 2.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.


---

# 02. Arrays, strings, and boundary handling

[Previous lesson](lessons/01-reason-about-work-before-writing-code.md) · [Next lesson](lessons/03-hash-maps-remember-what-a-scan-cannot.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Arrays give direct access by index; contiguous scans are often enough. Python lists can grow, but inserting near the beginning shifts later entries. Strings are immutable, so build pieces and join them when constructing large text. A run is a maximal adjacent block of equal items. Keeping one active run separates the current unfinished result from results already committed.

## Walk through an example

For "aaabbc", start with (a, 1), extend to (a, 3), then commit it when b arrives. Commit (b, 2) when c arrives. The loop ends with c still active, so append (c, 1) after the loop.

## Your exercise

Implement compress_runs(text), returning a list of (character, count) tuples for consecutive runs. Empty text returns []. Spaces and punctuation count as characters; preserve case.

Start in [the exercise file](exercises/02-arrays-strings-and-boundary-handling.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Handle empty input before reading text[0]. Store the current character and run length.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def compress_runs(text):
    if not text:
        return []
    result = []
    current, count = text[0], 1
    for char in text[1:]:
        if char == current:
            count += 1
        else:
            result.append((current, count))
            current, count = char, 1
    result.append((current, count))
    return result
```

### Why it works

Before each new character, result contains every completed run and current/count describes the one unfinished run. A changed character closes exactly that run. The final append closes the only run not ended by a change.

### Time and space

O(n) time. O(r) output space for r runs. This implementation also uses O(n) temporary space for text[1:]; iterate by index instead to avoid that slice.

</details>

## A mistake to watch for

Forgetting the final run makes a one-character input return an empty answer. Combining equal letters that are separated by other letters changes the problem into frequency counting.

## Retrieval check

Close the solution and answer: **What should "ab a" produce?**

<details><summary>Check your answer</summary>

[('a', 1), ('b', 1), (' ', 1), ('a', 1)]. The two a runs are separate.

</details>

## Optional extension

Replace the slice with an index loop and explain the effect on auxiliary space.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.


---

# 03. Hash maps: remember what a scan cannot

[Previous lesson](lessons/02-arrays-strings-and-boundary-handling.md) · [Next lesson](lessons/04-two-pointers-and-monotone-movement.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A hash map associates keys with information. A set remembers presence; a map can remember counts, positions, or accumulated results. The stored value must answer the future question. If the question asks whether something occurs exactly once in the entire input, a first encounter cannot settle it: a duplicate might appear later. Separate global counting from ordered selection.

## Walk through an example

For [8, 3, 8, 5, 3], the count map is {8: 2, 3: 2, 5: 1}. A second scan in original order first finds count 1 at index 3. Map order is irrelevant because the input scan determines the answer.

## Your exercise

Implement earliest_unique(values). Return the earliest index whose value occurs exactly once, or -1 if none exists. Values are hashable. Preserve the input.

Start in [the exercise file](exercises/03-hash-maps-remember-what-a-scan-cannot.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Use one pass to count and a second pass to select. Returning from the first pass is premature.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def earliest_unique(values):
    counts = Counter(values)
    return next((i for i, value in enumerate(values) if counts[value] == 1), -1)
```

### Why it works

After counting, each map entry is the exact frequency of its key. Scanning indices in increasing order means the first frequency-one item has no earlier qualifying item.

### Time and space

Expected O(n) time and O(u) auxiliary space. A count map may store up to n distinct keys.

</details>

## A mistake to watch for

Do not return the value when the contract asks for an index. Empty input and input containing only repeated values must return -1.

## Retrieval check

Close the solution and answer: **Can a set alone distinguish one occurrence from three?**

<details><summary>Check your answer</summary>

No. Both produce one membership entry. You need counts or another structure that records repeated membership.

</details>

## Optional extension

Return all unique-value indices while preserving input order. What extra space is output space?

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.


---

# 04. Two pointers and monotone movement

[Previous lesson](lessons/03-hash-maps-remember-what-a-scan-cannot.md) · [Next lesson](lessons/05-sliding-windows-and-reversible-state.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Two pointers work when moving a boundary eliminates candidates safely. Sorted input provides an ordering argument. If the sum of the two endpoints is below the target, pairing the left endpoint with any smaller right endpoint cannot improve that below-target sum. After evaluating the current pair, move the left endpoint. Symmetrically, an excessive sum allows moving the right endpoint. Track the best pair before discarding a boundary.

## Walk through an example

With [1, 4, 6, 10] and target 12: (1, 10) gives 11, then (4, 10) gives 14, then (4, 6) gives 10. The best difference is 1, so return (1, 10). An exact match can stop immediately.

## Your exercise

Implement closest_pair(sorted_values, target). Return values at two distinct positions whose sum is closest to target. The input is sorted in nondecreasing order. Any optimal tie is valid; fewer than two values returns None.

Start in [the exercise file](exercises/04-two-pointers-and-monotone-movement.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Start at both ends. Record the closest pair seen before advancing one pointer.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def closest_pair(sorted_values, target):
    if len(sorted_values) < 2:
        return None
    left, right = 0, len(sorted_values) - 1
    best = (sorted_values[left], sorted_values[right])
    while left < right:
        total = sorted_values[left] + sorted_values[right]
        if abs(total - target) < abs(sum(best) - target):
            best = (sorted_values[left], sorted_values[right])
        if total == target:
            break
        if total < target:
            left += 1
        else:
            right -= 1
    return best
```

### Why it works

When the sum is below target, all other pairs using the left endpoint and a smaller right endpoint are no closer than the current pair. The symmetric statement holds above target. Each discarded boundary therefore cannot hide a better unexplored pair.

### Time and space

O(n) time and O(1) auxiliary space. Sorting arbitrary input first would add O(n log n) time and may change the mutation contract.

</details>

## A mistake to watch for

Using left <= right permits reusing one position. Negative values are allowed, but unsorted input breaks the elimination proof.

## Retrieval check

Close the solution and answer: **Why is this approach unsafe for unsorted input?**

<details><summary>Check your answer</summary>

Moving right or left no longer predicts how the sum changes, so it can discard the optimal pair.

</details>

## Optional extension

Return indices instead of values and define a deterministic tie-breaking rule.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.


---

# 05. Sliding windows and reversible state

[Previous lesson](lessons/04-two-pointers-and-monotone-movement.md) · [Next lesson](lessons/06-prefix-sums-for-signed-ranges.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A sliding window represents a contiguous segment. Add the new right item, then remove left items until the segment satisfies a rule. This needs a property that lets boundary movement repair validity. With nonnegative costs, extending cannot decrease a sum and removing cannot increase it. Although a while loop sits inside a for loop, each element enters and leaves at most once.

## Walk through an example

For costs [2, 1, 3, 1] and budget 4, window [2, 1] has length 2. Adding 3 forces removal of 2 and leaves [1, 3]. Adding 1 removes the earlier 1 and leaves [3, 1]. The longest valid length is 2.

## Your exercise

Implement longest_budget_window(costs, budget). Return the longest contiguous segment length with sum at most budget. Costs and budget are nonnegative numbers; reject negative values with ValueError. Empty input returns 0.

Start in [the exercise file](exercises/05-sliding-windows-and-reversible-state.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Maintain left, total, and best. Update best only after restoring validity.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def longest_budget_window(costs, budget):
    """Nonnegative costs and budget. Return length, not slice."""
    if budget < 0 or any(cost < 0 for cost in costs):
        raise ValueError('costs and budget must be nonnegative')
    left = total = best = 0
    for right, cost in enumerate(costs):
        total += cost
        while total > budget:
            total -= costs[left]
            left += 1
        best = max(best, right - left + 1)
    return best
```

### Why it works

After shrinking, the window is valid. Every removed left endpoint made a sum too large and cannot become useful by extending the right edge with more nonnegative costs. Across the scan, both pointers move only forward.

### Time and space

O(n) time including validation and O(1) auxiliary space.

</details>

## A mistake to watch for

Negative costs destroy the monotonicity argument. For signed values, do not reuse this template without a new proof. Zero-cost entries must still contribute to window length.

## Retrieval check

Close the solution and answer: **Why does the inner loop not imply O(n²) here?**

<details><summary>Check your answer</summary>

The left pointer advances at most n times across all outer iterations, not n times per iteration.

</details>

## Optional extension

Return the half-open indices [start, end) of a longest valid window.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.


---

# 06. Prefix sums for signed ranges

[Previous lesson](lessons/05-sliding-windows-and-reversible-state.md) · [Next lesson](lessons/07-stacks-and-unresolved-candidates.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A prefix sum records the total before a position. The sum of values from i through j is prefix[j + 1] − prefix[i]. This turns a range question into a lookup for an earlier total. Unlike the previous window technique, this works with negative values. When counting all qualifying ranges, store how often each prefix occurred rather than only whether it occurred.

## Walk through an example

For [2, -2, 2] and target 2, prefix totals are 0, 2, 0, 2. The last prefix 2 finds two earlier zeros, contributing two ranges. Together with the first 2, the answer is 3.

## Your exercise

Implement count_target_ranges(values, target). Count nonempty contiguous ranges summing to target. Values may be negative or zero. Empty input returns 0.

Start in [the exercise file](exercises/06-prefix-sums-for-signed-ranges.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Seed the frequency map with prefix zero appearing once. Query prefix − target before recording the new prefix.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def count_target_ranges(values, target):
    seen = Counter({0: 1})
    prefix = answer = 0
    for value in values:
        prefix += value
        answer += seen[prefix - target]
        seen[prefix] += 1
    return answer
```

### Why it works

Before processing each new prefix, seen contains exactly the prefixes at earlier boundaries. Each matching earlier prefix determines one nonempty range ending now. Querying first prevents a zero-length range when target is zero.

### Time and space

Expected O(n) time and O(n) auxiliary space.

</details>

## A mistake to watch for

A set undercounts repeated prefix totals. Forgetting the initial zero loses ranges starting at index 0. Recording before querying adds empty ranges for target 0.

## Retrieval check

Close the solution and answer: **How many target-zero ranges are in [0, 0]?**

<details><summary>Check your answer</summary>

Three: each individual zero and the full two-element range.

</details>

## Optional extension

Return the length of the longest matching range by storing the earliest index of each prefix.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.


---

# 07. Stacks and unresolved candidates

[Previous lesson](lessons/06-prefix-sums-for-signed-ranges.md) · [Next lesson](lessons/08-queues-and-shortest-routes-without-weights.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A stack removes the most recently added item first. It can represent unfinished parsing, nested work, or candidates awaiting a future event. A monotonic stack keeps candidates in a useful order and removes those settled by the current item. Store indices when distance matters. Equal values need careful handling because strictly greater and greater-or-equal are different conditions.

## Walk through an example

For [20, 18, 21], day 0 waits on the stack, then day 1 joins it. Day 2 is warmer than both: pop day 1 and record 1, then pop day 0 and record 2. Day 2 never sees a warmer future day, so its answer remains 0.

## Your exercise

Implement next_warmer_wait(temperatures). For each day return the number of days until a strictly warmer temperature. Use 0 when no such future day exists.

Start in [the exercise file](exercises/07-stacks-and-unresolved-candidates.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Keep unresolved day indices. The current day resolves every smaller temperature at the stack top.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def next_warmer_wait(temperatures):
    waits = [0] * len(temperatures)
    pending = []
    for day, temperature in enumerate(temperatures):
        while pending and temperatures[pending[-1]] < temperature:
            earlier = pending.pop()
            waits[earlier] = day - earlier
        pending.append(day)
    return waits
```

### Why it works

The stack temperatures are nonincreasing. Popping a prior day at the first warmer incoming day gives its nearest qualifying future day: any earlier warmer day would already have popped it. Every index is pushed once and popped at most once.

### Time and space

O(n) time and O(n) auxiliary space, plus the O(n) answer.

</details>

## A mistake to watch for

Use < rather than <= when resolving candidates. Equal temperatures do not satisfy strictly warmer. A stack of values alone loses the original day indices.

## Retrieval check

Close the solution and answer: **What is the answer for [5, 5, 6]?**

<details><summary>Check your answer</summary>

[2, 1, 0]. The second 5 does not resolve the first.

</details>

## Optional extension

Find the next strictly smaller value instead. State the new stack invariant.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.


---

# 08. Queues and shortest routes without weights

[Previous lesson](lessons/07-stacks-and-unresolved-candidates.md) · [Next lesson](lessons/09-linked-lists-and-safe-pointer-changes.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A queue processes the oldest waiting item first. Breadth-first search explores distance 0, then distance 1, and so on when every edge costs one step. Use deque.popleft rather than list.pop(0). Mark a state visited when enqueuing it so multiple neighbors cannot queue it repeatedly. The definition of a goal matters as much as the traversal.

## Walk through an example

In ["#####", "#...#", "##.##", "##.##"], start (1, 1) reaches (1, 2), (2, 2), then boundary cell (3, 2). The minimum distance is 3. A start already on an open boundary has distance 0 under this exercise contract.

## Your exercise

Implement nearest_exit_steps(grid, start). The rectangular grid uses # for walls and . for open cells. Move up/down/left/right. Return the fewest steps to any boundary cell, or -1 if unreachable. An empty grid, blocked start, or out-of-bounds start returns -1. Ragged input raises ValueError.

Start in [the exercise file](exercises/08-queues-and-shortest-routes-without-weights.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

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


---

# 09. Linked lists and safe pointer changes

[Previous lesson](lessons/08-queues-and-shortest-routes-without-weights.md) · [Next lesson](lessons/10-binary-search-with-explicit-boundaries.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A linked list stores each value with a link to the next node. Moving to index k costs traversal, but relinking a node is constant work once its predecessor is known. Reversal is about preserving access while changing direction. Before overwriting current.next, save the following node. Otherwise the unprocessed suffix can become unreachable.

## Walk through an example

For A → B → C, save B, set A.next to None, then advance. Save C, set B.next to A, then advance. Finally set C.next to B. The new head is C; the old head A is now the tail.

## Your exercise

Implement reverse_chain(head) using the provided Node class. Reverse a finite acyclic singly linked list in place and return its new head. None returns None. Preserve node identities; do not create replacement nodes.

Start in [the exercise file](exercises/09-linked-lists-and-safe-pointer-changes.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

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


---

# 10. Binary search with explicit boundaries

[Previous lesson](lessons/09-linked-lists-and-safe-pointer-changes.md) · [Next lesson](lessons/11-recursion-as-a-contract-for-smaller-work.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Binary search repeatedly discards half a sorted search space. The reliable version begins by stating what each boundary means. For a lower bound, positions before left are known to contain values smaller than target; positions at or after right are known to contain values at least target. Search the half-open interval [left, right). A length-n input has n + 1 insertion boundaries.

## Walk through an example

For [2, 4, 4, 9] and target 4, start [0, 4). Middle 2 qualifies, so right becomes 2. Middle 1 qualifies, so right becomes 1. Middle 0 is too small, so left becomes 1. Both meet at the first 4.

## Your exercise

Implement lower_bound(values, target). Return the first index whose value is at least target in sorted nondecreasing input. Return len(values) if no value qualifies; empty input returns 0.

Start in [the exercise file](exercises/10-binary-search-with-explicit-boundaries.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Use right = len(values). A qualifying middle stays a possible answer, so set right = middle.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def lower_bound(values, target):
    left, right = 0, len(values)
    while left < right:
        middle = (left + right) // 2
        if values[middle] < target:
            left = middle + 1
        else:
            right = middle
    return left
```

### Why it works

Both updates preserve the boundary claims. Each update strictly shrinks the unresolved interval. When left equals right, every earlier element is too small and that boundary is the first possible qualifying index.

### Time and space

O(log n) time and O(1) auxiliary space for random-access input.

</details>

## A mistake to watch for

right = middle − 1 belongs to a different boundary convention. Mixing conventions causes missed answers or infinite loops. The returned index can equal n.

## Retrieval check

Close the solution and answer: **What does lower_bound([3, 3], 4) return?**

<details><summary>Check your answer</summary>

2, the insertion boundary after the last item.

</details>

## Optional extension

Search for the smallest feasible capacity in a monotone feasibility predicate instead of searching stored values.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.


---

# 11. Recursion as a contract for smaller work

[Previous lesson](lessons/10-binary-search-with-explicit-boundaries.md) · [Next lesson](lessons/12-tree-dfs-return-one-fact-update-another.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A recursive function promises to solve the same kind of problem on a smaller input. Identify the returned meaning, a base case, and a measure that decreases. The call stack stores unfinished work. Recursion is not automatically exponential: repeated subproblems and branching determine total work. Deep Python recursion can exceed the interpreter limit even when asymptotic work is linear.

## Walk through an example

For [2, [3, [], [4]], 1], the inner [4] returns 4, then [3, [], [4]] returns 7. The outer call adds 2 + 7 + 1 and returns 10. An empty list contributes zero.

## Your exercise

Implement nested_total(items). Input is a finite, acyclic nesting of Python lists and integers. Return the sum of every integer. Do not mutate input. Empty lists can appear at any depth.

Start in [the exercise file](exercises/11-recursion-as-a-contract-for-smaller-work.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

For each item, either add its integer value or ask the same function to sum the nested list.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def nested_total(items):
    """Finite, acyclic nested lists containing integers only."""
    total = 0
    for item in items:
        total += nested_total(item) if isinstance(item, list) else item
    return total
```

### Why it works

For an empty list the result is zero. Assuming recursive calls correctly total each smaller nested list, adding those totals and the direct integers counts every integer exactly once.

### Time and space

O(m) time for m visited list entries and O(h) call-stack space for nesting depth h. A very deep input may raise RecursionError.

</details>

## A mistake to watch for

Summing only the outer integers misses nested values. Cycles are outside the contract; do not claim this handles a list that contains itself.

## Retrieval check

Close the solution and answer: **Does two recursive calls always imply exponential time?**

<details><summary>Check your answer</summary>

No. If they visit disjoint portions of a tree, total work can still be linear in the total nodes.

</details>

## Optional extension

Implement an explicit stack version that handles deeply nested acyclic input.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.


---

# 12. Tree DFS: return one fact, update another

[Previous lesson](lessons/11-recursion-as-a-contract-for-smaller-work.md) · [Next lesson](lessons/13-tree-bfs-and-level-boundaries.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Trees connect nodes without cycles. In a binary tree each node has up to two children. A depth-first postorder traversal finishes the children before combining their results. Sometimes the fact a parent needs differs from the answer being optimized. For diameter, a parent needs one downward height, but a path passing through a node can combine both child heights.

## Walk through an example

A root with two leaf children receives heights 1 and 1. Its through-root path has 2 edges; it returns height 2. A chain of three nodes also has diameter 2. The longest path need not pass through the overall root.

## Your exercise

Implement tree_diameter(root) using Tree. Return the maximum number of edges on a simple path between any two nodes. Empty and single-node trees return 0. Assume a finite tree with no shared nodes or cycles.

Start in [the exercise file](exercises/12-tree-dfs-return-one-fact-update-another.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

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


---

# 13. Tree BFS and level boundaries

[Previous lesson](lessons/12-tree-dfs-return-one-fact-update-another.md) · [Next lesson](lessons/14-binary-search-trees-and-inherited-constraints.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Level-order traversal groups nodes by distance from the root. A queue naturally holds the next nodes to process, but children are added while the current level is being consumed. Capture the queue length at the start of each level; that snapshot separates current-level nodes from children appended for the next level.

## Walk through an example

For root 6 with children 2 and 10, queue width starts at 1 and produces mean 6. The next width is 2 and produces (2 + 10) / 2 = 6. Children of either node belong to the following level.

## Your exercise

Implement level_means(root), returning a list of arithmetic means from root level downward. Use the provided finite Tree structure. Empty input returns []. Floating-point output is acceptable.

Start in [the exercise file](exercises/13-tree-bfs-and-level-boundaries.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

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


---

# 14. Binary search trees and inherited constraints

[Previous lesson](lessons/13-tree-bfs-and-level-boundaries.md) · [Next lesson](lessons/15-graphs-components-and-visited-state.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A binary search tree imposes constraints from every ancestor, not only the parent. Under strict ordering, every value in a left subtree is smaller than its root and every value in a right subtree is larger. Pass an allowed open interval downward. A missing bound means unbounded; it is not a numeric sentinel that might collide with input.

## Walk through an example

Root 10 has left child 5, and 5 has right child 12. Each local parent-child comparison looks valid, but 12 lies in the left subtree of 10. It violates the inherited upper bound 10.

## Your exercise

Implement valid_bst(root). Use strict ordering, so duplicates are invalid. An empty tree is valid. Node values are integers; assume a finite proper tree.

Start in [the exercise file](exercises/14-binary-search-trees-and-inherited-constraints.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

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


---

# 15. Graphs: components and visited state

[Previous lesson](lessons/14-binary-search-trees-and-inherited-constraints.md) · [Next lesson](lessons/16-directed-dependencies-and-topological-order.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A graph generalizes a tree: cycles, disconnected regions, and multiple routes can exist. Use an adjacency list to store neighbors. In an undirected graph add each edge in both directions. A traversal from one unseen vertex reaches exactly its connected component. Restart from every unseen vertex to cover disconnected input, including isolated vertices.

## Walk through an example

With n = 6 and edges (0, 1), (1, 2), (3, 4), the regions are {0,1,2}, {3,4}, and {5}. Starting a fresh traversal at 0, 3, and 5 gives component count 3.

## Your exercise

Implement component_count(n, edges). Vertices are 0 through n − 1; n is nonnegative and endpoints are valid. Edges are undirected. Parallel edges and self-loops are allowed; they do not create extra components.

Start in [the exercise file](exercises/15-graphs-components-and-visited-state.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

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


---

# 16. Directed dependencies and topological order

[Previous lesson](lessons/15-graphs-components-and-visited-state.md) · [Next lesson](lessons/17-heaps-and-keeping-only-the-best-candidates.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Dependency edges have direction. A topological order places each prerequisite before the work that depends on it. Kahn’s algorithm tracks incoming edges remaining in the unprocessed graph. A zero-indegree vertex has no unfinished prerequisite and can be scheduled. If vertices remain but none is ready, a cycle blocks completion.

## Walk through an example

Edges 0 → 2 and 1 → 2 make both 0 and 1 initially ready. Removing each reduces indegree[2]. Only after both are processed does 2 enter the queue. Either [0,1,2] or [1,0,2] is valid.

## Your exercise

Implement dependency_order(n, edges), where (a, b) means a must happen before b. Return any valid ordering of vertices 0..n−1, or None if a cycle exists. Empty graph returns []. Endpoints are valid.

Start in [the exercise file](exercises/16-directed-dependencies-and-topological-order.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

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


---

# 17. Heaps and keeping only the best candidates

[Previous lesson](lessons/16-directed-dependencies-and-topological-order.md) · [Next lesson](lessons/18-greedy-choices-need-an-exchange-argument.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A heap exposes the smallest item efficiently without sorting the entire collection. Python heapq implements a min-heap. To retain the k largest values, keep a heap of size at most k: when it grows, remove its smallest member. The root then marks the weakest surviving candidate, which is exactly the kth largest once enough items have arrived.

## Walk through an example

For [6, 2, 9, 4] and k = 2, retain {6}, then {2,6}. Adding 9 ejects 2; adding 4 ejects 4. The final retained values are 6 and 9, so the answer is 6.

## Your exercise

Implement kth_largest(values, k). Count duplicates as separate positions in descending order. Do not mutate the input. Reject k outside 1..len(values) with ValueError.

Start in [the exercise file](exercises/17-heaps-and-keeping-only-the-best-candidates.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Push each value, and pop whenever the heap contains more than k values.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def kth_largest(values, k):
    if not 1 <= k <= len(values):
        raise ValueError('k must be between 1 and len(values)')
    heap = []
    for value in values:
        heappush(heap, value)
        if len(heap) > k:
            heappop(heap)
    return heap[0]
```

### Why it works

After each input, the heap contains the largest min(k, processed_count) values seen so far. A newly pushed value can only displace the smallest retained candidate. At completion the root is the kth largest.

### Time and space

O(n log(k + 1)) time and O(k) auxiliary space. For k = 1 this is linear; sorting instead costs O(n log n).

</details>

## A mistake to watch for

The heap’s list representation is not fully sorted. The maximum is not necessarily the last item. Duplicates matter unless the contract asks for distinct values.

## Retrieval check

Close the solution and answer: **For [5, 5, 2] with k = 2, what is the answer?**

<details><summary>Check your answer</summary>

5. The two 5s occupy the first and second positions.

</details>

## Optional extension

Adapt this into a streaming class that supports add(value) and reports the current kth largest after at least k observations.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.


---

# 18. Greedy choices need an exchange argument

[Previous lesson](lessons/17-heaps-and-keeping-only-the-best-candidates.md) · [Next lesson](lessons/19-backtracking-choose-explore-undo.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Greedy algorithms commit to a locally favorable choice without revisiting it. This requires proof, not intuition. For maximizing the count of nonoverlapping meetings with equal value, choosing the earliest finishing available meeting leaves at least as much room as any alternative first choice. That argument fails when meetings carry different rewards.

## Walk through an example

For meetings (0,4), (1,2), (2,3), (3,5), sort by finish and choose (1,2), then (2,3), then (3,5). Choosing the earliest starting meeting (0,4) would leave room for fewer meetings.

## Your exercise

Implement max_meetings(intervals). Return a maximum-size compatible subset of positive-duration half-open intervals [start, end). Touching endpoints do not overlap. Equal-value meetings, arbitrary input order, and negative times are allowed. Invalid duration raises ValueError.

Start in [the exercise file](exercises/18-greedy-choices-need-an-exchange-argument.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Sort by end time and accept a meeting when its start is at least the last accepted end.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def max_meetings(intervals):
    """Half-open [start, end); all intervals must have start < end."""
    if any(start >= end for start, end in intervals):
        raise ValueError('each meeting needs positive duration')
    selected, last_end = [], None
    for start, end in sorted(intervals, key=lambda interval: interval[1]):
        if last_end is None or start >= last_end:
            selected.append((start, end))
            last_end = end
    return selected
```

### Why it works

Take an optimal solution’s first meeting. Replace it with the earliest finishing meeting; the replacement cannot overlap any later meeting that the original first meeting allowed. Repeat this exchange on the remaining compatible suffix.

### Time and space

O(n log n) time and O(n) additional space for sorting and output. Input is not mutated.

</details>

## A mistake to watch for

Sorting by start time or shortest duration lacks this guarantee. If meetings have different values, maximizing their count is a different objective from maximizing reward.

## Retrieval check

Close the solution and answer: **Are (1, 3) and (3, 4) compatible here?**

<details><summary>Check your answer</summary>

Yes. Half-open intervals do not include their ending point.

</details>

## Optional extension

Give a counterexample to the rule “always take the shortest available meeting.”

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.


---

# 19. Backtracking: choose, explore, undo

[Previous lesson](lessons/18-greedy-choices-need-an-exchange-argument.md) · [Next lesson](lessons/20-dynamic-programming-on-one-dimension.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Backtracking explores a tree of partial decisions. A path holds the current candidate; a recursive call explores its extensions; undo restores the exact prior state. Generate combinations in increasing input-index order so the same selection is not produced in multiple orders. Pruning skips branches that cannot fill the remaining slots.

## Walk through an example

From [a, b, c] choose 2. Start with a, extend with b and then c, producing [a,b] and [a,c]. Undo a, start b, extend c, producing [b,c]. Never start the second choice before the first choice’s index.

## Your exercise

Implement choose_tags(tags, k). Input tags are distinct. Return all size-k selections as lists, preserving input order inside each selection. Any output order is valid. k = 0 returns [[]]; k outside 0..n returns [].

Start in [the exercise file](exercises/19-backtracking-choose-explore-undo.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Pass the next allowed start index. Append path.copy() at a complete selection, not the mutable path itself.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def choose_tags(tags, k):
    """Unique input tags; retain input order within each size-k selection."""
    if not 0 <= k <= len(tags):
        return []
    answer, path = [], []
    def search(start):
        if len(path) == k:
            answer.append(path.copy())
            return
        needed = k - len(path)
        for index in range(start, len(tags) - needed + 1):
            path.append(tags[index])
            search(index + 1)
            path.pop()
    search(0)
    return answer
```

### Why it works

Each selection has one unique increasing index sequence. The recursion follows exactly those sequences and cannot repeat them. Pruning only skips a suffix with fewer available items than remaining slots.

### Time and space

For valid k, O((k + 1) × C(n,k)) time and output space; O(k) recursion/path space excluding output. Enumeration cannot be polynomial for all k because output itself can be exponential.

</details>

## A mistake to watch for

Appending path without copying makes saved results change during undo. Forgetting to pop contaminates sibling branches.

## Retrieval check

Close the solution and answer: **Why does k = 0 have one selection rather than zero?**

<details><summary>Check your answer</summary>

There is exactly one way to select nothing: the empty selection.

</details>

## Optional extension

Support repeated input tags while returning unique selections; explain where duplicate branches are skipped.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.


---

# 20. Dynamic programming on one dimension

[Previous lesson](lessons/19-backtracking-choose-explore-undo.md) · [Next lesson](lessons/21-grid-dp-and-careful-memory-reuse.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Dynamic programming stores answers to overlapping subproblems. Define the state in a full sentence before choosing a recurrence. Here dp[s] is the minimum number of reusable tokens needed to make exact subtotal s. The last token has some denomination c, leaving subtotal s − c. Build states in increasing subtotal order so each dependency is already solved.

## Walk through an example

For denominations [1, 3, 4] and amount 6, greedy largest-first takes 4 + 1 + 1. DP considers the last token and finds 3 + 3 using two tokens. dp[0] is 0; an unreachable subtotal carries a sentinel larger than any possible valid count.

## Your exercise

Implement min_tokens(denominations, amount). Use unlimited copies of positive integer denominations to form a nonnegative integer amount exactly. Return the fewest tokens, or -1 if impossible. Empty denominations can form only zero. Invalid signs raise ValueError.

Start in [the exercise file](exercises/20-dynamic-programming-on-one-dimension.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

For each subtotal, try each denomination that fits and minimize dp[subtotal − coin] + 1.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def min_tokens(denominations, amount):
    if amount < 0 or any(coin <= 0 for coin in denominations):
        raise ValueError('amount must be nonnegative and tokens positive')
    dp = [0] + [amount + 1] * amount
    for subtotal in range(1, amount + 1):
        for coin in denominations:
            if coin <= subtotal:
                dp[subtotal] = min(dp[subtotal], dp[subtotal - coin] + 1)
    return dp[amount] if dp[amount] <= amount else -1
```

### Why it works

Any solution for subtotal s ends in some allowed token c. Removing it leaves an optimal smaller problem; using a nonoptimal remainder could only increase the count. Trying every final token includes an optimal solution.

### Time and space

O(A × d) time and O(A) auxiliary space, where A is the numeric amount and d is the number of denominations. This is pseudopolynomial in A, not polynomial in the bit length of A.

</details>

## A mistake to watch for

dp[0] must be zero. A greedy approach fails for arbitrary denominations. Coin values of zero or less invalidate the recurrence.

## Retrieval check

Close the solution and answer: **What is min_tokens([4, 6], 5)?**

<details><summary>Check your answer</summary>

-1: no exact combination exists.

</details>

## Optional extension

Store the last chosen denomination for each subtotal and reconstruct one optimal token list.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.


---

# 21. Grid DP and careful memory reuse

[Previous lesson](lessons/20-dynamic-programming-on-one-dimension.md) · [Next lesson](lessons/22-tries-organize-information-by-shared-prefixes.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Two-dimensional DP often represents progress along two coordinates. For right/down grid movement, each cell can be reached only from above or from the left. A full table makes this clear. A one-row optimization reuses memory: before updating column c, dp[c] means “from above,” while dp[c − 1] already means “from the left in this row.” Update direction therefore carries meaning.

## Walk through an example

For [[2, 9, 1], [1, 3, 2]], the first row’s totals are [2, 11, 12]. The next row becomes [3, 6, 8]. The cheapest path costs 8, including both start and destination.

## Your exercise

Implement minimum_grid_cost(grid). Grid is a nonempty rectangular matrix of integers, which may be negative. Start top-left and move only right or down to bottom-right. Include every visited cell’s cost. Empty or ragged input raises ValueError.

Start in [the exercise file](exercises/21-grid-dp-and-careful-memory-reuse.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Initialize dp[0] = 0 and other entries to infinity. At each cell add its cost to min(above, left).

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def minimum_grid_cost(grid):
    """Nonempty rectangular integer grid; move right/down, include endpoints."""
    if not grid or not grid[0] or any(len(row) != len(grid[0]) for row in grid):
        raise ValueError('grid must be nonempty and rectangular')
    cols = len(grid[0])
    dp = [float('inf')] * cols
    dp[0] = 0
    for row in grid:
        for col, cost in enumerate(row):
            dp[col] = cost + min(dp[col], dp[col - 1] if col else float('inf'))
    return dp[-1]
```

### Why it works

Every route into a cell has a final move from above or left. Minimizing over those optimal prefixes gives the best route to that cell. Row-major order solves both dependencies before their values are needed.

### Time and space

O(rows × columns) time and O(columns) auxiliary space.

</details>

## A mistake to watch for

Negative cells are safe here because the movement graph has no cycles. A negative-weight general graph would require different reasoning. One-row costs alone do not retain a reconstructable path.

## Retrieval check

Close the solution and answer: **Why can updating columns right-to-left break this implementation?**

<details><summary>Check your answer</summary>

The left neighbor would still contain the previous row’s value rather than the current row’s solved cost.

</details>

## Optional extension

Build the full table and a predecessor table to return both minimum cost and a path.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.


---

# 22. Tries: organize information by shared prefixes

[Previous lesson](lessons/21-grid-dp-and-careful-memory-reuse.md) · [Next lesson](lessons/23-disjoint-sets-for-growing-connectivity.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A trie is a tree whose edges represent successive symbols. Words sharing a prefix share a traversal path. Hash maps answer exact-key questions; a trie makes prefix navigation explicit. Store a count at each node to answer how many inserted entries share that prefix without traversing the whole subtree. Dictionary child maps avoid allocating an entire alphabet at every node.

## Walk through an example

Insert "map", "math", and "map" again. The path m → a has count 3, while m → a → p has count 2. Query "mat" returns 1. Query "z" returns 0. The empty prefix matches all three inserted entries.

## Your exercise

Implement PrefixIndex with add(word) and count_prefix(prefix). Inputs are Python strings. Count duplicate inserts separately. Empty words are valid, and querying the empty prefix returns the total number of inserted entries.

Start in [the exercise file](exercises/22-tries-organize-information-by-shared-prefixes.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

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


---

# 23. Disjoint sets for growing connectivity

[Previous lesson](lessons/22-tries-organize-information-by-shared-prefixes.md) · [Next lesson](lessons/24-weighted-routes-and-dijkstra-s-frontier.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Disjoint-set union tracks which group each vertex belongs to while connections are added. Each group has a representative root. Union joins roots, rather than arbitrary nodes. Union by size attaches the smaller tree under the larger one; path compression shortens later finds. This structure answers connectivity efficiently but does not retain actual graph paths.

## Walk through an example

Start with four groups {0}, {1}, {2}, {3}. union(0,1) leaves three groups. union(2,3) leaves two. union(1,2) leaves one. union(0,3) returns False because those vertices already share a representative.

## Your exercise

Implement DisjointSets(n) with find(node), union(a,b), and groups. Vertices are valid IDs 0..n−1. union returns True only when it merges two distinct groups. Start with groups = n.

Start in [the exercise file](exercises/23-disjoint-sets-for-growing-connectivity.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

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


---

# 24. Weighted routes and Dijkstra’s frontier

[Previous lesson](lessons/23-disjoint-sets-for-growing-connectivity.md) · [Next lesson](lessons/25-bits-and-representation-contracts.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

When edges have unequal nonnegative costs, FIFO order no longer settles the cheapest route. Dijkstra’s algorithm expands the smallest tentative distance using a priority queue. Relaxation asks whether a route through the current vertex improves a neighbor. A simple heap implementation inserts improved entries without deleting old ones; discard stale entries when popped.

## Walk through an example

Edges 0 → 1 cost 8, 0 → 2 cost 2, and 2 → 1 cost 1 first propose distance 8 for vertex 1. Expanding vertex 2 improves it to 3. Later the heap entry (8,1) is stale and ignored.

## Your exercise

Implement shortest_costs(n, edges, source). Directed edges are (a,b,cost), endpoints and source are valid, n >= 1, and costs are nonnegative finite integers. Return distances from source, using float("inf") for unreachable vertices. Reject negative edge costs.

Start in [the exercise file](exercises/24-weighted-routes-and-dijkstra-s-frontier.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

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


---

# 25. Bits and representation contracts

[Previous lesson](lessons/24-weighted-routes-and-dijkstra-s-frontier.md) · [Next lesson](lessons/26-a-complete-interview-clarify-derive-test.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Bitwise operators work on binary representations. XOR places a 1 where two bits differ. The expression x & (x − 1) removes the lowest set bit of a positive integer: subtracting one flips that bit to zero and lower zeros to ones, and AND removes the newly set lower bits. Python integers have arbitrary precision; fixed-width assumptions need to be stated explicitly.

## Walk through an example

For a = 10 (1010) and b = 3 (0011), XOR is 1001. Clearing its lowest set bit produces 1000; clearing again produces 0000. Two bit positions differ.

## Your exercise

Implement differing_bits(a,b) for nonnegative Python integers. Return the number of differing binary positions, treating absent leading positions as zero. Negative inputs raise ValueError. Do not assume a 32-bit machine word.

Start in [the exercise file](exercises/25-bits-and-representation-contracts.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

Compute XOR, then count how often you can clear its lowest set bit before reaching zero.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def differing_bits(a, b):
    if a < 0 or b < 0:
        raise ValueError('use nonnegative integers')
    difference, count = a ^ b, 0
    while difference:
        difference &= difference - 1
        count += 1
    return count
```

### Why it works

XOR selects precisely the differing positions. Each clearing iteration removes exactly one selected position and leaves all others unchanged. The number of iterations equals the desired count.

### Time and space

There are k iterations for k differing bits. With B-bit arbitrary-precision Python integers, a conservative bit-work bound is O((k + 1)B), with O(B) temporary bit storage. Fixed-width O(k) reasoning is a different model.

</details>

## A mistake to watch for

Python negative integers behave like an unbounded signed representation for bitwise operations. The positive-integer clearing loop can fail to terminate on a negative value.

## Retrieval check

Close the solution and answer: **What is the answer when a equals b?**

<details><summary>Check your answer</summary>

Zero, because their XOR is zero and the loop runs zero times.

</details>

## Optional extension

Define an explicit width w, mask both values to w bits, and explain how that changes negative-input semantics.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.


---

# 26. A complete interview: clarify, derive, test

[Previous lesson](lessons/25-bits-and-representation-contracts.md) · [Mock interview rubric](ASSESSMENT.md) · [Full course](README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A coding interview evaluates more than recall. Clarify inputs and outputs, give a simple correct baseline, identify the expensive repeated work, state an invariant, implement, and test boundaries aloud. If stuck, name the assumption you cannot yet justify. A useful explanation connects each pointer or stored value to a concrete question about the input.

## Walk through an example

For sorted timestamps [1, 2, 4, 7, 7] and duration 3, [1,4) contains 1 and 2 but excludes 4. The span [7,10) contains both 7s. The maximum is 2. A single left pointer removes timestamps too far from the new rightmost event.

## Your exercise

Mock interview: implement busiest_span(timestamps,duration). Input is a sorted nondecreasing list of numeric event times. Return the maximum event count in any half-open interval [start,start+duration). Duplicate times are separate events. Duration must be positive; reject otherwise. Empty input returns 0.

Start in [the exercise file](exercises/26-a-complete-interview-clarify-derive-test.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

After adding the right event, discard left events while right_time − left_time >= duration. A surviving window has spread strictly less than duration.

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
from collections import Counter, deque
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Optional

def busiest_span(timestamps, duration):
    """Sorted timestamps; maximum events in any half-open span of duration."""
    if duration <= 0:
        raise ValueError('duration must be positive')
    left = best = 0
    for right, timestamp in enumerate(timestamps):
        while timestamp - timestamps[left] >= duration:
            left += 1
        best = max(best, right - left + 1)
    return best
```

### Why it works

Every valid set of contiguous events has spread less than duration and can be covered by a half-open interval starting at its first event. Shrinking removes exactly the left endpoints whose spread is too large for the current right endpoint. Taking the maximum over all right endpoints covers an optimal set.

### Time and space

O(n) time and O(1) auxiliary space for already sorted input. For unsorted input, discuss sorting and the resulting O(n log n) cost first.

</details>

## A mistake to watch for

Using > instead of >= includes an event at the excluded right boundary. Describe the half-open contract before coding rather than patching tests afterward.

## Retrieval check

Close the solution and answer: **What does [5, 5, 5] with duration 1 return?**

<details><summary>Check your answer</summary>

3. All three distinct events fit in [5,6).

</details>

## Optional extension

Do a second mock: timestamps arrive unsorted in batches. Discuss whether to sort, merge sorted batches, or use an online data structure before implementing anything.

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
