from typing import Any, Iterable, Iterator, Optional

from ...._base import BaseHeap
from ....arrays import DynamicTypedArray


class DynamicTypedMinHeap(BaseHeap):
    """
    A resizable min-heap backed by DynamicTypedArray.
    Enforces a single element type for all items.
    The root is always the smallest element.

    Supported dtypes: int, float, bool, str

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

    __slots__ = ("_data", "_dtype", "_str_length")

    def __init__(
        self,
        dtype: type,
        *args,
        str_length: Optional[int] = None,
    ) -> None:
        """
        Creates a resizable typed min-heap with optional initial elements.

        Args:
            dtype:      Element type. Supported: int, float, bool, str.
            *args:      Optional initial elements. Heap property is established
                        via heapify — order of args does not matter.
            str_length: Max characters per str element (default: 20).

        Raises:
            TypeError: If dtype is not a supported type.
            TypeError: If any element in args is not dtype.

        Examples:
            h = DynamicTypedMinHeap(int)            # empty
            h = DynamicTypedMinHeap(int, 5, 3, 1)   # root=1
        """
        self._dtype: type = dtype
        self._data: DynamicTypedArray = DynamicTypedArray(
            dtype=dtype, str_length=str_length
        )
        self._str_length: int = self._data._str_length

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
        Type validation is handled by DynamicTypedArray.append internally.

        Time complexity: O(log n) amortized — O(n) on resize

        Raises:
            TypeError: If value is not dtype.
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
        length = len(self._data)
        if length == 1:
            self._data.remove(0)
            return root
        last = self._data[length - 1]
        self._data.remove(length - 1)
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
            iterable: Any iterable of dtype values.

        Raises:
            TypeError: If iterable is not iterable.
            TypeError: If any value is not dtype.
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

    def copy(self) -> "DynamicTypedMinHeap":
        """
        Returns a shallow copy with the same dtype and elements.

        Time complexity: O(n)
        """
        new_heap = DynamicTypedMinHeap(dtype=self._dtype, str_length=self._str_length)
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
        """
        Returns True if value exists in the heap. O(n)
        Returns False instantly for wrong type.
        """
        return value in self._data

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both heaps have the same dtype, size, and elements
        in the same internal positions.
        """
        if not isinstance(other, DynamicTypedMinHeap):
            return NotImplemented
        if self._dtype != other._dtype or len(self._data) != len(other._data):
            return False
        for i in range(len(self._data)):
            if self._data[i] != other._data[i]:
                return False
        return True

    def __repr__(self) -> str:
        """
        Returns string representation of the heap.
        Format: DynamicTypedMinHeap(int, size=3)[1, 3, 2]
                                                  root

        Time complexity: O(n)
        """
        elements = ", ".join(repr(self._data[i]) for i in range(len(self._data)))
        return (
            f"DynamicTypedMinHeap({self._dtype.__name__}, "
            f"size={len(self._data)})"
            f"[{elements}]"
        )
