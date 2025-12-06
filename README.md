# Algorithm-Project
----------------------------------------
# Graph Algorithms – DFS, BFS, Topological Sort, SCC

A small Python project for exploring classic graph algorithms:

- Breadth-First Search (BFS)
- Depth-First Search (DFS) + edge classification
- Topological Sort (for DAGs)
- Strongly Connected Components (SCCs, e.g. Kosaraju)

This repo is intended as both a learning resource and a base for visualization (UI) of graph traversal steps.

> Note: Some comments and docs are written in English and Korean together, since this project was made while studying algorithms.

---

## Features

- **Directed / Undirected graphs**
- **BFS**: level-order traversal, shortest path in unweighted graphs
- **DFS**:
  - Discovery / finish time for each node
  - Edge types (tree / back / forward / cross edge)
- **Topological Sort**:
  - Defined only for **DAGs** (Directed Acyclic Graphs)
  - Automatically detects cycles via back edges
- **SCC (Strongly Connected Components)**:
  - Groups nodes that are mutually reachable
  - Implemented using an SCC algorithm (e.g. Kosaraju)

---

## Algorithms Overview

### 1. BFS (Breadth-First Search)

- **Purpose**:
  - Find the shortest path (in number of edges) from a start node in an unweighted graph
  - Traverse the graph level by level
- **Key idea**:
  - Use a **queue**
  - Visit all neighbors of the current node before moving deeper

Pseudo-code:

```python
from collections import deque

def bfs(adj, start):
    visited = set()
    order = []
    q = deque([start])

    visited.add(start)

    while q:
        v = q.popleft()
        order.append(v)

        for nb in adj.get(v, []):
            if nb not in visited:
                visited.add(nb)
                q.append(nb)

    return order
