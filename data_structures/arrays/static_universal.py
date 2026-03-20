import ctypes
from typing import Any, Iterator

from ..tools import validate_index


class StaticUniversalArray:
    """
    A fixed-size array that accepts any Python object.
    Built on top of ctypes.py_object — each slot stores a pointer
    to a PyObject, just like CPython stores items in a list internally.

    Unlike Python list, this array:
    - Has no dynamic resizing
    - Has no append, insert or remove
    - Provides raw indexed access only

    Use this as a low-level building block for higher-level structures.

    Time complexity:
        __getitem__: O(1)
        __setitem__: O(1)
        __iter__:    O(n)
        __len__:     O(1)
    """

    __slots__ = ("_capacity", "_data")

    def __init__(self, capacity: Any) -> None:
        """
        Creates data structure array with received capacity
        and initializes all slots as None, to avoid getting garbage from memory.
        """
        if not isinstance(capacity, int):
            raise TypeError(
                f"Capacity value must be positive integer, got ({type(capacity).__name__})"
            )
        if capacity <= 0:
            raise ValueError(f"Capacity must be more than 0, got ({capacity})")

        self._capacity = capacity
        self._data = (ctypes.py_object * self._capacity)()
        for index in range(self._capacity):
            self._data[index] = None

    def __getitem__(self, index: Any) -> Any:
        """Returns value at given index."""
        index = validate_index(index, self._capacity)
        return self._data[index]

    def __setitem__(self, index: Any, value: Any) -> None:
        """Sets value to given index."""
        index = validate_index(index, self._capacity)
        self._data[index] = value

    def __len__(self) -> int:
        """Returns capacity of array."""
        return self._capacity

    def __iter__(self) -> Iterator[Any]:
        """Iterates all slots including empty (None) ones."""
        for index in range(self._capacity):
            yield self._data[index]

    def __repr__(self) -> str:
        items = [self._data[i] for i in range(self._capacity)]
        return f"StaticUniversalArray(capacity={self._capacity}, slots={items})"
