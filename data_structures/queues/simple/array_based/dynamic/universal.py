from typing import Any, Iterator

from ....._base import BaseQueue
from .....arrays import DynamicUniversalArray


class DynamicUniversalQueue(BaseQueue):
    """
    A dynamic queue backed by DynamicUniversalArray.
    Grows automatically when capacity is exceeded.
    Accepts any Python type - no dtype restriction.
    Follows FIFO (First In, First Out) principle.

    Growth formula (delegated to DynamicUniversalArray - same as CPython list):
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

    __slots__ = ("_data",)

    def __init__(self, *args) -> None:
        """
        Creates a dynamic universal queue with optional initial elements.

        Args:
            *args: Optional initial elements, added left to right (first = front).

        Examples:
            q = DynamicUniversalQueue()             # empty
            q = DynamicUniversalQueue(1, "hi", 3.0) # front=1
        """
        self._data: DynamicUniversalArray = DynamicUniversalArray()

        for item in args:
            self.enqueue(item)

    # -------------------------------------------------------------------------
    # Core operations

    def enqueue(self, value: Any) -> None:
        """
        Adds value to the rear of the queue.
        Triggers resize if underlying array is at capacity.

        Time complexity: O(1) amortized - O(n) on resize
        """
        self._data.append(value)

    def dequeue(self) -> Any:
        """
        Removes and returns the value form the front of the queue.
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

    def copy(self) -> "DynamicUniversalQueue":
        """
        Returns a shallow copy with same elements.

        Time complexity: O(n)
        """
        new_queue = DynamicUniversalQueue()
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
        """Returns True if the queue is not empty. O(1)"""
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
        """Returns True if both structure data attrs are equal."""
        if not isinstance(other, DynamicUniversalQueue):
            return NotImplemented
        return self._data == other._data

    def __contains__(self, value: Any) -> bool:
        """
        Returns True if value exists in the queue. O(n)
        """
        return value in self._data

    def __repr__(self) -> str:
        """
        Returns string representation of the queue.
        Format: DynamicUniversalQueue(size=3)[1, 'hi', 3.0]
                                            front       rear

        Time complexity: O(n)
        """
        size = len(self._data)
        elements = ", ".join(repr(self._data[i]) for i in range(len(self._data)))
        return f"DynamicUniversalQueue(size={size})[{elements}]"
