from typing import Any, Iterator

from ...._base import BaseStack
from ....arrays import DynamicUniversalArray


class DynamicUniversalStack(BaseStack):
    """
    A dynamic stack backed by DynamicUniversalArray.
    Grows automatically when capacity is exceeded.
    Accepts any Python type — no dtype restriction.
    Follows LIFO (Last In, First Out) principle.

    Growth formula (delegated to DynamicUniversalArray — same as CPython list):
        new_capacity = capacity + (capacity >> 3) + (3 if capacity < 9 else 6)

    Time complexity:
        push:         O(1) amortized — O(n) on resize
        pop:          O(1)
        peek:         O(1)
        clear:        O(n)
        copy:         O(n)
        is_empty:     O(1)
        __len__:      O(1)
        __bool__:     O(1)
        __iter__:     O(n) — top to bottom
        __reversed__: O(n)
        __contains__: O(n)
        __repr__:     O(n)
        __eq__:       O(n)
    """

    __slots__ = ("_data",)

    def __init__(self, *args) -> None:
        """
        Creates a dynamic universal stack with optional initial elements.

        Args:
            *args: Optional initial elements, pushed left to right (last = top).

        Examples:
            s = DynamicUniversalStack()              # empty
            s = DynamicUniversalStack(1, "hi", 3.0)  # top=3.0
        """
        self._data: DynamicUniversalArray = DynamicUniversalArray()

        for item in args:
            self.push(item)

    # -------------------------------------------------------------------------
    # Core operations

    def push(self, value: Any) -> None:
        """
        Pushes value onto the top of the stack.
        Triggers resize if underlying array is at capacity.

        Time complexity: O(1) amortized — O(n) on resize
        """
        self._data.append(value)

    def pop(self) -> Any:
        """
        Removes and returns the top element.

        Time complexity: O(1)

        Raises:
            IndexError: If stack is empty.
        """
        if self.is_empty():
            raise IndexError("Pop from an empty stack")
        return self._data.remove(len(self._data) - 1)

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

    def clear(self) -> None:
        """
        Removes all elements. Does not shrink the underlying buffer.

        Time complexity: O(n)
        """
        self._data.clear()

    def copy(self) -> "DynamicUniversalStack":
        """
        Returns a shallow copy with the same elements.

        Time complexity: O(n)
        """
        new_stack = DynamicUniversalStack()
        for i in range(len(self._data)):
            new_stack._data.append(self._data[i])
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
        """Returns True if both structure data attrs are equal."""
        if not isinstance(other, DynamicUniversalStack):
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
        Format: DynamicUniversalStack(size=3)[3.0, 'hi', 1]
                                             top          bottom

        Time complexity: O(n)
        """
        size = len(self._data)
        elements = ", ".join(repr(self._data[i]) for i in range(size - 1, -1, -1))
        return f"DynamicUniversalStack(size={size})[{elements}]"
