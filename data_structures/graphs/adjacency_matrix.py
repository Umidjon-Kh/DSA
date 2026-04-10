from typing import Any, Iterator, List, Optional, Tuple, Union

from .._base import BaseGraph
from ..arrays import DynamicUniversalArray
from ..hash_tables import OpenAddressingHashMap


class AdjacencyMatrixGraph(BaseGraph):
    """
    A graph backed by a 2D matrix of DynamicUniversalArrays.

    Vertices are mapped to integer indices via an OpenAddressingHashMap.
    _matrix[i][j] holds the edge value from vertex at index i to vertex at index j:
        None  — no edge exists
        True  — edge exists (unweighted graphs)
        value — edge weight (weighted graphs, int or float)

    Supports directed and undirected, weighted and unweighted modes
    controlled by constructor flags.

    For unweighted graphs, edge presence is stored as True internally,
    but get_neighbors always returns None as weight — consistent with
    AdjacencyListGraph behaviour.
    For undirected graphs, every edge is mirrored: matrix[i][j] == matrix[j][i].

    Time complexity:
        add_vertex:     O(V) — must extend every existing row
        remove_vertex:  O(V²) — must rebuild the full matrix
        get_vertices:   O(V)
        add_edge:       O(1)
        remove_edge:    O(1)
        has_edge:       O(1)
        get_neighbors:  O(V) — must scan a full matrix row
        clear:          O(1)
        copy:           O(V²)
        __len__:        O(1)
        __bool__:       O(1)
        __iter__:       O(V)
        __reversed__:   O(V)
        __contains__:   O(1) average
        __eq__:         O(V²)
        __repr__:       O(1)
    """

    __slots__ = (
        "_matrix",
        "_vertex_to_index",
        "_index_to_vertex",
        "_directed",
        "_weighted",
        "_size",
    )

    def __init__(
        self, *args: Tuple, directed: bool = False, weighted: bool = False
    ) -> None:
        """
        Creates an AdjacencyMatrixGraph with optional initial vertices and edges.

        Each positional argument must be a tuple:
            (v1,)        — adds a single vertex
            (v1, v2)     — adds an unweighted edge between v1 and v2
            (v1, v2, w)  — adds a weighted edge (only if weighted=True)

        Args:
            *args:    Tuples representing vertices or edges.
            directed: If True, edges are one-directional. Default False.
            weighted: If True, edges store a numeric weight. Default False.

        Examples:
            g = AdjacencyMatrixGraph()
            g = AdjacencyMatrixGraph((1,), (2,), directed=True)
            g = AdjacencyMatrixGraph((1, 2), (2, 3))
            g = AdjacencyMatrixGraph((1, 2, 0.5), weighted=True)

        Raises:
            ValueError: If an argument is not a non-empty tuple.
            ValueError: If a tuple has more than 3 elements.
        """
        self._matrix: DynamicUniversalArray = DynamicUniversalArray()
        self._vertex_to_index: OpenAddressingHashMap = OpenAddressingHashMap()
        self._index_to_vertex: DynamicUniversalArray = DynamicUniversalArray()
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

        Extends every existing row with a new None column, then
        appends a new row of (_size + 1) None entries.

        Time complexity: O(V)
        """
        if self._vertex_to_index.contains(vertex):
            return

        for i in range(self._size):
            self._matrix[i].append(None)

        new_row: DynamicUniversalArray = DynamicUniversalArray()
        for _ in range(self._size + 1):
            new_row.append(None)

        self._matrix.append(new_row)
        self._vertex_to_index.insert(vertex, self._size)
        self._index_to_vertex.append(vertex)
        self._size += 1

    def remove_vertex(self, vertex: Any) -> None:
        """
        Removes vertex and all its associated edges from the graph.

        If vertex does not exist, does nothing.

        Rebuilds the entire matrix, skipping the row and column of the
        removed vertex. Vertex-to-index mappings are reassigned in order.

        Time complexity: O(V²)
        """
        if not self._vertex_to_index.contains(vertex):
            return

        removed_index: int = self._vertex_to_index.get(vertex)
        new_matrix: DynamicUniversalArray = DynamicUniversalArray()
        new_vertex_to_index: OpenAddressingHashMap = OpenAddressingHashMap()
        new_index_to_vertex: DynamicUniversalArray = DynamicUniversalArray()

        new_idx: int = 0
        for old_i in range(self._size):
            if old_i == removed_index:
                continue

            v: Any = self._index_to_vertex[old_i]
            new_vertex_to_index.insert(v, new_idx)
            new_index_to_vertex.append(v)

            new_row: DynamicUniversalArray = DynamicUniversalArray()
            for old_j in range(self._size):
                if old_j == removed_index:
                    continue
                new_row.append(self._matrix[old_i][old_j])

            new_matrix.append(new_row)
            new_idx += 1

        self._matrix = new_matrix
        self._vertex_to_index = new_vertex_to_index
        self._index_to_vertex = new_index_to_vertex
        self._size -= 1

    def get_vertices(self) -> List[Any]:
        """
        Returns a list of all vertices in insertion order.

        Time complexity: O(V)
        """
        return [self._index_to_vertex[i] for i in range(self._size)]

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
        For undirected graphs, both directions are added.

        Weight is stored only if the graph was created with weighted=True.
        If weighted=True and weight is not provided, raises ValueError.
        If weighted=False, weight is ignored entirely and True is stored
        internally to mark edge presence.

        If the edge already exists, does nothing.

        Time complexity: O(1)

        Raises:
            ValueError: If v1 == v2 (self-loops are not supported).
            ValueError: If graph is weighted and weight is not provided.
        """
        if v1 == v2:
            raise ValueError("Self-loops are not supported.")
        if self._weighted and weight is None:
            raise ValueError("Graph is weighted — weight must be provided.")

        self.add_vertex(v1)
        self.add_vertex(v2)

        if self.has_edge(v1, v2):
            return

        stored: Any = weight if self._weighted else True
        i: int = self._vertex_to_index.get(v1)
        j: int = self._vertex_to_index.get(v2)

        self._matrix[i][j] = stored
        if not self._directed:
            self._matrix[j][i] = stored

    def remove_edge(self, v1: Any, v2: Any) -> None:
        """
        Removes the edge between v1 and v2.

        If the edge does not exist, does nothing.
        For undirected graphs, both directions are removed.

        Time complexity: O(1)
        """
        if not self._vertex_to_index.contains(v1) or not self._vertex_to_index.contains(
            v2
        ):
            return

        i: int = self._vertex_to_index.get(v1)
        j: int = self._vertex_to_index.get(v2)

        self._matrix[i][j] = None
        if not self._directed:
            self._matrix[j][i] = None

    def has_edge(self, v1: Any, v2: Any) -> bool:
        """
        Returns True if an edge exists between v1 and v2.

        For undirected graphs, has_edge(v1, v2) == has_edge(v2, v1).
        For directed graphs, has_edge(v1, v2) may differ from has_edge(v2, v1).

        Time complexity: O(1)
        """
        if not self._vertex_to_index.contains(v1) or not self._vertex_to_index.contains(
            v2
        ):
            return False

        i: int = self._vertex_to_index.get(v1)
        j: int = self._vertex_to_index.get(v2)
        return self._matrix[i][j] is not None

    def get_neighbors(
        self, vertex: Any
    ) -> List[Tuple[Any, Optional[Union[int, float]]]]:
        """
        Returns a list of (neighbor, weight) pairs for the given vertex.

        For unweighted graphs, weight is always None.
        For weighted graphs, weight is the value assigned to that edge.

        Time complexity: O(V) — scans the full matrix row

        Raises:
            KeyError: If vertex does not exist in the graph.
        """
        if not self._vertex_to_index.contains(vertex):
            raise KeyError(f"Vertex {vertex!r} does not exist in the graph.")

        i: int = self._vertex_to_index.get(vertex)
        result: List[Tuple[Any, Optional[Union[int, float]]]] = []

        for j in range(self._size):
            val: Any = self._matrix[i][j]
            if val is not None:
                neighbor: Any = self._index_to_vertex[j]
                stored_weight: Optional[Union[int, float]] = (
                    val if self._weighted else None
                )
                result.append((neighbor, stored_weight))

        return result

    # -------------------------------------------------------------------------
    # Dunder methods

    def clear(self) -> None:
        """
        Removes all vertices and edges from the graph.

        Drops all internal references — GC handles the matrix rows.

        Time complexity: O(1)
        """
        self._matrix = DynamicUniversalArray()
        self._vertex_to_index = OpenAddressingHashMap()
        self._index_to_vertex = DynamicUniversalArray()
        self._size = 0

    def copy(self) -> "AdjacencyMatrixGraph":
        """
        Returns a shallow copy of the graph preserving all vertices,
        edges, and constructor flags.

        Each matrix row is copied into a new DynamicUniversalArray —
        vertex objects themselves are shared, not duplicated.

        Time complexity: O(V²)
        """
        new_graph = AdjacencyMatrixGraph(
            directed=self._directed, weighted=self._weighted
        )
        new_graph._vertex_to_index = self._vertex_to_index.copy()
        new_graph._index_to_vertex = self._index_to_vertex.copy()
        for i in range(self._size):
            new_graph._matrix.append(self._matrix[i].copy())
        new_graph._size = self._size
        return new_graph

    def __len__(self) -> int:
        """Returns the number of vertices in the graph. O(1)"""
        return self._size

    def __bool__(self) -> bool:
        """Returns True if the graph contains at least one vertex. O(1)"""
        return self._size > 0

    def __iter__(self) -> Iterator[Any]:
        """Yields all vertices in insertion order. O(V)"""
        for i in range(self._size):
            yield self._index_to_vertex[i]

    def __reversed__(self) -> Iterator[Any]:
        """Yields all vertices in reverse insertion order. O(V)"""
        for i in range(self._size - 1, -1, -1):
            yield self._index_to_vertex[i]

    def __contains__(self, vertex: Any) -> bool:
        """Returns True if vertex exists in the graph. O(1) average"""
        return self._vertex_to_index.contains(vertex)

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both graphs have identical vertices, edges,
        weights, and constructor flags.

        Compares neighbor sets per vertex — insertion order and internal
        index layout do not affect equality.

        Time complexity: O(V²)
        """
        if not isinstance(other, AdjacencyMatrixGraph):
            return NotImplemented
        if self._directed != other._directed or self._weighted != other._weighted:
            return False
        if self._size != other._size:
            return False
        for vertex in self:
            if not other._vertex_to_index.contains(vertex):
                return False
            self_neighbors = set(self.get_neighbors(vertex))
            other_neighbors = set(other.get_neighbors(vertex))
            if self_neighbors != other_neighbors:
                return False
        return True

    def __repr__(self) -> str:
        """
        Returns a string representation of the graph.
        Format: AdjacencyMatrixGraph(vertices=3, directed=False, weighted=True)

        Time complexity: O(1)
        """
        return (
            f"AdjacencyMatrixGraph("
            f"vertices={self._size}, "
            f"directed={self._directed}, "
            f"weighted={self._weighted})"
        )
