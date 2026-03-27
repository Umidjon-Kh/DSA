from typing import Any, Iterator, Optional

from ...._base import BaseBoundedStack
from ...._tools import validate_capacity
from ....arrays import StaticUniversalArray


class StaticUniversalStack(BaseBoundedStack):
    """
    A fixed-capacity stack backed by StaticUniversalArray.
    Accepts any Python type — no dtype restriction.
    Follows LIFO (Last In, First Out) principle.

    Time complexity:
        push:         O(1)
        pop:          O(1)
        peek:         O(1)
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

    __slots__ = ("_data", "_top")

    def __init__(self, *args, capacity: Optional[int] = None) -> None:
        """
        Creates a fixed-capacity universal stack with optional initial elements.

        Args:
            capacity: Maximum number of elements the stack can hold.
            *args:    Optional initial elements, pushed left to right (last = top).

        Raises:
            TypeError:     If capacity is not an int.
            ValueError:    If capacity < 1.
            OverflowError: If len(args) > capacity.

        Examples:
            s = StaticUniversalStack(5)              # empty, capacity=5
            s = StaticUniversalStack(5, 1, "hi", 3)  # top=3, capacity=5
        """
        self._top: int = 0
        cap = validate_capacity(capacity, len(args), "StaticUniversalStack")
        self._data: StaticUniversalArray = StaticUniversalArray(capacity=cap)

        for item in args:
            self.push(item)

    # -------------------------------------------------------------------------
    # Core operations

    def push(self, value: Any) -> None:
        """
        Pushes value onto the top of the stack.

        Time complexity: O(1)

        Raises:
            OverflowError: If stack is full.
        """
        if self.is_full():
            raise OverflowError(f"Stack is full (capacity={len(self._data)})")
        self._data[self._top] = value
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
        value = self._data[self._top]
        self._data[self._top] = None
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
        return self._data[self._top - 1]

    def clear(self) -> None:
        """
        Removes all elements. Does not reallocate the buffer.

        Time complexity: O(1)
        """
        self._top = 0

    def copy(self) -> "StaticUniversalStack":
        """
        Returns a shallow copy with the same capacity.

        Time complexity: O(n)
        """
        new_stack = StaticUniversalStack(capacity=len(self._data))
        for index in range(self._top):
            new_stack._data[index] = self._data[index]
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
            yield self._data[i]

    def __eq__(self, other: object) -> bool:
        """Returns True if both structures data and top is equal."""
        if not isinstance(other, StaticUniversalStack):
            return NotImplemented
        if self._top != other._top:
            return False
        # Removed other conditions
        # Cause in data: StaticUniversalArrray it checks auto
        # Its DRY (Don't repeat yourself)
        return self._data == other._data

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields elements from bottom to top without modifying the stack.

        Time complexity: O(n)
        """
        for i in range(self._top):
            yield self._data[i]

    def __contains__(self, value: Any) -> bool:
        """Returns True if value exists in the stack. O(n)"""
        for i in range(self._top):
            if self._data[i] == value:
                return True
        return False

    def __repr__(self) -> str:
        """
        Returns string representation of the stack.
        Format: StaticUniversalStack(size=3, capacity=5)[3, 'hi', 1]
                                                         top         bottom

        Time complexity: O(n)
        """
        elements = ", ".join(repr(self._data[i]) for i in range(self._top - 1, -1, -1))
        return (
            f"StaticUniversalStack(size={self._top}, capacity={len(self._data)})"
            f"[{elements}]"
        )
