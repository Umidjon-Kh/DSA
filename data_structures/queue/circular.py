from dataclasses import dataclass, field
from typing import Optional, Any, Generator
from .single_node import SingleNode


@dataclass
class CircularQueue:
    _head: Optional[SingleNode] = field(default=None, repr=False)
    _tail: Optional[SingleNode] = field(default=None, repr=False)
    _size: int = field(init=False, default=0)

    def is_empty(self) -> bool:
        return self._head is None

    def enqueue(self, value) -> None:
        """Adds new node with any type of value"""
        new_node = SingleNode(value)

        # Checking one of the attrs(head, tail) None or not
        # cause if attr is None
        # It will be first element of queue
        if self._tail is None:
            self._head = self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node
            self._tail.next = self._head

        self._size += 1

    def dequeue(self) -> Any:
        """Removes first element in queue and returns it"""
        if self._head is not None and self._tail is not None:
            removed = self._head.value
            self._head = self._head.next

            if self._head is None:
                self._tail = None
            else:
                self._tail.next = self._head

            self._size -= 1
            return removed

        raise IndexError('Queue is empty')

    def peek(self) -> Any:
        """Shows first element(head) of queue"""
        if self._head is not None:
            return self._head.value

        raise IndexError('Queue is empty')

    def size(self) -> int:
        """Returns size of queue"""
        return self._size

    def copy(self) -> 'CircularQueue':
        """Returns copy of Queueu that not connected to this Queue"""
        copied_queue = CircularQueue()

        current = self._head
        count = 0
        while current:
            copied_queue.enqueue(current.value)
            current = current.next
            count += 1
            # Breaking if count equal to size of queue
            # Cause our queue is circular and never ends
            if count == self._size:
                break

        return copied_queue

    def __len__(self) -> int:
        """Returns size of Queue"""
        return self._size

    def __iter__(self) -> Generator[Any, None, None]:
        """For itering Queue nodes"""
        current = self._head
        count = 0

        while current:
            yield current.value
            current = current.next
            count += 1
            if count == self._size:
                return

    def __reversed__(self) -> Generator[Any, None, None]:
        """For Itering Queue in reversed"""
        for node_value in reversed(list(self)):
            yield node_value

    def __contains__(self, item) -> bool:
        """Checks Queue for contains item or not"""
        for node_value in list(self):
            if node_value == item:
                return True
        return False

    def __bool__(self) -> bool:
        """Returns true if Queue is not None"""
        return not self.is_empty()

    def __str__(self) -> str:
        """
        String method shows all Queue values in user frienly output
        """

        values = [value for value in list(self)]

        return f'CircularQueue(front - {values} - rear)'
