import ctypes
from typing import Any, Iterator


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
        Creates data structure array
        with received capacity and initializes all slots
        as None, to avoid getting garbage of Memory
        """
        # Validating capacity for right value
        # Checking for type
        if not isinstance(capacity, int):
            raise TypeError(
                f"Capacity value must be positive integer, got ({type(capacity).__name__})"
            )
        # Checking for value
        if capacity <= 0:
            raise ValueError(f"Capacity must be more than 0, got ({capacity})")

        # Allocate a fixed block of memory for capacity Python object pointers
        # (ctypes.py_object * capacity) creates the Array Type
        # calling () on it to allocate the actual memory
        self._capacity = capacity
        # Initializing all slots as None, to avoid getting garbage from Memory
        self._data = (ctypes.py_object * self._capacity)()
        for index in range(self._capacity):
            self._data[index] = None

    def __getitem__(self, index: Any) -> Any:
        """Returns value at given index."""
        # Checking type of received index
        if not isinstance(index, int):
            raise TypeError(
                f"Index must be positive integer, got ({type(index).__name__})"
            )
        # Convertig index if its negative integer
        if index < 0:
            index += self._capacity
        # Checking value of received index
        if index < 0 or index >= self._capacity:
            raise IndexError(
                f"Index {index} out of range for capacity {self._capacity}"
            )
        return self._data[index]

    def __setitem__(self, index: Any, value: Any) -> None:
        """Sets value to given index."""
        # Checking type of received index
        if not isinstance(index, int):
            raise TypeError(
                f"Index must be positive integer, got ({type(index).__name__})"
            )
        # Converting index if its negative integer
        if index < 0:
            index += self._capacity
        # Checking value of received index
        if index < 0 or index >= self._capacity:
            raise IndexError(
                f"Index {index} out of range for capacity {self._capacity}"
            )
        self._data[index] = value

    def __len__(self) -> int:
        """Returns length of data array"""
        return self._capacity

    def __iter__(self) -> Iterator[Any]:
        """Iterates the total capacity of the Array, not the number of filled slots"""
        for index in range(self._capacity):
            yield self._data[index]

    def __repr__(self) -> str:
        """Returns Representation instance of StaticUniversalArray"""
        items = [self._data[i] for i in range(self._capacity)]
        return f"StaticUniversalArray(capacity={self._capacity}, slots={items})"
