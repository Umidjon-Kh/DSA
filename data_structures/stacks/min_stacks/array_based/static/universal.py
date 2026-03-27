from typing import Any, Callable, Iterator, Optional

from ....._base import BaseBoundedStack
from ....._tools import validate_capacity
from .....arrays import StaticUniversalArray


class StaticUniversalMinStack(BaseBoundedStack):
    """
    A fixed-capacity min stack backed by StaticUniversalArray.
    Accepts any Python type - no dtype restriction and
    tracks current minimum object in O(1).
    Follows LIFO (Last In, First Out) principle.

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
    )

    def __init__(
        self,
        *args,
        capacity: Optional[int] = None,
        key: Optional[Callable] = None,
    ) -> None:
        """
        Creates a fixed-capacity universal min stack with optional initial elements.

        Args:
            *args: Optional initial elements, pushed left to right (last = top).
            capacity: Maximum number of elements the stack can hold.
            key:   Callable applied to each value before comparison.
                   Defaults to identity (lambda x: x) if None.
        Raises:
            TypeError:     if key function is provided but not callable.
            TypeError:     if capacity is not an int.
            ValueError:    if capacity < 1.
            OverflowError: if len(args) > capacity.
            TypeError:     if not provided at least one argument or capacity value.

        Examples:
            s = StaticUniversalMinStack(capacity=5)             # empty, capacity=5
            s = StaticUniversalMinStack(1, "hi", 3, capacity=5) # top=3, capacity=5
            s = StaticUniversalMinStack(key=lambda x: -x)       # max-as-min behaviour
            s = StaticUniversalMinStack(key=lambda x: x[1])     # keyed by second element
        """
        # Validating key args before initializing
        if key is not None:
            if not callable(key):
                raise TypeError(f"Key must be callable, got ({type(key).__name__})")
            self._key: Callable = key
        else:
            self._key: Callable = lambda x: x

        cap = validate_capacity(capacity, len(args), "StaticUniversalMinStack")
        self._data: StaticUniversalArray = StaticUniversalArray(capacity=cap)
        self._min_data: StaticUniversalArray = StaticUniversalArray(capacity=cap)
        self._top: int = 0
        self._min_top: int = 0

        for item in args:
            self.push(item)

    # -------------------------------------------------------------------------
    # Core operations

    def push(self, value: Any) -> None:
        """
        Pushes value onto the top of the main data.
        Also pushes onto the min data when the min data is empty
        or key(value) <= key(current minimum).

        Time complexity: O(1)

        Raises:
            OverflowError: if stack is full.
        """
        if self.is_full():
            raise OverflowError(f"Stack is full (capacity={len(self._data)})")
        self._data[self._top] = value
        self._top += 1

        if self._min_top == 0 or self._key(value) <= self._key(
            self._min_data[self._min_top - 1]
        ):
            self._min_data[self._min_top] = value
            self._min_top += 1

    def pop(self) -> Any:
        """
        Removes and returns the top element of main data.
        If key(popped) == key(current minimum), the min data is also popped.

        Time complexity: O(1)

        Raises:
            IndexError: if stack is empty.
        """
        if self.is_empty():
            raise IndexError("Pop from an empty stack")

        self._top -= 1
        value = self._data[self._top]
        self._data[self._top] = None

        # if stack is not empty, min_data never be None
        if self._key(value) == self._key(self._min_data[self._min_top - 1]):
            self._min_top -= 1
            self._min_data[self._min_top] = None

        return value

    def peek(self) -> Any:
        """
        Returns the top of element's value without removing it.

        Time complexity: O(1)

        Raises:
            IndexError: if stack is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from an empty stack")
        return self._data[self._top - 1]

    def min(self) -> Any:
        """
        Returns the current minimum value (by key) without removing it.

        Time complexity: O(1)

        Raises:
            IndexError: if stack is empty.
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

    def copy(self) -> "StaticUniversalMinStack":
        """
        Returns a shallow copy with the same capacity.

        Time complexity: O(n)
        """
        new_stack = StaticUniversalMinStack(capacity=len(self._data), key=self._key)
        for index in range(self._top):
            new_stack._data[index] = self._data[index]
            new_stack._min_data[index] = self._min_data[index]
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
            yield self._data[i]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StaticUniversalMinStack):
            return NotImplemented
        if self._top != other._top:
            return False
        # Checking to top cause if i use StaticArray eq method
        # It check for capacity equality too.
        for i in range(self._top):
            if self._data[i] != other._data[i]:
                return False
        return True

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
        Format: StaticUniversalMinStack(size=3, min=1)[3, 2, 1]
                                            top   bottom

        Time complexity: O(n)
        """
        min_repr = repr(self._min_data[self._min_top]) if self._min_top != 0 else "None"
        elements = ", ".join(self._data[i] for i in range(self._top - 1, -1, -1))
        return f"StaticUniversalMinStack(capacity={len(self._data)}, min={min_repr})[{elements}]"
