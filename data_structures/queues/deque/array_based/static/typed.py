from typing import Any, Iterator, Optional

from ....._base import BaseBoundedDeque
from ....._tools import validate_capacity, validate_value_type
from .....arrays import StaticTypedArray


class StaticTypedDeque(BaseBoundedDeque):
    """
    A fixed-capacity deque backed by StaticTypedArray.
    Enforces a single element type for all items.
    Supports insertion and removal from both ends.

    Supported dtypes: int, float, bool, str

    Naive implementation — front is always at index 0.
    enqueue_front and dequeue_front require shifting all elements.

    _rear — index where the next rear element will be written.

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

    __slots__ = ("_data", "_rear", "_dtype", "_str_length")

    def __init__(
        self,
        dtype: type,
        *args,
        str_length: Optional[int] = None,
        capacity: Optional[int] = None,
    ) -> None:
        """
        Creates a fixed-capacity typed deque with optional initial elements.

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
            d = StaticTypedDeque(int, capacity=5)           # empty, capacity=5
            d = StaticTypedDeque(int, 1, 2, 3, capacity=5)  # front=1, rear=3
        """
        self._dtype: type = dtype
        cap: int = validate_capacity(capacity, len(args), "StaticTypedDeque")
        self._data: StaticTypedArray = StaticTypedArray(
            dtype=dtype, capacity=cap, str_length=str_length
        )
        self._str_length: int = self._data._str_length
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
            OverflowError: If deque is full.
            TypeError:     If value is not dtype.
        """
        if self.is_full():
            raise OverflowError(f"Deque is full (capacity={len(self._data)})")
        validate_value_type(value, self._dtype)
        for i in range(self._rear, 0, -1):
            self._data._raw_set(i, self._data._raw_get(i - 1))
        self._data._raw_set(0, value)
        self._rear += 1

    def enqueue_rear(self, value: Any) -> None:
        """
        Adds value to the rear of the deque.

        Time complexity: O(1)

        Raises:
            OverflowError: If deque is full.
            TypeError:     If value is not dtype.
        """
        if self.is_full():
            raise OverflowError(f"Deque is full (capacity={len(self._data)})")
        validate_value_type(value, self._dtype)
        self._data._raw_set(self._rear, value)
        self._rear += 1

    def dequeue_front(self) -> Any:
        """
        Removes and returns the value from the front of the deque.
        Shifts all remaining elements one position to the left.

        Time complexity: O(n)

        Raises:
            IndexError: If deque is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from an empty deque")
        value = self._data._raw_get(0)
        self._rear -= 1
        for i in range(self._rear):
            self._data._raw_set(i, self._data._raw_get(i + 1))
        self._data._set_default(self._rear)
        return value

    def dequeue_rear(self) -> Any:
        """
        Removes and returns the value from the rear of the deque.

        Time complexity: O(1)

        Raises:
            IndexError: If deque is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from an empty deque")
        self._rear -= 1
        value = self._data._raw_get(self._rear)
        self._data._set_default(self._rear)
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
        return self._data._raw_get(0)

    def peek_rear(self) -> Any:
        """
        Returns the rear value without removing it.

        Time complexity: O(1)

        Raises:
            IndexError: If deque is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from an empty deque")
        return self._data._raw_get(self._rear - 1)

    def clear(self) -> None:
        """
        Removes all elements. Does not reallocate the buffer.

        Time complexity: O(n)
        """
        self._data.clear()
        self._rear = 0

    def copy(self) -> "StaticTypedDeque":
        """
        Returns a shallow copy with the same dtype and capacity.

        Time complexity: O(n)
        """
        new_deque = StaticTypedDeque(
            self._dtype, capacity=len(self._data), str_length=self._str_length
        )
        for i in range(self._rear):
            new_deque._data._raw_set(i, self._data._raw_get(i))
        new_deque._rear = self._rear
        return new_deque

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
            yield self._data._raw_get(i)

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields elements from rear to front without modifying the deque.

        Time complexity: O(n)
        """
        for i in range(self._rear - 1, -1, -1):
            yield self._data._raw_get(i)

    def __contains__(self, value: Any) -> bool:
        """
        Returns True if value exists in the deque. O(n)
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

    def __eq__(self, other: object) -> bool:
        """Returns True if both deques have the same dtype, size, and elements in order."""
        if not isinstance(other, StaticTypedDeque):
            return NotImplemented
        if self._rear != other._rear or self._dtype != other._dtype:
            return False
        for i in range(self._rear):
            if self._data._raw_get(i) != other._data._raw_get(i):
                return False
        return True

    def __repr__(self) -> str:
        """
        Returns string representation of the deque.
        Format: StaticTypedDeque(int, size=3, capacity=5)[1, 2, 3]
                                                           front  rear

        Time complexity: O(n)
        """
        elements = ", ".join(repr(self._data._raw_get(i)) for i in range(self._rear))
        return (
            f"StaticTypedDeque({self._dtype.__name__}, "
            f"size={self._rear}, capacity={len(self._data)})"
            f"[{elements}]"
        )
