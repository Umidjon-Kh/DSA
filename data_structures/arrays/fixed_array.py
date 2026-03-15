import ctypes
from typing import Any, Iterator


class FixedArray:
    """
    A fixed-size array built on top of ctypes.py_object.
    Unlike Python list, this array has no dynamic resizing or reserved capacity.
    Accepts any Python object (Any type) because py_object is a pointer
    to any Python object, just like CPython stores items internally.

    Used in: StaticCircularQueue

    Time complexity:
        __getitem__: O(1)
        __setitem__: O(1)
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError(f"Capacity must be greater than 0, got {capacity}")
        self._capacity = capacity
        # Allocate a fixed block of memory for `capacity` Python object pointers.
        # (ctypes.py_object * capacity) creates the array TYPE,
        # calling () on it allocates the actual memory.
        self._data = (ctypes.py_object * capacity)()
        # Initialize all slots to None to avoid reading garbage from memory.
        for i in range(self._capacity):
            self._data[i] = None

    def __getitem__(self, index: int) -> Any:
        """Returns value at given index."""
        if not isinstance(index, int):
            raise TypeError(f"Index must be int, not {type(index).__name__}")
        if index < 0 or index >= self._capacity:
            raise IndexError(f"Index {index} out of range for capacity {self._capacity}")
        return self._data[index]

    def __setitem__(self, index: int, value: Any) -> None:
        """Sets value at given index."""
        if not isinstance(index, int):
            raise TypeError(f"Index must be int, not {type(index).__name__}")
        if index < 0 or index >= self._capacity:
            raise IndexError(f"Index {index} out of range for capacity {self._capacity}")
        self._data[index] = value

    def __len__(self) -> int:
        """Returns the total capacity of the array, not the number of filled slots."""
        return self._capacity

    def __iter__(self) -> Iterator[Any]:
        """Iterates over all slots including empty (None) ones."""
        for i in range(self._capacity):
            yield self._data[i]

    def __repr__(self) -> str:
        items = [self._data[i] for i in range(self._capacity)]
        return f'FixedArray(capacity={self._capacity}, slots={items})'
