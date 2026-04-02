from typing import Any, Iterator

from ....._base import BaseDeque
from .....arrays import DynamicUniversalArray


class DynamicUniversalDeque(BaseDeque):
    """
    A dynamic deque backed by DynamicUniversalArray.
    Grows automatically when capacity is exceeded.
    Accepts any Python type - no dtype restriction.
    Follows FIFO (First In, First Out) principle.

    Growth formula (delegated to DynamicUniversalArray - same as CPython list):
        new_capacity = capacity + (capacity >> 3) + (3 if capacity < 9 else 6)

    Naive implementation - front is always at index 0.
    enqueue_front and dequeue_front require shifting all elements.

    Time complexity:
        enqueue_front:  O(n) — shifts all elements right
        enqueue_rear:   O(1)
        dequeue_front:  O(n) — shifts all elements left
        dequeue_rear:   O(1)
        peek_front:     O(1)
        peek_rear:      O(1)
        clear:          O(n)
        copy:           O(n)
        is_empty:       O(1)
        __len__:        O(1)
        __bool__:       O(1)
        __iter__:       O(n) — front to rear
        __reversed__:   O(n)
        __contains__:   O(n)
        __repr__:       O(n)
        __eq__:         O(n)
    """

    __slots__ = ("_data",)

    def __init__(self, *args) -> None:
        """
        Creates a dynamic universal deque with optional initial elements.

        Args:
            *args: optional initial elements, added left to right (first = front).

        Examples:
            d = DynamicUniversalDeque()             # empty
            d = DynamicUniversalDeque(1, "hi", 3.0) # front=1, rear=3.0
        """
        self._data: DynamicUniversalArray = DynamicUniversalArray()

        for item in args:
            self.enqueue_rear(item)

    # -------------------------------------------------------------------------
    # Core operations

    def enqueue_front(self, value: Any) -> None:
        """
        Adds value to the front of the deque.
        Shilfts all elements one position to the right first.
        Triggers resize if underlying array is at capacity.

        Time complexity: O(n) amortized - O(n) on resize
        """
        self._data.insert(0, value)

    def enqueue_rear(self, value: Any) -> None:
        """
        Adds value to the rear of the deque.
        Triggers resize if underlying array is at capacity.

        Time complexity: O(1) amortized - O(n) on resize
        """
        self._data.append(value)

    def dequeue_front(self) -> Any:
        """
        Removes and returns the value from the front of the deque.
        After removal, all remaining elements are shifted left.

        Time complexity: O(n)

        Raises:
            IndexError: if deque is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from an empty deque")
        return self._data.remove(0)

    def dequeue_rear(self) -> Any:
        """
        Removes and returns the value form the rear of the deque.

        Time complexity: O(1)

        Raises:
            IndexError: if deque is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from an empty deque")
        return self._data.remove(-1)

    def peek_front(self) -> Any:
        """
        Returns the front value without removing it.

        Time complexity: O(1)

        Raises:
            IndexError: if deque is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from an empty deque")
        return self._data[0]

    def peek_rear(self) -> Any:
        """
        Returns the rear value without removing it.

        Time complexity: O(1)

        Raises:
            IndexError: if deque is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from an empty deque")
        return self._data[-1]

    def clear(self) -> None:
        """
        Removes all elements. Does not reallocate the buffer.

        Time complexity: O(n)
        """
        self._data.clear()

    def copy(self) -> "DynamicUniversalDeque":
        """
        Returns a shallow copy with same elements.

        Time complexity: O(n)
        """
        new_deque = DynamicUniversalDeque()
        for i in range(len(self._data)):
            new_deque._data.append(self._data[i])
        return new_deque

    # -------------------------------------------------------------------------
    # State checks

    def is_empty(self) -> bool:
        """Returns True if the deque contains no elements. O(1)"""
        return len(self._data) == 0

    # -------------------------------------------------------------------------
    # Dunder methods

    def __len__(self) -> int:
        """Returns number of elements currently in the deque. O(1)"""
        return len(self._data)

    def __bool__(self) -> bool:
        """Returns True if the deque is not empty. O(1)"""
        return len(self._data) > 0

    def __iter__(self) -> Iterator[Any]:
        """
        Yields elements from front to rear without modifying the deque.

        Time complexity: O(n)
        """
        for i in range(len(self._data)):
            yield self._data[i]

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields elements from rear to front without modifying the deque.

        Time complexity: O(n)
        """
        for i in range(len(self._data) - 1, -1, -1):
            yield self._data[i]

    def __eq__(self, other: object) -> bool:
        """Returns True if both structure data attrs are equal."""
        if not isinstance(other, DynamicUniversalDeque):
            return NotImplemented
        return self._data == other._data

    def __contains__(self, value: Any) -> bool:
        """
        Returns True if value exists in the deque. O(n)
        """
        return value in self._data

    def __repr__(self) -> str:
        """
        Returns string representation of the deque.
        Format: DynamicUniversalDeque(size=3)[1, 'hi', 3.0]
                                            front       rear

        Time complexity: O(n)
        """
        size = len(self._data)
        elements = ", ".join(repr(self._data[i]) for i in range(len(self._data)))
        return f"DynamicUniversalDeque(size={size})[{elements}]"
