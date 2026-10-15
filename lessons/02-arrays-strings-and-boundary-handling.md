# 02. Arrays, strings, and boundary handling

[Previous lesson](01-reason-about-work-before-writing-code.md) · [Next lesson](03-hash-maps-remember-what-a-scan-cannot.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Arrays give direct access by index; contiguous scans are often enough. Python lists can grow, but inserting near the beginning shifts later entries. Strings are immutable, so build pieces and join them when constructing large text. A run is a maximal adjacent block of equal items. Keeping one active run separates the current unfinished result from results already committed.

## Walk through an example

For "aaabbc", start with (a, 1), extend to (a, 3), then commit it when b arrives. Commit (b, 2) when c arrives. The loop ends with c still active, so append (c, 1) after the loop.

## Your exercise

Implement compress_runs(text), returning a list of (character, count) tuples for consecutive runs. Empty text returns []. Spaces and punctuation count as characters; preserve case.

Start in [the exercise file](../exercises/02-arrays-strings-and-boundary-handling.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

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
