from typing import Any, Iterator, Optional

from ...._base import BaseDeque
from ....nodes import BiLinearNode


class NodeDeque(BaseDeque):
    """
    A dynamic deque backed by BiLinearNode.
    Accepts any Python type — no dtype restriction.
    Supports O(1) insertion and removal from both ends.

    _front — first node in the deque (dequeue_front side).
    _rear  — last node in the deque  (dequeue_rear side).

    Each node holds prev and next pointers, so both ends are reachable
    in O(1) without any shifting. No capacity limit.

    Example with elements [1, 2, 3]:

        None ← [1] ↔ [2] ↔ [3] → None
                ↑                   ↑
             _front               _rear

    Time complexity:
        enqueue_front:  O(1)
        enqueue_rear:   O(1)
        dequeue_front:  O(1)
        dequeue_rear:   O(1)
        peek_front:     O(1)
        peek_rear:      O(1)
        clear:          O(1)
        copy:           O(n)
        is_empty:       O(1)
        __len__:        O(1)
        __bool__:       O(1)
        __iter__:       O(n) — front to rear
        __reversed__:   O(n) — rear to front
        __contains__:   O(n)
        __repr__:       O(n)
        __eq__:         O(n)
    """

    __slots__ = ("_front", "_rear", "_size")

    def __init__(self, *args) -> None:
        """
        Creates a node-based deque with optional initial elements.

        Args:
            *args: Optional initial elements, added left to right (first = front).

        Examples:
            d = NodeDeque()           # empty
            d = NodeDeque(1, 2, 3)    # front=1, rear=3
        """
        self._front: Optional[BiLinearNode] = None
        self._rear: Optional[BiLinearNode] = None
        self._size: int = 0

        for item in args:
            self.enqueue_rear(item)

    # -------------------------------------------------------------------------
    # Core operations

    def enqueue_front(self, value: Any) -> None:
        """
        Creates a new node and places it at the front of the deque.
        The new node's next points to the previous front.
        The previous front's prev is updated to point back to the new node.
        If the deque is empty, the new node becomes both front and rear.

        Time complexity: O(1)
        """
        node = BiLinearNode(value)
        if self._front is None:
            self._front = node
            self._rear = node
        else:
            node.next = self._front
            self._front.prev = node
            self._front = node
        self._size += 1

    def enqueue_rear(self, value: Any) -> None:
        """
        Creates a new node and places it at the rear of the deque.
        The new node's prev points to the previous rear.
        The previous rear's next is updated to point to the new node.
        If the deque is empty, the new node becomes both front and rear.

        Time complexity: O(1)
        """
        node = BiLinearNode(value)
        if self._rear is None:
            self._front = node
            self._rear = node
        else:
            node.prev = self._rear
            self._rear.next = node
            self._rear = node
        self._size += 1

    def dequeue_front(self) -> Any:
        """
        Removes the front node and returns its value.
        Moves _front one node forward and severs the removed node's next pointer.
        If the deque becomes empty after removal, _rear is also set to None
        to avoid dangling references.

        Time complexity: O(1)

        Raises:
            IndexError: If deque is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from an empty deque")
        value = self._front.value  # type: ignore[union-attr]
        self._front = self._front.next  # type: ignore[union-attr]
        if self._front is None:
            self._rear = None
        else:
            self._front.prev = None
        self._size -= 1
        return value

    def dequeue_rear(self) -> Any:
        """
        Removes the rear node and returns its value.
        Moves _rear one node backward and severs the removed node's prev pointer.
        If the deque becomes empty after removal, _front is also set to None
        to avoid dangling references.

        Time complexity: O(1)

        Raises:
            IndexError: If deque is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from an empty deque")
        value = self._rear.value  # type: ignore[union-attr]
        self._rear = self._rear.prev  # type: ignore[union-attr]
        if self._rear is None:
            self._front = None
        else:
            self._rear.next = None
        self._size -= 1
        return value

    def peek_front(self) -> Any:
        """
        Returns the front element's value without removing it.

        Time complexity: O(1)

        Raises:
            IndexError: If deque is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from an empty deque")
        return self._front.value  # type: ignore[union-attr]

    def peek_rear(self) -> Any:
        """
        Returns the rear element's value without removing it.

        Time complexity: O(1)

        Raises:
            IndexError: If deque is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from an empty deque")
        return self._rear.value  # type: ignore[union-attr]

    def clear(self) -> None:
        """
        Removes all nodes by dropping front and rear references.

        Once both references are dropped, the entire chain becomes
        unreachable and is collected by Python's garbage collector.
        No manual traversal needed.

        Time complexity: O(1)
        """
        self._front = None
        self._rear = None
        self._size = 0

    def copy(self) -> "NodeDeque":
        """
        Returns a shallow copy of the deque preserving order.
        Traverses from front to rear and enqueues each value to the rear
        of the new deque.

        Time complexity: O(n)
        """
        new_deque = NodeDeque()
        current = self._front
        while current is not None:
            new_deque.enqueue_rear(current.value)
            current = current.next
        return new_deque

    # -------------------------------------------------------------------------
    # State checks

    def is_empty(self) -> bool:
        """Returns True if the deque contains no elements. O(1)"""
        return self._front is None

    # -------------------------------------------------------------------------
    # Dunder methods

    def __len__(self) -> int:
        """Returns number of elements currently in the deque. O(1)"""
        return self._size

    def __bool__(self) -> bool:
        """Returns True if the deque is not empty. O(1)"""
        return self._front is not None

    def __iter__(self) -> Iterator[Any]:
        """
        Yields elements from front to rear without modifying the deque.

        Time complexity: O(n)
        """
        current = self._front
        while current is not None:
            yield current.value
            current = current.next

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields elements from rear to front without modifying the deque.
        Uses the prev pointer of BiLinearNode — no extra memory needed.

        Time complexity: O(n)
        """
        current = self._rear
        while current is not None:
            yield current.value
            current = current.prev

    def __eq__(self, other: object) -> bool:
        """Returns True if both deques have the same elements in the same order."""
        if not isinstance(other, NodeDeque):
            return NotImplemented
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
        """Returns True if value exists in the deque. O(n)"""
        current = self._front
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False

    def __repr__(self) -> str:
        """
        Returns string representation of the deque.
        Format: NodeDeque(size=3)[1, 2, 3]
                                  front  rear

        Time complexity: O(n)
        """
        elements = ", ".join(repr(v) for v in self)
        return f"NodeDeque(size={self._size})[{elements}]"
