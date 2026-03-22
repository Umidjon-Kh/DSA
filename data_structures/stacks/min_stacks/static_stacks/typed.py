from typing import Any, Callable, Generator, Optional

from ....arrays import StaticTypedArray

_DTYPE_DEFAULTS = {
    int: 0,
    float: 0.0,
    bool: False,
    str: "",
}


class StaticTypedMinStack:
    """
    Creates two fixed-size stacks that accepts only single type for all elements.
    Build on top of StaticTypedArray.
    Follows LIFO (Last In, First Out) principle.

    Compared to StaticUniversalMinStack:
        It only stores single type elements in raw C values.
        It needs for users that need to store only one type object
        And needs a fixed and less memory usage.

    Raises OverflowError on push when full.
    Raises IndexError on pop/peek/get_min when empty.
    Raises TypeError if not provided at least one argument or capacity value.
    Raises TypeError if key function provided but not callable.
    Raises TypeError if pushed value is not initialized data type.
    Raises ValueError if str_length less than or equal to 0.
    Raises TypeError if str_length is provided but not positive integer.

    Time complexity:
        push:     O(1)
        pop:      O(1)
        peek:     O(1)
        get_min:  O(1)
        is_empty: O(1)
        is_full:  O(1)
        __len__:  O(1)
        __iter__: O(n) — from top to bottom
        copy:     O(n)
    """

    __slots__ = (
        "_top",
        "_min_top",
        "_main_data",
        "_min_data",
        "_capacity",
        "_key",
        "_dtype",
    )

    def __init__(
        self,
        *args,
        dtype: type,
        capacity: Any = None,
        str_length: Any = None,
        key: Optional[Callable] = None,
    ) -> None:
        """
        Creates two fixed-size typed stacks with given capacity.
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
            TypeError: if key function is provided but not callable.
            TypeError: if pushed value is not initialized data type.
            TypeError: if str_length is provided but not positive integer.
            ValueError: if str_length less than or equal to 0
        """
        # Validating capacity before initializing
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

        # Validating key function
        if key is not None:
            if not callable(key):
                raise TypeError(f"Key must be callable, got ({type(key).__name__})")
            self._key = key
        else:
            self._key = lambda x: x

        # Initializing data type
        self._dtype = dtype
        # Creating both data structures
        self._main_data = StaticTypedArray(
            self._capacity, dtype=dtype, str_length=str_length
        )
        self._min_data = StaticTypedArray(
            self._capacity, dtype=dtype, str_length=str_length
        )
        # Initialzing both tops of stacks
        self._top = -1
        self._min_top = -1
        # Pushing args to both datas
        for item in args:
            self.push(item)

    def push(self, value: Any) -> None:
        """
        Adds object to main stack and computes minimal
        using key function to get minimum object and adds it to
        min data. Value must match dtype.

        Raises:
            OverflowError: if stack is full.
            TypeError:     if value does not match dtype.
        """
        if self.is_full():
            raise OverflowError("Stack is full")
        self._top += 1
        self._main_data[self._top] = value
        if self._min_top == -1 or self._key(value) <= self._key(
            self._min_data[self._min_top]
        ):
            self._min_top += 1
            self._min_data[self._min_top] = value

    def is_empty(self) -> bool:
        """Returns True if stack has no elements."""
        return self._top == -1

    def is_full(self) -> bool:
        """Returns True if stack has reached its capacity."""
        return self._top == self._capacity - 1

    def pop(self) -> Any:
        """
        Removes and returns object from the top of the main data.
        If main data top object and min data top object
        computed minimal value is equal resets the slot to dtype default.

        Returns:
            Value at the top.
        Raises:
            IndexError: if stack is empty.
        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        removed = self._main_data[self._top]
        self._main_data[self._top] = _DTYPE_DEFAULTS[self._dtype]
        self._top -= 1
        if self._key(removed) == self._key(self._min_data[self._min_top]):
            self._min_data[self._min_top] = _DTYPE_DEFAULTS[self._dtype]
            self._min_top -= 1
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
        return self._main_data[self._top]

    def get_min(self) -> Any:
        """
        Returns the actual minimal object in the stack.(min_data top)

        Returns:
            Actual min object in stack.
        Raises:
            IndexError: if stack is empty.
        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._min_data[self._min_top]

    def copy(self) -> "StaticTypedMinStack":
        """
        Creates a shallow copy of the stack.
        Returned stack has same capacity, size and (main_data, min_data).

        Time complexity: O(n)
        """
        copied = StaticTypedMinStack(
            capacity=self._capacity,
            key=self._key,
            dtype=self._dtype,
        )
        copied._main_data = self._main_data.copy()
        copied._top = self._top
        copied._min_data = self._min_data.copy()
        copied._min_top = self._min_top
        return copied

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both stacks have same elements in same order.
        Capacity and key is not compared — only contents (main_data and min_data).
        """
        if not isinstance(other, StaticTypedMinStack):
            return False
        if self._dtype != other._dtype:
            return False
        return list(other._main_data) == list(self._main_data)

    def __len__(self) -> int:
        """Returns capacity of the stack."""
        return len(self._main_data)

    def __iter__(self) -> Generator[Any, None, None]:
        """
        Iterates over values from top to bottom.
        Does not modify the stack.
        """
        current = self._top
        while current >= 0:
            yield self._main_data[current]
            current -= 1

    def __repr__(self) -> str:
        """
        Returns string representation of the stack.
        Example: StaticTypedMinStack(dtype=int, capacity=5, top=[3, 2, 1], min=1)
        """
        items = list(self)
        current_min = self._min_data[self._min_top] if self._min_top != -1 else None
        return f"StaticTypedMinStack(dtype={self._dtype.__name__}, capacity={self._capacity}, top={items}, min={current_min})"
