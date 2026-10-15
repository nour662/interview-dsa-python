"""Python 3.9+; standard library only. See lessons for contracts and proofs."""
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


def earliest_unique(values):
    counts = Counter(values)
    return next((i for i, value in enumerate(values) if counts[value] == 1), -1)


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


def count_target_ranges(values, target):
    seen = Counter({0: 1})
    prefix = answer = 0
    for value in values:
        prefix += value
        answer += seen[prefix - target]
        seen[prefix] += 1
    return answer


def next_warmer_wait(temperatures):
    waits = [0] * len(temperatures)
    pending = []
    for day, temperature in enumerate(temperatures):
        while pending and temperatures[pending[-1]] < temperature:
            earlier = pending.pop()
            waits[earlier] = day - earlier
        pending.append(day)
    return waits


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


def lower_bound(values, target):
    left, right = 0, len(values)
    while left < right:
        middle = (left + right) // 2
        if values[middle] < target:
            left = middle + 1
        else:
            right = middle
    return left


def nested_total(items):
    """Finite, acyclic nested lists containing integers only."""
    total = 0
    for item in items:
        total += nested_total(item) if isinstance(item, list) else item
    return total


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


def kth_largest(values, k):
    if not 1 <= k <= len(values):
        raise ValueError('k must be between 1 and len(values)')
    heap = []
    for value in values:
        heappush(heap, value)
        if len(heap) > k:
            heappop(heap)
    return heap[0]


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


def min_tokens(denominations, amount):
    if amount < 0 or any(coin <= 0 for coin in denominations):
        raise ValueError('amount must be nonnegative and tokens positive')
    dp = [0] + [amount + 1] * amount
    for subtotal in range(1, amount + 1):
        for coin in denominations:
            if coin <= subtotal:
                dp[subtotal] = min(dp[subtotal], dp[subtotal - coin] + 1)
    return dp[amount] if dp[amount] <= amount else -1


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


def differing_bits(a, b):
    if a < 0 or b < 0:
        raise ValueError('use nonnegative integers')
    difference, count = a ^ b, 0
    while difference:
        difference &= difference - 1
        count += 1
    return count


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
