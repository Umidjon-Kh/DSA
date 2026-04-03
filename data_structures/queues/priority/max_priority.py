from typing import Any, Iterator

from ..._base import BasePriorityQueue
from ...heaps import DynamicUniversalMaxHeap
from .priority_object import PriorityObject


class MaxPriorityQueue(BasePriorityQueue):
    """
    A dynamic priority queue that always dequeues the element with the
    highest priority number first.

    Backed by DynamicUniversalMaxHeap. Wrapping into PriorityObject is
    handled internally — the caller simply passes a value and a priority.
    The heap orders elements via PriorityObject.__gt__ so the root is
    always the object with the largest priority number.

    ── Ordering ─────────────────────────────────────────────────────────────
    Higher priority number = dequeued first.

        q.enqueue("low urgency",  priority=1)
        q.enqueue("high urgency", priority=10)
        q.dequeue()  →  "high urgency"   # priority=10 comes out first

    ── Backed by heap ────────────────────────────────────────────────────────
    Internally every value is wrapped in a PriorityObject and pushed onto
    a DynamicUniversalMaxHeap. The heap grows automatically — no capacity
    argument is needed. The PriorityObject wrapper is never exposed to the
    caller — dequeue() and peek() return the raw value.

    ── Time complexity ───────────────────────────────────────────────────────
        enqueue:      O(log n)
        dequeue:      O(log n)
        peek:         O(1)
        clear:        O(1)
        copy:         O(n log n)
        is_empty:     O(1)
        __len__:      O(1)
        __bool__:     O(1)
        __iter__:     O(n) — yields (value, priority) tuples, internal heap order
        __reversed__: O(n)
        __contains__: O(n) — checks by value only
        __repr__:     O(n)
        __eq__:       O(n)
    """

    __slots__ = ("_heap",)

    def __init__(self, *args: tuple) -> None:
        """
        Creates a max priority queue with optional initial elements.

        Args:
            *args: Optional (value, priority) tuples inserted left to right.

        Raises:
            TypeError:  If any arg is not a (value, priority) tuple.
            TypeError:  If priority is not int or float.

        Examples:
            q = MaxPriorityQueue()
            q = MaxPriorityQueue(("low urgency", 1), ("high urgency", 10))
        """
        self._heap: DynamicUniversalMaxHeap = DynamicUniversalMaxHeap()

        for item in args:
            self.enqueue(item[0], item[1])

    # -------------------------------------------------------------------------
    # Core operations

    def enqueue(self, value: Any, priority: int | float) -> None:
        """
        Wraps value and priority into a PriorityObject and pushes it
        onto the heap. The heap restores the max-heap property via
        sift_up after insertion.

        Time complexity: O(log n)

        Raises:
            TypeError: If priority is not int or float.
        """
        self._heap.push(PriorityObject(value, priority))

    def dequeue(self) -> Any:
        """
        Removes and returns the value of the element with the highest
        priority number. The PriorityObject wrapper is discarded —
        only the raw value is returned.

        Time complexity: O(log n)

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from an empty priority queue")
        return self._heap.pop().value

    def peek(self) -> Any:
        """
        Returns the value of the element with the highest priority number
        without removing it. The PriorityObject wrapper is not exposed.

        Time complexity: O(1)

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from an empty priority queue")
        return self._heap.peek().value

    def peek_priority(self) -> int | float:
        """
        Returns the priority number of the front element without removing it.

        Time complexity: O(1)

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from an empty priority queue")
        return self._heap.peek().priority

    def clear(self) -> None:
        """
        Removes all elements from the queue.

        Time complexity: O(1)
        """
        self._heap.clear()

    def copy(self) -> "MaxPriorityQueue":
        """
        Returns a shallow copy of the queue with the same elements.
        The copy is built by pushing each PriorityObject from the internal
        heap into a new MaxPriorityQueue — heap property is preserved.

        Time complexity: O(n log n)
        """
        new_queue = MaxPriorityQueue()
        for item in self._heap:
            new_queue._heap.push(item)
        return new_queue

    # -------------------------------------------------------------------------
    # State checks

    def is_empty(self) -> bool:
        """Returns True if the queue contains no elements. O(1)"""
        return self._heap.is_empty()

    # -------------------------------------------------------------------------
    # Dunder methods

    def __len__(self) -> int:
        """Returns number of elements currently in the queue. O(1)"""
        return len(self._heap)

    def __bool__(self) -> bool:
        """Returns True if the queue is not empty. O(1)"""
        return not self._heap.is_empty()

    def __iter__(self) -> Iterator[tuple]:
        """
        Yields (value, priority) tuples in internal heap order (root first).
        The result is NOT sorted by priority — call dequeue() repeatedly
        for priority-ordered output.

        Time complexity: O(n)
        """
        for item in self._heap:
            yield item.value, item.priority

    def __reversed__(self) -> Iterator[tuple]:
        """
        Yields (value, priority) tuples in reverse internal heap order.

        Time complexity: O(n)
        """
        for item in reversed(self._heap):
            yield item.value, item.priority

    def __contains__(self, value: Any) -> bool:
        """
        Returns True if any element in the queue holds the given value. O(n)
        Comparison is done on value only — priority is not considered.
        """
        for item in self._heap:
            if item.value == value:
                return True
        return False

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both queues have the same elements in the same
        internal heap positions.

        Two queues built from the same elements in different insertion
        orders may produce different internal arrangements and thus
        compare as not equal even if their dequeue order is identical.
        """
        if not isinstance(other, MaxPriorityQueue):
            return NotImplemented
        return self._heap == other._heap

    def __repr__(self) -> str:
        """
        Returns string representation of the queue.
        Format: MaxPriorityQueue(size=2)[(value='high urgency', priority=10), ...]
                                         root (highest priority number)

        Time complexity: O(n)
        """
        elements = ", ".join(
            f"(value={item.value!r}, priority={item.priority!r})" for item in self._heap
        )
        return f"MaxPriorityQueue(size={len(self._heap)})[{elements}]"
