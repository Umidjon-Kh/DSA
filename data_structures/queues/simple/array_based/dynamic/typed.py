from typing import Any, Iterator, Optional

from ....._base import BaseQueue
from .....arrays import DynamicTypedArray


class DynamicTypedQueue(BaseQueue):
    """
    A dynamic queue backed by DynamicTypedArray.
    Grows automatically when capacity is exceeded.
    Enforces a single element type for all items.
    Follows FIFO (First In, First Out) principle.

    Supported dtypes: int, float, bool, str

    Growth formula (delegated to DynamicTypedArray - same as CPython list):
        new_capacity = capacity + (capacity >> 3) + (3 if capacity < 9 else 6)

    Simple Queue — naive implementation, front always at index 0.
    After every dequeue, all elements need to be shifted left.

    Time complexity:
        enqueue:        O(1) amortized — O(n) on resize
        dequeue:        O(n) needs to shift all elements from right to left
        peek:           O(1)
        clear:          O(n)
        copy:           O(n)
        is_empty:       O(1)
        __len__:        O(1)
        __bool__:       O(1)
        __iter__:       O(n) - front to rear
        __reversed__:   O(n)
        __contains__:   O(n)
        __repr__:       O(n)
        __eq__:         O(n)
    """

    __slots__ = ("_data", "_dtype", "_str_length")

    def __init__(
        self,
        dtype: type,
        *args,
        str_length: Optional[int] = None,
    ) -> None:
        """
        Creates a dynamic typed queue with optional initial elements.

        Args:
            dtype:      Element type. Supported: int, float, bool, str.
            *args:      Optional initial elements, added left to right (first = front)
            str_length: Max characters per str element (default 20).

        Raises:
            TypeError: if dtype is not a supported type.
            TypeError: if any elements in args is not dtype.

        Examples:
            q = DynamicTypedQueue(int)          # empty
            q = DynamicTypedQueue(int, 1, 2, 3) # front=1
        """
        self._dtype: type = dtype
        self._data: DynamicTypedArray = DynamicTypedArray(
            dtype=dtype, str_length=str_length
        )
        self._str_length = self._data._str_length

        for item in args:
            self.enqueue(item)

    # -------------------------------------------------------------------------
    # Core operations

    def enqueue(self, value: Any) -> None:
        """
        Adds value to rear of the queue.
        Triggers resize if underlying array is at capacity.

        Time complexity: O(1) amortized - O(n) on resize

        Raises:
            TypeError: if value is not dtype.
        """
        self._data.append(value)

    def dequeue(self) -> Any:
        """
        Removes and returns the value from the front of the queue.
        After removal, all remaining elements are shifted left.

        Time complexity: O(n)

        Raises:
            IndexError: if queue is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue")
        return self._data.remove(0)

    def peek(self) -> Any:
        """
        Returns the front element without removing it.

        Time complexity: O(1)

        Raises:
            IndexError: if queue is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from an empty queue")
        return self._data[0]

    def clear(self) -> None:
        """
        Removes all elements. Does not reallocate the buffer.

        Time complexity: O(n)
        """
        self._data.clear()

    def copy(self) -> "DynamicTypedQueue":
        """
        Returns a shallow copy with same dtype and elements.

        Time complexity: O(n)
        """
        new_queue = DynamicTypedQueue(
            dtype=self._dtype,
            str_length=self._str_length,
        )
        for i in range(len(self._data)):
            new_queue._data.append(self._data[i])
        return new_queue

    # -------------------------------------------------------------------------
    # State checks

    def is_empty(self) -> bool:
        """Returns True if the queue contains no elements. O(1)"""
        return len(self._data) == 0

    # -------------------------------------------------------------------------
    # Dunder methods

    def __len__(self) -> int:
        """Returns number of elements currently in the queue. O(1)"""
        return len(self._data)

    def __bool__(self) -> bool:
        """Returns True if queue is not empty. O(1)"""
        return len(self._data) > 0

    def __iter__(self) -> Iterator[Any]:
        """
        Yields elements from front to rear without modifying the queue.

        Time complexity: O(n)
        """
        for i in range(len(self._data)):
            yield self._data[i]

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields elements from rear to front without modifying the queue.

        Time complexity: O(n)
        """
        for i in range(len(self._data) - 1, -1, -1):
            yield self._data[i]

    def __eq__(self, other: object) -> bool:
        """Returns True if both structures data and dtypes are equal."""
        if not isinstance(other, DynamicTypedQueue):
            return NotImplemented
        return self._data == other._data

    def __contains__(self, value: Any) -> bool:
        """
        Returns True if value exists in queue. O(n)
        Returns False instantly for wrong type.
        """
        return value in self._data

    def __repr__(self) -> str:
        """
        Returns string representation of the queue.
        Format: DynamicTypedQueue(int, size=3)[1, 2, 3]
                                            front    rear

        Time complexity: O(n)
        """
        size = len(self._data)
        elements = ", ".join(repr(self._data[i]) for i in range(len(self._data)))
        return f"DynamicTypedQueue({self._dtype.__name__}, size={size})[{elements}]"
