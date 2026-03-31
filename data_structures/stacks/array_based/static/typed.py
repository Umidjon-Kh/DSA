from typing import Any, Iterator, Optional

from ...._base import BaseBoundedStack
from ...._tools import validate_capacity, validate_value_type
from ....arrays import StaticTypedArray


class StaticTypedStack(BaseBoundedStack):
    """
    A fixed-capacity stack backed by StaticTypedArray.
    Enforces a single element type for all items.
    Follows LIFO (Last In, First Out) principle.

    Supported dtypes: int, float, bool, str

    Time complexity:
        push:         O(1)
        pop:          O(1)
        peek:         O(1)
        clear:        O(n)
        copy:         O(n)
        is_empty:     O(1)
        is_full:      O(1)
        __len__:      O(1)
        __bool__:     O(1)
        __iter__:     O(n) — top to bottom
        __reversed__: O(n)
        __contains__: O(n)
        __repr__:     O(n)
        __eq__:       O(n)
    """

    __slots__ = ("_data", "_top", "_dtype", "_str_length")

    def __init__(
        self,
        dtype: type,
        *args,
        str_length: Optional[int] = None,
        capacity: Optional[int] = None,
    ) -> None:
        """
        Creates a fixed-capacity typed stack with optional initial elements.

        Args:
            dtype:      Element type. Supported: int, float, bool, str.
            capacity:   Maximum number of elements the stack can hold.
            *args:      Optional initial elements, pushed left to right (last = top).
            str_length: Max characters per str element (default: 20).

        Raises:
            TypeError:     If dtype is not a supported type.
            TypeError:     If capacity is not an int.
            ValueError:    If capacity < 1.
            TypeError:     If any element in args is not dtype.
            OverflowError: If len(args) > capacity.
            TypeError:     if not provided at least one argument or capacity value.

        Examples:
            s = StaticTypedStack(int, capacity=5)           # empty, capacity=5
            s = StaticTypedStack(int, 1, 2, 3, capacity=5)  # top=3, capacity=5
        """
        self._dtype: type = dtype
        self._top: int = 0
        cap: int = validate_capacity(capacity, len(args), "StaticTypedStack")
        self._data: StaticTypedArray = StaticTypedArray(
            dtype=dtype, capacity=cap, str_length=str_length
        )
        self._str_length: int = self._data._str_length

        for item in args:
            self.push(item)

    # -------------------------------------------------------------------------
    # Core operations

    def push(self, value: Any) -> None:
        """
        Pushes value onto the top of the stack.

        Time complexity: O(1)

        Raises:
            TypeError:     If value is not dtype.
            OverflowError: If stack is full.
        """
        if self.is_full():
            raise OverflowError(f"Stack is full (capacity={len(self._data)})")
        validate_value_type(value, self._dtype)
        self._data._raw_set(self._top, value)
        self._top += 1

    def pop(self) -> Any:
        """
        Removes and returns the top element.

        Time complexity: O(1)

        Raises:
            IndexError: If stack is empty.
        """
        if self.is_empty():
            raise IndexError("Pop from an empty stack")
        self._top -= 1
        value = self._data._raw_get(self._top)
        self._data._set_default(self._top)
        return value

    def peek(self) -> Any:
        """
        Returns the top element without removing it.

        Time complexity: O(1)

        Raises:
            IndexError: If stack is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from an empty stack")
        return self._data._raw_get(self._top - 1)

    def clear(self) -> None:
        """
        Removes all elements. Does not reallocate the buffer.

        Time complexity: O(n)
        """
        self._top = 0
        self._data.clear()

    def copy(self) -> "StaticTypedStack":
        """
        Returns a shallow copy with same dtype and capacity.

        Time complexity: O(n)
        """
        new_stack = StaticTypedStack(
            dtype=self._dtype,
            capacity=len(self._data),
            str_length=self._str_length,
        )
        for i in range(self._top):
            new_stack._data._raw_set(i, self._data._raw_get(i))
        new_stack._top = self._top
        return new_stack

    # -------------------------------------------------------------------------
    # State checks

    def is_empty(self) -> bool:
        """Returns True if the stack contains no elements. O(1)"""
        return self._top == 0

    def is_full(self) -> bool:
        """Returns True if the stack has reached its capacity. O(1)"""
        return self._top == len(self._data)

    # -------------------------------------------------------------------------
    # Dunder methods

    def __len__(self) -> int:
        """Returns number of elements currently in the stack. O(1)"""
        return self._top

    def __bool__(self) -> bool:
        """Returns True if the stack is not empty. O(1)"""
        return self._top > 0

    def __iter__(self) -> Iterator[Any]:
        """
        Yields elements from top to bottom without modifying the stack.

        Time complexity: O(n)
        """
        for i in range(self._top - 1, -1, -1):
            yield self._data._raw_get(i)

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields elements from bottom to top without modifying the stack.

        Time complexity: O(n)
        """
        for i in range(self._top):
            yield self._data._raw_get(i)

    def __eq__(self, other: object) -> bool:
        """Returns True if both structures data and dtype, top attrs equal."""
        if not isinstance(other, StaticTypedStack):
            return NotImplemented
        if self._top != other._top or self._dtype != other._dtype:
            return False
        # Checking to top cause if i use StaticArray eq method
        # It check for capacity equality too.
        for i in range(self._top):
            if self._data._raw_get(i) != other._data._raw_get(i):
                return False
        return True

    def __contains__(self, value: Any) -> bool:
        """
        Returns True if value exists in the stack. O(n)
        Returns False instantly for wrong type.
        """
        try:
            validate_value_type(value, self._dtype)
        except TypeError:
            return False
        for i in range(self._top):
            if self._data._raw_get(i) == value:
                return True
        return False

    def __repr__(self) -> str:
        """
        Returns string representation of the stack.
        Format: StaticTypedStack(int, size=3, capacity=5)[3, 2, 1]
                                                          top      bottom

        Time complexity: O(n)
        """
        elements = ", ".join(
            repr(self._data._raw_get(i)) for i in range(self._top - 1, -1, -1)
        )
        return (
            f"StaticTypedStack({self._dtype.__name__}, "
            f"size={self._top}, capacity={len(self._data)})"
            f"[{elements}]"
        )
