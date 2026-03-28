from typing import Any, Iterator

from ...._base import BaseDynamicArray
from ...._tools import validate_index, validate_insert_index
from ..static import StaticUniversalArray


class DynamicUniversalArray(BaseDynamicArray):
    """
    A dynamic array that grows automatically when capacity is exceeded.
    Built on top of StaticUniversalArray — accepts any Python type.

    Stores PyObject pointers so any object can be held.
    Trade-off vs DynamicTypedArray: more flexible, higher memory overhead per element.

    Growth formula (same as CPython list):
        new_capacity = capacity + (capacity >> 3) + (3 if capacity < 9 else 6)

    Initial capacity: max(4, len(args))

    Time complexity:
        append:       O(1) amortized — O(n) on resize
        insert:       O(n) — shifts elements to the right
        remove:       O(n) — shifts elements to the left
        clear:        O(n)
        copy:         O(n)
        __getitem__:  O(1)
        __setitem__:  O(1) — only for existing indices (0 to size-1)
        __len__:      O(1)
        __bool__:     O(1)
        __iter__:     O(n)
        __reversed__: O(n)
        __contains__: O(n)
        __eq__:       O(n)
        __repr__:     O(n)
        _resize:      O(n)
    """

    __slots__ = ("_data", "_capacity", "_size")

    def __init__(self, *args) -> None:
        """
        Creates a universal dynamic array with optional initial elements.

        Args:
            *args: Optional initial elements of any type.

        Examples:
            arr = DynamicUniversalArray()              # empty, capacity=4
            arr = DynamicUniversalArray(1, "hi", 3.0)  # [1, 'hi', 3.0], capacity=4
        """
        self._size: int = 0
        self._capacity: int = max(4, len(args))
        self._data: StaticUniversalArray = StaticUniversalArray(capacity=self._capacity)

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
        new_data = StaticUniversalArray(capacity=new_capacity)
        for index in range(self._size):
            new_data[index] = self._data[index]
        self._data = new_data
        self._capacity = new_capacity

    # -------------------------------------------------------------------------
    # Core operations

    def append(self, value: Any) -> None:
        """
        Appends value to the end of the array.
        Triggers resize if size == capacity.

        Time complexity: O(1) amortized — O(n) on resize
        """
        if self._size == self._capacity:
            self._resize()
        self._data[self._size] = value
        self._size += 1

    def insert(self, index: int, value: Any) -> None:
        """
        Inserts value at given index, shifting elements to the right.
        Supports negative indexing. Allows index == size (insert at end).

        Time complexity: O(n)

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range.
        """
        index = validate_insert_index(index, self._size)
        if self._size == self._capacity:
            self._resize()

        # Shift elements right
        for idx in range(self._size, index, -1):
            self._data[idx] = self._data[idx - 1]

        self._data[index] = value
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
        value = self._data[index]

        # Shift elements left
        for idx in range(index, self._size - 1):
            self._data[idx] = self._data[idx + 1]

        self._data[self._size - 1] = None
        self._size -= 1
        return value

    def clear(self) -> None:
        """
        Removes all elements. Resets size to 0 without reallocating the buffer.

        Time complexity: O(n)
        """
        self._size = 0
        self._data.clear()

    def copy(self) -> "DynamicUniversalArray":
        """
        Returns a shallow copy with the same elements.
        The copy has capacity equal to max(4, size).

        Time complexity: O(n)
        """
        new_arr = DynamicUniversalArray()
        for idx in range(self._size):
            new_arr.append(self._data[idx])
        return new_arr

    # -------------------------------------------------------------------------
    # Dunder methods

    def __getitem__(self, index: int) -> Any:
        """
        Returns element at given index. Supports negative indexing.
        Only valid for indices 0 to size-1.

        Time complexity: O(1)

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range.
        """
        index = validate_index(index, self._size)
        return self._data[index]

    def __setitem__(self, index: int, value: Any) -> None:
        """
        Sets element at given index. Supports negative indexing.
        Only valid for existing indices (0 to size-1).

        Time complexity: O(1)

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range.
        """
        index = validate_index(index, self._size)
        self._data[index] = value

    def __len__(self) -> int:
        """Returns number of elements currently in the array. O(1)"""
        return self._size

    def __bool__(self) -> bool:
        """Returns True if the array contains at least one element. O(1)"""
        return self._size > 0

    def __iter__(self) -> Iterator:
        """Yields elements from index 0 to size-1. O(n)"""
        for idx in range(self._size):
            yield self._data[idx]

    def __reversed__(self) -> Iterator[Any]:
        """Yields elements from right to left(back -> start). O(n)"""
        for idx in range(self._size - 1, -1, -1):
            yield self._data[idx]

    def __contains__(self, value: Any) -> bool:
        """Returns True if value exists in the array. O(n)"""
        for index in range(self._size):
            if self._data[index] == value:
                return True
        return False

    def __eq__(self, other: object) -> bool:
        """
        Returns True if other is a DynamicUniversalArray with the same size
        and elements in the same order. O(n)
        """
        if not isinstance(other, DynamicUniversalArray):
            return NotImplemented
        if self._size != other._size:
            return False
        for index in range(self._size):
            if self._data[index] != other._data[index]:
                return False
        return True

    def __repr__(self) -> str:
        """
        Returns string representation of the array.
        Format: DynamicUniversalArray(size=3, capacity=4)[1, 'hi', 3.0]

        Time complexity: O(n)
        """
        elements = ", ".join(repr(self._data[i]) for i in range(self._size))
        return (
            f"DynamicUniversalArray(size={self._size}, capacity={self._capacity})"
            f"[{elements}]"
        )
