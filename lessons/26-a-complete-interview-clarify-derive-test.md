# 26. A complete interview: clarify, derive, test

[Previous lesson](25-bits-and-representation-contracts.md) · [Mock interview rubric](../ASSESSMENT.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

A coding interview evaluates more than recall. Clarify inputs and outputs, give a simple correct baseline, identify the expensive repeated work, state an invariant, implement, and test boundaries aloud. If stuck, name the assumption you cannot yet justify. A useful explanation connects each pointer or stored value to a concrete question about the input.

## Walk through an example

For sorted timestamps [1, 2, 4, 7, 7] and duration 3, [1,4) contains 1 and 2 but excludes 4. The span [7,10) contains both 7s. The maximum is 2. A single left pointer removes timestamps too far from the new rightmost event.

## Your exercise

Mock interview: implement busiest_span(timestamps,duration). Input is a sorted nondecreasing list of numeric event times. Return the maximum event count in any half-open interval [start,start+duration). Duplicate times are separate events. Duration must be positive; reject otherwise. Empty input returns 0.

Start in [the exercise file](../exercises/26-a-complete-interview-clarify-derive-test.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

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
