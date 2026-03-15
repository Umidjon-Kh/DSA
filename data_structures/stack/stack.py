from dataclasses import dataclass, field
from typing import Optional, Any, Generator
from .node import Node


@dataclass
class Stack:
    _top: Optional[Node] = field(default=None, repr=False)
    _size: int = field(init=False, default=0)

    def is_empty(self) -> bool:
        return self._top is None

    def push(self, value: Any) -> None:
        """Adds new node with any type of value"""
        new_node = Node(value)
        new_node.next = self._top
        self._top = new_node
        self._size += 1

    def pop(self) -> Any:
        """Removes last element in Stack and returns it"""
        if self._top is not None:
            removed = self._top
            self._top = self._top.next

            self._size -= 1
            return removed.value

        raise IndexError('Stack is empty')

    def peek(self) -> Any:
        """Shows last in element in stack"""
        if self._top is not None:
            return self._top.value

        raise IndexError('Stack is empty')

    def copy(self) -> 'Stack':
        """Returns a copy of Stack that not connected to this Stack"""
        temp = Stack()
        copied_stack = Stack()

        current = self._top

        # Copying all values from stack nodes
        # But reversed cause our node dont know about previous node
        while current:
            temp.push(current.value)
            current = current.next

        # Pushing all temp stack nodes to copied stack
        # Properly to equal self stack nodes
        while temp._top is not None:
            value = temp.pop()
            copied_stack.push(value)

        return copied_stack

    def __len__(self) -> int:
        """Returns size of Stack"""
        return self._size

    def __iter__(self) -> Generator[Any, None, None]:
        """For iterating Stack nodes"""
        current = self._top
        while current:
            yield current.value
            current = current.next

    def __reversed__(self) -> Generator[Any, None, None]:
        """For itering Stack in reversed"""
        temp = Stack()

        current = self._top

        while current:
            temp.push(current.value)
            current = current.next

        while temp._top is not None:
            yield temp.pop()

    def __contains__(self, item) -> bool:
        """Checks Stack for contains item or not"""
        current = self._top
        while current:
            if current.value == item:
                return True
            current = current.next
        return False

    def __bool__(self) -> bool:
        """Returns true if Stack is not None"""
        return not self.is_empty()

    def __str__(self) -> str:
        """
        String method shows all Stack values in user frinedly output
        """
        values = []
        current = self._top

        while current:
            values.append(current.value)
            current = current.next

        return 'Stack(top -> ' + ' -> '.join(map(str, values)) + ')'
