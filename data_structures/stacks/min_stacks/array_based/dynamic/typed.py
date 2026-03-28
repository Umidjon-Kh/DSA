from typing import Any, Callable, Iterator, Optional

from ....._base import BaseStack
from ....._tools import validate_key_function
from .....arrays import DynamicTypedArray


class DynamicTypedMinStack(BaseStack):
    """
    A dynamic stack backed by DynamicTypedArray.
    Grows automatically when capacity is exceeded and
    tracks current minimum object in O(1).
    Follows LIFO (Last In, First Out) principle.

    Supported dtypes: int, float, bool, str

    Growth formula (delegated to DynamicTypedArray — same as CPython list):
        new_capacity = capacity + (capacity >> 3) + (3 if capacity < 9 else 6)

    A key function maps each stored value to a comparable key.
    The minimum is tracked by key, not raw value.

    _data = main array to store all pushed objects.
    _min_data = to store only current minimum objects computed by key.

    A value is pushed onto the min stack only when the min stack is empty
    or key(value) <= key(current minimum). On pop, if the poped value's
    key matches the current minimum's key, the min stack is also popped.

    Time complexity:
        push:         O(1) amortized - O(n) on resize
        pop:          O(1)
        peek:         O(1)
        min:          O(1)
        clear:        O(1)
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

    __slots__ = (
        "_data",
        "_min_data",
        "_dtype",
        "_str_length",
        "_key",
    )

    def __init__(
        self,
        dtype: type,
        *args,
        str_length: Optional[int] = None,
        key: Optional[Callable] = None,
    ) -> None:
        """
        Creates a dynamic min stack with optional initial elements.

        Args:
            *args:      Optional initial elements, pushed left to right (last = top).
            dtype:      Element type. Supported: int, float, bool, str.
            str_length: Max characters per str element (default: 20)
            key:        Callable applied to each value before comparison.
                        Defaults to identity (lambda x: x) if None.

        Raises:
            TypeError: if dtype is not supported type.
            TypeError: if any element in args is not dtype.
            TypeError: if key is provided but not callable.

        Examples:
            s = DynamicTypedMinStack(int)                 # empty
            s = DynamicTypedMinStack(int, 1, 2, 4)        # top=3
            s = DynamicTypedMinStack(key=lambda x: -x)    # max-as-min behaviour
            s = DynamicTypedMinStack(key=lambda x: x[1])  # keyed by second element
        """
        self._key: Callable = validate_key_function(key)
        self._dtype = dtype
        self._data: DynamicTypedArray = DynamicTypedArray(
            dtype=dtype, str_length=str_length
        )
        self._min_data: DynamicTypedArray = DynamicTypedArray(
            dtype=dtype, str_length=str_length
        )
        self._str_length = self._data._str_length

        for item in args:
            self.push(item)

    # -------------------------------------------------------------------------
    # Core operations

    def push(self, value: Any) -> None:
        """
        Pushes value onto the top of the main data.
        Also pushes onto the min data when the min data is empty
        or key(value) <= key(current minimum).

        Time complexity: O(1) amortized — O(n) on resize

        Raises:
            TypeError: If value is not dtype.
        """
        self._data.append(value)

        if not self._min_data or self._key(value) <= self._key(
            self._min_data[len(self._min_data) - 1]
        ):
            self._min_data.append(value)

    def pop(self) -> Any:
        """
        Removes and returns the top of main data.
        If key(popped) == key(current minimum), the min data is also popped.

        Time complexity: O(1)

        Raises:
            IndexError: if stack is empty
        """
        if self.is_empty():
            raise IndexError("Pop from an empty stack")

        value = self._data.remove(len(self._data) - 1)

        if self._key(value) == self._key(self._min_data[len(self._min_data) - 1]):
            self._min_data.remove(len(self._min_data) - 1)

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
        return self._data[len(self._data) - 1]

    def min(self) -> Any:
        """
        Returns the current minimum value (by key) wihtout removing it.

        Time complexity: O(1)

        Raises:
            IndexError: if stack is empty
        """
        if self.is_empty():
            raise IndexError("Min from an empty stack")
        return self._min_data[len(self._min_data) - 1]

    def clear(self) -> None:
        """
        Removes all elements. Does not shrink the underlying buffer.

        Time complexity: O(n)
        """
        self._data.clear()
        self._min_data.clear()

    def copy(self) -> "DynamicTypedMinStack":
        """
        Returns a shallow copy with the same elements.

        Time complexity: O(n)
        """
        new_stack = DynamicTypedMinStack(
            dtype=self._dtype,
            str_length=self._str_length,
            key=self._key,
        )
        for i in range(len(self._data)):
            new_stack._data.append(self._data[i])
            if len(self._min_data) > i:
                new_stack._min_data.append(self._min_data[i])
        return new_stack

    # -------------------------------------------------------------------------
    # State checks

    def is_empty(self) -> bool:
        """Returns True if the stack contains no elements. O(1)"""
        return len(self._data) == 0

    # -------------------------------------------------------------------------
    # Dunder methods

    def __len__(self) -> int:
        """Returns number of elements currently in the stack. O(1)"""
        return len(self._data)

    def __bool__(self) -> bool:
        """Returns True if the stack is not empty. O(1)"""
        return len(self._data) > 0

    def __iter__(self) -> Iterator[Any]:
        """
        Yields elements from top to bottom without modifying the stack.

        Time complexity: O(n)
        """
        for i in range(len(self._data) - 1, -1, -1):
            yield self._data[i]

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields elements from bottom to top without modifying the stack.

        Time complexity: O(n)
        """
        for i in range(len(self._data)):
            yield self._data[i]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DynamicTypedMinStack):
            return NotImplemented
        # I removed other conditions
        # Cause in data: DynamicTypedArray it checks auto.
        return self._data == other._data

    def __contains__(self, value: Any) -> bool:
        """Returns True if value exists in the stack. O(n)"""
        return value in self._data

    def __repr__(self) -> str:
        """
        Returns string representation of the stack.
        Format: DynamicTypedMinStack(size=3, min=1)[3, 2, 1]
                                            top   bottom

        Time complexity: O(n)
        """
        min_repr = (
            repr(self._min_data[len(self._min_data) - 1]) if self._min_data else None
        )
        elements = ", ".join(repr(v) for v in self)
        return f"DynamicTypedMinStack({self._dtype.__name__}, size={len(self._data)}, min={min_repr})[{elements}]"
