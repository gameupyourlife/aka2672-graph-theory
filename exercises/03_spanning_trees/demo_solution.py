"""Unit 3: Spanning trees, Union-Find and Kruskal's algorithm - DEMO SOLUTION.

Kruskal's algorithm is *greedy*: it looks at the edges from light to heavy
and keeps an edge whenever it does not close a cycle. The cut property
(README.md, section 2) guarantees that this simple rule produces a minimum
spanning tree.

The only difficult question is "would this edge close a cycle?", i.e. "are
both end vertices already in the same tree of the current forest?". The
Union-Find data structure answers it almost in constant time.

Runtime: sorting the edges costs O(|E| log |E|); the Union-Find operations
afterwards cost O(|E| * alpha(|V|)), which is practically linear. So the
sorting step dominates.
"""

import heapq
import itertools
import sys
from collections.abc import Iterable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.generators import small_weighted_graph
from lib.graph import Edge, Graph, Vertex


class UnionFind:
    """A partition of elements into disjoint sets ("disjoint-set forest").

    Every set is stored as a small internal tree: ``parent[x]`` is the
    parent of ``x``, and the root of a tree (``parent[root] == root``) is the
    *representative* of its set.

    Two optimisations keep the internal trees flat:

    * **union by size** - the root of the smaller set is hung below the root
      of the larger set, so a tree with k elements has height <= log2(k);
    * **path compression** - after ``find(x)`` every element on the way from
      ``x`` to the root points directly to the root.
    """

    def __init__(self, elements: Iterable[Vertex] = ()) -> None:
        """Create one singleton set ``{x}`` for every ``x`` in ``elements``."""
        self.parent: dict[Vertex, Vertex] = {}
        # size[root] = number of elements in the set of root. Only the
        # entries of roots are meaningful.
        self.size: dict[Vertex, int] = {}
        for x in elements:
            self.add(x)

    def add(self, x: Vertex) -> None:
        """Add ``x`` as a new singleton set (no-op if ``x`` is present)."""
        if x not in self.parent:
            self.parent[x] = x  # x is a root: the only element of its set
            self.size[x] = 1

    def find(self, x: Vertex) -> Vertex:
        """Return the representative (root) of the set containing ``x``.

        Raises:
            KeyError: If ``x`` was never added.
        """
        if x not in self.parent:
            raise KeyError(f"{x!r} is not an element of this UnionFind")

        # 1st pass: walk up to the root.
        root = x
        while self.parent[root] != root:
            root = self.parent[root]

        # 2nd pass (path compression): let every element on the way point
        # directly to the root. The result does not change, but the next
        # find() for these elements needs only one step.
        while self.parent[x] != root:
            next_x = self.parent[x]
            self.parent[x] = root
            x = next_x
        return root

    def union(self, x: Vertex, y: Vertex) -> bool:
        """Merge the sets containing ``x`` and ``y``.

        Returns:
            ``True`` if two different sets were merged, ``False`` if they
            were already the same set.

        Raises:
            KeyError: If ``x`` or ``y`` was never added.
        """
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False  # same set already - for Kruskal: a cycle!

        # Union by size: the smaller tree goes below the larger one. Only
        # the elements of the smaller set get one step deeper, and their set
        # at least doubles in size - so no element can get deeper than
        # log2(n) steps.
        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_y] = root_x  # important: re-hang the ROOT, not y
        self.size[root_x] += self.size[root_y]
        return True

    def connected(self, x: Vertex, y: Vertex) -> bool:
        """Return ``True`` if ``x`` and ``y`` are in the same set.

        Raises:
            KeyError: If ``x`` or ``y`` was never added.
        """
        return self.find(x) == self.find(y)


def kruskal(graph: Graph) -> list[Edge]:
    """Return a minimum spanning forest of an undirected weighted graph.

    Raises:
        ValueError: If the graph is directed.
    """
    if graph.directed:
        raise ValueError("kruskal() expects an undirected graph")

    # At the start every vertex is a tree of its own (the empty forest).
    components = UnionFind(graph.vertices())
    forest: list[Edge] = []

    # Greedy: lightest edges first. sorted() returns a new list, the graph
    # itself is not changed.
    for edge in sorted(graph.edges(), key=lambda e: e.weight):
        # union() succeeds exactly if u and v were in different trees. Then
        # the edge joins two trees and cannot close a cycle - keep it.
        # Otherwise u and v are already connected and the edge would close
        # a cycle (it is the heaviest edge on that cycle) - skip it.
        if components.union(edge.u, edge.v):
            forest.append(edge)
    return forest


def spanning_tree_weight(edges: Iterable[Edge]) -> float:
    """Return the total weight of the given edges (0 for no edges)."""
    return sum(edge.weight for edge in edges)


def prim(graph: Graph, start: Vertex) -> list[Edge]:
    """OPTIONAL: Return a minimum spanning tree of the component of ``start``.

    Raises:
        KeyError: If ``start`` is not a vertex of the graph.
        ValueError: If the graph is directed.
    """
    if graph.directed:
        raise ValueError("prim() expects an undirected graph")
    if start not in graph:
        raise KeyError(f"Start vertex {start!r} is not in the graph")

    in_tree: set[Vertex] = {start}
    tree: list[Edge] = []
    # The heap holds candidate edges (weight, tie, u, v) with u in the tree.
    # The running number "tie" decides between equal weights, so heapq never
    # has to compare two vertices (which might not be comparable).
    tie = itertools.count()
    heap: list[tuple[float, int, Vertex, Vertex]] = []
    for v in graph.neighbors(start):
        heapq.heappush(heap, (graph.weight(start, v), next(tie), start, v))

    while heap:
        weight, _, u, v = heapq.heappop(heap)  # lightest edge leaving the tree?
        if v in in_tree:
            continue  # outdated entry: v joined the tree in the meantime
        # By the cut property (S = current tree) this edge is safe.
        in_tree.add(v)
        tree.append(Edge(u, v, weight))
        for w in graph.neighbors(v):
            if w not in in_tree:
                heapq.heappush(heap, (graph.weight(v, w), next(tie), v, w))
    return tree


def count_components(graph: Graph) -> int:
    """OPTIONAL: Return the number of connected components, using only UnionFind.

    Raises:
        ValueError: If the graph is directed.
    """
    if graph.directed:
        raise ValueError("count_components() expects an undirected graph")
    components = UnionFind(graph.vertices())
    count = graph.num_vertices()  # at the start: every vertex alone
    for u, v, _weight in graph.edges():
        if components.union(u, v):
            count -= 1  # two sets became one
    return count


if __name__ == "__main__":
    uf = UnionFind(["Michel", "Ida", "Alfred", "Lina"])
    print("union(Michel, Ida):       ", uf.union("Michel", "Ida"))
    print("union(Ida, Michel):       ", uf.union("Ida", "Michel"))
    print("connected(Ida, Michel):   ", uf.connected("Ida", "Michel"))
    print("connected(Michel, Alfred):", uf.connected("Michel", "Alfred"))
    print()

    graph = small_weighted_graph()
    print("Kruskal on the Lönneberga graph:")
    tree = kruskal(graph)
    for edge in tree:
        print(f"  {edge.u} - {edge.v} ({edge.weight})")
    print("Total weight:", spanning_tree_weight(tree))
    print("Prim from Markt, total weight:", spanning_tree_weight(prim(graph, "Markt")))
    print()

    graph.add_vertex("Vimmerby")  # an isolated vertex: now 2 components
    forest = kruskal(graph)
    print(
        f"With isolated Vimmerby: {len(forest)} edges, "
        f"{count_components(graph)} components (a spanning forest)"
    )
