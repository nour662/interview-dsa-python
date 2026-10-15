# 20. Dynamic programming on one dimension

[Previous lesson](19-backtracking-choose-explore-undo.md) · [Next lesson](21-grid-dp-and-careful-memory-reuse.md) · [Full course](../README.md)

**Prerequisite:** The earlier lessons in this course; review unfamiliar prerequisites before continuing.
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

Dynamic programming stores answers to overlapping subproblems. Define the state in a full sentence before choosing a recurrence. Here dp[s] is the minimum number of reusable tokens needed to make exact subtotal s. The last token has some denomination c, leaving subtotal s − c. Build states in increasing subtotal order so each dependency is already solved.

## Walk through an example

For denominations [1, 3, 4] and amount 6, greedy largest-first takes 4 + 1 + 1. DP considers the last token and finds 3 + 3 using two tokens. dp[0] is 0; an unreachable subtotal carries a sentinel larger than any possible valid count.

## Your exercise

Implement min_tokens(denominations, amount). Use unlimited copies of positive integer denominations to form a nonnegative integer amount exactly. Return the fewest tokens, or -1 if impossible. Empty denominations can form only zero. Invalid signs raise ValueError.

Start in [the exercise file](../exercises/20-dynamic-programming-on-one-dimension.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

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
