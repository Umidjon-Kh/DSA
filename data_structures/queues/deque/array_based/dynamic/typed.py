from typing import Any, Iterator, Optional

from ....._base import BaseDeque
from .....arrays import DynamicTypedArray


class DynamicTypedDeque(BaseDeque):
    """
    A dynamic deque backed by DynamicTypedArray.
    Grows automatically when capacity is exceeded.
    Enfroces a single element type for all items.
    Follows FIFO (First In, First Out) principle.

    Supported dtypes: int, float, bool, str

    Growth formula (delegated to DynamicTypedArray - same as CPython list):
        new_capacity = capacity + (capacity >> 3) + (3 if capacity < 9 else 6)

    Naive implementation — front is always at index 0.
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

    __slots__ = ("_data", "_dtype", "_str_length")

    def __init__(
        self,
        dtype: type,
        *args,
        str_length: Optional[int] = None,
    ) -> None:
        """
        Creates a dynamic typed deque with optional initial elements.

        Args:
            dtype:      Elements type. Supported: int, float, bool, str.
            *args:      Optional initial elements, added left to right (first = front).
            str_length: Max characters per str element (default 20)

        Raises:
            TypeError: if dtype is not supported type.
            TypeError: if any elements in args is not dtype.

        Examples:
            d = DynamicTypedDeque(int)          # empty
            d = DynamicTypedDeque(int, 1, 2, 3) # fron=1, rear=3
        """
        self._dtype: type = dtype
        self._data: DynamicTypedArray = DynamicTypedArray(
            dtype=dtype, str_length=str_length
        )
        self._str_length = self._data._str_length

        for item in args:
            self.enqueue_rear(item)

    # -------------------------------------------------------------------------
    # Core operations

    def enqueue_front(self, value: Any) -> None:
        """
        Adds value to the front of the deque.
        Shifts all existing elements one position to the right first.
        Triggers resize if underlying array is at capacity.

        Time complexity: O(1) amortized - O(n) on resize

        Raises:
            TypeError: if value is not dtype.
        """
        self._data.insert(0, value)

    def enqueue_rear(self, value: Any) -> None:
        """
        Adds value to the front of the deque.
        Also triggers resize if underlying array is at capacity.

        Time complexity: O(1) amortized- O(n) on resize.

        Raises:
            TypeError: if value is not dtype.
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
        Removes and returns the value from the front of the deque.

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
            IndexError: If deque is empty.
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

    def copy(self) -> "DynamicTypedDeque":
        """
        Returns a shallow copy with the same dtype and elements.

        Time complexity: O(n)
        """
        new_deque = DynamicTypedDeque(
            dtype=self._dtype,
            str_length=self._str_length,
        )
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
        """Returns True if deque is not empty. O(1)"""
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
        """Returns True if both structures data and dtypes are equal."""
        if not isinstance(other, DynamicTypedDeque):
            return NotImplemented
        return self._data == other._data

    def __contains__(self, value: Any) -> bool:
        """
        Returns True if value exists in deque. O(n)
        Returns False instantly for wrong type.
        """
        return value in self._data

    def __repr__(self) -> str:
        """
        Returns string representation of the queue.
        Format: DynamicTypedDeque(int, size=3)[1, 2, 3]
                                            front    rear

        Time complexity: O(n)
        """
        size = len(self._data)
        elements = ", ".join(repr(self._data[i]) for i in range(len(self._data)))
        return f"DynamicTypedDeque({self._dtype.__name__}, size={size})[{elements}]"
