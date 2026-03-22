from typing import Any, Callable, Generator, Optional

from ..nodes import SingleNode


class DynamicNodeMinStack:
    """
    Creates two dynamic stacks that grows automatically when capacity is exceeded.
    Build on top of the SingleNode (like SinglyLinkedList).
    Follows LIFO (Last In, First Out) principle.

    Compared to other MinStacks:
        1) main_head and min_head instead of big data structures it only have
           pointer to head node that next attr points to next node in the chain.
        2) Each push creates a new node pointing to the previous head.
        3) Each pop removes the head and returns its value.
        4) Unlike array-based stacks — no contiguous memory,
        5) no resize overhead. Each element is an independent node.

    Raises IndexError on pop/peek/get_min when empty.
    Raises TypeError if key is provided but not callable.

    Time complexity:
        push:     O(1)
        pop:      O(1)
        peek:     O(1)
        get_min:  O(1)
        is_empty: O(1)
        __len__:  O(1)
        __iter__: O(n) — from top to bottom
        copy:     O(n*2)
    """

    __slots__ = (
        "_main_head",
        "_min_head",
        "_size",
        "_key",
    )

    def __init__(self, *args, key: Optional[Callable] = None) -> None:
        """
        Creates two node-based stacks with optional initial values.

        Args:
            *args: Optional initial values pushed bottom to top(head -> next).
            key: Function that computes minimal of two objects.

        Raises:
            TypeError: if key is provided but not callable.
        """
        # Validating received key function before initializing
        if key is not None:
            if not callable(key):
                raise TypeError(f"Key must be callable, got ({type(key).__name__})")
            self._key = key
        else:
            self._key = lambda x: x
        self._main_head: Optional[SingleNode] = None
        self._min_head: Optional[SingleNode] = None
        self._size = 0
        # Pushing args to both chains(nodes)
        for item in args:
            self.push(item)

    def push(self, value: Any) -> None:
        """
        Creates a new node and places it on top of the stack.
        New node's next point to the previous head.
        If received object computed value is less than computed min head,
        Point that object next attr to previous min_head.
        """
        new_node = SingleNode(value)
        new_node.next = self._main_head
        self._main_head = new_node
        if self._min_head is None or self._key(value) <= self._key(
            self._min_head.value
        ):
            new_node = SingleNode(value)
            new_node.next = self._min_head
            self._min_head = new_node
        self._size += 1

    def is_empty(self) -> bool:
        """Returns True if stack size equal to 0"""
        return self._size == 0

    def pop(self) -> Any:
        """
        Removes and returns node value from the main_head and
        Sets main_head's next node to main_head(new_head).
        Moves min_head to next node if min_head computed value is
        equal to main_head computed value.

        Returns:
            Value at the top.
        Raises:
            IndexError: if stack is empty.
        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        removed = self._main_head.value  # type: ignore[union-attr]
        self._main_head = self._main_head.next  # type: ignore[union-attr]
        self._size -= 1
        if self._key(removed) == self._key(self._min_head.value):  # type: ignore[union-attr]
            self._min_head = self._min_head.next  # type: ignore[union-attr]
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
        return self._main_head.value  # type: ignore[union-attr]

    def copy(self) -> "DynamicNodeMinStack":
        """
        Creates a shallow copy of the stack.
        Elements firstly saves in temp stack with reversed property,
        after that pushes to main copy stack in right order.

        Time complexity: O(n*2)
        """
        # Creating reversed nodes chain
        temp_node = None
        current = self._main_head
        while current is not None:
            new_node = SingleNode(current.value)
            new_node.next = temp_node
            temp_node = new_node
            current = current.next

        # Pushing all them in right order to copied
        copied = DynamicNodeMinStack(key=self._key)
        current = temp_node
        while current is not None:
            copied.push(current.value)
            current = current.next
        return copied

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
        return self._min_head.value  # type: ignore[union-attr]

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both stacks have same elements in same order.
        """
        if not isinstance(other, DynamicNodeMinStack):
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
        current = self._main_head
        while current is not None:
            yield current.value
            current = current.next

    def __repr__(self) -> str:
        """
        Returns string representation of the stack.
        Example: DynamicNodeMinStack(top=[3, 2, 1], min=1)
        """
        items = list(self)
        current_min = self._min_head.value if self._min_head is not None else None
        return f"DynamicNodeMinStack(top={items}, min={current_min})"
