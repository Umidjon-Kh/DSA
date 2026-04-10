from abc import abstractmethod
from typing import Any, List, Optional, Tuple, Union

from .base_collection import BaseCollection


class BaseGraph(BaseCollection):
    """
    Abstract base class for all graph types.

    Defines the shared interface for adjacency list, adjacency matrix,
    and edge list graph implementations. Extends BaseCollection with
    graph-specific operations: vertex and edge management, neighbor
    queries, and structural checks.

    All graph implementations support directed and weighted modes
    controlled by constructor flags — no separate subclasses needed.

    Subclasses:
        AdjacencyListGraph   — dict-based, O(1) add vertex/edge, O(deg) neighbor lookup
        AdjacencyMatrixGraph — 2D matrix, O(1) edge lookup, O(V²) space

    Required to implement (in addition to BaseCollection):
        add_vertex, remove_vertex, get_vertices,
        add_edge, remove_edge, has_edge, get_neighbors
    """

    __slots__ = ()

    @abstractmethod
    def add_vertex(self, vertex: Any) -> None:
        """
        Adds vertex to the graph.

        If vertex already exists, does nothing.

        Time complexity: defined by subclass.
        """
        ...

    @abstractmethod
    def remove_vertex(self, vertex: Any) -> None:
        """
        Removes vertex and all its associated edges from the graph.

        If vertex does not exist, does nothing.

        Time complexity: defined by subclass.
        """
        ...

    @abstractmethod
    def get_vertices(self) -> List[Any]:
        """
        Returns a list of all vertices in the graph.

        Time complexity: defined by subclass.
        """
        ...

    @abstractmethod
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
        If weighted=False, weight is ignored entirely.

        Time complexity: defined by subclass.

        Raises:
            ValueError: If v1 == v2 (self-loops are not supported).
            ValueError: If graph is weighted and weight is not provided.
        """
        ...

    @abstractmethod
    def remove_edge(self, v1: Any, v2: Any) -> None:
        """
        Removes the edge between v1 and v2.

        If the edge does not exist, does nothing.
        For undirected graphs, both directions are removed.

        Time complexity: defined by subclass.
        """
        ...

    @abstractmethod
    def has_edge(self, v1: Any, v2: Any) -> bool:
        """
        Returns True if an edge exists between v1 and v2.

        For undirected graphs, has_edge(v1, v2) == has_edge(v2, v1).
        For directed graphs, has_edge(v1, v2) may differ from has_edge(v2, v1).

        Time complexity: defined by subclass.
        """
        ...

    @abstractmethod
    def get_neighbors(
        self, vertex: Any
    ) -> List[Tuple[Any, Optional[Union[int, float]]]]:
        """
        Returns a list of (neighbor, weight) pairs for the given vertex.

        For unweighted graphs, weight is always None.
        For weighted graphs, weight is the value assigned to that edge.

        Time complexity: defined by subclass.

        Raises:
            KeyError: If vertex does not exist in the graph.
        """
        ...


class BaseEdgeListGraph(BaseCollection):
    """
    Abstract base class for edge list graph implementations.

    Separate from BaseGraph because an edge list has fundamentally
    different semantics — the primary entity is the edge, not the
    vertex. Vertices exist only as endpoints of edges and cannot
    be added or removed independently.

    __len__ returns the number of edges (not vertices), and __iter__
    yields (v1, v2, weight) tuples — or (v1, v2, None) for unweighted graphs.

    Supports directed and weighted modes controlled by constructor flags.

    Subclasses:
        EdgeListGraph — flat list of edges, minimal memory, O(E) lookups

    Required to implement (in addition to BaseCollection):
        add_edge, remove_edge, has_edge, get_edges
    """

    __slots__ = ()

    @abstractmethod
    def add_edge(
        self,
        v1: Any,
        v2: Any,
        weight: Optional[Union[int, float]] = None,
    ) -> None:
        """
        Adds an edge between v1 and v2.

        For undirected graphs, both directions are stored.

        Weight is stored only if the graph was created with weighted=True.
        If weighted=True and weight is not provided, raises ValueError.
        If weighted=False, weight is ignored entirely.

        Time complexity: defined by subclass.

        Raises:
            ValueError: If v1 == v2 (self-loops are not supported).
            ValueError: If graph is weighted and weight is not provided.
        """
        ...

    @abstractmethod
    def remove_edge(self, v1: Any, v2: Any) -> None:
        """
        Removes the edge between v1 and v2.

        If the edge does not exist, does nothing.
        For undirected graphs, both directions are removed.

        Time complexity: defined by subclass.
        """
        ...

    @abstractmethod
    def has_edge(self, v1: Any, v2: Any) -> bool:
        """
        Returns True if an edge exists between v1 and v2.

        For undirected graphs, has_edge(v1, v2) == has_edge(v2, v1).
        For directed graphs, has_edge(v1, v2) may differ from has_edge(v2, v1).

        Time complexity: defined by subclass.
        """
        ...

    @abstractmethod
    def get_edges(self) -> List[Tuple[Any, Any, Optional[Union[int, float]]]]:
        """
        Returns a list of all edges as (v1, v2, weight) tuples.

        For unweighted graphs, weight is always None.
        For undirected graphs, each edge appears once — not both directions.

        Time complexity: defined by subclass.
        """
        ...
