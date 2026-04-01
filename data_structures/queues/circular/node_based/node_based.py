from typing import Any, Iterator, Optional

from ...._base import BaseQueue
from ....nodes import LinearNode


class NodeCircularQueue(BaseQueue):
    """
    A dynamic circular queue backed by LinearNode.
    Accepts any Python type — no dtype restriction.
    Follows FIFO (First In, First Out) principle.

    Uses a single _rear pointer. The circular invariant is maintained
    by always keeping _rear.next pointing to the front node.

    _rear       — last node in the queue (enqueue side).
    _rear.next  — first node in the queue (dequeue side / front).

    This means we only need one pointer to access both ends in O(1):
        front = _rear.next
        rear  = _rear

    Example with elements [1, 2, 3]:
        _rear → [3] → [1] → [2] → [3] (back to start)
                       ↑ front

    Time complexity:
        enqueue:      O(1)
        dequeue:      O(1)
        peek:         O(1)
        clear:        O(1)
        copy:         O(n)
        is_empty:     O(1)
        __len__:      O(1)
        __bool__:     O(1)
        __iter__:     O(n) — front to rear
        __reversed__: O(n)
        __contains__: O(n)
        __repr__:     O(n)
        __eq__:       O(n)
    """

    __slots__ = ("_rear", "_size")

    def __init__(self, *args) -> None:
        """
        Creates a node-based circular queue with optional initial elements.

        Args:
            *args: Optional initial elements, added left to right (first = front).

        Examples:
            q = NodeCircularQueue()           # empty
            q = NodeCircularQueue(1, 2, 3)    # front=1, rear=3
        """
        self._rear: Optional[LinearNode] = None
        self._size: int = 0

        for item in args:
            self.enqueue(item)

    # -------------------------------------------------------------------------
    # Core operations

    def enqueue(self, value: Any) -> None:
        """
        Adds value at the rear of the queue.

        Creates a new node. If the queue is empty, the node points
        to itself — it is both front and rear. Otherwise, the new
        node is inserted between the current rear and the front,
        then _rear advances to the new node.

        Time complexity: O(1)
        """
        node = LinearNode(value)
        if self._rear is None:
            node.next = node
        else:
            node.next = self._rear.next
            self._rear.next = node
        self._rear = node
        self._size += 1

    def dequeue(self) -> Any:
        """
        Removes and returns the value from the front of the queue.

        The front is always _rear.next. After removal, _rear.next
        advances to the next node. If the queue had only one element,
        _rear is set to None to mark it as empty.

        Time complexity: O(1)

        Raises:
            IndexError: If queue is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue")
        front = self._rear.next  # type: ignore[union-attr]
        value = front.value  # type: ignore[union-attr]
        if front is self._rear:
            self._rear = None
        else:
            self._rear.next = front.next  # type: ignore[union-attr]
        front.next = None  # type: ignore[union-attr]
        self._size -= 1
        return value

    def peek(self) -> Any:
        """
        Returns the front element without removing it.
        Front is always _rear.next.

        Time complexity: O(1)

        Raises:
            IndexError: If queue is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from an empty queue")
        return self._rear.next.value  # type: ignore[union-attr]

    def clear(self) -> None:
        """
        Removes all nodes by dropping the rear reference.

        Once rear is None the circular chain becomes unreachable
        and is collected by Python's garbage collector.

        Time complexity: O(1)
        """
        self._rear = None
        self._size = 0

    def copy(self) -> "NodeCircularQueue":
        """
        Returns a shallow copy of the queue preserving order.

        Time complexity: O(n)
        """
        new_queue = NodeCircularQueue()
        for value in self:
            new_queue.enqueue(value)
        return new_queue

    # -------------------------------------------------------------------------
    # State checks

    def is_empty(self) -> bool:
        """Returns True if the queue contains no elements. O(1)"""
        return self._rear is None

    # -------------------------------------------------------------------------
    # Dunder methods

    def __len__(self) -> int:
        """Returns number of elements currently in the queue. O(1)"""
        return self._size

    def __bool__(self) -> bool:
        """Returns True if the queue is not empty. O(1)"""
        return self._rear is not None

    def __iter__(self) -> Iterator[Any]:
        """
        Yields elements from front to rear without modifying the queue.
        Uses a step counter to avoid infinite loop over the circular chain.

        Time complexity: O(n)
        """
        if self._rear is None:
            return
        current = self._rear.next
        for _ in range(self._size):
            yield current.value  # type: ignore[union-attr]
            current = current.next  # type: ignore[union-attr]

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields elements from rear to front without modifying the queue.
        Collects all values first, then yields in reverse.

        Time complexity: O(n)
        """
        values = list(self)
        for value in reversed(values):
            yield value

    def __contains__(self, value: Any) -> bool:
        """Returns True if value exists in the queue. O(n)"""
        for v in self:
            if v == value:
                return True
        return False

    def __eq__(self, other: object) -> bool:
        """Returns True if both queues have the same elements in the same order."""
        if not isinstance(other, NodeCircularQueue):
            return NotImplemented
        if self._size != other._size:
            return False
        for a, b in zip(self, other):
            if a != b:
                return False
        return True

    def __repr__(self) -> str:
        """
        Returns string representation of the queue.
        Format: NodeCircularQueue(size=3)[1, 2, 3]
                                          front  rear

        Time complexity: O(n)
        """
        elements = ", ".join(repr(v) for v in self)
        return f"NodeCircularQueue(size={self._size})[{elements}]"
