from typing import Any, Generator

from ...arrays import DynamicUniversalArray


class DynamicUniversalStack:
    """
    A dynamic stack that grows automatically when capacity is exceeded.
    Built on top of DynamicUniversalArray — accepts any Python object.
    Follows LIFO (Last In, First Out) principle.

    Unlike StaticUniversalStack — never raises OverflowError.
    Growth is handled automatically by DynamicUniversalArray.

    Raises IndexError on pop/peek when empty.

    Time complexity:
        push:     O(1) amortized — O(n) on resize
        pop:      O(1)
        peek:     O(1)
        is_empty: O(1)
        __len__:  O(1)
        __iter__: O(n) — from top to bottom
        copy:     O(n)
    """

    __slots__ = ("_data",)

    def __init__(self, *args) -> None:
        """
        Creates a dynamic stack with optional initial values.

        Args:
            *args: Optional initial values pushed bottom to top.

        Examples:
            stack = DynamicUniversalStack()        # empty
            stack = DynamicUniversalStack(1, 2, 3) # top is 3
        """
        self._data = DynamicUniversalArray(*args)

    def push(self, value: Any) -> None:
        """
        Adds value to the top of the stack.
        Grows automatically if needed.

        Time complexity: O(1) amortized, O(n) on resize.
        """
        self._data.append(value)

    def pop(self) -> Any:
        """
        Removes and returns value from the top of the stack.

        Returns:
            Value at the top.

        Raises:
            IndexError: if stack is empty.
        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._data.remove(-1)

    def peek(self) -> Any:
        """
        Returns value at the top without removing it.

        Returns:
            Value at the top.

        Raises:
            IndexError: if stack is empty.
        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._data[-1]

    def is_empty(self) -> bool:
        """Returns True if stack has no elements."""
        return len(self._data) == 0

    def copy(self) -> "DynamicUniversalStack":
        """
        Creates a shallow copy of the stack.
        Returned stack has same elements in same order.

        Time complexity: O(n)
        """
        copied = DynamicUniversalStack()
        copied._data = self._data.copy()
        return copied

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both stacks have same elements in same order.
        """
        if not isinstance(other, DynamicUniversalStack):
            return False
        return list(self) == list(other)

    def __len__(self) -> int:
        """Returns number of elements in the stack."""
        return len(self._data)

    def __iter__(self) -> Generator[Any, None, None]:
        """
        Iterates over values from top to bottom.
        Does not modify the stack.
        """
        current = len(self._data) - 1
        while current >= 0:
            yield self._data[current]
            current -= 1

    def __repr__(self) -> str:
        """
        Returns string representation of the stack.
        Example: DynamicUniversalStack(top=[3, 2, 1])
        """
        items = list(self)
        return f"DynamicUniversalStack(top={items})"
