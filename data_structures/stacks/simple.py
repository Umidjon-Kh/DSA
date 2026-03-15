from dataclasses import dataclass, field
from typing import Optional, Any, Generator
from ..nodes import SingleNode


@dataclass
class SimpleStack:
    """
    Stack data structure — LIFO (Last In, First Out).
    Built on top of SingleNode (Singly Linked List).

    Why SLL instead of list:
        - push/pop are always O(1), no memory reallocation
        - physically impossible to access elements by index — stack is protected by structure

    Visual representation:
        push(1), push(2), push(3)
        top → [3] → [2] → [1] → None

    Time complexity:
        push:  O(1)
        pop:   O(1)
        peek:  O(1)
        search (__contains__): O(n)
    """

    _top: Optional[SingleNode] = field(default=None, repr=False)
    _size: int = field(init=False, default=0)

    def is_empty(self) -> bool:
        """Returns True if stack has no elements."""
        return self._top is None

    def push(self, value: Any) -> None:
        """
        Creates a new node and places it on top of the stack.
        New node points to the previous top.
        """
        new_node = SingleNode(value)
        new_node.next = self._top
        self._top = new_node
        self._size += 1

    def pop(self) -> Any:
        """
        Removes and returns the top element.
        Raises IndexError if stack is empty.
        """
        if self._top is not None:
            removed = self._top
            self._top = self._top.next
            self._size -= 1
            return removed.value
        raise IndexError('Stack is empty')

    def peek(self) -> Any:
        """
        Returns the top element without removing it.
        Raises IndexError if stack is empty.
        """
        if self._top is not None:
            return self._top.value
        raise IndexError('Stack is empty')

    def size(self) -> int:
        """Returns the number of elements in the stack."""
        return self._size

    def copy(self) -> 'SimpleStack':
        """
        Returns a deep copy of the stack with no shared references.
        Uses a temporary stack to reverse the order back to original.
        """
        temp = SimpleStack()
        copied = SimpleStack()

        current = self._top
        while current:
            temp.push(current.value)
            current = current.next

        while temp._top is not None:
            copied.push(temp.pop())

        return copied

    def __len__(self) -> int:
        """Returns the number of elements in the stack."""
        return self._size

    def __bool__(self) -> bool:
        """Returns True if stack has at least one element."""
        return not self.is_empty()

    def __iter__(self) -> Generator[Any, None, None]:
        """Iterates from top to bottom."""
        current = self._top
        while current:
            yield current.value
            current = current.next

    def __reversed__(self) -> Generator[Any, None, None]:
        """
        Iterates from bottom to top.
        Uses a temporary stack to reverse the traversal order.
        """
        temp = SimpleStack()
        current = self._top
        while current:
            temp.push(current.value)
            current = current.next
        while temp._top is not None:
            yield temp.pop()

    def __contains__(self, item: Any) -> bool:
        """Returns True if item exists in the stack. O(n)."""
        current = self._top
        while current:
            if current.value == item:
                return True
            current = current.next
        return False

    def __str__(self) -> str:
        """Human-friendly string showing stack from top to bottom."""
        values = []
        current = self._top
        while current:
            values.append(str(current.value))
            current = current.next
        return 'Stack(top -> ' + ' -> '.join(values) + ')'
