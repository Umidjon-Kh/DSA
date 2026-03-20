from typing import Any, Iterator

from ..tools import validate_index, validate_insert_index
from .static_universal import StaticUniversalArray


class DynamicUniversalArray:
    """
    A dynamic array that grows automatically when capacity is exceeded.
    Built on top of StaticUniversalArray — accepts any Python object.

    When capacity is full, creates a new StaticUniversalArray using
    CPython's growth formula and copies all elements. Old array is
    discarded and collected by GC.

    Growth formula (same as CPython list):
        new_capacity = capacity + (capacity >> 3) + (3 if capacity < 9 else 6)

    Initial capacity: max(4, len(args))

    Time complexity:
        append:      O(1) amortized — O(n) on resize
        insert:      O(n) — shifts all elements to the right
        remove:      O(n) — shifts all elements to the left
        __getitem__: O(1)
        __setitem__: O(1) — only for existing indices (0 to size-1)
        __len__:     O(1)
        __iter__:    O(n)
        _resize:     O(n)
    """

    __slots__ = ("_data", "_capacity", "_size")

    def __init__(self, *args) -> None:
        """
        Creates a dynamic array with optional initial elements.
        Initial capacity is max(4, len(args)) to avoid
        immediate resize when elements are provided.

        Args:
            *args: Optional initial elements of any type.

        Examples:
            arr = DynamicUniversalArray()           # empty, capacity=4
            arr = DynamicUniversalArray(1, 2, 3)    # capacity=4, size=3
            arr = DynamicUniversalArray(*range(10)) # capacity=10, size=10
        """
        self._capacity = max(4, len(args))
        self._size = 0
        self._data = StaticUniversalArray(self._capacity)
        for item in args:
            self.append(item)

    def _resize(self) -> None:
        """
        Grows capacity using CPython's list growth formula and copies
        all existing elements into the new StaticUniversalArray.
        Old array is discarded and collected by GC.

        Called automatically by append and insert when size == capacity.
        Never call this manually.

        Time complexity: O(n)
        """
        new_capacity = (
            self._capacity + (self._capacity >> 3) + (3 if self._capacity < 9 else 6)
        )
        new_data = StaticUniversalArray(new_capacity)
        for index in range(self._size):
            new_data[index] = self._data[index]
        self._data = new_data
        self._capacity = new_capacity

    def append(self, value: Any) -> None:
        """
        Adds value to the end of the array.
        If capacity is exceeded — triggers _resize() first.

        Time complexity: O(1) amortized, O(n) on resize.
        """
        if self._size == self._capacity:
            self._resize()
        self._data[self._size] = value
        self._size += 1

    def insert(self, index: Any, value: Any) -> None:
        """
        Inserts value at given index by shifting all elements
        to the right of index one position forward.
        If capacity is exceeded — triggers _resize() first.
        Allows index == size (insert at end).

        Time complexity: O(n) — shifts up to n elements.

        Raises:
            TypeError:  if index is not int.
            IndexError: if index is out of range.
        """
        index = validate_insert_index(index, self._size)
        if self._size == self._capacity:
            self._resize()
        for idx in range(self._size, index, -1):
            self._data[idx] = self._data[idx - 1]
        self._data[index] = value
        self._size += 1

    def remove(self, index: Any) -> Any:
        """
        Removes and returns element at given index by shifting all
        elements to the right of index one position backward.
        Does not resize down — capacity stays the same.

        Time complexity: O(n) — shifts up to n elements.

        Returns:
            Removed value.

        Raises:
            TypeError:  if index is not int.
            IndexError: if index is out of range.
        """
        index = validate_index(index, self._size)
        removed = self._data[index]
        for idx in range(index, self._size - 1):
            self._data[idx] = self._data[idx + 1]
        self._data[self._size - 1] = None
        self._size -= 1
        return removed

    def __getitem__(self, index: Any) -> Any:
        """Returns value at given index. O(1)."""
        index = validate_index(index, self._size)
        return self._data[index]

    def __setitem__(self, index: Any, value: Any) -> None:
        """
        Replaces value at given index.
        Only works for existing indices (0 to size-1).
        Use append or insert to add new elements. O(1).
        """
        index = validate_index(index, self._size)
        self._data[index] = value

    def __len__(self) -> int:
        """Returns number of elements (not capacity)."""
        return self._size

    def __iter__(self) -> Iterator[Any]:
        """Iterates only filled elements (0 to size-1)."""
        for index in range(self._size):
            yield self._data[index]

    def __repr__(self) -> str:
        items = [self._data[i] for i in range(self._size)]
        return f"DynamicUniversalArray(size={self._size}, capacity={self._capacity}, items={items})"
