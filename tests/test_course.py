import bisect
import itertools
import math
import random
import unittest
from collections import deque

from solutions import core as s


def lists(alphabet=(-1, 0, 1), maximum=5):
    for length in range(maximum + 1):
        yield from itertools.product(alphabet, repeat=length)


class CourseTests(unittest.TestCase):
    def test_01_equal_pairs(self):
        for values in lists():
            expected = sum(values[i] == values[j] for i in range(len(values)) for j in range(i))
            self.assertEqual(s.count_equal_pairs(values), expected)

    def test_02_runs(self):
        self.assertEqual(s.compress_runs(''), [])
        self.assertEqual(s.compress_runs('a'), [('a', 1)])
        self.assertEqual(s.compress_runs('aaabbc'), [('a', 3), ('b', 2), ('c', 1)])
        self.assertEqual(s.compress_runs('ab a'), [('a', 1), ('b', 1), (' ', 1), ('a', 1)])
        for chars in lists(('a', 'b'), 6):
            text = ''.join(chars)
            result = s.compress_runs(text)
            self.assertEqual(''.join(char * count for char, count in result), text)
            self.assertTrue(all(a[0] != b[0] for a, b in zip(result, result[1:])))
            self.assertTrue(all(count > 0 for _, count in result))

    def test_03_unique(self):
        for values in lists():
            expected = next((i for i, value in enumerate(values) if values.count(value) == 1), -1)
            self.assertEqual(s.earliest_unique(values), expected)

    def test_04_closest(self):
        for length in range(6):
            for values in itertools.combinations_with_replacement(range(-2, 3), length):
                for target in range(-4, 5):
                    result = s.closest_pair(values, target)
                    if length < 2:
                        self.assertIsNone(result)
                    else:
                        pairs = list(itertools.combinations(values, 2))
                        self.assertIn(result, pairs)
                        self.assertEqual(abs(sum(result) - target), min(abs(sum(pair) - target) for pair in pairs))

    def test_05_window(self):
        for values in lists((0, 1, 3), 5):
            for budget in range(6):
                expected = max([0] + [j - i for i in range(len(values)) for j in range(i + 1, len(values) + 1) if sum(values[i:j]) <= budget])
                self.assertEqual(s.longest_budget_window(values, budget), expected)
        for costs, budget in [([-1], 2), ([1], -1)]:
            with self.assertRaises(ValueError):
                s.longest_budget_window(costs, budget)

    def test_06_prefix(self):
        for values in lists():
            for target in range(-2, 3):
                expected = sum(sum(values[i:j]) == target for i in range(len(values)) for j in range(i + 1, len(values) + 1))
                self.assertEqual(s.count_target_ranges(values, target), expected)

    def test_07_stack(self):
        for values in lists((1, 2, 3), 6):
            expected = [next((j - i for j in range(i + 1, len(values)) if values[j] > value), 0) for i, value in enumerate(values)]
            self.assertEqual(s.next_warmer_wait(values), expected)

    def test_08_maze(self):
        self.assertEqual(s.nearest_exit_steps([], (0, 0)), -1)
        self.assertEqual(s.nearest_exit_steps(['#'], (0, 0)), -1)
        self.assertEqual(s.nearest_exit_steps(['.'], (0, 0)), 0)
        self.assertEqual(s.nearest_exit_steps(['...'], (-1, 0)), -1)
        self.assertEqual(s.nearest_exit_steps(['###', '#.#', '###'], (1, 1)), -1)
        self.assertEqual(s.nearest_exit_steps(['#####', '#...#', '##.##', '##.##'], (1, 1)), 3)
        with self.assertRaises(ValueError):
            s.nearest_exit_steps(['..', '.'], (0, 0))
        with self.assertRaises(ValueError):
            s.nearest_exit_steps(['', '.'], (0, 0))
        self.assertEqual(s.nearest_exit_steps([''], (0, 0)), -1)
        # Every 3x3 wall arrangement; independent layer-set reachability oracle.
        for mask in range(1 << 9):
            grid = [''.join('#' if mask & (1 << (r * 3 + c)) else '.' for c in range(3)) for r in range(3)]
            if grid[1][1] == '#':
                expected = -1
            else:
                expected = 1 if any(grid[r][c] == '.' for r, c in [(0, 1), (1, 0), (1, 2), (2, 1)]) else -1
            self.assertEqual(s.nearest_exit_steps(grid, (1, 1)), expected)

    def test_09_chain(self):
        self.assertIsNone(s.reverse_chain(None))
        for length in range(1, 12):
            nodes = [s.Node(i) for i in range(length)]
            for a, b in zip(nodes, nodes[1:]):
                a.next = b
            current = s.reverse_chain(nodes[0])
            for node in reversed(nodes):
                self.assertIs(current, node)
                current = current.next
            self.assertIsNone(current)

    def test_10_binary(self):
        for values in lists():
            values = sorted(values)
            for target in range(-3, 4):
                self.assertEqual(s.lower_bound(values, target), bisect.bisect_left(values, target))

    def test_11_nested(self):
        self.assertEqual(s.nested_total([]), 0)
        self.assertEqual(s.nested_total([2, [3, [], [4]], 1]), 10)
        self.assertEqual(s.nested_total([[-2], [3, [-1]]]), 0)
        rng = random.Random(11)
        def make(depth):
            if depth == 0:
                value = rng.randint(-10, 10)
                return value, value
            pairs = [make(depth - 1) for _ in range(rng.randrange(4))]
            return [p[0] for p in pairs], sum(p[1] for p in pairs)
        for _ in range(100):
            value, expected = make(4)
            self.assertEqual(s.nested_total(value), expected)

    def test_12_diameter(self):
        self.assertEqual(s.tree_diameter(None), 0)
        self.assertEqual(s.tree_diameter(s.Tree(1)), 0)
        self.assertEqual(s.tree_diameter(s.Tree(1, s.Tree(2), s.Tree(3))), 2)
        # Longest path lies below the overall root.
        root = s.Tree(0, s.Tree(1, s.Tree(2, s.Tree(3)), s.Tree(4, None, s.Tree(5))))
        self.assertEqual(s.tree_diameter(root), 4)
        rng = random.Random(12)
        for _ in range(70):
            nodes = [s.Tree(i) for i in range(rng.randrange(1, 20))]
            adjacency = [[] for _ in nodes]
            slots = [(0, 'left'), (0, 'right')]
            for child in range(1, len(nodes)):
                index = rng.randrange(len(slots))
                parent, side = slots.pop(index)
                setattr(nodes[parent], side, nodes[child])
                adjacency[parent].append(child)
                adjacency[child].append(parent)
                slots.extend([(child, 'left'), (child, 'right')])
            expected = 0
            for start in range(len(nodes)):
                queue, seen = deque([(start, 0)]), {start}
                while queue:
                    vertex, distance = queue.popleft()
                    expected = max(expected, distance)
                    for neighbor in adjacency[vertex]:
                        if neighbor not in seen:
                            seen.add(neighbor)
                            queue.append((neighbor, distance + 1))
            self.assertEqual(s.tree_diameter(nodes[0]), expected)

    def test_13_levels(self):
        self.assertEqual(s.level_means(None), [])
        self.assertEqual(s.level_means(s.Tree(6, s.Tree(2), s.Tree(10))), [6, 6])
        self.assertEqual(s.level_means(s.Tree(-2, None, s.Tree(4, s.Tree(7)))), [-2, 4, 7])

    def test_14_bst(self):
        self.assertTrue(s.valid_bst(None))
        self.assertTrue(s.valid_bst(s.Tree(10, s.Tree(5), s.Tree(12))))
        self.assertFalse(s.valid_bst(s.Tree(10, s.Tree(5, None, s.Tree(12)))))
        self.assertFalse(s.valid_bst(s.Tree(10, s.Tree(10))))
        self.assertTrue(s.valid_bst(s.Tree(10**100, s.Tree(-10**100))))

    def test_15_components(self):
        self.assertEqual(s.component_count(0, []), 0)
        self.assertEqual(s.component_count(4, []), 4)
        self.assertEqual(s.component_count(6, [(0, 1), (1, 2), (3, 4)]), 3)
        self.assertEqual(s.component_count(3, [(0, 0), (0, 1), (0, 1)]), 2)
        # Exhaustive undirected graphs; transitive closure is the independent oracle.
        n = 4
        candidates = list(itertools.combinations(range(n), 2))
        for mask in range(1 << len(candidates)):
            edges = [edge for i, edge in enumerate(candidates) if mask & (1 << i)]
            reach = [[i == j for j in range(n)] for i in range(n)]
            for a, b in edges:
                reach[a][b] = reach[b][a] = True
            for k in range(n):
                for i in range(n):
                    for j in range(n):
                        reach[i][j] |= reach[i][k] and reach[k][j]
            expected = sum(not any(reach[i][j] for j in range(i)) for i in range(n))
            self.assertEqual(s.component_count(n, edges), expected)

    def test_16_topology(self):
        self.assertEqual(s.dependency_order(0, []), [])
        for n in range(1, 4):
            candidates = list(itertools.product(range(n), repeat=2))
            for mask in range(1 << len(candidates)):
                edges = [edge for i, edge in enumerate(candidates) if mask & (1 << i)]
                valid = []
                for order in itertools.permutations(range(n)):
                    pos = {v: i for i, v in enumerate(order)}
                    if all(pos[a] < pos[b] for a, b in edges):
                        valid.append(order)
                result = s.dependency_order(n, edges)
                if valid:
                    self.assertIn(tuple(result), valid)
                else:
                    self.assertIsNone(result)

    def test_17_heap(self):
        for values in lists():
            for k in range(1, len(values) + 1):
                self.assertEqual(s.kth_largest(values, k), sorted(values, reverse=True)[k - 1])
        for values, k in [([], 1), ([2], 0), ([2], 2)]:
            with self.assertRaises(ValueError):
                s.kth_largest(values, k)

    def test_18_greedy(self):
        candidates = [(0, 4), (1, 2), (2, 3), (3, 5), (-2, 0), (1, 5)]
        for mask in range(1 << len(candidates)):
            values = [v for i, v in enumerate(candidates) if mask & (1 << i)]
            best = 0
            for length in range(len(values) + 1):
                for subset in itertools.combinations(values, length):
                    ordered = sorted(subset)
                    if all(a[1] <= b[0] for a, b in zip(ordered, ordered[1:])):
                        best = max(best, length)
            result = s.max_meetings(values)
            self.assertEqual(len(result), best)
            self.assertTrue(all(item in values for item in result))
            self.assertTrue(all(a[1] <= b[0] for a, b in zip(result, result[1:])))
        with self.assertRaises(ValueError):
            s.max_meetings([(2, 2)])

    def test_19_backtrack(self):
        for length in range(7):
            for k in range(length + 1):
                tags = list(range(length))
                result = s.choose_tags(tags, k)
                self.assertEqual(sorted(map(tuple, result)), list(itertools.combinations(tags, k)))
                self.assertEqual(len({id(path) for path in result}), len(result))
        self.assertEqual(s.choose_tags([1], 2), [])
        self.assertEqual(s.choose_tags([1], -1), [])

    def test_20_tokens(self):
        for size in range(5):
            for coins in itertools.combinations(range(1, 6), size):
                for amount in range(15):
                    queue, seen, expected = deque([(0, 0)]), {0}, -1
                    while queue:
                        total, steps = queue.popleft()
                        if total == amount:
                            expected = steps
                            break
                        for coin in coins:
                            value = total + coin
                            if value <= amount and value not in seen:
                                seen.add(value)
                                queue.append((value, steps + 1))
                    self.assertEqual(s.min_tokens(coins, amount), expected)
        self.assertEqual(s.min_tokens([1, 3, 4], 6), 2)
        for coins, amount in [([0], 2), ([-1], 3), ([1], -1)]:
            with self.assertRaises(ValueError):
                s.min_tokens(coins, amount)

    def test_21_grid(self):
        self.assertEqual(s.minimum_grid_cost([[2, 9, 1], [1, 3, 2]]), 8)
        def brute(grid, row=0, col=0):
            if row == len(grid) - 1 and col == len(grid[0]) - 1:
                return grid[row][col]
            options = []
            if row + 1 < len(grid):
                options.append(brute(grid, row + 1, col))
            if col + 1 < len(grid[0]):
                options.append(brute(grid, row, col + 1))
            return grid[row][col] + min(options)
        for cells in itertools.product((-1, 0, 2), repeat=6):
            grid = [list(cells[:3]), list(cells[3:])]
            self.assertEqual(s.minimum_grid_cost(grid), brute(grid))
        self.assertEqual(s.minimum_grid_cost([[-3]]), -3)
        for grid in ([], [[]], [[1], [1, 2]]):
            with self.assertRaises(ValueError):
                s.minimum_grid_cost(grid)

    def test_22_trie(self):
        index = s.PrefixIndex()
        words = ['', 'map', 'math', 'map', 'm', 'é', 'éclair']
        self.assertEqual(index.count_prefix(''), 0)
        for i, word in enumerate(words):
            index.add(word)
            for prefix in ('', 'm', 'ma', 'map', 'mat', 'z', 'é', 'écl'):
                self.assertEqual(index.count_prefix(prefix), sum(w.startswith(prefix) for w in words[:i + 1]))

    def test_23_dsu(self):
        self.assertEqual(s.DisjointSets(0).groups, 0)
        rng = random.Random(23)
        groups = s.DisjointSets(12)
        labels = list(range(12))
        for _ in range(100):
            a, b = rng.randrange(12), rng.randrange(12)
            changed = labels[a] != labels[b]
            self.assertEqual(groups.union(a, b), changed)
            old, new = labels[b], labels[a]
            labels = [new if label == old else label for label in labels]
            self.assertEqual(groups.groups, len(set(labels)))
            for i in range(12):
                for j in range(12):
                    self.assertEqual(groups.find(i) == groups.find(j), labels[i] == labels[j])

    def test_24_dijkstra(self):
        self.assertEqual(s.shortest_costs(4, [(0, 1, 8), (0, 2, 2), (2, 1, 1)], 0), [0, 3, 2, math.inf])
        with self.assertRaises(ValueError):
            s.shortest_costs(2, [(0, 1, -1)], 0)
        rng = random.Random(24)
        # Independent Floyd-Warshall oracle, including zero weights and disconnected graphs.
        for _ in range(100):
            n = rng.randrange(1, 8)
            edges = [(a, b, rng.randrange(8)) for a in range(n) for b in range(n) if rng.random() < .3]
            distances = [[0 if a == b else math.inf for b in range(n)] for a in range(n)]
            for a, b, cost in edges:
                distances[a][b] = min(distances[a][b], cost)
            for k in range(n):
                for a in range(n):
                    for b in range(n):
                        distances[a][b] = min(distances[a][b], distances[a][k] + distances[k][b])
            for source in range(n):
                self.assertEqual(s.shortest_costs(n, edges, source), distances[source])

    def test_25_bits(self):
        for a in range(40):
            for b in range(40):
                self.assertEqual(s.differing_bits(a, b), bin(a ^ b).count('1'))
        self.assertEqual(s.differing_bits(1 << 120, 1), 2)
        for a, b in [(-1, 0), (0, -2)]:
            with self.assertRaises(ValueError):
                s.differing_bits(a, b)

    def test_26_interview(self):
        for length in range(7):
            for times in itertools.combinations_with_replacement(range(5), length):
                for duration in (1, 2, 3, 5):
                    expected = max([0] + [sum(start <= time < start + duration for time in times) for start in times])
                    self.assertEqual(s.busiest_span(times, duration), expected)
        for duration in (0, -1):
            with self.assertRaises(ValueError):
                s.busiest_span([1], duration)


if __name__ == '__main__':
    unittest.main()
