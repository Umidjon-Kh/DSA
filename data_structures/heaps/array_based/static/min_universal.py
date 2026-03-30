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
        cap: int = validate_capacity(capacity, len(args), "StaticUniversalMinHeap")
        self._data: StaticUniversalArray = StaticUniversalArray(capacity=cap)

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

            if left < self._size and self._data[left] < self._data[smallest]:
                smallest = left
            if right < self._size and self._data[right] < self._data[smallest]:
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

        Time complexity: O(log n)

        Raises:
            OverflowError: if heap is full
        """
        if self.is_full():
            raise OverflowError(f"Heap is full (capacity={len(self._data)})")
        self._data[self._size] = value
        self._sift_up(self._size)
        self._size += 1

    def pop(self) -> Any:
        """
        Removes and returns the root element (minimum).

        Swaps root with the last element, removes the last slot,
        then restores the heap property via sift_down from the root.

        Time complexity: O(log n)

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

    def heapify(self, iterable: Iterable[Any]) -> None:
        """
        Builds the heap in-place from an iterable in O(n) time.

        Don't replaces any existing elements, only adds to the end.
        Loads all values into the internal array
        then applies Floyd's algorithm - sift_down from the last
        non leaf node up to the root.

        Time complexity: O(n)

        Args:
            iterable: Any iterable object.

        Raises:
            TypeError: If iterable is not iterable.
            OverflowError: if size + len(iterable) > capacity.
        """
        try:
            values = list(iterable)
        except TypeError:
            raise TypeError(f"Expected an iterable, got ({type(iterable).__name__!r})")
        if (self._size + len(values)) > len(self._data):
            raise OverflowError(
                f"Too many elements: {(self._size + len(values))} > capacity {len(self._data)}"
            )

        for i, value in enumerate(values, self._size):
            self._data[i] = value

        self._size += len(values)

        for i in range(self._size // 2 - 1, -1, -1):
            self._sift_down(i)

    def clear(self) -> None:
        """
        Removes all element. Does not reallocate the buffer.

        Time complexity: O(n)
        """
        self._size = 0
        self._data.clear()

    def copy(self) -> "StaticUniversalMinHeap":
        """
        Returns a shallow copy with the same capacity and data.

        Time complexity: O(n)
        """
        new_heap = StaticUniversalMinHeap(capacity=len(self._data))
        for i in range(self._size):
            new_heap._data[i] = self._data[i]
        new_heap._size = self._size
        return new_heap

    def ordered(self) -> Iterator[Any]:
        """
        Yields all elements in sorted order from smallest to largest.

        Works on a copy of the heap - the original is not modified.
        For unsorted internal order use __iter__ instead.

        Time complexity: O(n log n)
        """
        tmp = self.copy()
        for _ in range(tmp._size):
            yield tmp.pop()

    # -------------------------------------------------------------------------
    # State checks
    def is_empty(self) -> bool:
        """Returns True if the heap contains no elements. O(1)"""
        return self._size == 0

    def is_full(self) -> bool:
        """Returns True if the heap has reached its capacity. O(1)"""
        return self._size == len(self._data)

    # -------------------------------------------------------------------------
    # Dunder methods

    def __len__(self) -> int:
        """Returns number of elements currently in the heap. O(1)"""
        return self._size

    def __bool__(self) -> bool:
        """Returns True if the heap is not empty. O(1)"""
        return self._size > 0

    def __iter__(self) -> Iterator[Any]:
        """
        Yields elements in internal array order (root first).
        The result is not sorted — use ordered() for sorted iteration.

        Time complexity: O(n)
        """
        for i in range(self._size):
            yield self._data[i]

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields elements in reverse internal array order (last to root).

        Time complexity: O(n)
        """
        for i in range(self._size - 1, -1, -1):
            yield self._data[i]

    def __contains__(self, value: Any) -> bool:
        """
        Returns True if value exists in the heap. O(n)
        """
        for i in range(self._size):
            if self._data[i] == value:
                return True
        return False

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both heaps have the same dtype, size, and elements
        in the same internal positions.
        """
        if not isinstance(other, StaticUniversalMinHeap):
            return NotImplemented
        if self._size != other._size or self._data[0] != other._data[0]:
            return False
        for i in range(self._size):
            if self._data[i] != other._data[i]:
                return False
        return True

    def __repr__(self) -> str:
        """
        Returns string representation of the heap.
        Format: StaticUniversalMinHeap(size=3, capacity=5)[1, 3, 2]
                                                          root

        Time complexity: O(n)
        """
        elements = ", ".join(repr(self._data[i]) for i in range(self._size))
        return (
            f"StaticUniversalMinHeap(size={self._size}, capacity={len(self._data)})"
            f"[{elements}]"
        )
