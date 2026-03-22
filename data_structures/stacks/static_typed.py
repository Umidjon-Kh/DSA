from typing import Any, Generator

from ..arrays import StaticTypedArray

_DTYPE_DEFAULTS = {
    int: 0,
    float: 0.0,
    bool: False,
    str: "",
}


class StaticTypedStack:
    """
    A fixed-size stack that enforces a single type for all elements.
    Built on top of StaticTypedArray — elements stored as raw C values.
    Follows LIFO (Last In, First Out) principle.

    Supported dtypes: int, float, bool, str.

    Raises OverflowError on push when full.
    Raises IndexError on pop/peek when empty.
    Raises TypeError if not provided at least one argument or capacity value.
    Raises TypeError if pushed value is not initialized data type.


    Time complexity:
        push:     O(1)
        pop:      O(1)
        peek:     O(1)
        is_empty: O(1)
        is_full:  O(1)
        __len__:  O(1)
        __iter__: O(n) — from top to bottom
        copy:     O(n)
    """

    __slots__ = ("_top", "_data", "_capacity", "_dtype", "_str_length")

    def __init__(
        self, *args, dtype: type, capacity: Any = None, str_length: Any = None
    ) -> None:
        """
        Creates a fixed-size typed stack with given capacity.
        If capacity is None — uses len(args) as capacity.

        Args:
            *args:      Optional initial values pushed bottom to top. Must match dtype.
            dtype:      Element type. Supported: int, float, bool, str.
            capacity:   Maximum number of elements the stack can hold.
            str_length: Max string length for dtype=str (default 20).

        Raises:
            TypeError:    if capacity is not int or value does not match dtype.
            ValueError:   if capacity is less than or equal to 0.
            OverflowError: if len(args) exceeds capacity.
            TypeError: if not provided at least one argument or capacity value.
            Raises TypeError if pushed value is not initialized data type.
        """
        if capacity is not None:
            if not isinstance(capacity, int):
                raise TypeError(
                    f"Capacity value must be positive integer, got ({type(capacity).__name__})"
                )
            self._capacity = capacity
        elif args:
            self._capacity = len(args)
        else:
            raise TypeError("Expected at least one argument or capacity value.")

        self._dtype = dtype
        self._str_length = str_length
        self._data = StaticTypedArray(
            self._capacity, dtype=dtype, str_length=str_length
        )
        self._top = -1
        for item in args:
            self.push(item)

    def push(self, value: Any) -> None:
        """
        Adds value to the top of the stack.
        Value must match dtype.

        Raises:
            OverflowError: if stack is full.
            TypeError:     if value does not match dtype.
        """
        if self.is_full():
            raise OverflowError("Stack is full")
        self._top += 1
        self._data[self._top] = value

    def pop(self) -> Any:
        """
        Removes and returns value from the top of the stack.
        Resets the slot to dtype default value after removal.

        Returns:
            Value at the top.

        Raises:
            IndexError: if stack is empty.
        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        removed = self._data[self._top]
        self._data[self._top] = _DTYPE_DEFAULTS[self._dtype]
        self._top -= 1
        return removed

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
        return self._data[self._top]

    def is_empty(self) -> bool:
        """Returns True if stack has no elements."""
        return self._top == -1

    def is_full(self) -> bool:
        """Returns True if stack has reached its capacity."""
        return self._top == self._capacity - 1

    def copy(self) -> "StaticTypedStack":
        """
        Creates a shallow copy of the stack.
        Returned stack has same capacity, dtype, size and elements.

        Time complexity: O(n)
        """
        copied = StaticTypedStack(
            dtype=self._dtype, capacity=self._capacity, str_length=self._str_length
        )
        copied._data = self._data.copy()
        copied._top = self._top
        return copied

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both stacks have same dtype and
        same elements in same order.
        """
        if not isinstance(other, StaticTypedStack):
            return False
        if self._dtype != other._dtype:
            return False
        return list(self) == list(other)

    def __len__(self) -> int:
        """Returns capacity of the stack."""
        return self._capacity

    def __iter__(self) -> Generator[Any, None, None]:
        """
        Iterates over values from top to bottom.
        Does not modify the stack.
        """
        current = self._top
        while current >= 0:
            yield self._data[current]
            current -= 1

    def __repr__(self) -> str:
        """
        Returns string representation of the stack.
        Example: StaticTypedStack(dtype=int, capacity=5, top=[3, 2, 1])
        """
        items = list(self)
        return f"StaticTypedStack(dtype={self._dtype.__name__}, capacity={self._capacity}, top={items})"
