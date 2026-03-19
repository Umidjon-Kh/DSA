import ctypes
from typing import Any, Iterator


class Array:
    """
    A fixed size array build on top of the ctypes.py_object.
    Unlike Python list, this array has no dynamic resizing capacity.
    Accepts any Python object (Any type) cause py_object is a pointer
    to any Python object, just like CPython stores items internally

    Getting by index - O(1)
    Writing by index - O(1)
    Searching by element - O(n)
    Adding to end - O(1)
    Adding not to end - O(n) - need to move all right side elements
    Removing - O(n)
    """

    __slots__ = ("_capacity", "_data")

    def __init__(self, capacity: Any) -> None:
        if not isinstance(capacity, int):
            raise TypeError(
                f"Capacity value must be a positive integers, got({type(capacity).__name__})"
            )
        if capacity <= 0:
            raise ValueError(f"Capacity must be mode than 0, got ({capacity})")

        # Allocate  a fixed block of memory for capacity Python object pointers
        # (ctypes.py_object * capacity) creates the Array TYPE,
        # calling () on it allocate the actual memory
        self._capacity = capacity
        # Initizaling all slots to None to avoid reading garpage from memory
        self._data = (ctypes.py_object * self._capacity)()
        for index in range(self._capacity):
            self._data[index] = None

    def __getitem__(self, index: Any) -> Any:
        """Returns value at given index."""
        if not isinstance(index, int):
            raise TypeError(
                f"Index must be a positive integer, got ({type(index).__name__})"
            )
        if index < 0 or index >= self._capacity:
            raise IndexError(
                f"index {index} out of range for capacity {self._capacity}"
            )
        return self._data[index]

    def __setitem__(self, index: Any, value: Any) -> None:
        """Sets value at given index."""
        if not isinstance(index, int):
            raise TypeError(
                f"Index must be a positive integer, got ({type(index).__name__})"
            )
        if index < 0 or index >= self._capacity:
            raise IndexError(
                f"index {index} out of range for capacity {self._capacity}"
            )
        self._data[index] = value

    def __len__(self) -> int:
        """Retunrs length of data array"""
        return self._capacity

    def __iter__(self) -> Iterator[Any]:
        """Iterates the total capacity of the Array, not the number of filled slots"""
        for index in range(self._capacity):
            yield self._data[index]

    def __repr__(self) -> str:
        items = [self._data[i] for i in range(self._capacity)]
        return f"Array(capacity={self._capacity}, slots={items})"

    def __bool__(self) -> bool:
        """Retunrs true if self._data slots is not None"""
        return any(self._data[i] is not None for i in range(self._capacity))
