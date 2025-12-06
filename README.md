
# Algorithm-Project
----------------------------------------
# Graph Algorithms – DFS, BFS, Topological Sort, SCC

A Python project for exploring classic graph algorithms:

- Breadth-First Search (BFS)
- Depth-First Search (DFS) 
- Topological Sort (for DAGs) + edge classification
- Strongly Connected Components (SCCs)

This repo is intended as both a learning resource and a base for visualization (UI) of graph traversal steps.

---

## Features

- **Directed / Undirected graphs**
- **BFS**:
  - Level-order traversal
  - Report traversal order(visit order)
- **DFS**:
  - Depth-first order traversal
  - Report traversal order(visit order) 
  - Edge types (tree / back / forward / cross edge)
- **Topological Sort**:
  - Defined only for **DAGs** (Directed Acyclic Graphs)
  - Automatically detects cycles via back edges
  - Edge types (tree / back / forward / cross edge)
  - Report traversal order(Reverse the finishing time)
- **SCC (Strongly Connected Components)**:
  - Groups nodes that are mutually reachable
  - Implemented using an SCC algorithms

---

## Algorithms Overview

### 1. BFS (Breadth-First Search)

- **Key idea**:
  - Use a **queue**
  - Traverse the graph level by level
### 2. DFS(Depth-First Search)

- **Key idea**:
  - Use **a stack**
  - Go as **deep as possible** before backtracking
    
### 3. Topological Sort(Directed Acyclic Graph)
- **Key Idea:**
  - perforemed using **DFS finish times**
  - Nodes are sorted in **decresing order of finishing time**
  - only works on **DAG(Directed Acyclic Graph)**
### 4. SCC (Strongly Connected Components)

-**Key Idea:**
  - Based on **DFS + reversed graph**
  - A group of nodes where **every node can reach every other node**
  
