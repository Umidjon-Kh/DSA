import ctypes
from typing import Any, Iterator, Optional

from ..tools import validate_capacity, validate_index


class StaticUniversalArray:
    """
    A fixed-size array backed by a ctypes py_object buffer.
    Accepts any Python type — no dtype restriction.

    Stores PyObject pointers (references to Python objects),
    so memory overhead per element is higher than StaticTypedArray.
    Trade-off: flexibility vs memory efficiency.

    Initial elements default to None.

    capacity is optional — if omitted, it is derived from len(args).
    At least one of capacity or *args must be provided.

    Time complexity:
        clear:        O(n)
        copy:         O(n)
        __getitem__:  O(1)
        __setitem__:  O(1)
        __len__:      O(1)
        __bool__:     O(1)
        __iter__:     O(n)
        __reversed__: O(n)
        __contains__: O(n)
        __eq__:       O(n)
        __repr__:     O(n)
    """

    __slots__ = ("_data", "_capacity")

    def __init__(self, *args, capacity: Optional[int] = None) -> None:
        """
        Creates a fixed-size universal array with optional initial elements.

        Args:
            *args:    Optional initial elements of any type.
            capacity: Maximum number of elements the array can hold.
                      If omitted, capacity is set to len(args).
                      At least one of capacity or *args must be provided.

        Raises:
            TypeError:     If neither capacity nor args are provided.
            TypeError:     If capacity is provided but not an int.
            ValueError:    If capacity < 1.
            OverflowError: If len(args) > capacity.

        Examples:
            arr = StaticUniversalArray(capacity=5)           # [None, None, None, None, None]
            arr = StaticUniversalArray(1, "hi", 3)           # [1, 'hi', 3], capacity=3
            arr = StaticUniversalArray(1, "hi", capacity=5)  # [1, 'hi', None, None, None]
        """
        self._capacity: int = validate_capacity(
            capacity, len(args), "StaticUniversalArray"
        )
        self._data = (ctypes.py_object * self._capacity)()

        # Fill with None by default
        for i in range(self._capacity):
            self._data[i] = None

        # Set initial elements
        for i, val in enumerate(args):
            self._data[i] = val

    # -------------------------------------------------------------------------
    # Public interface
    def clear(self) -> None:
        """
        Resets all elements to their dtype default value.
        Time complexity: O(n)
        """
        for i in range(self._capacity):
            self._data[i] = None

    def copy(self) -> "StaticUniversalArray":
        """
        Returns a shallow copy with the same capacity and elements.

        Time complexity: O(n)
        """
        copied = StaticUniversalArray(capacity=self._capacity)
        for i in range(self._capacity):
            copied._data[i] = self._data[i]
        return copied

    # -------------------------------------------------------------------------
    # Dunder methods

    def __getitem__(self, index: int) -> Any:
        """
        Returns element at given index. Supports negative indexing.

        Time complexity: O(1)

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range.
        """
        index = validate_index(index, self._capacity)
        return self._data[index]

    def __setitem__(self, index: int, value: Any) -> None:
        """
        Sets element at given index. Supports negative indexing.
        Accepts any Python object including None.

        Time complexity: O(1)

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range.
        """
        index = validate_index(index, self._capacity)
        self._data[index] = value

    def __len__(self) -> int:
        """Returns the fixed capacity of the array. O(1)"""
        return self._capacity

    def __bool__(self) -> bool:
        """Returns True if capacity is greater than zero. O(1)"""
        return self._capacity > 0

    def __iter__(self) -> Iterator:
        """Yields all elements from index 0 to capacity-1. O(n)"""
        for i in range(self._capacity):
            yield self._data[i]

    def __reversed__(self) -> Iterator[Any]:
        """Yields elements from right to left(back -> start). O(n)"""
        for i in range(self._capacity - 1, -1, -1):
            yield self._data[i]

    def __contains__(self, value: Any) -> bool:
        """Returns True if value exists in the array. O(n)"""
        for i in range(self._capacity):
            if self._data[i] == value:
                return True
        return False

    def __eq__(self, other: object) -> bool:
        """
        Returns True if other is a StaticUniversalArray with the same capacity
        and elements in the same order. O(n)
        """
        if not isinstance(other, StaticUniversalArray):
            return NotImplemented
        if self._capacity != other._capacity:
            return False
        for i in range(self._capacity):
            if self._data[i] != other._data[i]:
                return False
        return True

    def __repr__(self) -> str:
        """
        Returns string representation of the array.
        Format: StaticUniversalArray(capacity=5)[1, 'hi', None, None, None]

        Time complexity: O(n)
        """
        elements = ", ".join(repr(self._data[i]) for i in range(self._capacity))
        return f"StaticUniversalArray(capacity={self._capacity})[{elements}]"
