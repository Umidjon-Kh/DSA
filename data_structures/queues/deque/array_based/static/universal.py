from typing import Any, Iterator, Optional

from ....._base import BaseBoundedDeque
from ....._tools import validate_capacity
from .....arrays import StaticUniversalArray


class StaticUniversalDeque(BaseBoundedDeque):
    """
    A fixed-capacity deque backed by StaticUniversalArray.
    Accepts any Python type - no dtype restriction.
    Follows FIFO (first In, First Out) principle.

    Naive implementation - front is always at index 0.
    enqueue_front and dequeue_front require shifting all elements.

    _rear - index where the next rear element will be written.

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
        is_full:        O(1)
        __len__:        O(1)
        __bool__:       O(1)
        __iter__:       O(n) — front to rear
        __reversed__:   O(n)
        __contains__:   O(n)
        __repr__:       O(n)
        __eq__:         O(n)
    """

    __slots__ = ("_data", "_rear")

    def __init__(self, *args, capacity: Optional[int] = None) -> None:
        """
        Creates a fixed-capacity universal deque with optional initial elements.

        Args:
            capacity: Maximum number of elements the deque can hold.
            *args:   Optioan initial elements, added left to right (first = front)

        Raises:
            TypeError:     if capacity is not an int.
            TypeError:     if not provided at least one argument or capacity value.
            ValueError:    if capacity < 1.
            OverflowError: if len(args) > capacity.

        Examples:
            d = StaticUniversalDeque(capacity=5)    # empty, capacity=5
            d = StaticUniversalDeque(1, 2, 3, capacity=5) # front=1, rear=3, capacity=5
        """
        cap: int = validate_capacity(capacity, len(args), "StaticUniversalDeque")
        self._data: StaticUniversalArray = StaticUniversalArray(capacity=cap)
        self._rear: int = 0

        for item in args:
            self.enqueue_rear(item)

    # -------------------------------------------------------------------------
    # Core operations

    def enqueue_front(self, value: Any) -> None:
        """
        Adds value to the front of the deque.
        Shifts all existing elements one position to the right first.

        Time complexity: O(n)

        Raises:
            OverflowError: if deque is full.
        """
        if self.is_full():
            raise OverflowError(f"Deque is full (capacity={len(self._data)})")
        for i in range(self._rear, 0, -1):
            self._data[i] = self._data[i - 1]
        self._data[0] = value
        self._rear += 1

    def enqueue_rear(self, value: Any) -> None:
        """
        Adds value to the rear of the deque.

        Time complexity: O(1)

        Raises:
            OverflowError: if deque is full.
        """
        if self.is_full():
            raise OverflowError(f"Deque is full (capacity={len(self._data)})")
        self._data[self._rear] = value
        self._rear += 1

    def dequeue_front(self) -> Any:
        """
        Removes and returns the value from the front of the deque.
        Shifts all reamaining elements one position to the left.

        Time complexity: O(n)

        Raises:
            IndexError: if deque is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from an empty deque")
        value = self._data[0]
        self._rear -= 1
        for i in range(self._rear):
            self._data[i] = self._data[i + 1]
        self._data[self._rear] = None
        return value

    def dequeue_rear(self) -> Any:
        """
        Removes and returns the value from the rear of the deque.

        Time complexity: O(1)

        Raises:
            IndexError: if deque is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from an empty deque")
        self._rear -= 1
        value = self._data[self._rear]
        self._data[self._rear] = None
        return value

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
        return self._data[self._rear - 1]

    def clear(self) -> None:
        """
        Removes all elements. Does not reallocate the buffer.

        Time complexity: O(n)
        """
        self._data.clear()
        self._rear = 0

    def copy(self) -> "StaticUniversalDeque":
        """
        Returns a shallow copy with the capacity and data.

        Time complexity: O(n)
        """
        new_queue = StaticUniversalDeque(capacity=len(self._data))

        for i in range(self._rear):
            new_queue._data[i] = self._data[i]
        new_queue._rear = self._rear
        return new_queue

    # -------------------------------------------------------------------------
    # State checks

    def is_empty(self) -> bool:
        """Returns True if the deque contains no elements. O(1)"""
        return self._rear == 0

    def is_full(self) -> bool:
        """Returns True if the deque has reached its capacity. O(1)"""
        return self._rear == len(self._data)

    # -------------------------------------------------------------------------
    # Dunder methods

    def __len__(self) -> int:
        """Returns number of elements currently in the deque. O(1)"""
        return self._rear

    def __bool__(self) -> bool:
        """Returns True if the deque is not empty. O(1)"""
        return self._rear > 0

    def __iter__(self) -> Iterator[Any]:
        """
        Yields elements from front to rear without modifying the deque.

        Time complexity: O(n)
        """
        for i in range(self._rear):
            yield self._data[i]

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields elements from rear to front without modifying the deque.

        Time complexity: O(n)
        """
        for i in range(self._rear - 1, -1, -1):
            yield self._data[i]

    def __contains__(self, value: Any) -> bool:
        """
        Returns True if value exists in the deque. O(n)
        """
        for i in range(self._rear):
            if self._data[i] == value:
                return True
        return False

    def __eq__(self, other: object) -> bool:
        """Returns True if both strcutures data and rear attrs are equal."""
        if not isinstance(other, StaticUniversalDeque):
            return NotImplemented
        if self._rear != other._rear:
            return False
        for i in range(self._rear):
            if self._data[i] != other._data[i]:
                return False
        return True

    def __repr__(self) -> str:
        """
        Returns string representation of the deque.
        Format: StaticUniversalDeque(size=3, capacity=5)[1, 2, 3]
                                                      front    rear

        Time complexity: O(n)
        """
        elements = ", ".join(repr(self._data[i]) for i in range(self._rear))
        return (
            f"StaticUniversalDeque(size={self._rear}, capacity={len(self._data)})"
            f"[{elements}]"
        )
