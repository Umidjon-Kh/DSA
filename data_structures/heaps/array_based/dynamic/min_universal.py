from typing import Any, Iterable, Iterator

from ...._base import BaseHeap
from ....arrays import DynamicUniversalArray


class DynamicUniversalMinHeap(BaseHeap):
    """
    A resizable min-heap backed by DynamicUniversalArray.
    Accepts any Python objects.
    The root is always the smallest element.

    Time complexity:
        push:         O(log n) amortized — O(n) on resize
        pop:          O(log n)
        peek:         O(1)
        heapify:      O(n) amortized
        ordered:      O(n log n)
        clear:        O(n)
        copy:         O(n)
        is_empty:     O(1)
        __len__:      O(1)
        __bool__:     O(1)
        __iter__:     O(n) — root to last (internal array order)
        __reversed__: O(n)
        __contains__: O(n)
        __repr__:     O(n)
        __eq__:       O(n)
    """

    __slots__ = ("_data",)

    def __init__(self, *args) -> None:
        """
        Creates a resizable universal min-heap with optional initial elements.

        Args:
            *args: Optional initial elements. Heap property is established
                   via heapify — order of args does not matter.

        Examples:
            h = DynamicUniversalMinHeap()          # empty
            h = DynamicUniversalMinHeap(5, 3, 1)   # root=1
        """
        self._data: DynamicUniversalArray = DynamicUniversalArray()

        if args:
            self.heapify(args)

    # -------------------------------------------------------------------------
    # Internal helpers

    def _swap(self, first: int, second: int) -> None:
        """
        Swaps elements at indices first and second in the internal array.

        Time complexity: O(1)
        """
        tmp = self._data[first]
        self._data[first] = self._data[second]
        self._data[second] = tmp

    # -------------------------------------------------------------------------
    # Heap operations

    def _sift_up(self, target: int) -> None:
        """
        Restores the heap property by moving element at index upward.

        Compares element at index with its parent repeatedly,
        swapping them while the element is smaller than its parent.
        Stops when the element reaches the root or finds a valid position.

        Time complexity: O(log n)

        Args:
            index: The index of the element to sift up.
        """
        while target > 0:
            parent = (target - 1) // 2
            if self._data[target] < self._data[parent]:
                self._swap(target, parent)
                target = parent
            else:
                break

    def _sift_down(self, target: int) -> None:
        """
        Restores the heap property by moving element at index downward.

        Compares element at index with its children repeatedly,
        swapping with the smaller child while the heap property is violated.
        Stops at a leaf or when no swap is needed.

        Time complexity: O(log n)

        Args:
            index: The index of the element to sift down.
        """
        while True:
            smallest = target
            left = 2 * target + 1
            right = 2 * target + 2
            size = len(self._data)

            if left < size and self._data[left] < self._data[smallest]:
                smallest = left
            if right < size and self._data[right] < self._data[smallest]:
                smallest = right

            if smallest == target:
                break

            self._swap(target, smallest)
            target = smallest

    # -------------------------------------------------------------------------
    # Core operations

    def push(self, value: Any) -> None:
        """
        Inserts value into the heap and restores the heap property via sift_up.

        Time complexity: O(log n) amortized — O(n) on resize
        """
        self._data.append(value)
        self._sift_up(len(self._data) - 1)

    def pop(self) -> Any:
        """
        Removes and returns the root element (minimum).

        Swaps root with the last element, removes the last slot,
        then restores the heap property via sift_down from the root.

        Time complexity: O(log n)

        Raises:
            IndexError: If heap is empty.
        """
        if self.is_empty():
            raise IndexError("Pop from an empty heap")
        root = self._data[0]
        n = len(self._data)
        if n == 1:
            self._data.remove(0)
            return root
        last = self._data[n - 1]
        self._data.remove(n - 1)
        self._data[0] = last
        self._sift_down(0)
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

    def heapify(self, iterable: Iterable[Any]) -> None:
        """
        Builds the heap in-place from an iterable in O(n) time.

        Does not replace existing elements, only appends to the end.
        Applies Floyd's algorithm — sift_down from the last
        non-leaf node up to the root.

        Time complexity: O(n) amortized

        Args:
            iterable: Any iterable object.

        Raises:
            TypeError: If iterable is not iterable.
        """
        try:
            values = list(iterable)
        except TypeError:
            raise TypeError(f"Expected an iterable, got ({type(iterable).__name__!r})")
        for value in values:
            self._data.append(value)

        for i in range(len(self._data) // 2 - 1, -1, -1):
            self._sift_down(i)

    def clear(self) -> None:
        """
        Removes all elements. Does not reallocate the buffer.

        Time complexity: O(n)
        """
        self._data.clear()

    def copy(self) -> "DynamicUniversalMinHeap":
        """
        Returns a shallow copy with the same elements.

        Time complexity: O(n)
        """
        new_heap = DynamicUniversalMinHeap()
        for i in range(len(self._data)):
            new_heap._data.append(self._data[i])
        return new_heap

    def ordered(self) -> Iterator[Any]:
        """
        Yields all elements in sorted order from smallest to largest.

        Works on a copy of the heap — the original is not modified.
        For unsorted internal order use __iter__ instead.

        Time complexity: O(n log n)
        """
        tmp = self.copy()
        while not tmp.is_empty():
            yield tmp.pop()

    # -------------------------------------------------------------------------
    # State checks

    def is_empty(self) -> bool:
        """Returns True if the heap contains no elements. O(1)"""
        return len(self._data) == 0

    # -------------------------------------------------------------------------
    # Dunder methods

    def __len__(self) -> int:
        """Returns number of elements currently in the heap. O(1)"""
        return len(self._data)

    def __bool__(self) -> bool:
        """Returns True if the heap is not empty. O(1)"""
        return len(self._data) > 0

    def __iter__(self) -> Iterator[Any]:
        """
        Yields elements in internal array order (root first).
        The result is not sorted — use ordered() for sorted iteration.

        Time complexity: O(n)
        """
        for i in range(len(self._data)):
            yield self._data[i]

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields elements in reverse internal array order (last to root).

        Time complexity: O(n)
        """
        for i in range(len(self._data) - 1, -1, -1):
            yield self._data[i]

    def __contains__(self, value: Any) -> bool:
        """Returns True if value exists in the heap. O(n)"""
        for i in range(len(self._data)):
            if self._data[i] == value:
                return True
        return False

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both heaps have the same size and elements
        in the same internal positions.
        """
        if not isinstance(other, DynamicUniversalMinHeap):
            return NotImplemented
        if len(self._data) != len(other._data):
            return False
        for i in range(len(self._data)):
            if self._data[i] != other._data[i]:
                return False
        return True

    def __repr__(self) -> str:
        """
        Returns string representation of the heap.
        Format: DynamicUniversalMinHeap(size=3)[1, 3, 2]
                                                 root

        Time complexity: O(n)
        """
        elements = ", ".join(repr(self._data[i]) for i in range(len(self._data)))
        return f"DynamicUniversalMinHeap(size={len(self._data)})[{elements}]"
