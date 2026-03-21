from typing import Any, Generator

from ..arrays import StaticUniversalArray


class StaticUniversalStack:
    """
    A fixed-size stack that accepts any Python object.
    Built on top of StaticUniversalArray.
    Follows LIFO (Last In, First Out) principle.

    Raises OverflowError on push when full.
    Raises IndexError on pop/peek when empty.

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

    __slots__ = ("_top", "_data", "_capacity")

    def __init__(self, *args, capacity: Any = None) -> None:
        """
        Creates a fixed-size stack with given capacity.

        Args:
            capacity: Maximum number of elements the stack can hold.

        Raises:
            TypeError:  if capacity is not int.
            ValueError: if capacity is less than or equal to 0.
        """
        if capacity is None:
            self._capacity = len(args)
        else:
            self._capacity = capacity
        self._data = StaticUniversalArray(self._capacity)
        self._top = -1
        # Received objects as *args pushing all them to data
        for item in args:
            self.push(item)

    def push(self, value: Any) -> None:
        """
        Adds value to the top of the stack.

        Raises:
            OverflowError: if stack is full.
        """
        if self.is_full():
            raise OverflowError("Stack is full")
        self._top += 1
        self._data[self._top] = value

    def pop(self) -> Any:
        """
        Removes and returns value from the top of the stack.
        Clears the slot after removal.

        Returns:
            Value at the top.

        Raises:
            IndexError: if stack is empty.
        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        removed = self._data[self._top]
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

    def copy(self) -> "StaticUniversalStack":
        """
        Creates a shallow copy of the stack.
        Returned stack has same capacity, size and elements.

        Time complexity: O(n)
        """
        copied = StaticUniversalStack(capacity=self._capacity)
        counter = 0
        while counter <= self._top:
            copied._data[counter] = self._data[counter]
            counter += 1
        copied._top = self._top
        return copied

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both stacks have same capacity,
        same size and same elements in same order.
        """
        if not isinstance(other, StaticUniversalStack):
            return False
        return list(self) == list(other)

    def __len__(self) -> int:
        """Returns number of elements currently in the stack (not capacity)."""
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
        Example: StaticUniversalStack(capacity=5, top=[3, 2, 1])
        """
        items = [*self]
        return f"StaticUniversalStack(capacity={self._capacity}, top=[{items}])"
