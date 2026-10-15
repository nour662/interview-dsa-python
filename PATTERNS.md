# Choose a pattern from the constraint

A keyword is a clue, not a proof. First write the output contract, input size, ordering, and mutation rules. State a simple baseline and identify its repeated work. Use this table to propose an approach, then check its assumptions.

| What the problem needs | Candidate | Assumption to check | Lesson |
| --- | --- | --- | --- |
| Counts or earlier matching items | Hash map | Keys are hashable; expected lookup cost is acceptable | [03](lessons/03-hash-maps-remember-what-a-scan-cannot.md) |
| A pair in ordered data | Two pointers | Moving one boundary safely eliminates candidates | [04](lessons/04-two-pointers-and-monotone-movement.md) |
| A longest contiguous valid segment | Sliding window | Validity can be restored monotonically by shrinking | [05](lessons/05-sliding-windows-and-reversible-state.md) |
| Range totals with signed values | Prefix sums and a map | Query earlier boundaries; decide counts vs earliest index | [06](lessons/06-prefix-sums-for-signed-ranges.md) |
| Next greater/smaller item | Monotonic stack | Decide strictly vs non-strictly greater | [07](lessons/07-stacks-and-unresolved-candidates.md) |
| Shortest route with equal edge costs | BFS | Every move has equal cost | [08](lessons/08-queues-and-shortest-routes-without-weights.md) |
| First qualifying boundary | Binary search | Qualification is monotone or data is sorted | [10](lessons/10-binary-search-with-explicit-boundaries.md) |
| Combine children into a subtree fact | Postorder DFS | Tree structure is acyclic; state returned to parent is clear | [12](lessons/12-tree-dfs-return-one-fact-update-another.md) |
| Prerequisites and ordering | Topological sort | Edges are directed; detect cycles | [16](lessons/16-directed-dependencies-and-topological-order.md) |
| Keep a small set of best candidates | Heap | A priority boundary suffices; full ordering is unnecessary | [17](lessons/17-heaps-and-keeping-only-the-best-candidates.md) |
| Commit to a local choice | Greedy | An exchange argument justifies it | [18](lessons/18-greedy-choices-need-an-exchange-argument.md) |
| Enumerate valid selections | Backtracking | Output size may itself be exponential | [19](lessons/19-backtracking-choose-explore-undo.md) |
| Optimize overlapping smaller problems | DP | Define state, recurrence, base cases, and dependency order | [20](lessons/20-dynamic-programming-on-one-dimension.md) |
| Prefix queries across many words | Trie | Prefix sharing justifies memory overhead | [22](lessons/22-tries-organize-information-by-shared-prefixes.md) |
| Connectivity as edges are added | Disjoint-set union | Arbitrary deletion and route reconstruction are not required | [23](lessons/23-disjoint-sets-for-growing-connectivity.md) |
| Cheapest route with nonnegative weights | Dijkstra | Negative edges are absent | [24](lessons/24-weighted-routes-and-dijkstra-s-frontier.md) |

## Three traps to recognize

**“It asks for a subarray, so use a window.”** Signed values can make removing a left value increase the total. Prove the monotonic rule; otherwise consider prefix information or another approach.

**“Take the largest denomination first.”** With denominations 1, 3, and 4, amount 6 uses two 3s, better than 4 + 1 + 1. A local rule needs a proof for the actual constraints.

**“BFS finds the shortest path.”** It finds the fewest edges, which is the cheapest route only when edge costs are equal. Different costs require a different frontier rule.

## A reusable explanation

“I am keeping **this state** because it answers **this future question**. Before each iteration, **this invariant** holds. This update preserves it because **this reason**. Each item can trigger **this many operations**, so time is **this bound** and extra space is **this bound**.”

If you cannot fill those blanks, revisit the proof before memorizing another template.
