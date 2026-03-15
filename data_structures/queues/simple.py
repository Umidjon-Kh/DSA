from dataclasses import dataclass, field
from typing import Optional, Any, Generator
from ..nodes import SingleNode


@dataclass
class SimpleQueue:
    """
    Simple Queue data structure — FIFO (First In, First Out).
    Built on top of SingleNode (Singly Linked List).

    Two pointers — head and tail — allow O(1) enqueue and dequeue.
    Without tail pointer, enqueue would require walking the entire list O(n).

    Visual representation:
        enqueue(1), enqueue(2), enqueue(3)
        head → [1] → [2] → [3] ← tail

        dequeue() → returns 1
        head → [2] → [3] ← tail

    Time complexity:
        enqueue: O(1)
        dequeue: O(1)
        peek:    O(1)
        search (__contains__): O(n)
    """

    _head: Optional[SingleNode] = field(default=None, repr=False)
    _tail: Optional[SingleNode] = field(default=None, repr=False)
    _size: int = field(init=False, default=0)

    def is_empty(self) -> bool:
        """Returns True if queue has no elements."""
        return self._head is None

    def enqueue(self, value: Any) -> None:
        """
        Adds a new node to the tail of the queue.
        If queue is empty, both head and tail point to the new node.
        """
        new_node = SingleNode(value)
        if self._tail is None:
            self._head = self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1

    def dequeue(self) -> Any:
        """
        Removes and returns the head element.
        If after removal head becomes None, tail is also set to None.
        Raises IndexError if queue is empty.
        """
        if self._head is not None:
            removed = self._head.value
            self._head = self._head.next
            if self._head is None:
                self._tail = None
            self._size -= 1
            return removed
        raise IndexError('Queue is empty')

    def peek(self) -> Any:
        """
        Returns the head element without removing it.
        Raises IndexError if queue is empty.
        """
        if self._head is not None:
            return self._head.value
        raise IndexError('Queue is empty')

    def size(self) -> int:
        """Returns the number of elements in the queue."""
        return self._size

    def copy(self) -> 'SimpleQueue':
        """Returns a deep copy of the queue with no shared references."""
        copied = SimpleQueue()
        current = self._head
        while current:
            copied.enqueue(current.value)
            current = current.next
        return copied

    def __len__(self) -> int:
        """Returns the number of elements in the queue."""
        return self._size

    def __bool__(self) -> bool:
        """Returns True if queue has at least one element."""
        return not self.is_empty()

    def __iter__(self) -> Generator[Any, None, None]:
        """Iterates from head to tail (FIFO order)."""
        current = self._head
        while current:
            yield current.value
            current = current.next

    def __reversed__(self) -> Generator[Any, None, None]:
        """Iterates from tail to head."""
        for value in reversed(list(self)):
            yield value

    def __contains__(self, item: Any) -> bool:
        """Returns True if item exists in the queue. O(n)."""
        current = self._head
        while current:
            if current.value == item:
                return True
            current = current.next
        return False

    def __eq__(self, other: object) -> bool:
        """Returns True if both queues have the same elements in the same order."""
        if not isinstance(other, SimpleQueue):
            return NotImplemented
        return list(self) == list(other)

    def __str__(self) -> str:
        """Human-friendly string showing queue from head to tail."""
        values = ' -> '.join(str(v) for v in self)
        return f'SimpleQueue(head -> {values} <- tail)'
