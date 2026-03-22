from typing import Any, Generator, Optional

from ..nodes import SingleNode


class DynamicNodeStack:
    """
    A dynamic stack built on top of SingleNode.
    Follows LIFO (Last In, First Out) principle.

    head = top of the stack.
    Each push creates a new node pointing to the previous head.
    Each pop removes the head and returns its value.

    Unlike array-based stacks — no contiguous memory,
    no resize overhead. Each element is an independent node.

    Raises IndexError on pop/peek when empty.

    Time complexity:
        push:     O(1)
        pop:      O(1)
        peek:     O(1)
        is_empty: O(1)
        __len__:  O(1)
        __iter__: O(n) — from top to bottom
        copy:     O(n*2)
    """

    __slots__ = ("_head", "_size")

    def __init__(self, *args) -> None:
        """
        Creates a node-based stack with optional initial values.

        Args:
            *args: Optional initial values pushed bottom to top.

        Examples:
            stack = DynamicNodeStack()        # empty
            stack = DynamicNodeStack(1, 2, 3) # top is 3
        """
        self._head: Optional[SingleNode] = None
        self._size: int = 0
        for item in args:
            self.push(item)

    def push(self, value: Any) -> None:
        """
        Creates a new node and places it on top of the stack.
        New node's next points to the previous head.

        Time complexity: O(1)
        """
        new_node = SingleNode(value)
        new_node.next = self._head
        self._head = new_node
        self._size += 1

    def pop(self) -> Any:
        """
        Removes and returns value from the top of the stack.
        Head is moved to the next node.

        Returns:
            Value at the top.

        Raises:
            IndexError: if stack is empty.
        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        value = self._head.value  # type: ignore[union-attr]
        self._head = self._head.next  # type: ignore[union-attr]
        self._size -= 1
        return value

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
        return self._head.value  # type: ignore[union-attr]

    def is_empty(self) -> bool:
        """Returns True if stack has no elements."""
        return self._head is None

    def copy(self) -> "DynamicNodeStack":
        """
        Creates a shallow copy of the stack.
        Elements firstly saves in temp stack with reversed property,
        after that pushes to main copy stack in right order.

        Time complexity: O(n*2)
        """
        temp = DynamicNodeStack()
        current = self._head
        while current is not None:
            temp.push(current.value)
            current = current.next
        copied = DynamicNodeStack()
        current = temp._head
        while current is not None:
            copied.push(current.value)
            current = current.next
        return copied

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both stacks have same elements in same order.
        """
        if not isinstance(other, DynamicNodeStack):
            return False
        return list(self) == list(other)

    def __len__(self) -> int:
        """Returns number of elements in the stack."""
        return self._size

    def __iter__(self) -> Generator[Any, None, None]:
        """
        Iterates over values from top to bottom.
        Does not modify the stack.
        """
        current = self._head
        while current is not None:
            yield current.value
            current = current.next

    def __repr__(self) -> str:
        """
        Returns string representation of the stack.
        Example: DynamicNodeStack(top=[3, 2, 1])
        """
        items = list(self)
        return f"DynamicNodeStack(top={items})"
