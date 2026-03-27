from typing import Any, Callable, Iterator, Optional

from ...._base import BaseStack
from ....nodes import LinearNode


class NodeMinStack(BaseStack):
    """
    A node-based stack with O(1) minimum tracking.
    Backed by two independent LinearNode chains: main and min.
    Follows LIFO (Last In, First Out) principle.

    A key function maps each stored value to a comparable key.
    The minimum is tracked by key, not raw value.

    _head = top of the main stack.
    _min_head = top of the min stack (current minimum by key).

    A value is pushed onto the min stack only when the min stack is empty
    or key(value) <= key(current minimum). On pop, if the popped value's
    key matches the current minimum's key, the min stack is also popped.

    Time complexity:
        push:         O(1)
        pop:          O(1)
        peek:         O(1)
        min:      O(1)
        clear:        O(1)
        copy:         O(n)
        is_empty:     O(1)
        __len__:      O(1)
        __bool__:     O(1)
        __iter__:     O(n) — top to bottom
        __reversed__: O(n)
        __contains__: O(n)
        __repr__:     O(n)
        __eq__:       O(n)
    """

    __slots__ = ("_head", "_min_head", "_size", "_min_size", "_key")

    def __init__(self, *args, key: Optional[Callable[[Any], Any]] = None) -> None:
        """
        Creates a node-based min stack with optional initial elements.

        Args:
            *args: Optional initial elements, pushed left to right (last = top).
            key:   Callable applied to each value before comparison.
                   Defaults to identity (lambda x: x) if None.

        Examples:
            s = NodeMinStack()                     # empty, key=identity
            s = NodeMinStack(3, 1, 2)              # top=2, min=1
            s = NodeMinStack(key=lambda x: -x)    # max-as-min behaviour
            s = NodeMinStack(key=lambda x: x[1])  # keyed by second element
        """
        self._head: Optional[LinearNode] = None
        self._min_head: Optional[LinearNode] = None
        self._size: int = 0
        self._min_size: int = 0
        self._key: Callable[[Any], Any] = key if key is not None else lambda x: x

        for item in args:
            self.push(item)

    # -------------------------------------------------------------------------
    # Core operations

    def push(self, value: Any) -> None:
        """
        Pushes value onto the top of the main stack.
        Also pushes onto the min stack when the min stack is empty
        or key(value) <= key(current minimum).

        Time complexity: O(1)
        """
        node = LinearNode(value)
        node.next = self._head
        self._head = node
        self._size += 1

        if self._min_head is None or self._key(value) <= self._key(
            self._min_head.value
        ):
            min_node = LinearNode(value)
            min_node.next = self._min_head
            self._min_head = min_node
            self._min_size += 1

    def pop(self) -> Any:
        """
        Removes and returns the top element of the main stack.
        If key(popped) == key(current minimum), the min stack is also popped.

        Time complexity: O(1)

        Raises:
            IndexError: If stack is empty.
        """
        if self.is_empty():
            raise IndexError("Pop from an empty stack")

        value = self._head.value  # type: ignore[union-attr]
        self._head = self._head.next  # type: ignore[union-attr]
        self._size -= 1

        if self._min_head is not None and self._key(value) == self._key(
            self._min_head.value
        ):
            self._min_head = self._min_head.next
            self._min_size -= 1

        return value

    def peek(self) -> Any:
        """
        Returns the top element's value without removing it.

        Time complexity: O(1)

        Raises:
            IndexError: If stack is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from an empty stack")
        return self._head.value  # type: ignore[union-attr]

    def min(self) -> Any:
        """
        Returns the current minimum value (by key) without removing it.

        Time complexity: O(1)

        Raises:
            IndexError: If stack is empty.
        """
        if self._min_head is None:
            raise IndexError("get_min from an empty stack")
        return self._min_head.value

    def clear(self) -> None:
        """
        Drops all nodes from both main and min stacks.

        Time complexity: O(1)
        """
        self._head = None
        self._min_head = None
        self._size = 0
        self._min_size = 0

    def copy(self) -> "NodeMinStack":
        """
        Returns a shallow copy preserving order and key function.
        Traverses bottom to top to rebuild in correct order.

        Time complexity: O(n)
        """
        new_stack = NodeMinStack(key=self._key)
        for v in reversed(self):
            new_stack.push(v)
        return new_stack

    # -------------------------------------------------------------------------
    # State checks

    def is_empty(self) -> bool:
        """Returns True if the stack contains no elements. O(1)"""
        return self._head is None

    # -------------------------------------------------------------------------
    # Dunder methods

    def __len__(self) -> int:
        """Returns number of elements currently in the stack. O(1)"""
        return self._size

    def __bool__(self) -> bool:
        """Returns True if the stack is not empty. O(1)"""
        return self._head is not None

    def __iter__(self) -> Iterator[Any]:
        """
        Yields elements from top to bottom without modifying the stack.

        Time complexity: O(n)
        """
        current = self._head
        while current is not None:
            yield current.value
            current = current.next

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields values from bottom to top.
        Builds a temporary reversed LinearNode chain, then traverses it.

        Time complexity: O(n)
        """
        temp_head: Optional[LinearNode] = None
        current = self._head
        while current is not None:
            temp = LinearNode(current.value)
            temp.next = temp_head
            temp_head = temp
            current = current.next
        current = temp_head
        while current is not None:
            yield current.value
            current = current.next

    def __eq__(self, other: object) -> bool:
        """Returns True if both stacks have equal elements in the same order."""
        if not isinstance(other, NodeMinStack):
            return NotImplemented
        if self._size != other._size:
            return False
        cur_a = self._head
        cur_b = other._head
        for _ in range(self._size):
            if cur_a.value != cur_b.value:  # type: ignore[union-attr]
                return False
            cur_a = cur_a.next  # type: ignore[union-attr]
            cur_b = cur_b.next  # type: ignore[union-attr]
        return True

    def __contains__(self, value: Any) -> bool:
        """Returns True if value exists in the stack. O(n)"""
        current = self._head
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False

    def __repr__(self) -> str:
        """
        Returns string representation of the stack.
        Format: NodeMinStack(size=3, min=1)[3, 2, 1]
                                            top   bottom

        Time complexity: O(n)
        """
        min_repr = repr(self._min_head.value) if self._min_head is not None else "None"
        elements = ", ".join(repr(v) for v in self)
        return f"NodeMinStack(size={self._size}, min={min_repr})[{elements}]"
