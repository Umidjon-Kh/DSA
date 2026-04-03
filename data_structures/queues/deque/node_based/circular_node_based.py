from typing import Any, Iterator

from ...._base import BaseDeque
from ....nodes import BiLinearNode


class CircularNodeDeque(BaseDeque):
    """
    A dynamic circular deque backed by BiLinearNode.
    Accepts any Python type — no dtype restriction.
    Supports O(1) insertion and removal from both ends.

    Uses a single sentinel node to eliminate all edge-case checks.
    The sentinel's next always points to the front, and its prev always
    points to the rear. An empty deque has the sentinel pointing to itself.

    ── Structure ────────────────────────────────────────────────────────────
    The sentinel acts as the anchor of the circular chain:

        sentinel.next → front node  (or sentinel itself if empty)
        sentinel.prev → rear node   (or sentinel itself if empty)

    Example with elements [1, 2, 3]:

        sentinel <-> [1] <-> [2] <-> [3] <-> (back to sentinel)
                    ↑                   ↑
                  front               rear

    Empty state:
        sentinel.next = sentinel
        sentinel.prev = sentinel

    ── Why a sentinel? ───────────────────────────────────────────────────────
    Without a sentinel, every enqueue and dequeue operation must check
    whether the deque is empty to handle the front/rear = None edge case.
    The sentinel eliminates those branches entirely — insertion and removal
    logic is the same regardless of how many elements exist.

    ── Time complexity ───────────────────────────────────────────────────────
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

    __slots__ = ("_sentinel", "_size")

    def __init__(self, *args) -> None:
        """
        Creates a circular node-based deque with optional initial elements.

        The sentinel is created first and points to itself in both directions,
        representing an empty circular chain. Each item in args is then
        enqueued to the rear.

        Args:
            *args: Optional initial elements, added left to right (first = front).

        Examples:
            d = CircularNodeDeque()           # empty
            d = CircularNodeDeque(1, 2, 3)    # front=1, rear=3
        """
        self._sentinel: BiLinearNode = BiLinearNode(None)
        self._sentinel.next = self._sentinel
        self._sentinel.prev = self._sentinel
        self._size: int = 0

        for item in args:
            self.enqueue_rear(item)

    # -------------------------------------------------------------------------
    # Internal helpers

    def _insert_between(
        self, value: Any, before: BiLinearNode, after: BiLinearNode
    ) -> None:
        """
        Creates a new node with given value and inserts it between
        the two given nodes.

        Before the call:  before <-> after
        After the call:   before <-> new_node <-> after

        This is the single insertion primitive used by both
        enqueue_front and enqueue_rear.

        Time complexity: O(1)

        Args:
            value:  The value to store in the new node.
            before: The node that will precede the new node.
            after:  The node that will follow the new node.
        """
        node = BiLinearNode(value)
        node.prev = before
        node.next = after
        before.next = node
        after.prev = node
        self._size += 1

    def _unlink(self, node: BiLinearNode) -> Any:
        """
        Removes the given node from the circular chain and returns its value.

        Before the call:  node.prev <-> node <-> node.next
        After the call:   node.prev <-> node.next   (node is isolated)

        Severs node.prev and node.next after relinking its neighbors
        so the removed node holds no references into the deque.

        This is the single removal primitive used by both
        dequeue_front and dequeue_rear.

        Time complexity: O(1)

        Args:
            node: The node to remove. Must not be the sentinel.

        Returns:
            The value stored in the removed node.
        """
        predecessor = node.prev  # type: ignore[assignment]
        successor = node.next  # type: ignore[assignment]
        predecessor.next = successor  # type: ignore[union-attr]
        successor.prev = predecessor  # type: ignore[union-attr]
        node.prev = None
        node.next = None
        self._size -= 1
        return node.value

    # -------------------------------------------------------------------------
    # Core operations

    def enqueue_front(self, value: Any) -> None:
        """
        Inserts value at the front of the deque.

        Inserts a new node between the sentinel and the current front node.
        If the deque is empty, the sentinel's next is itself, so the new
        node ends up between sentinel and sentinel — becoming both front and rear.

        Time complexity: O(1)
        """
        self._insert_between(value, self._sentinel, self._sentinel.next)  # type: ignore[arg-type]

    def enqueue_rear(self, value: Any) -> None:
        """
        Inserts value at the rear of the deque.

        Inserts a new node between the current rear node and the sentinel.
        If the deque is empty, the sentinel's prev is itself, so the new
        node ends up between sentinel and sentinel — becoming both front and rear.

        Time complexity: O(1)
        """
        self._insert_between(value, self._sentinel.prev, self._sentinel)  # type: ignore[arg-type]

    def dequeue_front(self) -> Any:
        """
        Removes and returns the value from the front of the deque.
        The front is always sentinel.next.

        Time complexity: O(1)

        Raises:
            IndexError: If deque is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from an empty deque")
        return self._unlink(self._sentinel.next)  # type: ignore[arg-type]

    def dequeue_rear(self) -> Any:
        """
        Removes and returns the value from the rear of the deque.
        The rear is always sentinel.prev.

        Time complexity: O(1)

        Raises:
            IndexError: If deque is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from an empty deque")
        return self._unlink(self._sentinel.prev)  # type: ignore[arg-type]

    def peek_front(self) -> Any:
        """
        Returns the front element's value without removing it.
        The front is always sentinel.next.

        Time complexity: O(1)

        Raises:
            IndexError: If deque is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from an empty deque")
        return self._sentinel.next.value  # type: ignore[union-attr]

    def peek_rear(self) -> Any:
        """
        Returns the rear element's value without removing it.
        The rear is always sentinel.prev.

        Time complexity: O(1)

        Raises:
            IndexError: If deque is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from an empty deque")
        return self._sentinel.prev.value  # type: ignore[union-attr]

    def clear(self) -> None:
        """
        Removes all nodes by resetting the sentinel to point to itself.

        Once the sentinel's next and prev are set back to the sentinel,
        the entire chain becomes unreachable and is collected by Python's
        garbage collector. No traversal needed.

        Time complexity: O(1)
        """
        self._sentinel.next = self._sentinel
        self._sentinel.prev = self._sentinel
        self._size = 0

    def copy(self) -> "CircularNodeDeque":
        """
        Returns a shallow copy of the deque preserving order.
        Traverses front to rear and enqueues each value to the rear
        of the new deque.

        Time complexity: O(n)
        """
        new_deque = CircularNodeDeque()
        for value in self:
            new_deque.enqueue_rear(value)
        return new_deque

    # -------------------------------------------------------------------------
    # State checks

    def is_empty(self) -> bool:
        """
        Returns True if the deque contains no elements.
        The deque is empty when the sentinel points to itself.

        Time complexity: O(1)
        """
        return self._sentinel.next is self._sentinel

    # -------------------------------------------------------------------------
    # Dunder methods

    def __len__(self) -> int:
        """Returns number of elements currently in the deque. O(1)"""
        return self._size

    def __bool__(self) -> bool:
        """Returns True if the deque is not empty. O(1)"""
        return self._sentinel.next is not self._sentinel

    def __iter__(self) -> Iterator[Any]:
        """
        Yields elements from front to rear without modifying the deque.
        Traversal stops when it reaches the sentinel again.

        Time complexity: O(n)
        """
        current = self._sentinel.next
        while current is not self._sentinel:
            yield current.value  # type: ignore[union-attr]
            current = current.next  # type: ignore[union-attr]

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields elements from rear to front without modifying the deque.
        Traversal stops when it reaches the sentinel again.
        Uses the prev pointer of BiLinearNode — no extra memory needed.

        Time complexity: O(n)
        """
        current = self._sentinel.prev
        while current is not self._sentinel:
            yield current.value  # type: ignore[union-attr]
            current = current.prev  # type: ignore[union-attr]

    def __eq__(self, other: object) -> bool:
        """Returns True if both deques have the same elements in the same order."""
        if not isinstance(other, CircularNodeDeque):
            return NotImplemented
        if self._size != other._size:
            return False
        for a, b in zip(self, other):
            if a != b:
                return False
        return True

    def __contains__(self, value: Any) -> bool:
        """Returns True if value exists in the deque. O(n)"""
        for v in self:
            if v == value:
                return True
        return False

    def __repr__(self) -> str:
        """
        Returns string representation of the deque.
        Format: CircularNodeDeque(size=3)[1, 2, 3]
                                          front  rear

        Time complexity: O(n)
        """
        elements = ", ".join(repr(v) for v in self)
        return f"CircularNodeDeque(size={self._size})[{elements}]"
