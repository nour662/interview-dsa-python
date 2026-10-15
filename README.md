# Interview DSA in Python

An original, independent interview-preparation course: **26 lessons, 26 exercises, Python reference implementations, correctness arguments, worked traces, and automated checks.** Start with basic Python; work toward explaining and solving unfamiliar interview problems.

This project is not affiliated with or endorsed by LeetCode. It teaches common computer-science topics in an independently chosen sequence. It does not reproduce LeetCode’s paid lessons, quizzes, problem text, videos, or editorial solutions, and it does not claim to be an exact replacement for that course. LeetCode is a trademark of its respective owner.

## Start here

1. Open [Lesson 01](lessons/01-reason-about-work-before-writing-code.md).
2. Read the idea and trace, then attempt the linked starter before opening hints.
3. Explain the invariant, test boundaries, and compare your implementation with the reference.
4. Return later and rebuild the idea without the page open.

Read the [complete guide](COURSE.md), [pattern decision guide](PATTERNS.md), [study pacing](STUDY_PLAN.md), and [mock interview assessment](ASSESSMENT.md). `index.html` is an offline searchable lesson directory: download the repository and open it locally; it links to Markdown files and is not a rendered lesson app. GitHub renders the lessons directly.

## Run the reference checks

Python 3.9+ and its standard library are sufficient. No packages or API keys are required.

```sh
python -m unittest discover -s tests -v
python check_content.py
```

These tests check the supplied **reference implementations**, including exhaustive small-input comparisons for several patterns. They do not prove every possible input correct. The lessons include the correctness reasoning and input contracts.

To test your own attempt, edit a starter in `exercises/` and select its lesson number:

```sh
python grade_exercise.py 01
```

The grader substitutes your implementation for that lesson’s reference in the same test suite. It selects that lesson’s relevant tests, including associated exhaustive comparisons where supplied. An untouched starter should fail with `NotImplementedError`. Tests are a feedback tool; add a boundary case of your own.

## Ordered lessons

| # | Lesson | Exercise entry point |
| --- | --- | --- |
| 01 | [Reason about work before writing code](lessons/01-reason-about-work-before-writing-code.md) | [`count_equal_pairs`](exercises/01-reason-about-work-before-writing-code.py) |
| 02 | [Arrays, strings, and boundary handling](lessons/02-arrays-strings-and-boundary-handling.md) | [`compress_runs`](exercises/02-arrays-strings-and-boundary-handling.py) |
| 03 | [Hash maps: remember what a scan cannot](lessons/03-hash-maps-remember-what-a-scan-cannot.md) | [`earliest_unique`](exercises/03-hash-maps-remember-what-a-scan-cannot.py) |
| 04 | [Two pointers and monotone movement](lessons/04-two-pointers-and-monotone-movement.md) | [`closest_pair`](exercises/04-two-pointers-and-monotone-movement.py) |
| 05 | [Sliding windows and reversible state](lessons/05-sliding-windows-and-reversible-state.md) | [`longest_budget_window`](exercises/05-sliding-windows-and-reversible-state.py) |
| 06 | [Prefix sums for signed ranges](lessons/06-prefix-sums-for-signed-ranges.md) | [`count_target_ranges`](exercises/06-prefix-sums-for-signed-ranges.py) |
| 07 | [Stacks and unresolved candidates](lessons/07-stacks-and-unresolved-candidates.md) | [`next_warmer_wait`](exercises/07-stacks-and-unresolved-candidates.py) |
| 08 | [Queues and shortest routes without weights](lessons/08-queues-and-shortest-routes-without-weights.md) | [`nearest_exit_steps`](exercises/08-queues-and-shortest-routes-without-weights.py) |
| 09 | [Linked lists and safe pointer changes](lessons/09-linked-lists-and-safe-pointer-changes.md) | [`reverse_chain`](exercises/09-linked-lists-and-safe-pointer-changes.py) |
| 10 | [Binary search with explicit boundaries](lessons/10-binary-search-with-explicit-boundaries.md) | [`lower_bound`](exercises/10-binary-search-with-explicit-boundaries.py) |
| 11 | [Recursion as a contract for smaller work](lessons/11-recursion-as-a-contract-for-smaller-work.md) | [`nested_total`](exercises/11-recursion-as-a-contract-for-smaller-work.py) |
| 12 | [Tree DFS: return one fact, update another](lessons/12-tree-dfs-return-one-fact-update-another.md) | [`tree_diameter`](exercises/12-tree-dfs-return-one-fact-update-another.py) |
| 13 | [Tree BFS and level boundaries](lessons/13-tree-bfs-and-level-boundaries.md) | [`level_means`](exercises/13-tree-bfs-and-level-boundaries.py) |
| 14 | [Binary search trees and inherited constraints](lessons/14-binary-search-trees-and-inherited-constraints.md) | [`valid_bst`](exercises/14-binary-search-trees-and-inherited-constraints.py) |
| 15 | [Graphs: components and visited state](lessons/15-graphs-components-and-visited-state.md) | [`component_count`](exercises/15-graphs-components-and-visited-state.py) |
| 16 | [Directed dependencies and topological order](lessons/16-directed-dependencies-and-topological-order.md) | [`dependency_order`](exercises/16-directed-dependencies-and-topological-order.py) |
| 17 | [Heaps and keeping only the best candidates](lessons/17-heaps-and-keeping-only-the-best-candidates.md) | [`kth_largest`](exercises/17-heaps-and-keeping-only-the-best-candidates.py) |
| 18 | [Greedy choices need an exchange argument](lessons/18-greedy-choices-need-an-exchange-argument.md) | [`max_meetings`](exercises/18-greedy-choices-need-an-exchange-argument.py) |
| 19 | [Backtracking: choose, explore, undo](lessons/19-backtracking-choose-explore-undo.md) | [`choose_tags`](exercises/19-backtracking-choose-explore-undo.py) |
| 20 | [Dynamic programming on one dimension](lessons/20-dynamic-programming-on-one-dimension.md) | [`min_tokens`](exercises/20-dynamic-programming-on-one-dimension.py) |
| 21 | [Grid DP and careful memory reuse](lessons/21-grid-dp-and-careful-memory-reuse.md) | [`minimum_grid_cost`](exercises/21-grid-dp-and-careful-memory-reuse.py) |
| 22 | [Tries: organize information by shared prefixes](lessons/22-tries-organize-information-by-shared-prefixes.md) | [`PrefixIndex`](exercises/22-tries-organize-information-by-shared-prefixes.py) |
| 23 | [Disjoint sets for growing connectivity](lessons/23-disjoint-sets-for-growing-connectivity.md) | [`DisjointSets`](exercises/23-disjoint-sets-for-growing-connectivity.py) |
| 24 | [Weighted routes and Dijkstra’s frontier](lessons/24-weighted-routes-and-dijkstra-s-frontier.md) | [`shortest_costs`](exercises/24-weighted-routes-and-dijkstra-s-frontier.py) |
| 25 | [Bits and representation contracts](lessons/25-bits-and-representation-contracts.md) | [`differing_bits`](exercises/25-bits-and-representation-contracts.py) |
| 26 | [A complete interview: clarify, derive, test](lessons/26-a-complete-interview-clarify-derive-test.md) | [`busiest_span`](exercises/26-a-complete-interview-clarify-derive-test.py) |

## Scope and honest limitations

This is a compact written course, not a video course, grading service, or hiring guarantee. It covers major interview patterns; it is not an exhaustive algorithms textbook. Segment trees, advanced string algorithms, balanced-tree implementation, and advanced DP optimizations are outside this edition. The examples assume the documented input contracts; arbitrary malformed input is not fully validated. Recursive implementations suit instructional-size inputs and may hit Python’s recursion limit on deep structures.

The course has its own exercises rather than a copied question bank. After learning a pattern, use your preferred practice platform to attempt an unfamiliar problem and explain why the pattern fits. Additional problem difficulty should follow understanding, not a daily streak.

## Maintain and contribute

Lesson content lives in `build_course.py`; implementations in `solutions/core.py`. Rebuild with `python build_course.py`, run both checks, and include a counterexample when fixing an algorithm. Never commit credentials or private progress records.

## License

MIT for this repository’s original text and code; see [LICENSE](LICENSE).
