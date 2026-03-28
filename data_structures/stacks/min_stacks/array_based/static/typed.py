from typing import Any, Callable, Iterator, Optional

from ....._base import BaseBoundedStack
from ....._tools import validate_capacity, validate_key_function, validate_value_type
from .....arrays import StaticTypedArray

_DTYPE_DEFAULTS = {
    int: 0,
    float: 0.0,
    bool: False,
    str: "",
}


class StaticTypedMinStack(BaseBoundedStack):
    """
    A fixed-capacity min stack backed by StaticTypedArray.
    Enforces a single element type for all items and
    tracks current minimum object in O(1).
    Follows LIFO (Last In, First Out) principle.

    Supported dtypes: int, float, bool, str

    A key function maps each stored value to a comparable key.
    The minimum is tracked by key, not raw value.

    _data = main array to store all pushed objects.
    _min_data = to store only current minimum objects computed by key.
    _top = top index of main data.
    _min_top = top index of min data.

    A value is pushed onto the min stack only when the min stack is empty
    or key(value) <= key(current minimum). On pop, if the poped value's
    key matches the current minimum's key, the min stack is also popped.

    Time complexity:
        push:         O(1)
        pop:          O(1)
        peek:         O(1)
        min:          O(1)
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

    __slots__ = (
        "_data",
        "_min_data",
        "_top",
        "_min_top",
        "_key",
        "_dtype",
        "_str_length",
    )

    def __init__(
        self,
        dtype: type,
        *args,
        str_length: Optional[int] = None,
        capacity: Optional[int] = None,
        key: Optional[Callable] = None,
    ) -> None:
        """
        Creates a fixed-capacity typed min stack with optional initial elements.

        Args:
            *args:      Optional initial elements, pushed left to right (last = top).
            dtype:      Element type. Supported: int, float, bool, str.
            capacity:   Maximum number of elements the stack can hold.
            str_length: Max characters per str element (default: 20).
            key:        Callable applied to each value before comparison.
                        Defaults to identity (lambda x: x) if None.

            Raises:
                TypeError:     if dtype is not supported type.
                TypeError:     if capacity is not an int.
                ValueError:    if capacity < 1.
                TypeError:     if any element in args is not dtype.
                OverflowError: if len(args) > capacity.
                TypeError:     if not provided at least one argument or capacity value.
                TypeError:     if key is provided but not callable.

            Examples:
                s = StaticTypedMinStack(int, capacity=5)          # empty, capacity=5
                s = StaticTypedMinStack(int, 1, 2, 4, capacity=5) # empty, capacity=5
                s = StaticTypedMinStack(key=lambda x: -x)         # max-as-min behaviour
                s = StaticTypedMinStack(key=lambda x: x[1])       # keyed by second element
        """
        self._key: Callable = validate_key_function(key)
        self._dtype: type = dtype
        self._top: int = 0
        self._min_top: int = 0
        cap: int = validate_capacity(capacity, len(args), "StaticTypedMinStack")
        self._data: StaticTypedArray = StaticTypedArray(
            dtype=dtype, capacity=cap, str_length=str_length
        )
        self._min_data: StaticTypedArray = StaticTypedArray(
            dtype=dtype, capacity=cap, str_length=str_length
        )

        self._str_length: int = self._data._str_length

        for item in args:
            self.push(item)

    # -------------------------------------------------------------------------
    # Core operations

    def push(self, value: Any) -> None:
        """
        Pushes values onto the top of the main data.
        Also pushes onto the min data when the min data is empty
        or key(value) <= key(current minimum).

        Time complexity: O(1)

        Raises:
            TypeError:     if value is not dtype.
            OverflowError: if stack is full
        """
        if self.is_full():
            raise OverflowError(f"Stack is full (capacity={len(self._data)})")
        validate_value_type(value, self._dtype)
        self._data._raw_set(self._top, value)
        self._top += 1

        if self._min_top == 0 or self._key(value) <= self._key(
            self._min_data._raw_get(self._min_top - 1)
        ):
            self._min_data._raw_set(self._min_top, value)
            self._min_top += 1

    def pop(self) -> Any:
        """
        Removes and returns the top of main data.
        If key(popped) == key(current minimum), the min data is also popped.

        Time complexity: O(1)

        Raises:
            IndexError: if stack is empty.
        """
        if self.is_empty():
            raise IndexError("Pop from an empty stack")
        self._top -= 1
        value = self._data._raw_get(self._top)
        self._data._raw_set(self._top, _DTYPE_DEFAULTS[self._dtype])

        # If stack is not empty, min_data never be None
        if self._key(value) == self._key(self._min_data._raw_get(self._min_top - 1)):
            self._min_top -= 1
            self._min_data._raw_set(self._min_top, _DTYPE_DEFAULTS[self._dtype])

        return value

    def peek(self) -> Any:
        """
        Returns the top element without removing it.

        Time complexity: O(1)

        Raises:
            IndexError: if stack is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from an empty stack")
        return self._data._raw_get(self._top - 1)

    def min(self) -> Any:
        """
        Returns the current minimum value (by key) without removing it.

        Time complexity: O(1)

        Raises:
            IndexError: if stack is empty
        """
        if self.is_empty():
            raise IndexError("Min from an empty stack")
        return self._min_data[self._min_top - 1]

    def clear(self) -> None:
        """
        Removes all elements. Does not reallocate the buffer.

        Time complexity: O(n)
        """
        self._top = 0
        self._min_top = 0
        self._data.clear()
        self._min_data.clear()

    def copy(self) -> "StaticTypedMinStack":
        """
        Returns a shallow copy with same dtype and capacity.

        Time complexity: O(n)
        """
        new_stack = StaticTypedMinStack(
            dtype=self._dtype,
            capacity=len(self._data),
            str_length=self._str_length,
            key=self._key,
        )
        for i in range(self._top):
            new_stack._data._raw_set(i, self._data._raw_get(i))
            new_stack._min_data._raw_set(i, self._min_data._raw_get(i))
        new_stack._top = self._top
        new_stack._min_top = self._min_top
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
        if not isinstance(other, StaticTypedMinStack):
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
        Format: StaticTypedMinStack(size=3, min=1)[3, 2, 1]
                                            top   bottom

        Time complexity: O(n)
        """
        min_repr = (
            repr(self._min_data[self._min_top - 1]) if self._min_top != 0 else "None"
        )
        elements = ", ".join(repr(v) for v in self)
        return f"StaticTypedMinStack({self._dtype.__name__}, capacity={len(self._data)}, min={min_repr})[{elements}]"
