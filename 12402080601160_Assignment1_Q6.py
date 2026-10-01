"""
Q6 - Python Module Dependency Resolver
Edge: A imports B means A depends on B, so B must load before A.
Uses Kahn's algorithm with a min-heap and DFS for cycle extraction.
"""
import heapq
import sys
from collections import defaultdict


def find_cycle(graph, nodes):
    color = {node: 0 for node in nodes}
    parent = {}

    def dfs(node):
        color[node] = 1
        for nxt in graph[node]:
            if color[nxt] == 0:
                parent[nxt] = node
                cycle = dfs(nxt)
                if cycle:
                    return cycle
            elif color[nxt] == 1:
                cycle = [nxt]
                cur = node
                while cur != nxt:
                    cycle.append(cur)
                    cur = parent[cur]
                cycle.append(nxt)
                cycle.reverse()
                return cycle
        color[node] = 2
        return None

    for node in sorted(nodes):
        if color[node] == 0:
            cycle = dfs(node)
            if cycle:
                return cycle
    return []


def solve(data):
    lines = [x.strip() for x in data.splitlines() if x.strip()]
    if not lines:
        raise ValueError("Empty input.")

    n, e = map(int, lines[0].split())
    if len(lines) != n + e + 1:
        raise ValueError("Incorrect number of lines.")

    modules = lines[1:n + 1]
    nodes = set(modules)
    if len(nodes) != n:
        raise ValueError("Duplicate module names are not allowed.")

    graph = defaultdict(set)
    indegree = {node: 0 for node in nodes}

    for line in lines[n + 1:]:
        a, b = line.split()
        if a not in nodes or b not in nodes:
            raise ValueError("Import references an unknown module.")
        # a depends on b -> edge b -> a
        if a not in graph[b]:
            graph[b].add(a)
            indegree[a] += 1

    heap = [node for node in nodes if indegree[node] == 0]
    heapq.heapify(heap)
    order = []

    while heap:
        node = heapq.heappop(heap)
        order.append(node)
        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                heapq.heappush(heap, nxt)

    if len(order) == n:
        return " ".join(order)

    # The remaining dependency graph contains at least one cycle.
    remaining = {node for node in nodes if indegree[node] > 0}
    cycle_graph = defaultdict(list)
    for src in remaining:
        for dst in graph[src]:
            if dst in remaining:
                cycle_graph[src].append(dst)
        cycle_graph[src].sort()

    cycle = find_cycle(cycle_graph, remaining)
    return "CYCLE\n" + " ".join(cycle)


def main():
    try:
        print(solve(sys.stdin.read()))
    except (ValueError, IndexError) as exc:
        print(f"INPUT_ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
