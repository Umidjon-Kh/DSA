from abc import abstractmethod
from typing import Any, Iterable, Iterator

from .base_collection import BaseCollection


class BaseHeap(BaseCollection):
    """
    Abstract base class for all heap types.

    Defines the interface for a complete binary tree that satisfies
    the heap property — every parent compares correctly with its children.
    Both min-heaps and max-heaps inherit from this, as do
    array-based and node-based implementations.

    Subclass:
        BaseBoundedHeap — adds capacity tracking and is_full check
                          for fixed-size heap implementations

    Required to implement (in addition to BaseCollection):
        push, pop, peek, is_empty, heapify, _sift_up, _sift_down
    """

    __slots__ = ()

    @abstractmethod
    def push(self, value: Any) -> None:
        """
        Inserts value into the heap and restores the heap property.

        Adds value at the end of the internal structure, then calls
        _sift_up to bubble it up to its correct position.

        Time complexity: O(log n)

        Raises:
            OverflowError: If the heap is full (bounded heaps only).
            TypeError:     If value type does not match dtype (typed heaps only).
        """
        ...

    @abstractmethod
    def pop(self) -> Any:
        """
        Removes and returns the root element (minimum or maximum).

        Swaps the root with the last element, removes the last element,
        then calls _sift_down to restore the heap property from the root.

        Time complexity: O(log n)

        Raises:
            IndexError: If the heap is empty.
        """
        ...

    @abstractmethod
    def peek(self) -> Any:
        """
        Returns the root element without removing it.

        The root is always the minimum (min-heap) or maximum (max-heap).

        Time complexity: O(1)

        Raises:
            IndexError: If the heap is empty.
        """
        ...

    @abstractmethod
    def is_empty(self) -> bool:
        """Returns True if the heap contains no elements."""
        ...

    @abstractmethod
    def heapify(self, iterable: Iterable[Any]) -> None:
        """
        Builds the heap in-place from an iterable in O(n) time.

        Replaces any existing elements. Uses the Floyd algorithm —
        applies _sift_down from the last non-leaf node up to the root.

        Time complexity: O(n)

        Args:
            iterable: Any iterable of values to build the heap from.

        Raises:
            TypeError: If iterable is not iterable.
            TypeError: If any value type does not match dtype (typed heaps only).
        """
        ...

    @abstractmethod
    def _sift_up(self, index: int) -> None:
        """
        Restores the heap property by moving element at index upward.

        Compares element at index with its parent repeatedly,
        swapping them while the heap property is violated.
        Stops when the element reaches the root or finds a valid position.

        Time complexity: O(log n)

        Args:
            index: The index of the element to sift up.
        """
        ...

    @abstractmethod
    def _sift_down(self, index: int) -> None:
        """
        Restores the heap property by moving element at index downward.

        Compares element at index with its children repeatedly,
        swapping with the more extreme child while the heap property
        is violated. Stops at a leaf or when no swap is needed.

        Time complexity: O(log n)

        Args:
            index: The index of the element to sift down.
        """
        ...

    def ordered(self) -> Iterator[Any]:
        """
        Yields all elements in sorted order from smallest to largest.

        Works on a copy of the heap — the original is not modified.
        For unsorted internal order use __iter__ instead.

        Time complexity: O(n log n)
        """
        ...


class BaseBoundedHeap(BaseHeap):
    """
    Abstract base class for fixed-capacity heaps.

    Extends BaseHeap with capacity tracking and a fullness check.
    Used by array-based static heap implementations.

    Required to implement (in addition to BaseHeap):
        is_full
    """

    __slots__ = ()

    @abstractmethod
    def is_full(self) -> bool:
        """Returns True if size == capacity."""
        ...
