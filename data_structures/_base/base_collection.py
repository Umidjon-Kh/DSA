from abc import ABC, abstractmethod
from typing import Any, Iterator


class BaseCollection(ABC):
    """
    Abstract base class for all collection types.

    Defines the shared interface that every data structure in this library
    must implement — regardless of whether it is an array, stack, queue,
    linked list, tree, graph, hash table, or heap.

    Subclasses specialize this by adding their own abstract methods
    (e.g. push/pop for stacks, enqueue/dequeue for queues).

    Required to implement:
        clear, copy
        __len__, __bool__, __iter__, __reversed__, __contains__, __repr__

    Time complexity of each method is defined by the concrete subclass.
    """

    @abstractmethod
    def clear(self) -> None:
        """Removes all elements from the collection."""
        ...

    @abstractmethod
    def copy(self) -> "BaseCollection":
        """Returns a shallow copy of the collection."""
        ...

    @abstractmethod
    def __len__(self) -> int:
        """Returns the number of elements currently in the collection."""
        ...

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """Returns True, if all data in objects are equal and same."""
        ...

    @abstractmethod
    def __bool__(self) -> bool:
        """Returns True if the collection contains at least one element."""
        ...

    @abstractmethod
    def __iter__(self) -> Iterator[Any]:
        """Yields elements from the collection in its natural order."""
        ...

    @abstractmethod
    def __reversed__(self) -> Iterator[Any]:
        """Yields elements in reverse order."""
        ...

    @abstractmethod
    def __contains__(self, value: Any) -> bool:
        """Returns True if value exists in the collection."""
        ...

    @abstractmethod
    def __repr__(self) -> str:
        """Returns a string representation of the collection."""
        ...
