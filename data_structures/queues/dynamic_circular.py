from dataclasses import dataclass, field
from collections.abc import Iterable
from typing import Optional, Any, Generator
from ..nodes import SingleNode


@dataclass
class DynamicCircularQueue:
    """
    Dynamic Circular Queue — FIFO queue where tail.next always points back to head.
    Built on top of SingleNode (Singly Linked List).

    The circular link means the queue forms a ring:
        head -> [1] -> [2] -> [3] -> (back to head)
                                    ^ tail

    Why circular:
        - Useful when you need to continuously cycle through elements
        - Real use cases: round-robin schedulers, buffered streams

    Note: This is a node-based circular queue — size is dynamic, no fixed capacity.
    For a fixed-capacity circular queue, see StaticCircularQueue.

    Time complexity:
        enqueue: O(1)
        dequeue: O(1)
        peek:    O(1)
        search (__contains__): O(n)
    """

    _head: Optional[SingleNode] = field(default=None, repr=False, init=False)
    _tail: Optional[SingleNode] = field(default=None, repr=False, init=False)
    _size: int = field(init=False, default=0)

    def is_empty(self) -> bool:
        """Returns True if queue has no elements."""
        return self._head is None

    def enqueue(self, value: Any) -> None:
        """
        Adds a new node to the tail and links tail.next back to head.
        If queue is empty, the single node points to itself.
        """
        new_node = SingleNode(value)
        if self._tail is None:
            # First element — points to itself, forming a ring of one
            self._head = self._tail = new_node
            new_node.next = self._head
        else:
            self._tail.next = new_node
            self._tail = new_node
            # Re-establish the circular link back to head
            self._tail.next = self._head
        self._size += 1

    def dequeue(self) -> Any:
        """
        Removes and returns the head element.
        Updates tail.next to point to the new head to keep the ring intact.
        Raises IndexError if queue is empty.
        """
        if self._head is not None and self._tail is not None:
            removed = self._head.value
            self._head = self._head.next

            if self._head is None or self._size == 1:
                # Queue is now empty — break the circular link
                self._head = self._tail = None
            else:
                # Re-establish the circular link to the new head
                self._tail.next = self._head

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

    def copy(self) -> 'DynamicCircularQueue':
        """Returns a deep copy of the queue with no shared references."""
        copied = DynamicCircularQueue()
        current = self._head
        for _ in range(self._size):
            # Linter requires explicit None check here since it cannot
            # infer that current is always set when _size > 0
            if current is not None:
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
        """
        Iterates from head through all elements exactly once.
        Uses a counter to stop after _size elements — without it
        the circular link would cause an infinite loop.
        """
        current = self._head
        for _ in range(self._size):
            if current is not None:
                yield current.value
                current = current.next

    def __reversed__(self) -> Generator[Any, None, None]:
        """Iterates from tail to head."""
        for value in reversed(list(self)):
            yield value

    def __contains__(self, item: Any) -> bool:
        """Returns True if item exists in the queue. O(n)."""
        current = self._head
        for _ in range(self._size):
            if current is not None:
                if current.value == item:
                    return True
                current = current.next
        return False

    def __eq__(self, other: object) -> bool:
        """Returns True if both structures have the same elements in the same order."""
        if not isinstance(other, Iterable):
            return NotImplemented
        return list(self) == list(other)

    def __str__(self) -> str:
        """Human-friendly string showing queue from head to tail with circular marker."""
        values = ' -> '.join(str(v) for v in self)
        return f'CircularQueue(front -> {values} -> (back to front))'
