"""Rebuild the original lessons, exercise starters, index, and combined guide."""
import ast
import csv
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Every explanation, exercise, and example here is newly authored for this project.
LESSONS = [
dict(title='Reason about work before writing code', symbol='count_equal_pairs',
concept='An algorithm is a sequence of decisions with a cost. Count how many times an operation can happen as the input grows. A loop nested inside another loop is not automatically quadratic: the question is whether their work multiplies. Big O describes growth rather than a stopwatch result. For Python dictionaries, use expected constant-time lookup under ordinary hashing assumptions; it is not a worst-case guarantee.',
trace='For values [4, 7, 4, 4], the three 4s form three pairs. Scanning left to right, their contributions are 0, 1, and 2. The 7 contributes 0. A frequency table replaces repeatedly scanning earlier items.',
exercise='Implement count_equal_pairs(values). Return the number of index pairs i < j whose values are equal. Values are hashable. Empty input returns 0; do not mutate the input.',
hint='Before recording the current value, ask how many matching values have already appeared.',
proof='Before each iteration, counts describes exactly the processed prefix and pairs counts every matching pair entirely inside it. Adding counts[value] introduces exactly the pairs ending at the new position. No pair is missed or counted twice.',
cost='Expected O(n) time and O(u) auxiliary space, where u is the number of distinct values. A direct comparison of all pairs costs O(n²) time and O(1) extra space.',
pitfall='Incrementing the frequency before adding its contribution counts each element as a pair with itself. Test [9] and [9, 9] to expose that error.',
quiz='If every value is equal, what is the result for n elements?', answer='n(n − 1) / 2. The output grows quadratically even though the counting algorithm is expected linear time.',
stretch='Write the quadratic version and compare results for every length-5 list over values 0, 1, and 2.'),
dict(title='Arrays, strings, and boundary handling', symbol='compress_runs',
concept='Arrays give direct access by index; contiguous scans are often enough. Python lists can grow, but inserting near the beginning shifts later entries. Strings are immutable, so build pieces and join them when constructing large text. A run is a maximal adjacent block of equal items. Keeping one active run separates the current unfinished result from results already committed.',
trace='For "aaabbc", start with (a, 1), extend to (a, 3), then commit it when b arrives. Commit (b, 2) when c arrives. The loop ends with c still active, so append (c, 1) after the loop.',
exercise='Implement compress_runs(text), returning a list of (character, count) tuples for consecutive runs. Empty text returns []. Spaces and punctuation count as characters; preserve case.',
hint='Handle empty input before reading text[0]. Store the current character and run length.',
proof='Before each new character, result contains every completed run and current/count describes the one unfinished run. A changed character closes exactly that run. The final append closes the only run not ended by a change.',
cost='O(n) time. O(r) output space for r runs. This implementation also uses O(n) temporary space for text[1:]; iterate by index instead to avoid that slice.',
pitfall='Forgetting the final run makes a one-character input return an empty answer. Combining equal letters that are separated by other letters changes the problem into frequency counting.',
quiz='What should "ab a" produce?', answer="[('a', 1), ('b', 1), (' ', 1), ('a', 1)]. The two a runs are separate.",
stretch='Replace the slice with an index loop and explain the effect on auxiliary space.'),
dict(title='Hash maps: remember what a scan cannot', symbol='earliest_unique',
concept='A hash map associates keys with information. A set remembers presence; a map can remember counts, positions, or accumulated results. The stored value must answer the future question. If the question asks whether something occurs exactly once in the entire input, a first encounter cannot settle it: a duplicate might appear later. Separate global counting from ordered selection.',
trace='For [8, 3, 8, 5, 3], the count map is {8: 2, 3: 2, 5: 1}. A second scan in original order first finds count 1 at index 3. Map order is irrelevant because the input scan determines the answer.',
exercise='Implement earliest_unique(values). Return the earliest index whose value occurs exactly once, or -1 if none exists. Values are hashable. Preserve the input.',
hint='Use one pass to count and a second pass to select. Returning from the first pass is premature.',
proof='After counting, each map entry is the exact frequency of its key. Scanning indices in increasing order means the first frequency-one item has no earlier qualifying item.',
cost='Expected O(n) time and O(u) auxiliary space. A count map may store up to n distinct keys.',
pitfall='Do not return the value when the contract asks for an index. Empty input and input containing only repeated values must return -1.',
quiz='Can a set alone distinguish one occurrence from three?', answer='No. Both produce one membership entry. You need counts or another structure that records repeated membership.',
stretch='Return all unique-value indices while preserving input order. What extra space is output space?'),
dict(title='Two pointers and monotone movement', symbol='closest_pair',
concept='Two pointers work when moving a boundary eliminates candidates safely. Sorted input provides an ordering argument. If the sum of the two endpoints is below the target, pairing the left endpoint with any smaller right endpoint cannot improve that below-target sum. After evaluating the current pair, move the left endpoint. Symmetrically, an excessive sum allows moving the right endpoint. Track the best pair before discarding a boundary.',
trace='With [1, 4, 6, 10] and target 12: (1, 10) gives 11, then (4, 10) gives 14, then (4, 6) gives 10. The best difference is 1, so return (1, 10). An exact match can stop immediately.',
exercise='Implement closest_pair(sorted_values, target). Return values at two distinct positions whose sum is closest to target. The input is sorted in nondecreasing order. Any optimal tie is valid; fewer than two values returns None.',
hint='Start at both ends. Record the closest pair seen before advancing one pointer.',
proof='When the sum is below target, all other pairs using the left endpoint and a smaller right endpoint are no closer than the current pair. The symmetric statement holds above target. Each discarded boundary therefore cannot hide a better unexplored pair.',
cost='O(n) time and O(1) auxiliary space. Sorting arbitrary input first would add O(n log n) time and may change the mutation contract.',
pitfall='Using left <= right permits reusing one position. Negative values are allowed, but unsorted input breaks the elimination proof.',
quiz='Why is this approach unsafe for unsorted input?', answer='Moving right or left no longer predicts how the sum changes, so it can discard the optimal pair.',
stretch='Return indices instead of values and define a deterministic tie-breaking rule.'),
dict(title='Sliding windows and reversible state', symbol='longest_budget_window',
concept='A sliding window represents a contiguous segment. Add the new right item, then remove left items until the segment satisfies a rule. This needs a property that lets boundary movement repair validity. With nonnegative costs, extending cannot decrease a sum and removing cannot increase it. Although a while loop sits inside a for loop, each element enters and leaves at most once.',
trace='For costs [2, 1, 3, 1] and budget 4, window [2, 1] has length 2. Adding 3 forces removal of 2 and leaves [1, 3]. Adding 1 removes the earlier 1 and leaves [3, 1]. The longest valid length is 2.',
exercise='Implement longest_budget_window(costs, budget). Return the longest contiguous segment length with sum at most budget. Costs and budget are nonnegative numbers; reject negative values with ValueError. Empty input returns 0.',
hint='Maintain left, total, and best. Update best only after restoring validity.',
proof='After shrinking, the window is valid. Every removed left endpoint made a sum too large and cannot become useful by extending the right edge with more nonnegative costs. Across the scan, both pointers move only forward.',
cost='O(n) time including validation and O(1) auxiliary space.',
pitfall='Negative costs destroy the monotonicity argument. For signed values, do not reuse this template without a new proof. Zero-cost entries must still contribute to window length.',
quiz='Why does the inner loop not imply O(n²) here?', answer='The left pointer advances at most n times across all outer iterations, not n times per iteration.',
stretch='Return the half-open indices [start, end) of a longest valid window.'),
dict(title='Prefix sums for signed ranges', symbol='count_target_ranges',
concept='A prefix sum records the total before a position. The sum of values from i through j is prefix[j + 1] − prefix[i]. This turns a range question into a lookup for an earlier total. Unlike the previous window technique, this works with negative values. When counting all qualifying ranges, store how often each prefix occurred rather than only whether it occurred.',
trace='For [2, -2, 2] and target 2, prefix totals are 0, 2, 0, 2. The last prefix 2 finds two earlier zeros, contributing two ranges. Together with the first 2, the answer is 3.',
exercise='Implement count_target_ranges(values, target). Count nonempty contiguous ranges summing to target. Values may be negative or zero. Empty input returns 0.',
hint='Seed the frequency map with prefix zero appearing once. Query prefix − target before recording the new prefix.',
proof='Before processing each new prefix, seen contains exactly the prefixes at earlier boundaries. Each matching earlier prefix determines one nonempty range ending now. Querying first prevents a zero-length range when target is zero.',
cost='Expected O(n) time and O(n) auxiliary space.',
pitfall='A set undercounts repeated prefix totals. Forgetting the initial zero loses ranges starting at index 0. Recording before querying adds empty ranges for target 0.',
quiz='How many target-zero ranges are in [0, 0]?', answer='Three: each individual zero and the full two-element range.',
stretch='Return the length of the longest matching range by storing the earliest index of each prefix.'),
dict(title='Stacks and unresolved candidates', symbol='next_warmer_wait',
concept='A stack removes the most recently added item first. It can represent unfinished parsing, nested work, or candidates awaiting a future event. A monotonic stack keeps candidates in a useful order and removes those settled by the current item. Store indices when distance matters. Equal values need careful handling because strictly greater and greater-or-equal are different conditions.',
trace='For [20, 18, 21], day 0 waits on the stack, then day 1 joins it. Day 2 is warmer than both: pop day 1 and record 1, then pop day 0 and record 2. Day 2 never sees a warmer future day, so its answer remains 0.',
exercise='Implement next_warmer_wait(temperatures). For each day return the number of days until a strictly warmer temperature. Use 0 when no such future day exists.',
hint='Keep unresolved day indices. The current day resolves every smaller temperature at the stack top.',
proof='The stack temperatures are nonincreasing. Popping a prior day at the first warmer incoming day gives its nearest qualifying future day: any earlier warmer day would already have popped it. Every index is pushed once and popped at most once.',
cost='O(n) time and O(n) auxiliary space, plus the O(n) answer.',
pitfall='Use < rather than <= when resolving candidates. Equal temperatures do not satisfy strictly warmer. A stack of values alone loses the original day indices.',
quiz='What is the answer for [5, 5, 6]?', answer='[2, 1, 0]. The second 5 does not resolve the first.',
stretch='Find the next strictly smaller value instead. State the new stack invariant.'),
dict(title='Queues and shortest routes without weights', symbol='nearest_exit_steps',
concept='A queue processes the oldest waiting item first. Breadth-first search explores distance 0, then distance 1, and so on when every edge costs one step. Use deque.popleft rather than list.pop(0). Mark a state visited when enqueuing it so multiple neighbors cannot queue it repeatedly. The definition of a goal matters as much as the traversal.',
trace='In ["#####", "#...#", "##.##", "##.##"], start (1, 1) reaches (1, 2), (2, 2), then boundary cell (3, 2). The minimum distance is 3. A start already on an open boundary has distance 0 under this exercise contract.',
exercise='Implement nearest_exit_steps(grid, start). The rectangular grid uses # for walls and . for open cells. Move up/down/left/right. Return the fewest steps to any boundary cell, or -1 if unreachable. An empty grid, blocked start, or out-of-bounds start returns -1. Ragged input raises ValueError.',
hint='Store (row, column, distance) in a queue. Check whether a popped cell is a goal.',
proof='FIFO processing ensures that all distance-d states are processed before distance-(d + 1) states. The first reachable boundary popped has minimum distance. Visited marking bounds each cell to one enqueue.',
cost='O(rows × columns) time and auxiliary space in the worst case.',
pitfall='Some other maze problems exclude the entrance as an exit; this one includes it. Do not import a different contract. Weighted moves require another shortest-path method.',
quiz='When is a plain BFS shortest-path guarantee valid?', answer='When each traversed edge has the same cost, commonly one step.',
stretch='Track predecessors and reconstruct one shortest route, including the starting cell.'),
dict(title='Linked lists and safe pointer changes', symbol='reverse_chain',
concept='A linked list stores each value with a link to the next node. Moving to index k costs traversal, but relinking a node is constant work once its predecessor is known. Reversal is about preserving access while changing direction. Before overwriting current.next, save the following node. Otherwise the unprocessed suffix can become unreachable.',
trace='For A → B → C, save B, set A.next to None, then advance. Save C, set B.next to A, then advance. Finally set C.next to B. The new head is C; the old head A is now the tail.',
exercise='Implement reverse_chain(head) using the provided Node class. Reverse a finite acyclic singly linked list in place and return its new head. None returns None. Preserve node identities; do not create replacement nodes.',
hint='Keep three references: previous, current, and a temporary following reference.',
proof='At every iteration, previous is the head of the reversed processed prefix and current is the untouched suffix head. Saving following preserves the suffix before relinking. When current becomes None, the entire list is the reversed prefix.',
cost='O(n) time and O(1) auxiliary space. The input nodes are reused.',
pitfall='Advancing through current.next after overwriting it follows the reversed link. A cyclic input violates this exercise precondition and needs separate cycle handling.',
quiz='Why should the original head eventually point to None?', answer='It becomes the new tail. Keeping its old next link could create a cycle.',
stretch='Reverse only the first k nodes and reconnect the suffix; define behavior when k exceeds length.'),
dict(title='Binary search with explicit boundaries', symbol='lower_bound',
concept='Binary search repeatedly discards half a sorted search space. The reliable version begins by stating what each boundary means. For a lower bound, positions before left are known to contain values smaller than target; positions at or after right are known to contain values at least target. Search the half-open interval [left, right). A length-n input has n + 1 insertion boundaries.',
trace='For [2, 4, 4, 9] and target 4, start [0, 4). Middle 2 qualifies, so right becomes 2. Middle 1 qualifies, so right becomes 1. Middle 0 is too small, so left becomes 1. Both meet at the first 4.',
exercise='Implement lower_bound(values, target). Return the first index whose value is at least target in sorted nondecreasing input. Return len(values) if no value qualifies; empty input returns 0.',
hint='Use right = len(values). A qualifying middle stays a possible answer, so set right = middle.',
proof='Both updates preserve the boundary claims. Each update strictly shrinks the unresolved interval. When left equals right, every earlier element is too small and that boundary is the first possible qualifying index.',
cost='O(log n) time and O(1) auxiliary space for random-access input.',
pitfall='right = middle − 1 belongs to a different boundary convention. Mixing conventions causes missed answers or infinite loops. The returned index can equal n.',
quiz='What does lower_bound([3, 3], 4) return?', answer='2, the insertion boundary after the last item.',
stretch='Search for the smallest feasible capacity in a monotone feasibility predicate instead of searching stored values.'),
dict(title='Recursion as a contract for smaller work', symbol='nested_total',
concept='A recursive function promises to solve the same kind of problem on a smaller input. Identify the returned meaning, a base case, and a measure that decreases. The call stack stores unfinished work. Recursion is not automatically exponential: repeated subproblems and branching determine total work. Deep Python recursion can exceed the interpreter limit even when asymptotic work is linear.',
trace='For [2, [3, [], [4]], 1], the inner [4] returns 4, then [3, [], [4]] returns 7. The outer call adds 2 + 7 + 1 and returns 10. An empty list contributes zero.',
exercise='Implement nested_total(items). Input is a finite, acyclic nesting of Python lists and integers. Return the sum of every integer. Do not mutate input. Empty lists can appear at any depth.',
hint='For each item, either add its integer value or ask the same function to sum the nested list.',
proof='For an empty list the result is zero. Assuming recursive calls correctly total each smaller nested list, adding those totals and the direct integers counts every integer exactly once.',
cost='O(m) time for m visited list entries and O(h) call-stack space for nesting depth h. A very deep input may raise RecursionError.',
pitfall='Summing only the outer integers misses nested values. Cycles are outside the contract; do not claim this handles a list that contains itself.',
quiz='Does two recursive calls always imply exponential time?', answer='No. If they visit disjoint portions of a tree, total work can still be linear in the total nodes.',
stretch='Implement an explicit stack version that handles deeply nested acyclic input.'),
dict(title='Tree DFS: return one fact, update another', symbol='tree_diameter',
concept='Trees connect nodes without cycles. In a binary tree each node has up to two children. A depth-first postorder traversal finishes the children before combining their results. Sometimes the fact a parent needs differs from the answer being optimized. For diameter, a parent needs one downward height, but a path passing through a node can combine both child heights.',
trace='A root with two leaf children receives heights 1 and 1. Its through-root path has 2 edges; it returns height 2. A chain of three nodes also has diameter 2. The longest path need not pass through the overall root.',
exercise='Implement tree_diameter(root) using Tree. Return the maximum number of edges on a simple path between any two nodes. Empty and single-node trees return 0. Assume a finite tree with no shared nodes or cycles.',
hint='Let height(None) be 0. At each node, left_height + right_height is a candidate diameter.',
proof='Every path has a highest node where its two downward portions meet. Postorder computes the longest available downward portion on each side. Taking the maximum of their sums therefore considers an optimal path at its highest node.',
cost='O(n) time and O(h) recursion space. A skewed tree has h = n and may exceed Python recursion depth.',
pitfall='Returning the diameter to the parent loses the height information needed for combination. Counting nodes rather than edges produces off-by-one answers.',
quiz='Can the diameter lie entirely in the left subtree?', answer='Yes. Updating a global best at every node covers that case.',
stretch='Return the actual endpoint values along with the diameter length.'),
dict(title='Tree BFS and level boundaries', symbol='level_means',
concept='Level-order traversal groups nodes by distance from the root. A queue naturally holds the next nodes to process, but children are added while the current level is being consumed. Capture the queue length at the start of each level; that snapshot separates current-level nodes from children appended for the next level.',
trace='For root 6 with children 2 and 10, queue width starts at 1 and produces mean 6. The next width is 2 and produces (2 + 10) / 2 = 6. Children of either node belong to the following level.',
exercise='Implement level_means(root), returning a list of arithmetic means from root level downward. Use the provided finite Tree structure. Empty input returns []. Floating-point output is acceptable.',
hint='Use width = len(queue) once per outer iteration and pop exactly width nodes.',
proof='At the start of a level, the queue contains precisely that level in order. Processing its captured width consumes all and only those nodes while appending their children. The invariant repeats for the next level.',
cost='O(n) time and O(w) queue space for maximum level width w, plus O(h) output. Floating-point arithmetic has ordinary precision limits.',
pitfall='Using a queue length that changes inside the inner loop mixes levels. A wide balanced tree can use more BFS memory than DFS.',
quiz='Which can use O(n) queue space: a chain or a broad tree?', answer='A broad tree. A chain has at most one node in its queue at a time.',
stretch='Produce the visible rightmost value of each level using the same level-boundary pattern.'),
dict(title='Binary search trees and inherited constraints', symbol='valid_bst',
concept='A binary search tree imposes constraints from every ancestor, not only the parent. Under strict ordering, every value in a left subtree is smaller than its root and every value in a right subtree is larger. Pass an allowed open interval downward. A missing bound means unbounded; it is not a numeric sentinel that might collide with input.',
trace='Root 10 has left child 5, and 5 has right child 12. Each local parent-child comparison looks valid, but 12 lies in the left subtree of 10. It violates the inherited upper bound 10.',
exercise='Implement valid_bst(root). Use strict ordering, so duplicates are invalid. An empty tree is valid. Node values are integers; assume a finite proper tree.',
hint='When descending left, replace the upper bound with the current value. When descending right, replace the lower bound.',
proof='Each call receives exactly the ancestor constraints for its subtree. Rejecting a value outside them detects a violation; narrowing the interval for each child preserves every earlier constraint.',
cost='O(n) time and O(h) recursion space. Searching a balanced BST is O(log n), but validating one requires inspecting all its nodes.',
pitfall='Checking only immediate children accepts deeply misplaced values. Decide duplicate policy explicitly rather than silently mixing < and <=.',
quiz='Does sorting a tree’s values prove that the original tree was a BST?', answer='No. Sorting discards structure. A strictly increasing inorder traversal would be a valid alternative check.',
stretch='Implement the inorder alternative iteratively, retaining only the previous visited value.'),
dict(title='Graphs: components and visited state', symbol='component_count',
concept='A graph generalizes a tree: cycles, disconnected regions, and multiple routes can exist. Use an adjacency list to store neighbors. In an undirected graph add each edge in both directions. A traversal from one unseen vertex reaches exactly its connected component. Restart from every unseen vertex to cover disconnected input, including isolated vertices.',
trace='With n = 6 and edges (0, 1), (1, 2), (3, 4), the regions are {0,1,2}, {3,4}, and {5}. Starting a fresh traversal at 0, 3, and 5 gives component count 3.',
exercise='Implement component_count(n, edges). Vertices are 0 through n − 1; n is nonnegative and endpoints are valid. Edges are undirected. Parallel edges and self-loops are allowed; they do not create extra components.',
hint='Maintain one visited set across all traversal starts. Mark before pushing onto the explicit stack.',
proof='A traversal follows exactly the edges reachable from its start, so it covers one complete component. No visited vertex starts another traversal. Every component eventually supplies one unseen start.',
cost='O(V + E) time and O(V + E) space including adjacency storage; traversal state alone is O(V).',
pitfall='Clearing visited between starts overcounts. Ignoring vertices that never appear in the edge list loses isolated components.',
quiz='How many components does n = 4 with no edges contain?', answer='Four: each isolated vertex is its own component.',
stretch='Return the vertices in each component and test that every vertex appears exactly once.'),
dict(title='Directed dependencies and topological order', symbol='dependency_order',
concept='Dependency edges have direction. A topological order places each prerequisite before the work that depends on it. Kahn’s algorithm tracks incoming edges remaining in the unprocessed graph. A zero-indegree vertex has no unfinished prerequisite and can be scheduled. If vertices remain but none is ready, a cycle blocks completion.',
trace='Edges 0 → 2 and 1 → 2 make both 0 and 1 initially ready. Removing each reduces indegree[2]. Only after both are processed does 2 enter the queue. Either [0,1,2] or [1,0,2] is valid.',
exercise='Implement dependency_order(n, edges), where (a, b) means a must happen before b. Return any valid ordering of vertices 0..n−1, or None if a cycle exists. Empty graph returns []. Endpoints are valid.',
hint='Build outgoing adjacency and an indegree array. Check the number of processed vertices at the end.',
proof='Every emitted vertex has zero incoming edges from unfinished work, so all of its prerequisites already precede it. A finite directed acyclic graph always has a zero-indegree vertex. If processing stalls early, the remaining subgraph contains a cycle.',
cost='O(V + E) time and O(V + E) space.',
pitfall='An undirected cycle detector does not solve directed scheduling. Different correct orders can exist, so tests should verify constraints instead of only one literal order.',
quiz='What should a self-loop 2 → 2 imply?', answer='A cycle, so no topological ordering exists.',
stretch='Return groups of tasks that can begin in parallel, respecting dependency layers.'),
dict(title='Heaps and keeping only the best candidates', symbol='kth_largest',
concept='A heap exposes the smallest item efficiently without sorting the entire collection. Python heapq implements a min-heap. To retain the k largest values, keep a heap of size at most k: when it grows, remove its smallest member. The root then marks the weakest surviving candidate, which is exactly the kth largest once enough items have arrived.',
trace='For [6, 2, 9, 4] and k = 2, retain {6}, then {2,6}. Adding 9 ejects 2; adding 4 ejects 4. The final retained values are 6 and 9, so the answer is 6.',
exercise='Implement kth_largest(values, k). Count duplicates as separate positions in descending order. Do not mutate the input. Reject k outside 1..len(values) with ValueError.',
hint='Push each value, and pop whenever the heap contains more than k values.',
proof='After each input, the heap contains the largest min(k, processed_count) values seen so far. A newly pushed value can only displace the smallest retained candidate. At completion the root is the kth largest.',
cost='O(n log(k + 1)) time and O(k) auxiliary space. For k = 1 this is linear; sorting instead costs O(n log n).',
pitfall='The heap’s list representation is not fully sorted. The maximum is not necessarily the last item. Duplicates matter unless the contract asks for distinct values.',
quiz='For [5, 5, 2] with k = 2, what is the answer?', answer='5. The two 5s occupy the first and second positions.',
stretch='Adapt this into a streaming class that supports add(value) and reports the current kth largest after at least k observations.'),
dict(title='Greedy choices need an exchange argument', symbol='max_meetings',
concept='Greedy algorithms commit to a locally favorable choice without revisiting it. This requires proof, not intuition. For maximizing the count of nonoverlapping meetings with equal value, choosing the earliest finishing available meeting leaves at least as much room as any alternative first choice. That argument fails when meetings carry different rewards.',
trace='For meetings (0,4), (1,2), (2,3), (3,5), sort by finish and choose (1,2), then (2,3), then (3,5). Choosing the earliest starting meeting (0,4) would leave room for fewer meetings.',
exercise='Implement max_meetings(intervals). Return a maximum-size compatible subset of positive-duration half-open intervals [start, end). Touching endpoints do not overlap. Equal-value meetings, arbitrary input order, and negative times are allowed. Invalid duration raises ValueError.',
hint='Sort by end time and accept a meeting when its start is at least the last accepted end.',
proof='Take an optimal solution’s first meeting. Replace it with the earliest finishing meeting; the replacement cannot overlap any later meeting that the original first meeting allowed. Repeat this exchange on the remaining compatible suffix.',
cost='O(n log n) time and O(n) additional space for sorting and output. Input is not mutated.',
pitfall='Sorting by start time or shortest duration lacks this guarantee. If meetings have different values, maximizing their count is a different objective from maximizing reward.',
quiz='Are (1, 3) and (3, 4) compatible here?', answer='Yes. Half-open intervals do not include their ending point.',
stretch='Give a counterexample to the rule “always take the shortest available meeting.”'),
dict(title='Backtracking: choose, explore, undo', symbol='choose_tags',
concept='Backtracking explores a tree of partial decisions. A path holds the current candidate; a recursive call explores its extensions; undo restores the exact prior state. Generate combinations in increasing input-index order so the same selection is not produced in multiple orders. Pruning skips branches that cannot fill the remaining slots.',
trace='From [a, b, c] choose 2. Start with a, extend with b and then c, producing [a,b] and [a,c]. Undo a, start b, extend c, producing [b,c]. Never start the second choice before the first choice’s index.',
exercise='Implement choose_tags(tags, k). Input tags are distinct. Return all size-k selections as lists, preserving input order inside each selection. Any output order is valid. k = 0 returns [[]]; k outside 0..n returns [].',
hint='Pass the next allowed start index. Append path.copy() at a complete selection, not the mutable path itself.',
proof='Each selection has one unique increasing index sequence. The recursion follows exactly those sequences and cannot repeat them. Pruning only skips a suffix with fewer available items than remaining slots.',
cost='For valid k, O((k + 1) × C(n,k)) time and output space; O(k) recursion/path space excluding output. Enumeration cannot be polynomial for all k because output itself can be exponential.',
pitfall='Appending path without copying makes saved results change during undo. Forgetting to pop contaminates sibling branches.',
quiz='Why does k = 0 have one selection rather than zero?', answer='There is exactly one way to select nothing: the empty selection.',
stretch='Support repeated input tags while returning unique selections; explain where duplicate branches are skipped.'),
dict(title='Dynamic programming on one dimension', symbol='min_tokens',
concept='Dynamic programming stores answers to overlapping subproblems. Define the state in a full sentence before choosing a recurrence. Here dp[s] is the minimum number of reusable tokens needed to make exact subtotal s. The last token has some denomination c, leaving subtotal s − c. Build states in increasing subtotal order so each dependency is already solved.',
trace='For denominations [1, 3, 4] and amount 6, greedy largest-first takes 4 + 1 + 1. DP considers the last token and finds 3 + 3 using two tokens. dp[0] is 0; an unreachable subtotal carries a sentinel larger than any possible valid count.',
exercise='Implement min_tokens(denominations, amount). Use unlimited copies of positive integer denominations to form a nonnegative integer amount exactly. Return the fewest tokens, or -1 if impossible. Empty denominations can form only zero. Invalid signs raise ValueError.',
hint='For each subtotal, try each denomination that fits and minimize dp[subtotal − coin] + 1.',
proof='Any solution for subtotal s ends in some allowed token c. Removing it leaves an optimal smaller problem; using a nonoptimal remainder could only increase the count. Trying every final token includes an optimal solution.',
cost='O(A × d) time and O(A) auxiliary space, where A is the numeric amount and d is the number of denominations. This is pseudopolynomial in A, not polynomial in the bit length of A.',
pitfall='dp[0] must be zero. A greedy approach fails for arbitrary denominations. Coin values of zero or less invalidate the recurrence.',
quiz='What is min_tokens([4, 6], 5)?', answer='-1: no exact combination exists.',
stretch='Store the last chosen denomination for each subtotal and reconstruct one optimal token list.'),
dict(title='Grid DP and careful memory reuse', symbol='minimum_grid_cost',
concept='Two-dimensional DP often represents progress along two coordinates. For right/down grid movement, each cell can be reached only from above or from the left. A full table makes this clear. A one-row optimization reuses memory: before updating column c, dp[c] means “from above,” while dp[c − 1] already means “from the left in this row.” Update direction therefore carries meaning.',
trace='For [[2, 9, 1], [1, 3, 2]], the first row’s totals are [2, 11, 12]. The next row becomes [3, 6, 8]. The cheapest path costs 8, including both start and destination.',
exercise='Implement minimum_grid_cost(grid). Grid is a nonempty rectangular matrix of integers, which may be negative. Start top-left and move only right or down to bottom-right. Include every visited cell’s cost. Empty or ragged input raises ValueError.',
hint='Initialize dp[0] = 0 and other entries to infinity. At each cell add its cost to min(above, left).',
proof='Every route into a cell has a final move from above or left. Minimizing over those optimal prefixes gives the best route to that cell. Row-major order solves both dependencies before their values are needed.',
cost='O(rows × columns) time and O(columns) auxiliary space.',
pitfall='Negative cells are safe here because the movement graph has no cycles. A negative-weight general graph would require different reasoning. One-row costs alone do not retain a reconstructable path.',
quiz='Why can updating columns right-to-left break this implementation?', answer='The left neighbor would still contain the previous row’s value rather than the current row’s solved cost.',
stretch='Build the full table and a predecessor table to return both minimum cost and a path.'),
dict(title='Tries: organize information by shared prefixes', symbol='PrefixIndex',
concept='A trie is a tree whose edges represent successive symbols. Words sharing a prefix share a traversal path. Hash maps answer exact-key questions; a trie makes prefix navigation explicit. Store a count at each node to answer how many inserted entries share that prefix without traversing the whole subtree. Dictionary child maps avoid allocating an entire alphabet at every node.',
trace='Insert "map", "math", and "map" again. The path m → a has count 3, while m → a → p has count 2. Query "mat" returns 1. Query "z" returns 0. The empty prefix matches all three inserted entries.',
exercise='Implement PrefixIndex with add(word) and count_prefix(prefix). Inputs are Python strings. Count duplicate inserts separately. Empty words are valid, and querying the empty prefix returns the total number of inserted entries.',
hint='Give the root its own count, and increment counts along every inserted path.',
proof='Each insertion increments precisely the nodes corresponding to its prefixes, including the empty prefix at the root. Therefore a reached node’s count equals the number of entries matching that prefix. A missing edge means zero matches.',
cost='Expected O(L) per insertion and O(P) per prefix query for lengths L and P. Total storage is O(total inserted characters) in the worst case, with substantial Python object overhead.',
pitfall='Without the root counter, empty-prefix queries fail. A terminal-word flag alone cannot count duplicate entries or all descendants.',
quiz='Does a prefix count of 2 prove the prefix itself was inserted?', answer='No. Two longer strings may share that prefix without the prefix being a complete inserted word.',
stretch='Add exact-word counts and then support deletion without making any counters negative.'),
dict(title='Disjoint sets for growing connectivity', symbol='DisjointSets',
concept='Disjoint-set union tracks which group each vertex belongs to while connections are added. Each group has a representative root. Union joins roots, rather than arbitrary nodes. Union by size attaches the smaller tree under the larger one; path compression shortens later finds. This structure answers connectivity efficiently but does not retain actual graph paths.',
trace='Start with four groups {0}, {1}, {2}, {3}. union(0,1) leaves three groups. union(2,3) leaves two. union(1,2) leaves one. union(0,3) returns False because those vertices already share a representative.',
exercise='Implement DisjointSets(n) with find(node), union(a,b), and groups. Vertices are valid IDs 0..n−1. union returns True only when it merges two distinct groups. Start with groups = n.',
hint='Compress paths during find. Decrease groups only after two different representatives are joined.',
proof='Each parent tree represents exactly one connected group. Joining representatives merges exactly two groups and cannot create an internal parent cycle. Compression changes a node’s parent only to another ancestor in the same group.',
cost='O(n) initialization and O(n) storage. With both heuristics, m operations take O(m α(n)) amortized time beyond initialization, where α grows extremely slowly; an individual operation need not be constant time.',
pitfall='Decrementing groups for an already connected pair gives incorrect counts. Standard DSU cannot efficiently undo arbitrary edge deletions.',
quiz='Can parent pointers reconstruct the original connecting edges?', answer='No. Union and compression change the representation; it is not the original graph.',
stretch='Process a stream of connections and report the component count after every addition.'),
dict(title='Weighted routes and Dijkstra’s frontier', symbol='shortest_costs',
concept='When edges have unequal nonnegative costs, FIFO order no longer settles the cheapest route. Dijkstra’s algorithm expands the smallest tentative distance using a priority queue. Relaxation asks whether a route through the current vertex improves a neighbor. A simple heap implementation inserts improved entries without deleting old ones; discard stale entries when popped.',
trace='Edges 0 → 1 cost 8, 0 → 2 cost 2, and 2 → 1 cost 1 first propose distance 8 for vertex 1. Expanding vertex 2 improves it to 3. Later the heap entry (8,1) is stale and ignored.',
exercise='Implement shortest_costs(n, edges, source). Directed edges are (a,b,cost), endpoints and source are valid, n >= 1, and costs are nonnegative finite integers. Return distances from source, using float("inf") for unreachable vertices. Reject negative edge costs.',
hint='Keep a distances array and a min-heap of (distance, vertex). Ignore a popped entry that no longer equals the stored distance.',
proof='When the smallest current tentative distance is popped, an undiscovered shorter route would have to pass through a frontier vertex with no greater distance. Nonnegative edges prevent such a route from appearing later. Relaxing outgoing edges preserves shortest known route costs.',
cost='For this lazy-heap implementation, O(V + E log(E + 2)) time and O(V + E) space. Heap storage may be O(E), including stale entries; parallel edges are allowed.',
pitfall='BFS can choose a more expensive path with fewer edges. Dijkstra is not correct with negative edges. Marking a vertex final when first enqueued is premature.',
quiz='Why can a negative edge invalidate a settled distance?', answer='A later route could reduce its total after reaching a farther vertex, contradicting the nondecreasing frontier argument.',
stretch='Store predecessors and reconstruct one cheapest route to a selected reachable destination.'),
dict(title='Bits and representation contracts', symbol='differing_bits',
concept='Bitwise operators work on binary representations. XOR places a 1 where two bits differ. The expression x & (x − 1) removes the lowest set bit of a positive integer: subtracting one flips that bit to zero and lower zeros to ones, and AND removes the newly set lower bits. Python integers have arbitrary precision; fixed-width assumptions need to be stated explicitly.',
trace='For a = 10 (1010) and b = 3 (0011), XOR is 1001. Clearing its lowest set bit produces 1000; clearing again produces 0000. Two bit positions differ.',
exercise='Implement differing_bits(a,b) for nonnegative Python integers. Return the number of differing binary positions, treating absent leading positions as zero. Negative inputs raise ValueError. Do not assume a 32-bit machine word.',
hint='Compute XOR, then count how often you can clear its lowest set bit before reaching zero.',
proof='XOR selects precisely the differing positions. Each clearing iteration removes exactly one selected position and leaves all others unchanged. The number of iterations equals the desired count.',
cost='There are k iterations for k differing bits. With B-bit arbitrary-precision Python integers, a conservative bit-work bound is O((k + 1)B), with O(B) temporary bit storage. Fixed-width O(k) reasoning is a different model.',
pitfall='Python negative integers behave like an unbounded signed representation for bitwise operations. The positive-integer clearing loop can fail to terminate on a negative value.',
quiz='What is the answer when a equals b?', answer='Zero, because their XOR is zero and the loop runs zero times.',
stretch='Define an explicit width w, mask both values to w bits, and explain how that changes negative-input semantics.'),
dict(title='A complete interview: clarify, derive, test', symbol='busiest_span',
concept='A coding interview evaluates more than recall. Clarify inputs and outputs, give a simple correct baseline, identify the expensive repeated work, state an invariant, implement, and test boundaries aloud. If stuck, name the assumption you cannot yet justify. A useful explanation connects each pointer or stored value to a concrete question about the input.',
trace='For sorted timestamps [1, 2, 4, 7, 7] and duration 3, [1,4) contains 1 and 2 but excludes 4. The span [7,10) contains both 7s. The maximum is 2. A single left pointer removes timestamps too far from the new rightmost event.',
exercise='Mock interview: implement busiest_span(timestamps,duration). Input is a sorted nondecreasing list of numeric event times. Return the maximum event count in any half-open interval [start,start+duration). Duplicate times are separate events. Duration must be positive; reject otherwise. Empty input returns 0.',
hint='After adding the right event, discard left events while right_time − left_time >= duration. A surviving window has spread strictly less than duration.',
proof='Every valid set of contiguous events has spread less than duration and can be covered by a half-open interval starting at its first event. Shrinking removes exactly the left endpoints whose spread is too large for the current right endpoint. Taking the maximum over all right endpoints covers an optimal set.',
cost='O(n) time and O(1) auxiliary space for already sorted input. For unsorted input, discuss sorting and the resulting O(n log n) cost first.',
pitfall='Using > instead of >= includes an event at the excluded right boundary. Describe the half-open contract before coding rather than patching tests afterward.',
quiz='What does [5, 5, 5] with duration 1 return?', answer='3. All three distinct events fit in [5,6).',
stretch='Do a second mock: timestamps arrive unsorted in batches. Discuss whether to sort, merge sorted batches, or use an online data structure before implementing anything.'),
]


def slug(title):
    import re
    return re.sub('[^a-z0-9]+', '-', title.lower()).strip('-')


def main():
    source = (ROOT / 'solutions/core.py').read_text()
    tree = ast.parse(source)
    nodes = {node.name: node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
    lines = source.splitlines()
    entries, combined = [], []
    for number, lesson in enumerate(LESSONS, 1):
        identifier = f'{number:02d}-{slug(lesson["title"])}'
        symbol = lesson['symbol']
        node = nodes[symbol]
        code = '\n'.join(lines[node.lineno - 1:node.end_lineno])
        if symbol == 'reverse_chain':
            code = '@dataclass\n' + ast.get_source_segment(source, nodes['Node']) + '\n\n' + code
        if symbol in ('tree_diameter', 'level_means', 'valid_bst'):
            code = '@dataclass\n' + ast.get_source_segment(source, nodes['Tree']) + '\n\n' + code
        imports = ('from collections import Counter, deque\n'
                   'from dataclasses import dataclass\n'
                   'from heapq import heappop, heappush\n'
                   'from typing import Optional\n\n')
        previous = f'[Previous lesson]({entries[-1]["file"].split("/")[-1]})' if entries else '[Course home](../README.md)'
        next_file = (f'{number + 1:02d}-{slug(LESSONS[number]["title"])}.md' if number < len(LESSONS) else None)
        following = f'[Next lesson]({next_file})' if next_file else '[Mock interview rubric](../ASSESSMENT.md)'
        text = f'''# {number:02d}. {lesson['title']}

{previous} · {following} · [Full course](../README.md)

**Prerequisite:** {'Basic Python functions, loops, lists, and dictionaries.' if number == 1 else 'The earlier lessons in this course; review unfamiliar prerequisites before continuing.'}
**Suggested pace:** 2–3 short sessions: understand, attempt, then explain and review. The timer is a limit, not a promise of mastery.

## The idea

{lesson['concept']}

## Walk through an example

{lesson['trace']}

## Your exercise

{lesson['exercise']}

Start in [the exercise file](../exercises/{identifier}.py). First describe a direct baseline, then write your improved approach. State the invariant before coding. Test an empty/minimal case, a normal case, and a case designed to break your assumption.

<details><summary>Hint — open after an honest attempt</summary>

{lesson['hint']}

</details>

<details><summary>Reference solution — compare after trying</summary>

```python
{imports}{code}
```

### Why it works

{lesson['proof']}

### Time and space

{lesson['cost']}

</details>

## A mistake to watch for

{lesson['pitfall']}

## Retrieval check

Close the solution and answer: **{lesson['quiz']}**

<details><summary>Check your answer</summary>

{lesson['answer']}

</details>

## Optional extension

{lesson['stretch']}

## Completion checkpoint

- [ ] Explain when this approach applies and one case when it does not.
- [ ] Attempt the exercise without copying the reference.
- [ ] Test boundary behavior and explain the time/space model.
- [ ] Rebuild the key idea from memory in a later session.

Confidence: 0 = unfamiliar, 1 = can follow, 2 = can solve with hints, 3 = can solve and explain independently. Record practice privately; checking off a page alone is not mastery.
'''
        (ROOT / 'lessons' / f'{identifier}.md').write_text(text)
        # Starters preserve signatures and model classes, but contain no algorithm.
        starter_node = ast.parse(ast.get_source_segment(source, node)).body[0]
        if isinstance(starter_node, ast.FunctionDef):
            starter_node.body = [ast.Raise(exc=ast.Call(func=ast.Name(id='NotImplementedError', ctx=ast.Load()), args=[], keywords=[]), cause=None)]
        else:
            for member in starter_node.body:
                if isinstance(member, ast.FunctionDef):
                    member.body = [ast.Raise(exc=ast.Call(func=ast.Name(id='NotImplementedError', ctx=ast.Load()), args=[], keywords=[]), cause=None)]
        starter = ast.unparse(ast.fix_missing_locations(starter_node))
        model_import = ('from solutions.core import Node\n' if symbol == 'reverse_chain' else
                        'from solutions.core import Tree\n' if symbol in ('tree_diameter', 'level_means', 'valid_bst') else '')
        (ROOT / 'exercises' / f'{identifier}.py').write_text(
            f'"""Exercise {number:02d}: {lesson["title"]}. See ../lessons/{identifier}.md.\n'
            'Run from the repository root with: python -m unittest discover -s tests -v\n'
            'Reference tests check solutions by default; use the exercise grader documented in README.\n"""\n'
            + model_import + '\n' + starter + '\n')
        entries.append(dict(number=number, title=lesson['title'], symbol=symbol, file=f'lessons/{identifier}.md', exercise=f'exercises/{identifier}.py'))
        # Combined guide needs repository-root paths and unique heading anchors.
        guide_text = text.replace('../', '').replace(f']({next_file})', f'](lessons/{next_file})') if next_file else text.replace('../', '')
        if number > 1:
            guide_text = guide_text.replace(f']({entries[-2]["file"].split("/")[-1]})', f']({entries[-2]["file"]})')
        combined.append(guide_text)
    (ROOT / 'course.json').write_text(json.dumps(entries, indent=2) + '\n')
    (ROOT / 'anki').mkdir(exist_ok=True)
    with (ROOT / 'anki/cards.csv').open('w', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['Front', 'Back', 'Tags'])
        for number, lesson in enumerate(LESSONS, 1):
            tag = f'interview_dsa lesson_{number:02d}'
            writer.writerow([f'{lesson["title"]}: {lesson["quiz"]}', lesson['answer'], tag])
            writer.writerow([f'Explain the correctness argument for {lesson["symbol"]}. Recall its lesson exercise first.', lesson['proof'], tag])
    (ROOT / 'COURSE.md').write_text('# Interview DSA in Python — complete reading guide\n\nOriginal independent educational material. Work one lesson at a time.\n\n' + '\n\n---\n\n'.join(combined))
    toc = '\n'.join(f'| {e["number"]:02d} | [{e["title"]}]({e["file"]}) | [`{e["symbol"]}`]({e["exercise"]}) |' for e in entries)
    (ROOT / 'README.md').write_text('''# Interview DSA in Python

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
''' + toc + '''

## Scope and honest limitations

This is a compact written course, not a video course, grading service, or hiring guarantee. It covers major interview patterns; it is not an exhaustive algorithms textbook. Segment trees, advanced string algorithms, balanced-tree implementation, and advanced DP optimizations are outside this edition. The examples assume the documented input contracts; arbitrary malformed input is not fully validated. Recursive implementations suit instructional-size inputs and may hit Python’s recursion limit on deep structures.

The course has its own exercises rather than a copied question bank. After learning a pattern, use your preferred practice platform to attempt an unfamiliar problem and explain why the pattern fits. Additional problem difficulty should follow understanding, not a daily streak.

## Maintain and contribute

Lesson content lives in `build_course.py`; implementations in `solutions/core.py`. Rebuild with `python build_course.py`, run both checks, and include a counterexample when fixing an algorithm. Never commit credentials or private progress records.

## License

MIT for this repository’s original text and code; see [LICENSE](LICENSE).
''')
    cards = '\n'.join(f'<li><a href="{e["file"]}">{e["number"]:02d}. {html.escape(e["title"])}</a></li>' for e in entries)
    (ROOT / 'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Interview DSA in Python</title><style>body{font:18px/1.6 system-ui,sans-serif;max-width:850px;margin:3rem auto;padding:0 1rem;background:#f8fafc;color:#172033}a{color:#174ca1}li{margin:.7rem 0}input{font:inherit;padding:.6rem;width:90%}label{display:block}footer{margin-top:3rem;font-size:.9rem}</style><h1>Interview DSA in Python</h1><p>26 original lessons. Learn a pattern, attempt an exercise, explain why it works.</p><p>Offline directory: links open Markdown source. On GitHub, use the README for rendered lessons.</p><label for="filter">Find a topic</label><input id="filter" type="search" placeholder="Try graphs, window, or dynamic"><ol style="list-style:none;padding:0">''' + cards + '''</ol><p id="empty" hidden>No matching lessons.</p><footer>Independent educational project. Not affiliated with LeetCode.</footer><script>const input=document.querySelector('#filter');input.addEventListener('input',()=>{let count=0;for(const item of document.querySelectorAll('li')){item.hidden=!item.textContent.toLowerCase().includes(input.value.toLowerCase());if(!item.hidden)count++;}document.querySelector('#empty').hidden=count>0;});</script></html>''')
    print(f'Built {len(entries)} lessons and exercise starters.')


if __name__ == '__main__':
    main()
