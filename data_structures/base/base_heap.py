from abc import abstractmethod
from typing import Any

from .base_collection import BaseCollection


class BaseHeap(BaseCollection):
    """
    Abstract base class for all heap types.

    Defines the shared interface for min-heap and max-heap implementations.
    A heap always exposes the highest-priority element at the top —
    the smallest for min-heap, the largest for max-heap.

    Iteration yields elements in heap order (level-order), not sorted order.
    Use pop() repeatedly to consume elements in priority order.

    Required to implement (in addition to BaseCollection):
        push, pop, peek, is_empty
    """

    @abstractmethod
    def push(self, value: Any) -> None:
        """
        Inserts value into the heap and restores the heap property.

        Time complexity: O(log n)

        Raises:
            TypeError: If value is not comparable with existing elements.
        """
        ...

    @abstractmethod
    def pop(self) -> Any:
        """
        Removes and returns the top element (min or max depending on implementation).
        Restores the heap property after removal.

        Time complexity: O(log n)

        Raises:
            IndexError: If the heap is empty.
        """
        ...

    @abstractmethod
    def peek(self) -> Any:
        """
        Returns the top element without removing it.

        Time complexity: O(1)

        Raises:
            IndexError: If the heap is empty.
        """
        ...

    @abstractmethod
    def is_empty(self) -> bool:
        """Returns True if the heap contains no elements."""
        ...
