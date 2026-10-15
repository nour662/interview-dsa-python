# 25. Bits and representation contracts

[Previous lesson](24-weighted-routes-and-dijkstra-s-frontier.md) · [Next lesson](26-a-complete-interview-clarify-derive-test.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Bitwise operators work on binary representations. XOR places a 1 where two bits differ. The expression x & (x − 1) removes the lowest set bit of a positive integer: subtracting one flips that bit to zero and lower zeros to ones, and AND removes the newly set lower bits. Python integers have arbitrary precision; fixed-width assumptions need to be stated explicitly.

## Walk through an example

For a = 10 (1010) and b = 3 (0011), XOR is 1001. Clearing its lowest set bit produces 1000; clearing again produces 0000. Two bit positions differ.

## Your exercise

Implement differing_bits(a,b) for nonnegative Python integers. Return the number of differing binary positions, treating absent leading positions as zero. Negative inputs raise ValueError. Do not assume a 32-bit machine word.

Start in [the exercise file](../exercises/25-bits-and-representation-contracts.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

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
