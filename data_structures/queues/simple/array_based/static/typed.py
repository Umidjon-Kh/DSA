from typing import Any, Iterator, Optional

from ....._base import BaseBoundedQueue
from ....._tools import validate_capacity, validate_value_type
from .....arrays import StaticTypedArray


class StaticTypedQueue(BaseBoundedQueue):
    """
    A fixed-capacity queue backed by StaticTypedArray.
    Enforces a single element type for all items.
    Follows FIFO (First In, First Out) principle.

    Supported dtypes: int, float, bool, str

    Simple Queue — naive implementation, front always at index 0.
    After every dequeue, all elements need to be shifted left.

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

    __slots__ = (
        "_data",
        "_rear",
        "_dtype",
        "_str_length",
    )

    def __init__(
        self,
        dtype: type,
        *args,
        str_length: Optional[int] = None,
        capacity: Optional[int] = None,
    ) -> None:
        """
        Creates a fixed-capacity typed queue with optional initial elements.

        Args:
            dtype:      Element type. Supported: int, float, bool, str.
            capacity:   Maximum number of elements the queue can hold.
            *args:      Optional initial elements, pushed left to right (first = front)
            str_length: Max characters per str element (default 20).

        Raises:
            TypeError:     if dtype is not a supported type.
            TypeError:     if capacity is not an int.
            ValueError:    if capacity < 1.
            TypeError:     if any element in args is not dtype.
            OverflowError: if len(args) > capacity.
            TypeError:     if not provided at least one argument or capacity value.

        Examples:
            s = StaticTypedQueue(int, capacity=5)            # empty, capacity=5
            s = StaticTypedQueue(int,  1, 2, 3, capacity=5)  # front=1, capacity=5
        """
        self._dtype: type = dtype
        cap: int = validate_capacity(capacity, len(args), "StaticTypedQueue")
        self._data: StaticTypedArray = StaticTypedArray(
            dtype=dtype, capacity=cap, str_length=str_length
        )
        self._rear: int = 0
        self._str_length = self._data._str_length

        for item in args:
            self.enqueue(item)

    # -------------------------------------------------------------------------
    # Core operations
    def enqueue(self, value: Any) -> None:
        """
        Adds value to the rear of the queue.

        Time complexity: O(1)

        Raises:
            TypeError:     if value is not dtype.
            OverflowError: if queue is full.
        """
        if self.is_full():
            raise OverflowError(f"Queue is full (capacity={len(self._data)})")
        validate_value_type(value, self._dtype)
        self._data._raw_set(self._rear, value)
        self._rear += 1

    def dequeue(self) -> Any:
        """
        Removes and returns the value from th front of the queue.
        After removing need to shift all elements from right to left.

        Time complexity: O(n)

        Raises:
            IndexError: if queue is empty.
        """
        if self.is_empty():
            raise IndexError("Pop from an empty queue")
        self._rear -= 1
        value = self._data._raw_get(0)
        # Shifting all elements from right to left
        for index in range(self._rear):
            self._data._raw_set(index, self._data._raw_get(index + 1))

        self._data._set_default(self._rear)
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
        return self._data._raw_get(0)

    def clear(self) -> None:
        """
        Removes all elements. Does not reallocate the buffer.

        Time complexity: O(n)
        """
        self._rear = 0
        self._data.clear()

    def copy(self) -> "StaticTypedQueue":
        """
        Returns a shallow copy with same dtype and capacity.

        Time complexity: O(n)
        """
        new_queue = StaticTypedQueue(
            dtype=self._dtype,
            capacity=len(self._data),
            str_length=self._str_length,
        )

        for i in range(self._rear):
            new_queue._data._raw_set(i, self._data._raw_get(i))
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

    def __len__(self) -> int:
        """Returns number of elements currently in the qeueu. O(1)"""
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
            yield self._data._raw_get(i)

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields elements from rear to front without modifying the queue.

        Time complexity: O(n)
        """
        for i in range(self._rear - 1, -1, -1):
            yield self._data._raw_get(i)

    def __eq__(self, other: object) -> bool:
        """Returns True if both structures data and dtype, rear and front attrs equal."""
        if not isinstance(other, StaticTypedQueue):
            return NotImplemented
        if self._rear != other._rear or self._dtype != other._dtype:
            return False
        for i in range(self._rear):
            if self._data._raw_get(i) != other._data._raw_get(i):
                return False
        return True

    def __contains__(self, value: Any) -> bool:
        """
        Returns True if value exists in the queue. O(n)
        Returns False instantly for wrong type.
        """
        try:
            validate_value_type(value, self._dtype)
        except TypeError:
            return False
        for i in range(self._rear):
            if self._data._raw_get(i) == value:
                return True
        return False

    def __repr__(self) -> str:
        """
        Returns string representation of the queue.
        Format: StaticTypedQueue(int, size=3, capacity=5)[1, 2, 3]
                                               front    rear

        Time complexity: O(n)
        """
        elements = ", ".join(repr(self._data._raw_get(i)) for i in range(self._rear))
        return (
            f"StaticTypedQueue({self._dtype.__name__}, "
            f"size={self._rear}, capacity={len(self._data)})"
            f"[{elements}]"
        )
