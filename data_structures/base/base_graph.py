from abc import abstractmethod
from typing import Any, List

from .base_collection import BaseCollection


class BaseGraph(BaseCollection):
    """
    Abstract base class for all graph types.

    Defines the shared interface for adjacency list and adjacency matrix graphs.
    Supports both directed and undirected graphs — the directed flag is set
    at construction in the concrete implementation.

    Iteration yields all vertices in the graph.
    __reversed__ yields vertices in reverse insertion order.
    __contains__ checks for vertex existence.

    Required to implement (in addition to BaseCollection):
        add_vertex, add_edge, remove_vertex, remove_edge,
        get_neighbors, has_vertex, has_edge
    """

    @abstractmethod
    def add_vertex(self, vertex: Any) -> None:
        """
        Adds a vertex to the graph.

        Raises:
            ValueError: If vertex already exists in the graph.
        """
        ...

    @abstractmethod
    def add_edge(self, source: Any, destination: Any, weight: Any = None) -> None:
        """
        Adds an edge between source and destination.
        For undirected graphs, adds the reverse edge as well.

        Raises:
            KeyError:   If source or destination vertex does not exist.
            ValueError: If the edge already exists.
        """
        ...

    @abstractmethod
    def remove_vertex(self, vertex: Any) -> None:
        """
        Removes a vertex and all edges connected to it.

        Raises:
            KeyError: If vertex does not exist in the graph.
        """
        ...

    @abstractmethod
    def remove_edge(self, source: Any, destination: Any) -> None:
        """
        Removes the edge between source and destination.
        For undirected graphs, removes the reverse edge as well.

        Raises:
            KeyError:   If source or destination vertex does not exist.
            ValueError: If the edge does not exist.
        """
        ...

    @abstractmethod
    def get_neighbors(self, vertex: Any) -> List[Any]:
        """
        Returns a list of all vertices adjacent to given vertex.

        Raises:
            KeyError: If vertex does not exist in the graph.
        """
        ...

    @abstractmethod
    def has_vertex(self, vertex: Any) -> bool:
        """Returns True if vertex exists in the graph."""
        ...

    @abstractmethod
    def has_edge(self, source: Any, destination: Any) -> bool:
        """
        Returns True if an edge exists from source to destination.

        Raises:
            KeyError: If source or destination vertex does not exist.
        """
        ...
