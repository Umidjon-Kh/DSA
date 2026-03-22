from typing import Any, Callable, Generator, Optional

from ..arrays import DynamicUniversalArray


class DynamicUniversalMinStack:
    """
    Creates two dynamic stacks that grows automatically when capacity is exceeded.
    Build on top of the DynamicUniversalArray - accepts any Python object.
    Follows LIFO (Last In, First Out) principle.

    Unlike StaticUniversalMinStack - never raises OverflowError.
    Growth is handled automatically by DynamicUniversalArray.

    Raises IndexError on pop/peek/get_min when empty.
    Raises TypeError if key function provided but not callable.

    Time complexity:
        push:     O(1) amortized, O(n) no resize
        pop:      O(1)
        peek:     O(1)
        get_min:  O(1)
        is_empty: O(1)
        __len__:  O(1)
        __iter__: O(n) — from top to bottom
        copy:     O(n)
    """

    __slots__ = (
        "_main_data",
        "_min_data",
        "_key",
    )

    def __init__(self, *args, key: Optional[Callable] = None) -> None:
        """
        Creates two dynamic stacks with optional values.

        Args:
            *args: Optional initial values pushed bottom to top.
            key: Function that computes minimal of two objects.

        Raises:
            TypeError: if key is provided but not callable.
        """
        # Validating ky function before initializing
        if key is not None:
            if not callable(key):
                raise TypeError(f"Key must be callable, got ({type(key).__name__})")
            self._key = key
        else:
            self._key = lambda x: x
        # Creating both data structures
        self._main_data = DynamicUniversalArray()
        self._min_data = DynamicUniversalArray()
        # Pushing args to both datas
        for item in args:
            self.push(item)

    def push(self, value: Any) -> None:
        """
        Adds object to main stack and computes minimal
        using key function to get minimum object and adds it to
        min data.
        """
        self._main_data.append(value)
        if len(self._min_data) == 0 or self._key(value) <= self._key(
            self._min_data[-1]
        ):
            self._min_data.append(value)

    def is_empty(self) -> bool:
        """Returns True if stack has no elements."""
        return len(self._main_data) == 0

    def pop(self) -> Any:
        """
        Removes and returns object from the top of the main data.
        If main data top object and min data top object
        computed minimal value is equal clears top of slot of min data too.

        Returns:
            Value at the top.

        Raises:
            IndexError: if stack is empty.
        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        removed = self._main_data.remove(-1)
        if self._key(removed) == self._key(self._min_data[-1]):
            self._min_data.remove(-1)
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
        return self._main_data[-1]

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
        return self._min_data[-1]

    def copy(self) -> "DynamicUniversalMinStack":
        """
        Creates a shalloew copy of the stack.
        Returned stack has same attrs and data structures.
        """
        copied = DynamicUniversalMinStack(key=self._key)
        copied._main_data = self._main_data.copy()
        copied._min_data = self._min_data.copy()
        return copied

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both stacks have same elements in same order.
        """
        if not isinstance(other, DynamicUniversalMinStack):
            return False
        return list(other._main_data) == list(self._main_data)

    def __len__(self) -> int:
        """Returns number of elements in the stack."""
        return len(self._main_data)

    def __iter__(self) -> Generator[Any, None, None]:
        """
        Iterates over values from top to bottom.
        Does not modify the stack.
        """
        current = len(self._main_data) - 1
        while current >= 0:
            yield self._main_data[current]
            current -= 1

    def __repr__(self) -> str:
        """
        Returns string representation of the stack.
        Example: DynamicUniversalMinStack(top=[3, 2, 1], min=1)
        """
        items = list(self)
        current_min = self._min_data[-1] if len(self._min_data) > 0 else None
        return f"DynamicUniversalMinStack(top={items}, min={current_min})"
