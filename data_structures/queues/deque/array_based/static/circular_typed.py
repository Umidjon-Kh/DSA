from typing import Any, Iterator, Optional

from ....._base import BaseBoundedDeque
from ....._tools import validate_capacity, validate_value_type
from .....arrays import StaticTypedArray


class StaticTypedCircularDeque(BaseBoundedDeque):
    """
    A fixed-capacity circular deque backed by StaticTypedArray.
    Enforces a single element type for all items.
    Supports O(1) insertion and removal from both ends.

    Supported dtypes: int, float, bool, str

    Uses circular indexing — front and rear wrap around the buffer
    using modulo arithmetic. No element shifting is ever needed.

    _front — index of the front element.
    _rear  — index where the next rear element will be written.
    _size  — number of elements currently in the deque.

    enqueue_front moves _front backward: (_front - 1) % capacity
    enqueue_rear  moves _rear  forward:  (_rear  + 1) % capacity
    dequeue_front moves _front forward:  (_front + 1) % capacity
    dequeue_rear  moves _rear  backward: (_rear  - 1) % capacity

    Time complexity:
        enqueue_front:  O(1)
        enqueue_rear:   O(1)
        dequeue_front:  O(1)
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

    __slots__ = ("_data", "_front", "_rear", "_size", "_dtype", "_str_length")

    def __init__(
        self,
        dtype: type,
        *args,
        str_length: Optional[int] = None,
        capacity: Optional[int] = None,
    ) -> None:
        """
        Creates a fixed-capacity circular typed deque with optional initial elements.

        Args:
            dtype:      Element type. Supported: int, float, bool, str.
            capacity:   Maximum number of elements the deque can hold.
            *args:      Optional initial elements, added left to right (first = front).
            str_length: Max characters per str element (default: 20).

        Raises:
            TypeError:     If dtype is not a supported type.
            TypeError:     If capacity is not an int.
            ValueError:    If capacity < 1.
            TypeError:     If any element in args is not dtype.
            OverflowError: If len(args) > capacity.
            TypeError:     If not provided at least one argument or capacity value.

        Examples:
            d = StaticTypedCircularDeque(int, capacity=5)           # empty, capacity=5
            d = StaticTypedCircularDeque(int, 1, 2, 3, capacity=5)  # front=1, rear=3
        """
        self._dtype: type = dtype
        cap: int = validate_capacity(capacity, len(args), "StaticTypedCircularDeque")
        self._data: StaticTypedArray = StaticTypedArray(
            dtype=dtype, capacity=cap, str_length=str_length
        )
        self._str_length: int = self._data._str_length
        self._front: int = 0
        self._rear: int = 0
        self._size: int = 0

        for item in args:
            self.enqueue_rear(item)

    # -------------------------------------------------------------------------
    # Core operations

    def enqueue_front(self, value: Any) -> None:
        """
        Adds value to the front of the deque.
        _front moves backward: (_front - 1) % capacity.

        Time complexity: O(1)

        Raises:
            OverflowError: If deque is full.
            TypeError:     If value is not dtype.
        """
        if self.is_full():
            raise OverflowError(f"Deque is full (capacity={len(self._data)})")
        validate_value_type(value, self._dtype)
        self._front = (self._front - 1) % len(self._data)
        self._data._raw_set(self._front, value)
        self._size += 1

    def enqueue_rear(self, value: Any) -> None:
        """
        Adds value to the rear of the deque.
        _rear moves forward: (_rear + 1) % capacity.

        Time complexity: O(1)

        Raises:
            OverflowError: If deque is full.
            TypeError:     If value is not dtype.
        """
        if self.is_full():
            raise OverflowError(f"Deque is full (capacity={len(self._data)})")
        validate_value_type(value, self._dtype)
        self._data._raw_set(self._rear, value)
        self._rear = (self._rear + 1) % len(self._data)
        self._size += 1

    def dequeue_front(self) -> Any:
        """
        Removes and returns the value from the front of the deque.
        _front moves forward: (_front + 1) % capacity.

        Time complexity: O(1)

        Raises:
            IndexError: If deque is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from an empty deque")
        value = self._data._raw_get(self._front)
        self._data._set_default(self._front)
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1
        return value

    def dequeue_rear(self) -> Any:
        """
        Removes and returns the value from the rear of the deque.
        _rear moves backward: (_rear - 1) % capacity.

        Time complexity: O(1)

        Raises:
            IndexError: If deque is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from an empty deque")
        self._rear = (self._rear - 1) % len(self._data)
        value = self._data._raw_get(self._rear)
        self._data._set_default(self._rear)
        self._size -= 1
        return value

    def peek_front(self) -> Any:
        """
        Returns the front value without removing it.

        Time complexity: O(1)

        Raises:
            IndexError: If deque is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from an empty deque")
        return self._data._raw_get(self._front)

    def peek_rear(self) -> Any:
        """
        Returns the rear value without removing it.

        Time complexity: O(1)

        Raises:
            IndexError: If deque is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from an empty deque")
        return self._data._raw_get((self._rear - 1) % len(self._data))

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

    def copy(self) -> "StaticTypedCircularDeque":
        """
        Returns a shallow copy with the same dtype and capacity.
        Elements are linearized — copy always has front=0.

        Time complexity: O(n)
        """
        new_deque = StaticTypedCircularDeque(
            dtype=self._dtype,
            capacity=len(self._data),
            str_length=self._str_length,
        )
        for i in range(self._size):
            index = (self._front + i) % len(self._data)
            new_deque._data._raw_set(i, self._data._raw_get(index))
        new_deque._rear = self._size
        new_deque._size = self._size
        return new_deque

    # -------------------------------------------------------------------------
    # State checks

    def is_empty(self) -> bool:
        """Returns True if the deque contains no elements. O(1)"""
        return self._size == 0

    def is_full(self) -> bool:
        """Returns True if the deque has reached its capacity. O(1)"""
        return self._size == len(self._data)

    # -------------------------------------------------------------------------
    # Dunder methods

    def __len__(self) -> int:
        """Returns number of elements currently in the deque. O(1)"""
        return self._size

    def __bool__(self) -> bool:
        """Returns True if the deque is not empty. O(1)"""
        return self._size > 0

    def __iter__(self) -> Iterator[Any]:
        """
        Yields elements from front to rear without modifying the deque.

        Time complexity: O(n)
        """
        for i in range(self._size):
            yield self._data._raw_get((self._front + i) % len(self._data))

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields elements from rear to front without modifying the deque.

        Time complexity: O(n)
        """
        for i in range(self._size - 1, -1, -1):
            yield self._data._raw_get((self._front + i) % len(self._data))

    def __contains__(self, value: Any) -> bool:
        """
        Returns True if value exists in the deque. O(n)
        Returns False instantly for wrong type.
        """
        try:
            validate_value_type(value, self._dtype)
        except TypeError:
            return False
        for i in range(self._size):
            if self._data._raw_get((self._front + i) % len(self._data)) == value:
                return True
        return False

    def __eq__(self, other: object) -> bool:
        """Returns True if both deques have the same dtype, size, and elements in order."""
        if not isinstance(other, StaticTypedCircularDeque):
            return NotImplemented
        if self._size != other._size or self._dtype != other._dtype:
            return False
        for i in range(self._size):
            a = self._data._raw_get((self._front + i) % len(self._data))
            b = other._data._raw_get((other._front + i) % len(other._data))
            if a != b:
                return False
        return True

    def __repr__(self) -> str:
        """
        Returns string representation of the deque.
        Format: StaticTypedCircularDeque(int, size=3, capacity=5)[1, 2, 3]
                                                             front  rear

        Time complexity: O(n)
        """
        elements = ", ".join(
            repr(self._data._raw_get((self._front + i) % len(self._data)))
            for i in range(self._size)
        )
        return (
            f"StaticTypedCircularDeque({self._dtype.__name__}, "
            f"size={self._size}, capacity={len(self._data)})"
            f"[{elements}]"
        )
