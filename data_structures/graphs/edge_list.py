from typing import Any, Iterator, List, Optional, Tuple, Union

from .._base import BaseEdgeListGraph
from ..arrays import DynamicUniversalArray


class EdgeListGraph(BaseEdgeListGraph):
    """
    A graph backed by a flat DynamicUniversalArray of (v1, v2, weight) tuples.

    The primary entity is the edge — vertices exist only as endpoints.
    There is no separate vertex registry; get_vertices() derives all unique
    vertices by scanning the edge list.

    Supports directed and undirected, weighted and unweighted modes
    controlled by constructor flags.

    For unweighted graphs, weight is always stored as None.
    For undirected graphs, every edge is stored once in insertion order
    (not both directions), but has_edge(v1, v2) and has_edge(v2, v1)
    both return True.

    __len__ returns the number of edges (not vertices).
    __iter__ yields (v1, v2, weight) tuples in insertion order.

    Time complexity:
        add_edge:       O(E) — duplicate check scans the list
        remove_edge:    O(E)
        has_edge:       O(E)
        get_edges:      O(E)
        get_vertices:   O(E)
        clear:          O(1)
        copy:           O(E)
        __len__:        O(1)
        __bool__:       O(1)
        __iter__:       O(E)
        __reversed__:   O(E)
        __contains__:   O(E)
        __eq__:         O(E²)
        __repr__:       O(1)
    """

    __slots__ = ("_edges", "_directed", "_weighted", "_size")

    def __init__(
        self, *args: Tuple, directed: bool = False, weighted: bool = False
    ) -> None:
        """
        Creates an EdgeListGraph with optional initial edges.

        Each positional argument must be a tuple:
            (v1, v2)     — adds an unweighted edge between v1 and v2
            (v1, v2, w)  — adds a weighted edge (only if weighted=True)

        Note: single-vertex tuples (v1,) are not supported — in an edge list
        vertices exist only as endpoints of edges.

        Args:
            *args:    Tuples representing edges.
            directed: If True, edges are one-directional. Default False.
            weighted: If True, edges store a numeric weight. Default False.

        Examples:
            g = EdgeListGraph()
            g = EdgeListGraph((1, 2), (2, 3))
            g = EdgeListGraph((1, 2, 0.5), (2, 3, 1.0), weighted=True)
            g = EdgeListGraph((1, 2), directed=True)

        Raises:
            ValueError: If an argument is not a tuple with 2 or 3 elements.
            ValueError: If v1 == v2 (self-loops are not supported).
            ValueError: If graph is weighted and weight is not provided.
        """
        self._edges: DynamicUniversalArray = DynamicUniversalArray()
        self._directed: bool = directed
        self._weighted: bool = weighted
        self._size: int = 0  # number of edges

        for item in args:
            if not isinstance(item, tuple) or len(item) not in (2, 3):
                raise ValueError(
                    f"Each argument must be a tuple with 2 or 3 elements, got: {item!r}"
                )
            if len(item) == 2:
                self.add_edge(item[0], item[1])
            else:
                self.add_edge(item[0], item[1], item[2])

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

        If the edge already exists, does nothing.
        For undirected graphs, the edge is stored once and both directions
        are considered equivalent.

        Weight is stored only if the graph was created with weighted=True.
        If weighted=True and weight is not provided, raises ValueError.
        If weighted=False, weight is ignored entirely.

        Time complexity: O(E) — duplicate check scans the list

        Raises:
            ValueError: If v1 == v2 (self-loops are not supported).
            ValueError: If graph is weighted and weight is not provided.
        """
        if v1 == v2:
            raise ValueError("Self-loops are not supported.")
        if self._weighted and weight is None:
            raise ValueError("Graph is weighted — weight must be provided.")

        if self.has_edge(v1, v2):
            return

        stored_weight = weight if self._weighted else None
        self._edges.append((v1, v2, stored_weight))
        self._size += 1

    def remove_edge(self, v1: Any, v2: Any) -> None:
        """
        Removes the edge between v1 and v2.

        If the edge does not exist, does nothing.
        For undirected graphs, either direction (v1→v2 or v2→v1) matches.

        Time complexity: O(E)
        """
        new_edges: DynamicUniversalArray = DynamicUniversalArray()
        removed = False

        for i in range(len(self._edges)):
            a, b, w = self._edges[i]
            match = (a == v1 and b == v2) or (
                not self._directed and a == v2 and b == v1
            )
            if match and not removed:
                removed = True  # skip only the first matching edge
            else:
                new_edges.append((a, b, w))

        if removed:
            self._edges = new_edges
            self._size -= 1

    def has_edge(self, v1: Any, v2: Any) -> bool:
        """
        Returns True if an edge exists between v1 and v2.

        For undirected graphs, has_edge(v1, v2) == has_edge(v2, v1).
        For directed graphs, has_edge(v1, v2) may differ from has_edge(v2, v1).

        Time complexity: O(E)
        """
        for i in range(len(self._edges)):
            a, b, _ = self._edges[i]
            if a == v1 and b == v2:
                return True
            if not self._directed and a == v2 and b == v1:
                return True
        return False

    def get_edges(self) -> List[Tuple[Any, Any, Optional[Union[int, float]]]]:
        """
        Returns a list of all edges as (v1, v2, weight) tuples.

        For unweighted graphs, weight is always None.
        For undirected graphs, each edge appears once in insertion order.

        Time complexity: O(E)
        """
        result = []
        for i in range(len(self._edges)):
            result.append(self._edges[i])
        return result

    def get_vertices(self) -> List[Any]:
        """
        Returns a list of all unique vertices derived from the edge list.

        Order is determined by first appearance across all edges (v1 before v2).
        Vertices that appear only as v2 are included after their first v1 mention.

        Time complexity: O(E)
        """
        seen = []
        for i in range(len(self._edges)):
            a, b, _ = self._edges[i]
            if a not in seen:
                seen.append(a)
            if b not in seen:
                seen.append(b)
        return seen

    def get_weight(self, v1: Any, v2: Any) -> Optional[Union[int, float]]:
        """
        Returns the weight of the edge between v1 and v2, or None if unweighted.

        For undirected graphs, either direction matches.

        Time complexity: O(E)

        Raises:
            KeyError: If the edge does not exist.
        """
        for i in range(len(self._edges)):
            a, b, w = self._edges[i]
            if a == v1 and b == v2:
                return w
            if not self._directed and a == v2 and b == v1:
                return w
        raise KeyError(f"Edge ({v1!r}, {v2!r}) does not exist.")

    # -------------------------------------------------------------------------
    # Collection methods

    def clear(self) -> None:
        """
        Removes all edges from the graph.

        Time complexity: O(1)
        """
        self._edges = DynamicUniversalArray()
        self._size = 0

    def copy(self) -> "EdgeListGraph":
        """
        Returns a shallow copy of the graph preserving all edges
        and constructor flags.

        Time complexity: O(E)
        """
        new_graph = EdgeListGraph(directed=self._directed, weighted=self._weighted)
        for i in range(len(self._edges)):
            a, b, w = self._edges[i]
            new_graph._edges.append((a, b, w))
        new_graph._size = self._size
        return new_graph

    # -------------------------------------------------------------------------
    # Dunder methods

    def __len__(self) -> int:
        """Returns the number of edges in the graph. O(1)"""
        return self._size

    def __bool__(self) -> bool:
        """Returns True if the graph contains at least one edge. O(1)"""
        return self._size > 0

    def __iter__(self) -> Iterator[Tuple[Any, Any, Optional[Union[int, float]]]]:
        """Yields (v1, v2, weight) tuples in insertion order. O(E)"""
        for i in range(len(self._edges)):
            yield self._edges[i]

    def __reversed__(self) -> Iterator[Tuple[Any, Any, Optional[Union[int, float]]]]:
        """Yields (v1, v2, weight) tuples in reverse insertion order. O(E)"""
        for i in range(self._size - 1, -1, -1):
            yield self._edges[i]

    def __contains__(self, value: Any) -> bool:
        """
        Returns True if value is a vertex that appears in any edge.

        Time complexity: O(E)
        """
        for i in range(len(self._edges)):
            a, b, _ = self._edges[i]
            if a == value or b == value:
                return True
        return False

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both graphs have the same edges (same set of tuples),
        weights, and constructor flags. Order does not matter.

        Time complexity: O(E²)
        """
        if not isinstance(other, EdgeListGraph):
            return NotImplemented
        if self._directed != other._directed or self._weighted != other._weighted:
            return False
        if self._size != other._size:
            return False

        # every edge in self must exist in other
        for i in range(len(self._edges)):
            a, b, w = self._edges[i]
            found = False
            for j in range(len(other._edges)):
                oa, ob, ow = other._edges[j]
                if a == oa and b == ob and w == ow:
                    found = True
                    break
            if not found:
                return False
        return True

    def __repr__(self) -> str:
        """
        Returns a string representation of the graph.
        Format: EdgeListGraph(edges=3, directed=False, weighted=True)

        Time complexity: O(1)
        """
        return (
            f"EdgeListGraph("
            f"edges={self._size}, "
            f"directed={self._directed}, "
            f"weighted={self._weighted})"
        )
