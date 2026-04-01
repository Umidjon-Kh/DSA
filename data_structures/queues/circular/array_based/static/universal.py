from typing import Any, Iterator, Optional

from ....._base import BaseBoundedQueue
from ....._tools import validate_capacity
from .....arrays import StaticUniversalArray


class StaticUniversalCircularQueue(BaseBoundedQueue):
    """
    A fixed-capacity circular queue backed by StaticUniversalArray.
    Accepts any Python type — no dtype restriction.
    Follows FIFO (First In, First Out) principle.

    Front and rear are indices that wrap around the buffer using
    modulo arithmetic — no element shifting needed.
    Both enqueue and dequeue are O(1).

    _front — index of the front element (dequeue side).
    _rear  — index where the next element will be written (enqueue side).
    _size  — number of elements currently in the queue.

    Time complexity:
        enqueue:      O(1)
        dequeue:      O(1)
        peek:         O(1)
        clear:        O(n)
        copy:         O(n)
        is_empty:     O(1)
        is_full:      O(1)
        __len__:      O(1)
        __bool__:     O(1)
        __iter__:     O(n) — front to rear
        __reversed__: O(n)
        __contains__: O(n)
        __repr__:     O(n)
        __eq__:       O(n)
    """

    __slots__ = ("_data", "_front", "_rear", "_size")

    def __init__(self, *args, capacity: Optional[int] = None) -> None:
        """
        Creates a fixed-capacity circular universal queue with optional initial elements.

        Args:
            *args:    Optional initial elements, added left to right (first = front).
            capacity: Maximum number of elements the queue can hold.

        Raises:
            TypeError:     If capacity is not an int.
            TypeError:     If not provided at least one argument or capacity value.
            ValueError:    If capacity < 1.
            OverflowError: If len(args) > capacity.

        Examples:
            q = StaticUniversalCircularQueue(capacity=5)           # empty, capacity=5
            q = StaticUniversalCircularQueue(1, 2, 3, capacity=5)  # front=1, capacity=5
        """
        cap: int = validate_capacity(
            capacity, len(args), "StaticUniversalCircularQueue"
        )
        self._data: StaticUniversalArray = StaticUniversalArray(capacity=cap)
        self._front: int = 0
        self._rear: int = 0
        self._size: int = 0

        for item in args:
            self.enqueue(item)

    # -------------------------------------------------------------------------
    # Core operations

    def enqueue(self, value: Any) -> None:
        """
        Adds value at the rear of the queue.
        Rear index advances using modulo: (rear + 1) % capacity.

        Time complexity: O(1)

        Raises:
            OverflowError: If queue is full.
        """
        if self.is_full():
            raise OverflowError(f"Queue is full (capacity={len(self._data)})")
        self._data[self._rear] = value
        self._rear = (self._rear + 1) % len(self._data)
        self._size += 1

    def dequeue(self) -> Any:
        """
        Removes and returns the value from the front of the queue.
        Front index advances using modulo: (front + 1) % capacity.
        No element shifting — O(1).

        Time complexity: O(1)

        Raises:
            IndexError: If queue is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue")
        value = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1
        return value

    def peek(self) -> Any:
        """
        Returns the front element without removing it.

        Time complexity: O(1)

        Raises:
            IndexError: If queue is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from an empty queue")
        return self._data[self._front]

    def clear(self) -> None:
        """
        Removes all elements and resets front and rear to 0.
        Does not reallocate the buffer.

        Time complexity: O(n)
        """
        self._data.clear()
        self._front = 0
        self._rear = 0
        self._size = 0

    def copy(self) -> "StaticUniversalCircularQueue":
        """
        Returns a shallow copy with the same capacity and elements.

        Time complexity: O(n)
        """
        new_queue = StaticUniversalCircularQueue(capacity=len(self._data))
        for i in range(self._size):
            index = (self._front + i) % len(self._data)
            new_queue._data[i] = self._data[index]
        new_queue._rear = self._size % len(self._data)
        new_queue._size = self._size
        return new_queue

    # -------------------------------------------------------------------------
    # State checks

    def is_empty(self) -> bool:
        """Returns True if the queue contains no elements. O(1)"""
        return self._size == 0

    def is_full(self) -> bool:
        """Returns True if the queue has reached its capacity. O(1)"""
        return self._size == len(self._data)

    # -------------------------------------------------------------------------
    # Dunder methods

    def __len__(self) -> int:
        """Returns number of elements currently in the queue. O(1)"""
        return self._size

    def __bool__(self) -> bool:
        """Returns True if the queue is not empty. O(1)"""
        return self._size > 0

    def __iter__(self) -> Iterator[Any]:
        """
        Yields elements from front to rear without modifying the queue.

        Time complexity: O(n)
        """
        for i in range(self._size):
            yield self._data[(self._front + i) % len(self._data)]

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields elements from rear to front without modifying the queue.

        Time complexity: O(n)
        """
        for i in range(self._size - 1, -1, -1):
            yield self._data[(self._front + i) % len(self._data)]

    def __contains__(self, value: Any) -> bool:
        """Returns True if value exists in the queue. O(n)"""
        for i in range(self._size):
            if self._data[(self._front + i) % len(self._data)] == value:
                return True
        return False

    def __eq__(self, other: object) -> bool:
        """Returns True if both queues have the same size and elements in order."""
        if not isinstance(other, StaticUniversalCircularQueue):
            return NotImplemented
        if self._size != other._size:
            return False
        for i in range(self._size):
            a = self._data[(self._front + i) % len(self._data)]
            b = other._data[(other._front + i) % len(other._data)]
            if a != b:
                return False
        return True

    def __repr__(self) -> str:
        """
        Returns string representation of the queue.
        Format: StaticUniversalCircularQueue(size=3, capacity=5)[1, 2, 3]
                                                           front  rear

        Time complexity: O(n)
        """
        elements = ", ".join(
            repr(self._data[(self._front + i) % len(self._data)])
            for i in range(self._size)
        )
        return (
            f"StaticUniversalCircularQueue(size={self._size}, capacity={len(self._data)})"
            f"[{elements}]"
        )
