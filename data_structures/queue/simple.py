from dataclasses import dataclass, field
from typing import Optional, Any, Generator
from .single_node import SingleNode


@dataclass
class SimpleQueue:
    _head: Optional[SingleNode] = field(default=None, repr=False)
    _tail: Optional[SingleNode] = field(default=None, repr=False)
    _size: int = field(init=False, default=0)

    def is_empty(self) -> bool:
        return self._head is None

    def enqueue(self, value) -> None:
        """Adds new node with any type of value"""
        new_node = SingleNode(value)
        # Checking one of tha attrs(head, tail) None or not
        # cause if attr is None
        # It will be first element of queue
        if self._tail is None:
            self._head = self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node

        self._size += 1

    def dequeue(self) -> Any:
        """Removes first element in queue and returns it"""
        if self._head is not None:
            removed = self._head.value
            self._head = self._head.next

            # Checking new head is none or not
            # if none it means the queue is empty
            # And need to define tail as None
            if self._head is None:
                self._tail = None

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

    def copy(self) -> 'SimpleQueue':
        """Returns copy of Queue that not connected to this Queue"""
        copied_queue = SimpleQueue()

        current = self._head
        while current:
            copied_queue.enqueue(current.value)
            current = current.next

        return copied_queue

    def __len__(self) -> int:
        """Returns size of Queue"""
        return self._size

    def __iter__(self) -> Generator[Any, None, None]:
        """For iterating Queue nodes"""
        current = self._head

        while current:
            yield current.value
            current = current.next

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

    def __bool__(self):
        """Returns true if Queue is not None"""
        return not self.is_empty()

    def __str__(self) -> str:
        """
        String method shows all Queue values in user friendly output
        """

        values = [value for value in list(self)]

        return 'SimpleQueue(head -> ' + ' -> '.join(map(str, values)) + ' <- tail)'
