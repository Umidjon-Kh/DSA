from dataclasses import dataclass, field
from typing import Any, Generator, Optional
from ..nodes import DoubleNode


@dataclass
class Deque:
    """
    A Deque (Double-ended Queue) is a data structure accessible from both ends.
    Built on a DLL (Doubly Linked List), each node knows next and prev.

    It is a generalization of Stack and Queue:
    - add_back + remove_back -> Stack (LIFO)
    - add_back + remove_front -> Queue (FIFO)
    - add_front + remove_back -> Stack (LIFO)
    - add_fron + remove_front -> Queue (FIFO)
    - all four operations → pure Deque

    All operations are O(1) thanks to the prev pointer in DoubleNode.
    """

    _head: Optional[DoubleNode] = field(default=None, repr=False, init=False)
    _tail: Optional[DoubleNode] = field(default=None, repr=False, init=False)
    _size: int = field(init=False, default=0)

    def is_empty(self) -> bool:
        """Returns True if queue has no elements"""
        return self._size == 0

    def add_front(self, value: Any) -> None:
        """
        Adds a new node to the front(head) of the queue.
        If queue is empty, both head and tail point to the new node
        """
        new_node = DoubleNode(value)
        if self._head is None:
            self._head = self._tail = new_node
        else:
            new_node.next = self._head
            self._head.prev = new_node
            self._head = new_node
        self._size += 1

    def add_back(self, value: Any) -> None:
        """
        Adds a new node to the back(tail) of the queue.
        If queue is empty, both head and tail point to the new node
        """
        new_node = DoubleNode(value)
        if self._tail is None:
            self._head = self._tail = new_node
        else:
            new_node.prev = self._tail
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1

    def remove_front(self) -> Any:
        """
        Removes and returns the front(head) element.
        If after removal head becomes None, tail is also set to None.
        Raises IndexError if queue is empty
        """
        if self._head is not None:
            removed = self._head.value
            self._head = self._head.next
            if self._head is None:
                self._tail = None
            else:
                self._head.prev = None
            self._size -= 1
            return removed
        raise IndexError('Queue is empty')

    def remove_back(self) -> Any:
        """
        Removes and returns the back(tail) element.
        If after removal tail becomes None, head also set to None.
        Raises IndexError if queue is None
        """
        if self._tail is not None:
            removed = self._tail.value
            self._tail = self._tail.prev
            if self._tail is None:
                self._head = None
            else:
                self._tail.next = None
            self._size -= 1
            return removed
        raise IndexError('Queue is empty')

    def peek_front(self) -> Any:
        """
        Returns the fron(head) element without removing it.
        Raises IndexError if queue is empty.
        """
        if self._head is not None:
            return self._head.value
        raise IndexError('Queue is empty')

    def peek_back(self) -> Any:
        """
        Retunrs the back(tail) element wihtout removing it.
        Raises IndexError if queue is empty
        """
        if self._tail is not None:
            return self._tail.value
        raise IndexError('Queue is empty')

    def size(self) -> int:
        """Returns the number of elements in the queue."""
        return self._size

    def copy(self) -> 'Deque':
        """Retruns a deep copy of the queue with no shared references."""
        copied = Deque()
        current = self._head
        while current:
            copied.add_back(current.value)
            current = current.next
        return copied

    def __len__(self) -> int:
        """Returns the number of elements in the queue."""
        return self._size

    def __bool__(self) -> bool:
        """Returns True if queue has at least one element"""
        return not self.is_empty()

    def __iter__(self) -> Generator[Any, None, None]:
        """Iterates from head to tail."""
        current = self._head
        while current:
            yield current.value
            current = current.next

    def __reversed__(self) -> Generator[Any, None, None]:
        """Iterates from tail to head."""
        current = self._tail
        while current:
            yield current.value
            current = current.prev

    def __contains__(self, item: Any) -> bool:
        """Returns True if item exists in the queue. O(n)"""
        current = self._head
        while current:
            if current.value == item:
                return True
            current = current.next
        return False

    def __eq__(self, other: object) -> bool:
        """Returns True if both queues have the same element in the same order."""
        if not isinstance(other, Deque):
            return NotImplemented
        return list(self) == list(other)

    def __str__(self) -> str:
        """Human-friendly string showing queue from head to tail."""
        values = ' -> '.join(str(v) for v in self)
        return f'Deque(head -> {values} <- tail)'
