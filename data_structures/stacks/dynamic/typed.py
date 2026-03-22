from typing import Any, Generator

from ...arrays import DynamicTypedArray


class DynamicTypedStack:
    """
    A dynamic stack that grows automatically when capacity is exceeded.
    Built on top of DynamicTypedArray — enforces a single type for all elements.
    Follows LIFO (Last In, First Out) principle.

    Unlike StaticTypedStack — never raises OverflowError.
    Growth is handled automatically by DynamicTypedArray.

    Supported dtypes: int, float, bool, str.

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

    __slots__ = ("_data", "_dtype")

    def __init__(self, *args, dtype: type, str_length: Any = None) -> None:
        """
        Creates a dynamic typed stack with optional initial values.

        Args:
            *args:      Optional initial values pushed bottom to top. Must match dtype.
            dtype:      Element type. Supported: int, float, bool, str.
            str_length: Max string length for dtype=str (default 20).

        Examples:
            stack = DynamicTypedStack(dtype=int)           # empty int stack
            stack = DynamicTypedStack(1, 2, 3, dtype=int)  # top is 3
        """
        self._dtype = dtype
        self._data = DynamicTypedArray(dtype, *args, str_length=str_length)

    def push(self, value: Any) -> None:
        """
        Adds value to the top of the stack.
        Value must match dtype.
        Grows automatically if needed.

        Time complexity: O(1) amortized, O(n) on resize.

        Raises:
            TypeError: if value does not match dtype.
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

    def copy(self) -> "DynamicTypedStack":
        """
        Creates a shallow copy of the stack.
        Returned stack has same dtype, str_length and elements.

        Time complexity: O(n)
        """
        copied = DynamicTypedStack(dtype=self._dtype)
        copied._data = self._data.copy()
        return copied

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both stacks have same dtype and
        same elements in same order.
        """
        if not isinstance(other, DynamicTypedStack):
            return False
        if self._dtype != other._dtype:
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
        Example: DynamicTypedStack(dtype=int, top=[3, 2, 1])
        """
        items = list(self)
        return f"DynamicTypedStack(dtype={self._dtype.__name__}, top={items})"
