from typing import Any, Iterator, Optional

from ....._base import BaseBoundedQueue
from ....._tools import validate_capacity
from .....arrays import StaticUniversalArray


class StaticUniversalQueue(BaseBoundedQueue):
    """
    A fixed-capacity queue backed by StaticUniversalArray.
    Accepts any Python type - no dtype restriction.
    Follows FIFO (First In, First Out) principle.

    Time complexity:
        enqueue:        O(1)
        dequeue:        O(n) needs to shift all elements from right to left
        peek:           O(1)
        clear:          O(n)
        copy:           O(n)
        is_empty:       O(1)
        is_full:        O(1)
        __len__:        O(1)
        __bool__:       O(1)
        __iter__:       O(n) - front to rear
        __reversed__:   O(n)
        __contains__:   O(n)
        __repr__:       O(n)
        __eq__:         O(n)
    """

    __slots__ = ("_data", "_rear")

    def __init__(self, *args, capacity: Optional[int] = None) -> None:
        """
        Creates a fixed-capacity universal queue with optional initial elements.

        Args:
            capacity: Maximum numbers of elements the queue can hold.
            *args:    Optional initial elements, added left to right (first = front).

        Raises:
            TypeError:     if capacity is not an int.
            TypeError:     if not provided at least one argument or capacity value.
            ValueError:    if capacity < 1.
            OverflowError: if len(args) > capacity.

        Examples:
            q = StaticUniversalQueue(capacity=5)            # empty, capacity=5
            q = StaticUniversalQueue(1, 2, 3, capacity=5)  # front=1, capacity=5
        """
        self._rear: int = 0
        cap: int = validate_capacity(capacity, len(args), "StaticUniversalQueue")
        self._data: StaticUniversalArray = StaticUniversalArray(capacity=cap)

        for item in args:
            self.enqueue(item)

    # -------------------------------------------------------------------------
    # Core operations

    def enqueue(self, value: Any) -> None:
        """
        Adds value to the rear of the queue.

        Time complexity: O(1)

        Raises:
            OverflowError: if queue is full.
        """
        if self.is_full():
            raise OverflowError(f"Queue is full (capacity={len(self._data)})")
        self._data[self._rear] = value
        self._rear += 1

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
        self._rear -= 1
        value = self._data[0]
        # Shifting all elements from right to left
        for index in range(self._rear):
            self._data[index] = self._data[index + 1]

        self._data[self._rear] = None
        return value

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
        self._rear = 0
        self._data.clear()

    def copy(self) -> "StaticUniversalQueue":
        """
        Returns a shallow copy with same capacity and data.

        Time complexity: O(n)
        """
        new_queue = StaticUniversalQueue(capacity=len(self._data))

        for i in range(self._rear):
            new_queue._data[i] = self._data[i]
        new_queue._rear = self._rear
        return new_queue

    # -------------------------------------------------------------------------
    # State checks

    def is_empty(self) -> bool:
        """Returns True if the queue contains no elements. O(1)"""
        return self._rear == 0

    def is_full(self) -> bool:
        """Returns True if the queue has reached its capacity. O(1)"""
        return self._rear == len(self._data)

    # -------------------------------------------------------------------------
    # Dunder methods

    def __len__(self) -> int:
        """Returns number of elements currently in the queue. O(1)"""
        return self._rear

    def __bool__(self) -> bool:
        """Returns True if the queue is not empty. O(1)"""
        return self._rear > 0

    def __iter__(self) -> Iterator[Any]:
        """
        Yields elements from front to rear without modifying the queue.

        Time complexity: O(n)
        """
        for i in range(self._rear):
            yield self._data[i]

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields elements from rear to front without modifying the queue.

        Time complexity: O(n)
        """
        for i in range(self._rear - 1, -1, -1):
            yield self._data[i]

    def __eq__(self, other: object) -> bool:
        """Returns True if both structures data and rear attrs are equal."""
        if not isinstance(other, StaticUniversalQueue):
            return NotImplemented
        if self._rear != other._rear:
            return False
        for i in range(self._rear):
            if self._data[i] != other._data[i]:
                return False
        return True

    def __contains__(self, value: Any) -> bool:
        """
        Returns True if value exists in the queue. O(n)
        """
        for i in range(self._rear):
            if self._data[i] == value:
                return True
        return False

    def __repr__(self) -> str:
        """
        Returns string representation of the queue.
        Format: StaticUniversalQueue(size=3, capacity=5)[1, 2, 3]
                                               front    rear

        Time complexity: O(n)
        """
        elements = ", ".join(repr(self._data[i]) for i in range(self._rear))
        return (
            f"StaticUniversalQueue(size={self._rear}, capacity={len(self._data)})"
            f"[{elements}]"
        )
