from typing import Any, Iterator, Optional

from ...nodes import SingleNode


class NodeStack:
    """
    A dynamic stack backed by SingleNode.
    Follows LIFO (Last In, First Out) principle.

    head = top of the stack.
    Each push creates a new node pointing to the previous head.
    Each pop removes the head and returns its value.

    No resize overhead — each element is an independent node.
    No capacity limit.

    Time complexity:
        push:         O(1)
        pop:          O(1)
        peek:         O(1)
        clear:        O(1)
        copy:         O(n)
        is_empty:     O(1)
        __len__:      O(1)
        __bool__:     O(1)
        __iter__:     O(n) — top to bottom
        __contains__: O(n)
        __repr__:     O(n)
    """

    __slots__ = ("_head", "_size")

    def __init__(self, *args) -> None:
        """
        Creates a node-based stack with optional initial elements.

        Args:
            *args: Optional initial elements, pushed left to right (last = top).

        Examples:
            s = NodeStack()        # empty
            s = NodeStack(1, 2, 3) # top=3
        """
        self._head: Optional[SingleNode] = None
        self._size: int = 0

        for item in args:
            self.push(item)

    # -------------------------------------------------------------------------
    # Core operations

    def push(self, value: Any) -> None:
        """
        Creates a new node and places it on top of the stack.
        New node's next points to the previous head.

        Time complexity: O(1)
        """
        node = SingleNode(value)
        node.next = self._head
        self._head = node
        self._size += 1

    def pop(self) -> Any:
        """
        Removes the top node and returns its value.

        Time complexity: O(1)

        Raises:
            IndexError: If stack is empty.
        """
        if self.is_empty():
            raise IndexError("Pop from an empty stack")
        value = self._head.value  # type: ignore[union-attr]
        self._head = self._head.next  # type: ignore[union-attr]
        self._size -= 1
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

    def clear(self) -> None:
        """
        Removes all nodes by dropping the head reference.

        Time complexity: O(1)
        """
        self._head = None
        self._size = 0

    def copy(self) -> "NodeStack":
        """
        Returns a shallow copy of the stack preserving order.
        Traverses bottom to top to rebuild in correct order.

        Time complexity: O(n)
        """
        values = list(reversed(list(self)))
        new_stack = NodeStack()
        for v in values:
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
        Yields values from tail to head.
        Builds a temporary reversed SingleNode chain, then traverses it.

        Time complexity: O(n)
        """
        temp_head: Optional[SingleNode] = None
        current = self._head
        while current is not None:
            temp = SingleNode(current.value)
            temp.next = temp_head
            temp_head = temp
            current = current.next
        current = temp_head
        while current is not None:
            yield current.value
            current = current.next

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
        Format: NodeStack(size=3)[3, 2, 1]
                                  top   bottom

        Time complexity: O(n)
        """
        elements = ", ".join(repr(v) for v in self)
        return f"NodeStack(size={self._size})[{elements}]"
