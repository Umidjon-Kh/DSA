from typing import Any, Iterator, List, Optional, Tuple, Union

from .._base import BaseGraph
from ..arrays import DynamicUniversalArray
from ..hash_tables import OpenAddressingHashMap


class AdjacencyListGraph(BaseGraph):
    """
    A graph backed by an OpenAddressingHashMap of DynamicUniversalArrays.

    Each vertex is a key in the hash map. Its value is a
    DynamicUniversalArray of (neighbor, weight) tuples representing
    all outgoing edges from that vertex.

    Supports directed and undirected, weighted and unweighted modes
    controlled by constructor flags.

    For unweighted graphs, weight is always stored as None.
    For undirected graphs, every edge is stored in both directions.

    Time complexity:
        add_vertex:     O(1) amortized
        remove_vertex:  O(V + E) — must scan all adjacency arrays
        get_vertices:   O(V)
        add_edge:       O(1) amortized
        remove_edge:    O(deg(v)) — scans neighbor array
        has_edge:       O(deg(v))
        get_neighbors:  O(deg(v))
        clear:          O(1)
        copy:           O(V + E)
        __len__:        O(1)
        __bool__:       O(1)
        __iter__:       O(V)
        __reversed__:   O(V)
        __contains__:   O(1) average
        __eq__:         O(V + E)
        __repr__:       O(1)
    """

    __slots__ = ("_adjacency", "_directed", "_weighted", "_size")

    def __init__(
        self, *args: Tuple, directed: bool = False, weighted: bool = False
    ) -> None:
        """
        Creates an AdjacencyListGraph with optional initial vertices and edges.

        Each positional argument must be a tuple:
            (v1,)        — adds a single vertex
            (v1, v2)     — adds an unweighted edge between v1 and v2
            (v1, v2, w)  — adds a weighted edge (only if weighted=True)

        Args:
            *args:    Tuples representing vertices or edges.
            directed: If True, edges are one-directional. Default False.
            weighted: If True, edges store a numeric weight. Default False.

        Examples:
            g = AdjacencyListGraph()
            g = AdjacencyListGraph((1,), (2,), directed=True)
            g = AdjacencyListGraph((1, 2), (2, 3))
            g = AdjacencyListGraph((1, 2, 0.5), weighted=True)

        Raises:
            ValueError: If an argument is not a non-empty tuple.
            ValueError: If a tuple has more than 3 elements.
        """
        self._adjacency: OpenAddressingHashMap = OpenAddressingHashMap()
        self._directed: bool = directed
        self._weighted: bool = weighted
        self._size: int = 0

        for item in args:
            if not isinstance(item, tuple) or len(item) == 0:
                raise ValueError(
                    f"Each argument must be a non-empty tuple, got: {item!r}"
                )
            if len(item) == 1:
                self.add_vertex(item[0])
            elif len(item) == 2:
                self.add_edge(item[0], item[1])
            elif len(item) == 3:
                self.add_edge(item[0], item[1], item[2])
            else:
                raise ValueError(f"Tuple must have 1, 2, or 3 elements, got: {item!r}")

    # -------------------------------------------------------------------------
    # Vertex operations

    def add_vertex(self, vertex: Any) -> None:
        """
        Adds vertex to the graph.

        If vertex already exists, does nothing.

        Time complexity: O(1) amortized
        """
        if not self._adjacency.contains(vertex):
            self._adjacency.insert(vertex, DynamicUniversalArray())
            self._size += 1

    def remove_vertex(self, vertex: Any) -> None:
        """
        Removes vertex and all its associated edges from the graph.

        If vertex does not exist, does nothing.

        Time complexity: O(V + E)
        """
        if not self._adjacency.contains(vertex):
            return

        self._adjacency.delete(vertex)
        self._size -= 1

        for v in self._adjacency.keys():
            neighbors: DynamicUniversalArray = self._adjacency.get(v)
            new_neighbors: DynamicUniversalArray = DynamicUniversalArray()
            for i in range(len(neighbors)):
                n, w = neighbors[i]
                if n != vertex:
                    new_neighbors.append((n, w))
            self._adjacency.insert(v, new_neighbors)

    def get_vertices(self) -> List[Any]:
        """
        Returns a list of all vertices in the graph.

        Time complexity: O(V)
        """
        return list(self._adjacency.keys())

    # -------------------------------------------------------------------------
    # Edge operations

    def add_edge(
        self,
        v1: Any,
        v2: Any,
        weight: Optional[Union[int, float]] = None,
    ) -> None:
        """
        Adds an edge between v1 and v2.

        If either vertex does not exist, it is created automatically.
        If either vertex is connected - does nothing.
        For undirected graphs, both directions are added.

        Weight is stored only if the graph was created with weighted=True.
        If weighted=True and weight is not provided, raises ValueError.
        If weighted=False, weight is ignored entirely.

        Time complexity: O(1) amortized

        Raises:
            ValueError: If v1 == v2 (self-loops are not supported).
            ValueError: If graph is weighted and weight is not provided.
        """
        if v1 == v2:
            raise ValueError("Self-loops are not supported.")
        if self._weighted and weight is None:
            raise ValueError("Graph is weighted — weight must be provided.")

        stored_weight = weight if self._weighted else None

        self.add_vertex(v1)
        self.add_vertex(v2)

        if self.has_edge(v1, v2):
            return

        self._adjacency.get(v1).append((v2, stored_weight))
        if not self._directed:
            self._adjacency.get(v2).append((v1, stored_weight))

    def remove_edge(self, v1: Any, v2: Any) -> None:
        """
        Removes the edge between v1 and v2.

        If the edge does not exist, does nothing.
        For undirected graphs, both directions are removed.

        Time complexity: O(deg(v))
        """
        if not self._adjacency.contains(v1) or not self._adjacency.contains(v2):
            return

        self._adjacency.insert(v1, self._filter_neighbor(self._adjacency.get(v1), v2))
        if not self._directed:
            self._adjacency.insert(
                v2, self._filter_neighbor(self._adjacency.get(v2), v1)
            )

    def _filter_neighbor(
        self, neighbors: DynamicUniversalArray, target: Any
    ) -> DynamicUniversalArray:
        """
        Returns a new DynamicUniversalArray with target removed.

        Time complexity: O(deg(v))
        """
        result = DynamicUniversalArray()
        for i in range(len(neighbors)):
            n, w = neighbors[i]
            if n != target:
                result.append((n, w))
        return result

    def has_edge(self, v1: Any, v2: Any) -> bool:
        """
        Returns True if an edge exists between v1 and v2.

        For undirected graphs, has_edge(v1, v2) == has_edge(v2, v1).
        For directed graphs, has_edge(v1, v2) may differ from has_edge(v2, v1).

        Time complexity: O(deg(v))
        """
        if not self._adjacency.contains(v1):
            return False
        neighbors: DynamicUniversalArray = self._adjacency.get(v1)
        for i in range(len(neighbors)):
            if neighbors[i][0] == v2:
                return True
        return False

    def get_neighbors(
        self, vertex: Any
    ) -> List[Tuple[Any, Optional[Union[int, float]]]]:
        """
        Returns a list of (neighbor, weight) pairs for the given vertex.

        For unweighted graphs, weight is always None.
        For weighted graphs, weight is the value assigned to that edge.

        Time complexity: O(deg(v))

        Raises:
            KeyError: If vertex does not exist in the graph.
        """
        if not self._adjacency.contains(vertex):
            raise KeyError(f"Vertex {vertex!r} does not exist in the graph.")
        return list(self._adjacency.get(vertex))

    # -------------------------------------------------------------------------
    # Collection methods

    def clear(self) -> None:
        """
        Removes all vertices and edges from the graph.

        Time complexity: O(1)
        """
        self._adjacency.clear()
        self._size = 0

    def copy(self) -> "AdjacencyListGraph":
        """
        Returns a deep copy of the graph preserving all vertices,
        edges, and constructor flags.

        The copy is fully independent — modifying it does not affect the original.

        Time complexity: O(V + E)
        """
        new_graph = AdjacencyListGraph(directed=self._directed, weighted=self._weighted)
        # Deep copy: create new hash map with copied neighbor arrays
        for vertex in self._adjacency.keys():
            neighbors_copy = self._adjacency.get(vertex).copy()
            new_graph._adjacency.insert(vertex, neighbors_copy)
        new_graph._size = self._size
        return new_graph

    # -------------------------------------------------------------------------
    # Dunder methods

    def __len__(self) -> int:
        """Returns the number of vertices in the graph. O(1)"""
        return self._size

    def __bool__(self) -> bool:
        """Returns True if the graph contains at least one vertex. O(1)"""
        return self._size > 0

    def __iter__(self) -> Iterator[Any]:
        """Yields all vertices in the graph. O(V)"""
        yield from self._adjacency.keys()

    def __reversed__(self) -> Iterator[Any]:
        """Yields all vertices in reverse insertion order. O(V)"""
        vertices = list(self._adjacency.keys())
        for i in range(len(vertices) - 1, -1, -1):
            yield vertices[i]

    def __contains__(self, vertex: Any) -> bool:
        """Returns True if vertex exists in the graph. O(1) average"""
        return self._adjacency.contains(vertex)

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both graphs have identical vertices, edges,
        weights, and constructor flags.

        Time complexity: O(V + E)
        """
        if not isinstance(other, AdjacencyListGraph):
            return NotImplemented
        if self._directed != other._directed or self._weighted != other._weighted:
            return False
        if self._size != other._size:
            return False
        for vertex in self._adjacency.keys():
            if not other._adjacency.contains(vertex):
                return False
            self_neighbors = set(self.get_neighbors(vertex))
            other_neighbors = set(other.get_neighbors(vertex))
            if self_neighbors != other_neighbors:
                return False
        return True

    def __repr__(self) -> str:
        """
        Returns a string representation of the graph.
        Format: AdjacencyListGraph(vertices=3, directed=False, weighted=True)

        Time complexity: O(1)
        """
        return (
            f"AdjacencyListGraph("
            f"vertices={self._size}, "
            f"directed={self._directed}, "
            f"weighted={self._weighted})"
        )
