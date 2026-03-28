from typing import Any, Iterable, Iterator, Optional

from ...._base import BaseBoundedHeap
from ...._tools import validate_capacity
from ....arrays import StaticUniversalArray


class StaticUniversalMinHeap(BaseBoundedHeap):
    """
    A fixed-capacity min-heap backed by StaticUniversalArray.
    Accepts any Python objects.
    The root is always the smallest element.

    Time complexity:
        push:         O(log n)
        pop:          O(log n)
        peek:         O(1)
        heapify:      O(n)
        ordered:      O(n log n)
        clear:        O(n)
        copy:         O(n)
        is_empty:     O(1)
        is_full:      O(1)
        __len__:      O(1)
        __bool__:     O(1)
        __iter__:     O(n) — root to last (internal array order)
        __reversed__: O(n)
        __contains__: O(n)
        __repr__:     O(n)
        __eq__:       O(n)
    """

    __slots__ = ("_data", "_size")

    def __init__(self, *args, capacity: Optional[int] = None) -> None:
        """
        Creates a fixed-capacity universal min-heap with optional initial elements.

        Args:
            *args: Optional initial elements. Heap property is established
                   via heapify - order of args does not matter.
            capacity: Maximum number of elements the heap can hold.

        Raises:
            TypeError:     if capacity is provided but not integer.
            ValueError:    if capacity is less than or equal to 0.
            OverflowError: if len(args) > capacity.
            TypeError:     if not provided at least one argument or capacity value.

        Examples:
            h = StaticUniversalMinHeap(capacity=5)          # empty, capacity=5
            h = StaticUniversalMinHeap(5, 6, 7, 8, 8,)      # root=5, capacity=5
        """
        self._size: int = 0
        cap: int = validate_capacity(capacity, len(args), "StaticUniversalMinheap")
        self._data: StaticUniversalArray = StaticUniversalArray(capacity=cap)

        if args:
            self.heapify(args)

    # -------------------------------------------------------------------------
    # Internal helpers

    def _swap(self, first: int, second: int) -> None:
        """
        Swaps elements at indices i and j in the internal array.

        Time complexity: O(1)
        """
        tmp = self._data[first]
        self._data[first] = self._data[second]
        self._data[second] = tmp

    # -------------------------------------------------------------------------
    # Heap operations

    def _sift_up(self, index: int) -> None:
        """
        Restores the heap property by moving element at index upward.

        Compares element at index with its parent repeatedly,
        swapping them while the element is smaller than its parent.
        Stops when the element reaches the root or finds a valid position.

        Time complexity: O(log n)

        Args:
            index: The index of the element to sift up.
        """
        while index > 0:
            parent = (index - 1) // 2
            if self._data[index] < self._data[parent]:
                self._swap(index, parent)
                index = parent
            else:
                break

    def _sift_down(self, index: int) -> None:
        """
        restores the heap property by moving element at index downward.

        Compares element at index with its children repeatedly,
        swapping with the similar child while the heap property is violated.
        Stops at a leaf or when no swap is needed.

        Time complexity: O(log n)

        Args:
            index: The index of the element to sift down.
        """
        while True:
            smallest = index
            left = 2 * index + 1
            right = 2 * index + 1

            if left < self._size and self._data[left] < self._data[smallest]:
                smallest = left
            if right < self._size and self._data[right] < self._data[smallest]:
                smallest = right

            if smallest == index:
                break

            self._swap(index, smallest)
            index = smallest

    # -------------------------------------------------------------------------
    # Core operations
    def push(self, value: Any) -> None:
        """
        Inserts value into the heap and restores the heap property via sift_up.

        Time complexity: O(log n)

        Raises:
            OverflowError: if heap is full
        """
        if self.is_full():
            raise OverflowError(f"Heap if sull (capacity={len(self._data)})")
        self._data[self._size] = value
        self._sift_up(self._size)
        self._size += 1

    def pop(self) -> Any:
        """
        Removes and returns the root element (minimum).

        Swaps root with the last element, removes the last slot,
        then restores the heap property via sift_down from the root.

        Time complexiyt: O(log n)

        Raises:
            IndexError: if heap is empty.
        """
        if self.is_empty():
            raise IndexError("Pop from an empty heap")
        root = self._data[0]
        self._size -= 1
        if self._size > 0:
            self._data[0] = self._data[self._size]
            self._sift_down(0)
        self._data[self._size] = None
        return root

    def peek(self) -> Any:
        """
        Returns the root element (minimum) without removing it.

        Time complexity: O(1)

        Raises:
            IndexError: If heap is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from an empty heap")
        return self._data[0]
