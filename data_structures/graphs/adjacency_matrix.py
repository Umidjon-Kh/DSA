from typing import Any, Iterator, List, Optional, Tuple, Union

from .._base import BaseGraph
from ..arrays import DynamicUniversalArray
from ..hash_tables import OpenAddressingHashMap


class AdjacencyMatrixGraph(BaseGraph):
    """
    A graph backed by a 2D matrix (DynamicUniversalArray of DynamicUniversalArrays).

    Vertices are mapped to integer indices via an OpenAddressingHashMap.
    The matrix cell [i][j] stores the edge weight (or True for unweighted),
    or None if no edge exists.

    Supports directed and undirected, weighted and unweighted modes
    controlled by constructor flags.

    For unweighted graphs, existing edges are stored as True.
    For undirected graphs, matrix is always symmetric: [i][j] == [j][i].

    Trade-offs vs AdjacencyListGraph:
        + has_edge:       O(1)  — direct index lookup
        - add_vertex:     O(V)  — must expand every existing row + new row
        - remove_vertex:  O(V²) — must rebuild entire matrix
        - space:          O(V²) — always, even for sparse graphs

    Time complexity:
        add_vertex:     O(V)
        remove_vertex:  O(V²)
        get_vertices:   O(V)
        add_edge:       O(1)
        remove_edge:    O(1)
        has_edge:       O(1)
        get_neighbors:  O(V)
        clear:          O(1)
        copy:           O(V²)
        __len__:        O(1)
        __bool__:       O(1)
        __iter__:       O(V)
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
    # Internal helpers

    def _get_index(self, vertex: Any) -> Optional[int]:
        """Returns the matrix index for vertex, or None if not found. O(1)"""
        if not self._vertex_to_index.contains(vertex):
            return None
        return self._vertex_to_index.get(vertex)

    # -------------------------------------------------------------------------
    # Vertex operations

    def add_vertex(self, vertex: Any) -> None:
        """
        Adds vertex to the graph.

        Expands every existing row by one None cell,
        then appends a new row of all None cells.

        If vertex already exists, does nothing.

        Time complexity: O(V)
        """
        if self._vertex_to_index.contains(vertex):
            return

        new_index = self._size

        # Expand every existing row with one None (no edge to new vertex yet)
        for i in range(self._size):
            self._matrix[i].append(None)

        # Add new row — all None, length = new_size
        new_row = DynamicUniversalArray()
        for _ in range(self._size + 1):
            new_row.append(None)
        self._matrix.append(new_row)

        # Register vertex
        self._vertex_to_index.insert(vertex, new_index)
        self._index_to_vertex.append(vertex)
        self._size += 1

    def remove_vertex(self, vertex: Any) -> None:
        """
        Removes vertex and all its associated edges from the graph.

        Rebuilds the entire matrix without the removed vertex's row and column.

        If vertex does not exist, does nothing.

        Time complexity: O(V²)
        """
        idx = self._get_index(vertex)
        if idx is None:
            return

        # Save old vertex list before rebuilding
        old_vertices = [self._index_to_vertex[i] for i in range(self._size)]

        # Build new matrix skipping row and column at idx
        new_matrix = DynamicUniversalArray()
        for i in range(self._size):
            if i == idx:
                continue
            new_row = DynamicUniversalArray()
            for j in range(self._size):
                if j == idx:
                    continue
                new_row.append(self._matrix[i][j])
            new_matrix.append(new_row)

        self._matrix = new_matrix

        # Rebuild mappings from saved list
        self._vertex_to_index = OpenAddressingHashMap()
        self._index_to_vertex = DynamicUniversalArray()
        new_i = 0
        for old_i, v in enumerate(old_vertices):
            if old_i == idx:
                continue
            self._vertex_to_index.insert(v, new_i)
            self._index_to_vertex.append(v)
            new_i += 1

        self._size -= 1

    def get_vertices(self) -> List[Any]:
        """
        Returns a list of all vertices in the graph.

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
        If edge already exists, does nothing.
        For undirected graphs, both directions are set.

        Weight is stored only if the graph was created with weighted=True.
        If weighted=True and weight is not provided, raises ValueError.
        If weighted=False, edge is stored as True.

        Time complexity: O(V) due to add_vertex calls.

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

        i = self._get_index(v1)
        j = self._get_index(v2)
        stored = weight if self._weighted else True

        self._matrix[i][j] = stored  # type: ignore[union-attr]
        if not self._directed:
            self._matrix[j][i] = stored  # type: ignore[union-attr]

    def remove_edge(self, v1: Any, v2: Any) -> None:
        """
        Removes the edge between v1 and v2.

        If the edge does not exist, does nothing.
        For undirected graphs, both directions are cleared.

        Time complexity: O(1)
        """
        i = self._get_index(v1)
        j = self._get_index(v2)
        if i is None or j is None:
            return

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
        i = self._get_index(v1)
        j = self._get_index(v2)
        if i is None or j is None:
            return False
        return self._matrix[i][j] is not None

    def get_neighbors(
        self, vertex: Any
    ) -> List[Tuple[Any, Optional[Union[int, float]]]]:
        """
        Returns a list of (neighbor, weight) pairs for the given vertex.

        For unweighted graphs, weight is always None.
        For weighted graphs, weight is the value assigned to that edge.

        Time complexity: O(V)

        Raises:
            KeyError: If vertex does not exist in the graph.
        """
        idx = self._get_index(vertex)
        if idx is None:
            raise KeyError(f"Vertex {vertex!r} does not exist in the graph.")

        result = []
        for j in range(self._size):
            cell = self._matrix[idx][j]
            if cell is not None:
                neighbor = self._index_to_vertex[j]
                weight = cell if self._weighted else None
                result.append((neighbor, weight))
        return result

    # -------------------------------------------------------------------------
    # Collection methods

    def clear(self) -> None:
        """
        Removes all vertices and edges from the graph.

        Time complexity: O(1)
        """
        self._matrix = DynamicUniversalArray()
        self._vertex_to_index = OpenAddressingHashMap()
        self._index_to_vertex = DynamicUniversalArray()
        self._size = 0

    def copy(self) -> "AdjacencyMatrixGraph":
        """
        Returns a deep copy of the graph preserving all vertices,
        edges, and constructor flags.

        The copy is fully independent — modifying it does not affect the original.

        Time complexity: O(V²)
        """
        new_graph = AdjacencyMatrixGraph(
            directed=self._directed, weighted=self._weighted
        )
        new_graph._vertex_to_index = self._vertex_to_index.copy()
        new_graph._index_to_vertex = self._index_to_vertex.copy()

        # Deep copy: copy each row of the matrix
        new_matrix = DynamicUniversalArray()
        for i in range(len(self._matrix)):
            new_matrix.append(self._matrix[i].copy())
        new_graph._matrix = new_matrix
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

        Time complexity: O(V²)
        """
        if not isinstance(other, AdjacencyMatrixGraph):
            return NotImplemented
        if self._directed != other._directed or self._weighted != other._weighted:
            return False
        if self._size != other._size:
            return False

        for i in range(self._size):
            v1 = self._index_to_vertex[i]
            j_other = other._get_index(v1)
            if j_other is None:
                return False  # вершина есть в self, но нет в other
            for j in range(self._size):
                v2 = self._index_to_vertex[j]
                k_other = other._get_index(v2)
                if k_other is None:
                    return False
                if self._matrix[i][j] != other._matrix[j_other][k_other]:
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
