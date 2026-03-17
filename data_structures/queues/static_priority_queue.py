from dataclasses import dataclass, field
from typing import Any, Generator, Optional
from ..arrays import FixedArray


@dataclass(frozen=True, slots=True)
class PriorityItem:
    """
    A container that pairs a value with its priority.
    Used internally by PriorityQueue to track element ordering.
    Higher priority number means higher urgency.
    """

    value: Any
    priority: int


@dataclass
class PriorityQueue:
    """
    A Priority Queue where each element carries a priority number.
    dequeue always returns the element with the highest priority,
    regardless of insertion order.

    Naive implementation built on FixedArray — no sorting on insert.
    enqueue: O(1) — append to next free slot.
    dequeue: O(n) — linear scan to find max priority.
    peek:    O(n) — same scan without removal.

    For O(log n) operations, see the Heap-based implementation.
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
        """Returns True if queue has reached its capacity"""
        return self._size == self._capacity

    def enqueue(self, value: Any, priority: int) -> None:
        """
        Adds value to the lost at _tail index.
        Advances _tail using module to wrap arount: (tail + 1) % capacity.
        Raises MemoryEror if queue is full
        """
        if not self.is_full():
            self._array[self._tail] = PriorityItem(value, priority)
            self._tail += 1
            self._size += 1
            return
        raise MemoryError(f'Queue is full (capacity={self._capacity})')

    def dequeue(self) -> Any:
        """
        Removes and returns value of highest object in array.
        Too slow cause needs to checks array values
        While not gets value with highest priority.
        Raises IndexError if queue is empty.
        """
        if not self.is_empty():
            max_idx = 0
            for index in range(1, self._size):
                item = self._array[index]
                if item.priority > self._array[max_idx].priority:
                    max_idx = index
            # Saving removal object value
            removed = self._array[max_idx].value
            # Swiping all elements after max_idx to left
            for index in range(max_idx, self._size - 1):
                self._array[index] = self._array[index + 1]
            # Clearing last slot
            self._array[self._size - 1] = None
            self._tail -= 1
            self._size -= 1
            return removed
        raise IndexError('Queue is empty')
