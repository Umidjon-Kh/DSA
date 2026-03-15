from dataclasses import dataclass, field
from typing import Any, Generator
from ..arrays import FixedArray


@dataclass
class StaticCircularQueue:
    """
    Static Circular Queue — fixed-capacity FIFO queue built on FixedArray (ctypes).
    This is the "true" circular queue — memory never grows or shrinks.

    Uses two index pointers (head, tail) instead of node pointers.
    The circular behavior is achieved with modulo arithmetic: (index + 1) % capacity.
    No Node objects are created — raw memory slots are reused.

    Why this is more memory-efficient than node-based:
        - Fixed memory block allocated once at creation
        - No Node object overhead per element
        - Slots are reused after dequeue — memory never leaks

    Visual representation (capacity=5):
        Initial:  [_, _, _, _, _]  head=0, tail=0
        enqueue:  [1, 2, 3, _, _]  head=0, tail=3
        dequeue:  [_, 2, 3, _, _]  head=1, tail=3
        enqueue:  [5, 2, 3, 4, _]  head=1, tail=4  (tail wraps around)
        enqueue:  [5, 2, 3, 4, 6]  head=1, tail=0  (tail wrapped to 0 via % 5)

    Real-world use cases:
        - OS keyboard input buffer
        - Audio streaming buffers
        - Fixed-size log ring buffers

    Time complexity:
        enqueue: O(1)
        dequeue: O(1)
        peek:    O(1)
        search (__contains__): O(n)
    """

    _capacity: int
    _array: FixedArray = field(init=False, repr=False)
    _head: int = field(init=False, repr=False, default=0)
    _tail: int = field(init=False, repr=False, default=0)
    _size: int = field(init=False, default=0)

    def __post_init__(self) -> None:
        self._array = FixedArray(self._capacity)

    def is_empty(self) -> bool:
        """Returns True if queue has no elements."""
        return self._size == 0

    def is_full(self) -> bool:
        """Returns True if queue has reached its capacity."""
        return self._size == self._capacity

    def enqueue(self, value: Any) -> None:
        """
        Adds value to the slot at _tail index.
        Advances _tail using modulo to wrap around: (tail + 1) % capacity.
        Raises MemoryError if queue is full.
        """
        if not self.is_full():
            self._array[self._tail] = value
            self._tail = (self._tail + 1) % self._capacity
            self._size += 1
            return
        raise MemoryError(f'Queue is full (capacity={self._capacity})')

    def dequeue(self) -> Any:
        """
        Removes and returns value at _head index.
        Clears the slot, then advances _head using modulo.
        Raises IndexError if queue is empty.
        """
        if not self.is_empty():
            removed = self._array[self._head]
            # Clear the slot so old references don't linger in memory
            self._array[self._head] = None
            self._head = (self._head + 1) % self._capacity
            self._size -= 1
            return removed
        raise IndexError('Queue is empty')

    def peek(self) -> Any:
        """
        Returns the head element without removing it.
        Raises IndexError if queue is empty.
        """
        if not self.is_empty():
            return self._array[self._head]
        raise IndexError('Queue is empty')

    def size(self) -> int:
        """Returns the number of elements in the queue."""
        return self._size

    def copy(self) -> 'StaticCircularQueue':
        """
        Returns an exact physical copy — same capacity, same slot positions,
        same head and tail indices. Not just same values in same order.
        """
        copied = StaticCircularQueue(self._capacity)
        for i in range(self._capacity):
            copied._array[i] = self._array[i]
        copied._head = self._head
        copied._tail = self._tail
        copied._size = self._size
        return copied

    def __len__(self) -> int:
        """Returns the number of elements in the queue."""
        return self._size

    def __bool__(self) -> bool:
        """Returns True if queue has at least one element."""
        return not self.is_empty()

    def __iter__(self) -> Generator[Any, None, None]:
        """
        Iterates from head through all _size elements in FIFO order.
        Uses modulo to correctly handle wrap-around.

        Example: capacity=5, head=3, tail=1, size=3
            indices visited: 3, 4, 0  (wraps around via % 5)
        """
        for i in range(self._size):
            yield self._array[(self._head + i) % self._capacity]

    def __reversed__(self) -> Generator[Any, None, None]:
        """
        Iterates from tail to head in reverse FIFO order.
        Uses _size-1 as starting offset to land on the last filled slot.

        Example: capacity=5, head=3, tail=1, size=3
            indices visited: 0, 4, 3  (last filled → first filled)
        """
        for i in range(self._size - 1, -1, -1):
            yield self._array[(self._head + i) % self._capacity]

    def __contains__(self, item: Any) -> bool:
        """
        Returns True if item exists in the queue.
        Only checks filled slots — not the entire capacity.
        """
        for i in range(self._size):
            if self._array[(self._head + i) % self._capacity] == item:
                return True
        return False

    def __eq__(self, other: object) -> bool:
        """Returns True if both queues have same elements in same order."""
        if not isinstance(other, StaticCircularQueue):
            return NotImplemented
        return list(self) == list(other)

    def __str__(self) -> str:
        """Human-friendly string showing only the filled elements."""
        values = list(self)
        return f'StaticCircularQueue(capacity={self._capacity}, front -> {values} <- rear)'
