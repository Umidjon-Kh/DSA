from typing import Any, Iterator, Optional

from ...._base import BaseQueue
from ....nodes import LinearNode


class NodeQueue(BaseQueue):
    """
    A dynamic queue backed by LinearNode.
    Accepts any Python type — no dtype restriction.
    Follows FIFO (First In, First Out) principle.

    _front = head of the queue (dequeue side).
    _rear  = tail of the queue (enqueue side).

    Each enqueue creates a new node linked after the current rear.
    Each dequeue removes the front node and returns its value.
    No resize overhead — each element is an independent node.
    No capacity limit.

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

    __slots__ = ("_front", "_rear", "_size")

    def __init__(self, *args) -> None:
        """
        Creates a node-based queue with optional initial elements.

        Args:
            *args: Optional initial elements, added left to right (first = front).

        Examples:
            q = NodeQueue()           # empty
            q = NodeQueue(1, 2, 3)    # front=1, rear=3
        """
        self._front: Optional[LinearNode] = None
        self._rear: Optional[LinearNode] = None
        self._size: int = 0

        for item in args:
            self.enqueue(item)

    # -------------------------------------------------------------------------
    # Core operations

    def enqueue(self, value: Any) -> None:
        """
        Creates a new node and places it at the rear of the queue.
        New node's next is None. Previous rear's next points to new node.
        If the queue is empty, the new node becomes both front and rear.

        Time complexity: O(1)
        """
        node = LinearNode(value)
        if self._rear is None:
            self._front = node
            self._rear = node
        else:
            self._rear.next = node
            self._rear = node
        self._size += 1

    def dequeue(self) -> Any:
        """
        Removes the front node and returns its value.
        Moves front one node forward.
        If the queue becomes empty after removal,
        rear is also set to None to avoid dangling references.

        Time complexity: O(1)

        Raises:
            IndexError: If queue is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue")
        value = self._front.value  # type: ignore[union-attr]
        self._front = self._front.next  # type: ignore[union-attr]
        if self._front is None:
            self._rear = None
        self._size -= 1
        return value

    def peek(self) -> Any:
        """
        Returns the front element's value without removing it.

        Time complexity: O(1)

        Raises:
            IndexError: If queue is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from an empty queue")
        return self._front.value  # type: ignore[union-attr]

    def clear(self) -> None:
        """
        Removes all nodes by dropping front and rear references.

        Once front is None the entire chain becomes unreachable
        and is collected by Python's garbage collector.

        Time complexity: O(1)
        """
        self._front = None
        self._rear = None
        self._size = 0

    def copy(self) -> "NodeQueue":
        """
        Returns a shallow copy of the queue preserving order.

        Time complexity: O(n)
        """
        new_queue = NodeQueue()
        current = self._front
        while current is not None:
            new_queue.enqueue(current.value)
            current = current.next
        return new_queue

    # -------------------------------------------------------------------------
    # State checks

    def is_empty(self) -> bool:
        """Returns True if the queue contains no elements. O(1)"""
        return self._front is None

    # -------------------------------------------------------------------------
    # Dunder methods

    def __len__(self) -> int:
        """Returns number of elements currently in the queue. O(1)"""
        return self._size

    def __bool__(self) -> bool:
        """Returns True if the queue is not empty. O(1)"""
        return self._front is not None

    def __iter__(self) -> Iterator[Any]:
        """
        Yields elements from front to rear without modifying the queue.

        Time complexity: O(n)
        """
        current = self._front
        while current is not None:
            yield current.value
            current = current.next

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields values from rear to front.
        Builds a temporary reversed LinearNode chain, then traverses it.

        Time complexity: O(n)
        """
        temp_front: Optional[LinearNode] = None
        current = self._front
        while current is not None:
            temp = LinearNode(current.value)
            temp.next = temp_front
            temp_front = temp
            current = current.next
        current = temp_front
        while current is not None:
            yield current.value
            current = current.next

    def __eq__(self, other: object) -> bool:
        """Returns True if both queues have the same elements in the same order."""
        if not isinstance(other, NodeQueue):
            return NotImplemented
        if self._size == 0 and other._size == 0:
            return True
        if self._size != other._size:
            return False
        cur_a = self._front
        cur_b = other._front
        for _ in range(self._size):
            if cur_a.value != cur_b.value:  # type: ignore[union-attr]
                return False
            cur_a = cur_a.next  # type: ignore[union-attr]
            cur_b = cur_b.next  # type: ignore[union-attr]
        return True

    def __contains__(self, value: Any) -> bool:
        """Returns True if value exists in the queue. O(n)"""
        current = self._front
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False

    def __repr__(self) -> str:
        """
        Returns string representation of the queue.
        Format: NodeQueue(size=3)[1, 2, 3]
                                  front  rear

        Time complexity: O(n)
        """
        elements = ", ".join(repr(v) for v in self)
        return f"NodeQueue(size={self._size})[{elements}]"
