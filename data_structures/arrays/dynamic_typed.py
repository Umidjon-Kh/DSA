from typing import Any, Iterator

from ..tools import validate_index, validate_insert_index
from .static_typed import StaticTypedArray

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
        append:       O(1) amortized — O(n) on resize
        insert:       O(n) — shifts elements to the right
        remove:       O(n) — shifts elements to the left
        __getitem__:  O(1)
        __setitem__:  O(1) — only for existing indices (0 to size-1)
        __len__:      O(1)
        __iter__:     O(n)
        __contains__: O(n)
        __repr__:     O(n)
        _resize:      O(n)
    """

    __slots__ = ("_data", "_capacity", "_size", "_dtype", "_str_length")

    def __init__(self, dtype: type, *args, str_length: int = 1) -> None:
        """
        Creates a typed dynamic array with optional initial elements.

        Args:
            dtype:      Element type. Supported: int, float, bool, str.
            *args:      Optional initial elements. Must all be of type dtype.
            str_length: Max characters per str element (default: 1). Ignored for other dtypes.

        Raises:
            TypeError: If dtype is not a supported type.
            TypeError: If any element in args is not dtype.

        Examples:
            arr = DynamicTypedArray(int)           # empty, capacity=4
            arr = DynamicTypedArray(int, 1, 2, 3)  # [1, 2, 3], capacity=4
            arr = DynamicTypedArray(int, *range(10))  # capacity grows automatically
        """
        self._dtype: type = dtype
        self._str_length: int = str_length
        self._size: int = 0
        self._capacity: int = max(4, len(args))
        self._data: StaticTypedArray = StaticTypedArray(
            dtype, self._capacity, str_length=str_length
        )

        for item in args:
            self.append(item)

    # -------------------------------------------------------------------------
    # Internal helpers

    def _resize(self) -> None:
        """
        Allocates a larger buffer and copies existing elements into it.
        Uses CPython's growth formula to amortize resize cost.

        Growth formula:
            new_capacity = capacity + (capacity >> 3) + (3 if capacity < 9 else 6)

        Time complexity: O(n)
        """
        new_capacity = (
            self._capacity + (self._capacity >> 3) + (3 if self._capacity < 9 else 6)
        )
        new_data = StaticTypedArray(
            self._dtype, new_capacity, str_length=self._str_length
        )
        for i in range(self._size):
            new_data._raw_set(i, self._data._raw_get(i))
        self._data = new_data
        self._capacity = new_capacity

    # -------------------------------------------------------------------------
    # Core operations

    def append(self, value: Any) -> None:
        """
        Appends value to the end of the array.
        Triggers resize if size == capacity.

        Time complexity: O(1) amortized — O(n) on resize

        Raises:
            TypeError: If value is not dtype.
        """
        if (
            not isinstance(value, self._dtype)
            or self._dtype is int
            and isinstance(value, bool)
        ):
            raise TypeError(
                f"Expected {self._dtype.__name__}, got {type(value).__name__!r}"
            )
        if self._size == self._capacity:
            self._resize()
        self._data._raw_set(self._size, value)
        self._size += 1

    def insert(self, index: int, value: Any) -> None:
        """
        Inserts value at given index, shifting elements to the right.
        Supports negative indexing. Allows index == size (insert at end).

        Time complexity: O(n)

        Raises:
            TypeError:  If index is not int or value is not dtype.
            IndexError: If index is out of range.
        """
        index = validate_insert_index(index, self._size)
        if (
            not isinstance(value, self._dtype)
            or self._dtype is int
            and isinstance(value, bool)
        ):
            raise TypeError(
                f"Expected {self._dtype.__name__}, got {type(value).__name__!r}"
            )
        if self._size == self._capacity:
            self._resize()

        # Shift elements right
        for i in range(self._size, index, -1):
            self._data._raw_set(i, self._data._raw_get(i - 1))

        self._data._raw_set(index, value)
        self._size += 1

    def remove(self, index: int) -> Any:
        """
        Removes and returns element at given index, shifting elements left.
        Supports negative indexing.

        Time complexity: O(n)

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range or array is empty.
        """
        if self._size == 0:
            raise IndexError("Remove from an empty array")
        index = validate_index(index, self._size)
        value = self._data._raw_get(index)

        # Shift elements left
        for i in range(index, self._size - 1):
            self._data._raw_set(i, self._data._raw_get(i + 1))

        # Reset last slot to default
        self._data._raw_set(self._size - 1, _DTYPE_DEFAULTS[self._dtype])
        self._size -= 1
        return value

    # -------------------------------------------------------------------------
    # Dunder methods

    def __getitem__(self, index: int) -> Any:
        """
        Returns element at given index. Supports negative indexing.
        Only valid for indices 0 to size-1 (not full capacity).

        Time complexity: O(1)

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range.
        """
        index = validate_index(index, self._size)
        return self._data._raw_get(index)

    def __setitem__(self, index: int, value: Any) -> None:
        """
        Sets element at given index. Supports negative indexing.
        Only valid for existing indices (0 to size-1).

        Time complexity: O(1)

        Raises:
            TypeError:  If index is not int or value is not dtype.
            IndexError: If index is out of range.
        """
        index = validate_index(index, self._size)
        if (
            not isinstance(value, self._dtype)
            or self._dtype is int
            and isinstance(value, bool)
        ):
            raise TypeError(
                f"Expected {self._dtype.__name__}, got {type(value).__name__!r}"
            )
        self._data._raw_set(index, value)

    def __len__(self) -> int:
        """Returns number of elements currently in the array. O(1)"""
        return self._size

    def __iter__(self) -> Iterator[Any]:
        """Yields elements from index 0 to size-1. O(n)"""
        for i in range(self._size):
            yield self._data._raw_get(i)

    def __reversed__(self) -> Iterator[Any]:
        """Yields elements from right to left(back -> start). O(n)"""
        for i in range(self._size - 1, -1, -1):
            yield self._data._raw_get(i)

    def __contains__(self, value: Any) -> bool:
        """
        Returns True if value exists in the array. O(n)
        Returns False instantly if received value type is not matchs data type.
        """
        if (
            not isinstance(value, self._dtype)
            or self._dtype is int
            and isinstance(value, bool)
        ):
            return False
        for i in range(self._capacity):
            if self._data._raw_get(i) == value:
                return True
        return False

    def __repr__(self) -> str:
        """
        Returns string representation of the array.
        Format: DynamicTypedArray(int, size=3, capacity=4)[1, 2, 3]

        Time complexity: O(n)
        """
        elements = ", ".join(repr(self._data._raw_get(i)) for i in range(self._size))
        return (
            f"DynamicTypedArray({self._dtype.__name__}, "
            f"size={self._size}, capacity={self._capacity})"
            f"[{elements}]"
        )
