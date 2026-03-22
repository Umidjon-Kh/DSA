from typing import Any, Iterator

from ...tools import validate_index, validate_insert_index
from ..static import StaticTypedArray

_DTYPE_DEFAULTS = {
    int: 0,
    float: 0.0,
    bool: False,
    str: "",
}


class DynamicTypedArray:
    """
    A dynamic array that grows automatically when capacity is exceeded.
    Built on top of StaticTypedArray — enforces a single type for all elements.

    Same resizing logic as DynamicUniversalArray but stores raw C values
    instead of PyObject pointers — less memory overhead per element.

    Supported dtypes: int, float, bool, str

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

    __slots__ = ("_data", "_capacity", "_size", "_dtype", "_str_length")

    def __init__(self, dtype: type, *args, str_length: Any = None) -> None:
        """
        Creates a typed dynamic array with optional initial elements.

        Args:
            dtype:      Element type. Supported: int, float, bool, str.
            *args:      Optional initial elements. Must match dtype.
            str_length: Max string length for dtype=str (default 20).

        Examples:
            arr = DynamicTypedArray(int)            # empty int array
            arr = DynamicTypedArray(int, 1, 2, 3)   # int array with elements
            arr = DynamicTypedArray(str, str_length=50)  # str array, max 50 chars
        """
        self._dtype = dtype
        self._str_length = str_length
        self._capacity = max(4, len(args))
        self._size = 0
        self._data = StaticTypedArray(
            self._capacity,
            dtype=dtype,
            str_length=str_length,
        )
        for item in args:
            self.append(item)

    def _resize(self) -> None:
        """
        Grows capacity using CPython's list growth formula and copies
        all existing elements into the new StaticTypedArray.
        Old array is discarded and collected by GC.

        Time complexity: O(n)
        """
        new_capacity = (
            self._capacity + (self._capacity >> 3) + (3 if self._capacity < 9 else 6)
        )
        new_data = StaticTypedArray(
            new_capacity,
            dtype=self._dtype,
            str_length=self._str_length,
        )
        for index in range(self._size):
            new_data[index] = self._data[index]
        self._data = new_data
        self._capacity = new_capacity

    def append(self, value: Any) -> None:
        """
        Adds value to the end of the array.
        Value must match dtype.
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
        Value must match dtype.
        If capacity is exceeded — triggers _resize() first.
        Allows index == size (insert at end).

        Time complexity: O(n)

        Raises:
            TypeError:  if index is not int or value does not match dtype.
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
        Removes and returns element at given index.
        Does not resize down — capacity stays the same.

        Time complexity: O(n)

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
        self._size -= 1
        self._data[self._size] = _DTYPE_DEFAULTS[self._dtype]
        return removed

    def __getitem__(self, index: Any) -> Any:
        """Returns value at given index. O(1)."""
        index = validate_index(index, self._size)
        return self._data[index]

    def __setitem__(self, index: Any, value: Any) -> None:
        """
        Replaces value at given index.
        Value must match dtype. O(1).
        """
        index = validate_index(index, self._size)
        self._data[index] = value

    def copy(self) -> "DynamicTypedArray":
        """
        Creates a shallow copy of the array.
        Time complexity: O(n)
        """
        copied = DynamicTypedArray(
            self._dtype,
            *[self._data[i] for i in range(self._size)],
            str_length=self._str_length,
        )
        return copied

    def __eq__(self, other: Any) -> bool:
        """Checks for equality of all data in both objects"""
        if not isinstance(other, DynamicTypedArray):
            return False
        if self._dtype != other._dtype or self._size != other._size:
            return False
        return all(self._data[i] == other._data[i] for i in range(self._size))

    def __len__(self) -> int:
        """Returns number of elements (not capacity)."""
        return self._size

    def __iter__(self) -> Iterator[Any]:
        """Iterates only filled elements (0 to size-1)."""
        for index in range(self._size):
            yield self._data[index]

    def __repr__(self) -> str:
        items = [self._data[i] for i in range(self._size)]
        return f"DynamicTypedArray(dtype={self._dtype.__name__}, size={self._size}, capacity={self._capacity}, items={items})"
