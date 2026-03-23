from typing import Any, Iterator

from ...arrays import DynamicTypedArray


class DynamicTypedStack:
    """
    A dynamic stack backed by DynamicTypedArray.
    Grows automatically when capacity is exceeded.
    Enforces a single element type for all items.
    Follows LIFO (Last In, First Out) principle.

    Supported dtypes: int, float, bool, str

    Growth formula (delegated to DynamicTypedArray — same as CPython list):
        new_capacity = capacity + (capacity >> 3) + (3 if capacity < 9 else 6)

    Time complexity:
        push:         O(1) amortized — O(n) on resize
        pop:          O(1)
        peek:         O(1)
        clear:        O(1)
        copy:         O(n)
        is_empty:     O(1)
        __len__:      O(1)
        __bool__:     O(1)
        __iter__:     O(n) — top to bottom
        __reversed__: O(n)
        __contains__: O(n)
        __repr__:     O(n)
    """

    __slots__ = ("_data", "_dtype", "_str_length")

    def __init__(self, dtype: type, *args, str_length: int = 1) -> None:
        """
        Creates a dynamic typed stack with optional initial elements.

        Args:
            dtype:      Element type. Supported: int, float, bool, str.
            *args:      Optional initial elements, pushed left to right (last = top).
            str_length: Max characters per str element (default: 1).

        Raises:
            TypeError: If dtype is not a supported type.
            TypeError: If any element in args is not dtype.

        Examples:
            s = DynamicTypedStack(int)           # empty
            s = DynamicTypedStack(int, 1, 2, 3)  # top=3
        """
        self._dtype: type = dtype
        self._str_length: int = str_length
        self._data: DynamicTypedArray = DynamicTypedArray(dtype, str_length=str_length)

        for item in args:
            self.push(item)

    # -------------------------------------------------------------------------
    # Core operations

    def push(self, value: Any) -> None:
        """
        Pushes value onto the top of the stack.
        Triggers resize if underlying array is at capacity.

        Time complexity: O(1) amortized — O(n) on resize

        Raises:
            TypeError: If value is not dtype.
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

        Time complexity: O(1)
        """
        self._data._size = 0

    def copy(self) -> "DynamicTypedStack":
        """
        Returns a shallow copy with the same dtype and elements.

        Time complexity: O(n)
        """
        new_stack = DynamicTypedStack(self._dtype, str_length=self._str_length)
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

    def __contains__(self, value: Any) -> bool:
        """
        Returns True if value exists in the stack. O(n)
        Returns False instantly for wrong type.
        """
        return value in self._data

    def __repr__(self) -> str:
        """
        Returns string representation of the stack.
        Format: DynamicTypedStack(int, size=3)[3, 2, 1]
                                              top    bottom

        Time complexity: O(n)
        """
        size = len(self._data)
        elements = ", ".join(repr(self._data[i]) for i in range(size - 1, -1, -1))
        return f"DynamicTypedStack({self._dtype.__name__}, size={size})[{elements}]"
