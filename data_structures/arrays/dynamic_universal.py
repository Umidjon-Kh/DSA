from typing import Any, Iterator

from .static_universal import StaticUniversalArray


class DynamicUniversalArray:
    """
    A dynamic array that grows automatically when capacity is exceeded.
    Built on top of StaticUniversalArray — accepts any Python object.

    When capacity is full, creates a new StaticUniversalArray with
    double the capacity and copies all elements. Old array is
    discarded and collected by GC.

    Growth factor: 2
    Initial capacity: 4

    Unlike Python list this implementation is transparent —
    you can see exactly how resizing works internally.

    Time complexity:
        append:  O(1) amortized — O(n) on resize
        insert:  O(n) — shifts all elements to the right
        remove:  O(n) — shifts all elements to the left
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
            arr = DynamicUniversalArray()          # empty, capacity=4
            arr = DynamicUniversalArray(1, 2, 3)   # capacity=4, size=3
            arr = DynamicUniversalArray(*range(10)) # capacity=10, size=10
        """
        # Calculating capacity value
        self._capacity = max(4, len(args))
        # size of our array
        self._size = 0
        # Creating StaticUniversalArray with capacity
        self._data = StaticUniversalArray(self._capacity)

    def append(self, value: Any) -> None:
        """
        Adds value to the end of the array.
        If capacity is exceeded — triggers _resize() first.

        Time complexity: O(1) amortized, O(n) on resize.

        Args:
            value: Any Python object.
        """
        # Checking internal storage size is full or not
        if self._size == self._capacity:
            # If full calls _resize method
            self._resize()
        self._data[self._size] = value
        self._size += 1

    def _resize(self) -> None:
        """
        Not doubles, Calculates the capacity by creating a new StaticUniversalArray
        and copying all existing elements into it.
        Old array is discarded and collected by GC.

        Called automatically by append and insert when size == capacity.
        Never call this manually.

        Time complexity: O(n)
        """
        # Calculating new capacity like list capacity formule
        new_capacity = self._capacity + (self._capacity >> 3) + (3 if self._capacity < 9 else 6)
        new_data = StaticUniversalArray(new_capacity)

        # Appending new array with old array objects
        for index in range(self._size):
            new_data[index] = self._data[index]

        # Setting new capacity and new data
        self._data = new_data
        self._capacity = new_capacity

    def insert(self, index: Any, value: Any) -> None:
        """
        Inserts value at given index by shifting all elements
        to the right of index one position forward.
        If capacity is exceeded — triggers _resize() first.

        Time complexity: O(n) — shifts up to n elements.

        Args:
            index: Position to insert at. Must be 0 <= index <= size.
            value: Any Python object.

        Raises:
            TypeError:  if index is not int.
            IndexError: if index is out of range.
        """
        # Checkinig index for type
        if not isinstance(index, int):
            raise TypeError(f"Index must be positive integer, got ({type(index).__name__})")

        # Converting index if received negative integer
        if index < 0:
            index += self._size
        # Checking index out of range or not
        if index < 0 or index > self._size:
            raise IndexError(f"Index {index} out of range for size {self._size}")
        # Checking internal storage is full or not
        if self._size == self._capacity:
            # If full calls _resize method
            self._resize()

        # Shifting all elements
        # from end to received index to the right
        for idx in range(self._size, index, - 1):
            self._data[idx] = self._data[idx - 1]

        # Setting new value
        self._data[index] = value
        self._size += 1


    def remove(self, index: Any) -> Any:
        """
        Removes element at given index by shifting all elements
        to the right of index one position backward.
        Does not resize down — capacity stays the same.

        Time complexity: O(n) — shifts up to n elements.

        Args:
            index: Position to remove. Must be 0 <= index < size.

        Raises:
            TypeError:  if index is not int.
            IndexError: if index is out of range.

        Returns:
            Any value at given index.
        """
        # Checkinig index for type
        if not isinstance(index, int):
            raise TypeError(f"Index must be positive integer, got ({type(index).__name__})")
        # Converting index if received negative integer
        if index < 0:
            index += self._size
        # Checking index out of range or not
        if index < 0 or index > self._size:
            raise IndexError(f"Index {index} out of range for size {self._size}")

        # Saving element to remove to return it
        removed = self._data[index]

        # Shifting elements to the left from end to index
        for idx in range(index, self._size - 1):
            self._data[idx] = self._data[idx + 1]

        # Wiping last element of data to avoid dublicate
        self._data[self._size - 1] = None
        self._size -= 1

        return removed

    def __getitem__(self, index: Any) -> Any:
        """
        Only returns element at given index.
        Time complexity: O(1) - only returns.

        Raises:
            TypeError: if index is not int
            IndexError: if index out of range
        Returns:
            Any value at given index
        """
        # Checkinig index for type
        if not isinstance(index, int):
            raise TypeError(f"Index must be positive integer, got ({type(index).__name__})")
        # Converting index if received negative integer
        if index < 0:
            index += self._size
        # Checking index out of range or not
        if index < 0 or index > self._size:
            raise IndexError(f"Index {index} out of range for size {self._size}")

        return self._data[index]

    def __setitem__(self, index: Any, value: Any) -> None:
        """
        Sets value at given index dont resizes dont shifts.
        Only needs for changing value of given index.
        Dont changes value of reserve index shelfs.
        Time conplexity: O(1) - only changes the value of given index.

        Raises:
            TypeError: if index is not int
            IndexError: if index out of range
        """
        # Checkinig index for type
        if not isinstance(index, int):
            raise TypeError(f"Index must be positive integer, got ({type(index).__name__})")
        # Converting index if received negative integer
        if index < 0:
            index += self._size
        # Checking index out of range or not
        if index < 0 or index > self._size:
            raise IndexError(f"Index {index} out of range for size {self._size}")

        self._data[index] = value

    def __len__(self) -> int:
        """Returns length of array"""
        return self._size

    def __iter__(self) -> Iterator[Any]:
        for index in range(self._size):
            yield self._data[index]

    def __repr__(self) -> str:
        """Returns Representation of DynamicUniversalArray"""
        items = [self._data[i] for i in range(self._size)]
        return f"DynamicUniversalArray(size={self._size}, items={items})"
