#graph_model.py
from collections import deque
class GraphModel:
    def __init__(self):
        self.directed = False
        self._next_id = 0
        self.nodes = set()
        self.edges = []

        # ----- DFS / Topo / SCC metadata -----
        self.discover = {}        # node_id -> discovery time
        self.finish = {}          # node_id -> finish time

        self.tree_edges = []      # list[(u, v)]
        self.back_edges = []
        self.forward_edges = []
        self.cross_edges = []    

        self.has_cycle = False

        self.scc_result = []

    # ------------- basic graph ops -------------

    def clear(self):
        self.directed = False
        self._next_id = 0
        self.nodes.clear()
        self.edges.clear()

        self.discover.clear()
        self.finish.clear()
        self.tree_edges.clear()
        self.back_edges.clear()
        self.forward_edges.clear()
        self.cross_edges.clear()
        self.has_cycle = False
        self.scc_result.clear()

    def add_node(self) -> int:
        self._next_id += 1
        nid = self._next_id
        self.nodes.add(nid)
        return nid

    def add_edge(self, u: int, v: int):
        if u in self.nodes and v in self.nodes:
            self.edges.append((u, v))

    def set_directed(self, flag: bool):
        self.directed = flag

    # ------------- adjacency -------------

    def build_adj(self) -> dict[int, list[int]]:
        adj = {nid: set() for nid in self.nodes}
        for u, v in self.edges:
            adj[u].add(v)
            if not self.directed:
                adj[v].add(u)

        # Sort neighbors by node ID for deterministic traversal.
        return {nid: sorted(neighbors) for nid, neighbors in adj.items()}

    # ------------- BFS / DFS steps -------------

    def bfs_steps(self, start_id: int):
        if start_id not in self.nodes:
            return []

        adj = self.build_adj()
        visited = set()
        order = []
        q = deque([start_id])
        steps = []

        # Initial snapshot
        steps.append({
            "current": None,
            "struct": list(q),
            "visited": [],
            "order": [],
        })

        while q:
            v = q.popleft()
            if v not in visited:
                visited.add(v)
                order.append(v)
                steps.append({
                    "current": v,
                    "struct": list(q),
                    "visited": list(visited),
                    "order": list(order),
                })
                for nb in adj.get(v, []):
                    if nb not in visited:
                        q.append(nb)
                        steps.append({
                            "current": v,
                            "struct": list(q),
                            "visited": list(visited),
                            "order": list(order),
                        })

        return steps

    def dfs_steps(self, start_id: int):
        if start_id not in self.nodes:
            return []

        adj = self.build_adj()
        node_ids = sorted(self.nodes)

        color = {nid: "white" for nid in node_ids}
        parent = {nid: None for nid in node_ids}
        self.discover = {nid: 0 for nid in node_ids}
        self.finish = {nid: 0 for nid in node_ids}
        self.tree_edges = []
        self.back_edges = []
        self.forward_edges = []
        self.cross_edges = []
        self.has_cycle = False

        time = 0
        visited_set = set()
        order: list[int] = []
        steps: list[dict] = []

        stack: list[tuple[int, int]] = []
        stack.append((start_id, 0))

        def stack_ids():
            return [u for (u, _) in stack]

        # Initial snapshot
        steps.append({
            "current": None,
            "struct": stack_ids(),
            "visited": [],
            "order": [],
        })

        while stack:
            u, idx = stack[-1]

            if color[u] == "white":
                time += 1
                color[u] = "gray"
                self.discover[u] = time
                visited_set.add(u)
                order.append(u)

                steps.append({
                    "current": u,
                    "struct": stack_ids(),
                    "visited": sorted(visited_set),
                    "order": list(order),
                })

            neighbors = adj.get(u, [])
            if idx < len(neighbors):
                nb = neighbors[idx]
                stack[-1] = (u, idx + 1)

                if color[nb] == "white":
                    # Tree edge
                    self.tree_edges.append((u, nb))
                    parent[nb] = u

                    stack.append((nb, 0))
                    steps.append({
                        "current": u,
                        "struct": stack_ids(),
                        "visited": sorted(visited_set),
                        "order": list(order),
                    })

                elif color[nb] == "gray":
                    # Back edge (cycle)
                    self.back_edges.append((u, nb))
                    self.has_cycle = True

                else:  # color[nb] == "black"
                    if self.discover[u] < self.discover[nb]:
                        self.forward_edges.append((u, nb))
                    else:
                        self.cross_edges.append((u, nb))

                continue

            color[u] = "black"
            time += 1
            self.finish[u] = time

            stack.pop()
            steps.append({
                "current": u,
                "struct": stack_ids(),
                "visited": sorted(visited_set),
                "order": list(order),
            })

        return steps

    def topo_steps(self):
        steps = []
        adj = self.build_adj()
        node_ids = sorted(self.nodes)

        color = {nid: "white" for nid in node_ids}
        parent = {nid: None for nid in node_ids}
        self.discover = {nid: 0 for nid in node_ids}
        self.finish = {nid: 0 for nid in node_ids}
        self.tree_edges = []
        self.back_edges = []
        self.forward_edges = []
        self.cross_edges = []
        self.has_cycle = False

        time = 0
        visited_set = set()
        topo_order: list[int] = []
        stack: list[int] = []

        steps.append({
            "current": None,
            "struct": list(stack),
            "visited": [],
            "order": [],
        })

        def dfs_visit(u: int):
            nonlocal time

            stack.append(u)
            time += 1
            self.discover[u] = time
            color[u] = "gray"
            visited_set.add(u)

            steps.append({
                "current": u,
                "struct": list(stack),
                "visited": sorted(visited_set),
                "order": list(topo_order),
            })

            for nb in adj.get(u, []):
                if color[nb] == "white":
                    self.tree_edges.append((u, nb))
                    parent[nb] = u
                    dfs_visit(nb)
                elif color[nb] == "gray":
                    self.back_edges.append((u, nb))
                    self.has_cycle = True
                else:  # 'black'
                    if self.discover[u] < self.discover[nb]:
                        self.forward_edges.append((u, nb))
                    else:
                        self.cross_edges.append((u, nb))

            color[u] = "black"
            time += 1
            self.finish[u] = time

            topo_order.insert(0, u)

            stack.pop()
            steps.append({
                "current": u,
                "struct": list(stack),
                "visited": sorted(visited_set),
                "order": list(topo_order),
            })

        for nid in node_ids:
            if color[nid] == "white":
                dfs_visit(nid)

        is_dag = not (self.directed and self.has_cycle)
        return steps, is_dag

    def scc_kosaraju(self):
        if not self.directed:

            return [], [], {}


        topo_steps, _ = self.topo_steps()

        if topo_steps:
            finish_order_desc = topo_steps[-1]["order"]
        else:
            finish_order_desc = []

        if not finish_order_desc:
            finish_order_desc = sorted(
                self.nodes,
                key=lambda x: self.finish.get(x, 0),
                reverse=True,
            )

        adj = self.build_adj()
        rev_adj = {nid: [] for nid in self.nodes}
        for u in adj:
            for v in adj[u]:
                rev_adj[v].append(u)

        visited = set()
        sccs: list[list[int]] = []
        group_map: dict[int, int] = {}

        steps: list[dict] = []
        stack: list[int] = []
        visit_order_flat: list[int] = []

        # Initial snapshot
        steps.append({
            "current": None,
            "struct": [],
            "visited": [],
            "order": [],
        })

        def dfs_rev(u: int, comp: list[int]):
            visited.add(u)
            comp.append(u)
            stack.append(u)
            visit_order_flat.append(u)

            steps.append({
                "current": u,
                "struct": list(stack),
                "visited": sorted(visited),
                "order": list(visit_order_flat),
            })

            for nb in rev_adj.get(u, []):
                if nb not in visited:
                    dfs_rev(nb, comp)

            stack.pop()
            steps.append({
                "current": u,
                "struct": list(stack),
                "visited": sorted(visited),
                "order": list(visit_order_flat),
            })

        group_id = 1
        for nid in finish_order_desc:
            if nid not in visited:
                comp: list[int] = []
                dfs_rev(nid, comp)
                sccs.append(comp)

                for node in comp:
                    group_map[node] = group_id

                group_id += 1

        self.scc_result = sccs
        return steps, sccs, group_map

    def print_scc_groups(self, sccs, group_map):

        result = {}
        for node, gid in group_map.items():
            if gid not in result:
                result[gid] = []
            result[gid].append(node)

        print("=== SCC Groups ===")
        for gid in sorted(result.keys()):
            print(f"Group {gid}: {result[gid]}")