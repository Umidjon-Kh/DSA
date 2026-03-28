from typing import Any, Iterable, Iterator, Optional

from ...._base import BaseBoundedHeap
from ...._tools import validate_capacity, validate_value_type
from ....arrays import StaticTypedArray

_DTYPE_DEFAULTS = {
    int: 0,
    float: 0.0,
    bool: False,
    str: "",
}


class StaticTypedMinHeap(BaseBoundedHeap):
    """
    A fixed-capacity min-heap backed by StaticTypedArray.
    Enforces a single element type for all items.
    The root is always the smallest element.

    Supported dtypes: int, float, bool, str

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

    __slots__ = ("_data", "_size", "_dtype", "_str_length")

    def __init__(
        self,
        dtype: type,
        *args,
        str_length: Optional[int] = None,
        capacity: Optional[int] = None,
    ) -> None:
        """
        Creates a fixed-capacity typed min-heap with optional initial elements.

        Args:
            dtype:      Element type. Supported: int, float, bool, str.
            capacity:   Maximum number of elements the heap can hold.
            *args:      Optional initial elements. Heap property is established
                        via heapify — order of args does not matter.
            str_length: Max characters per str element (default: 20).

        Raises:
            TypeError:     If dtype is not a supported type.
            TypeError:     If capacity is not an int.
            ValueError:    If capacity < 1.
            TypeError:     If any element in args is not dtype.
            OverflowError: If len(args) > capacity.
            TypeError:     If not provided at least one argument or capacity value.

        Examples:
            h = StaticTypedMinHeap(int, capacity=5)           # empty, capacity=5
            h = StaticTypedMinHeap(int, 5, 3, 1, capacity=5)  # root=1, capacity=5
        """
        self._dtype: type = dtype
        self._size: int = 0
        cap: int = validate_capacity(capacity, len(args), "StaticTypedMinHeap")
        self._data: StaticTypedArray = StaticTypedArray(
            dtype=dtype, capacity=cap, str_length=str_length
        )
        self._str_length: int = self._data._str_length

        if args:
            self.heapify(args)

    # -------------------------------------------------------------------------
    # Internal helpers

    def _swap(self, i: int, j: int) -> None:
        """
        Swaps elements at indices i and j in the internal array.

        Time complexity: O(1)
        """
        tmp = self._data._raw_get(i)
        self._data._raw_set(i, self._data._raw_get(j))
        self._data._raw_set(j, tmp)

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
            if self._data._raw_get(index) < self._data._raw_get(parent):
                self._swap(index, parent)
                index = parent
            else:
                break

    def _sift_down(self, index: int) -> None:
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
            smallest = index
            left = 2 * index + 1
            right = 2 * index + 2

            if left < self._size and self._data._raw_get(left) < self._data._raw_get(
                smallest
            ):
                smallest = left

            if right < self._size and self._data._raw_get(right) < self._data._raw_get(
                smallest
            ):
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
            OverflowError: If heap is full.
            TypeError:     If value is not dtype.
        """
        if self.is_full():
            raise OverflowError(f"Heap is full (capacity={len(self._data)})")
        validate_value_type(value, self._dtype)
        self._data._raw_set(self._size, value)
        self._sift_up(self._size)
        self._size += 1

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
        root = self._data._raw_get(0)
        self._size -= 1
        if self._size > 0:
            self._data._raw_set(0, self._data._raw_get(self._size))
            self._sift_down(0)
        self._data._raw_set(self._size, _DTYPE_DEFAULTS[self._dtype])
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
        return self._data._raw_get(0)

    def heapify(self, iterable: Iterable[Any]) -> None:
        """
        Builds the heap in-place from an iterable in O(n) time.

        Replaces any existing elements. Loads all values into the internal
        array then applies Floyd's algorithm — sift_down from the last
        non-leaf node up to the root.

        Time complexity: O(n)

        Args:
            iterable: Any iterable of dtype values.

        Raises:
            TypeError:     If iterable is not iterable.
            TypeError:     If any value is not dtype.
            OverflowError: If len(iterable) > capacity.
        """
        try:
            values = list(iterable)
        except TypeError:
            raise TypeError(f"Expected an iterable, got {type(iterable).__name__!r}")
        if len(values) > len(self._data):
            raise OverflowError(
                f"Too many elements: {len(values)} > capacity {len(self._data)}"
            )
        self._size += len(values)
        for i, value in enumerate(values):
            validate_value_type(value, self._dtype)
            self._data._raw_set(i, value)

        for i in range(self._size // 2 - 1, -1, -1):
            self._sift_down(i)

    def clear(self) -> None:
        """
        Removes all elements. Does not reallocate the buffer.

        Time complexity: O(n)
        """
        self._size = 0
        self._data.clear()

    def copy(self) -> "StaticTypedMinHeap":
        """
        Returns a shallow copy with the same dtype and capacity.

        Time complexity: O(n)
        """
        new_heap = StaticTypedMinHeap(
            self._dtype, capacity=len(self._data), str_length=self._str_length
        )
        for i in range(self._size):
            new_heap._data._raw_set(i, self._data._raw_get(i))
        new_heap._size = self._size
        return new_heap

    def ordered(self) -> Iterator[Any]:
        """
        Yields all elements in sorted order from smallest to largest.

        Works on a copy of the heap — the original is not modified.
        For unsorted internal order use __iter__ instead.

        Time complexity: O(n log n)
        """
        tmp = self.copy()
        while tmp._size > 0:
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
            yield self._data._raw_get(i)

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields elements in reverse internal array order (last to root).

        Time complexity: O(n)
        """
        for i in range(self._size - 1, -1, -1):
            yield self._data._raw_get(i)

    def __contains__(self, value: Any) -> bool:
        """
        Returns True if value exists in the heap. O(n)
        Returns False instantly for wrong type.
        """
        if (
            not isinstance(value, self._dtype)
            or self._dtype is int
            and isinstance(value, bool)
        ):
            return False
        for i in range(self._size):
            if self._data._raw_get(i) == value:
                return True
        return False

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both heaps have the same dtype, size, and elements
        in the same internal positions.
        """
        if not isinstance(other, StaticTypedMinHeap):
            return NotImplemented
        if self._size != other._size or self._dtype != other._dtype:
            return False
        for i in range(self._size):
            if self._data._raw_get(i) != other._data._raw_get(i):
                return False
        return True

    def __repr__(self) -> str:
        """
        Returns string representation of the heap.
        Format: StaticTypedMinHeap(int, size=3, capacity=5)[1, 3, 2]
                                                             root

        Time complexity: O(n)
        """
        elements = ", ".join(repr(self._data._raw_get(i)) for i in range(self._size))
        return (
            f"StaticTypedMinHeap({self._dtype.__name__}, "
            f"size={self._size}, capacity={len(self._data)})"
            f"[{elements}]"
        )
