from typing import Any, Iterator, Optional

from ...nodes import DoubleNode
from ...tools import validate_index, validate_insert_index


class CircularDoublyLinkedList:
    """
    A circular doubly linked list backed by DoubleNode.
    tail.next always points to head, and head.prev always points to tail.

    _get_node uses O(n/2) traversal — starts from tail if index is closer to it.
    __iter__ and __reversed__ use a step counter instead of a None check
    to avoid infinite loops.

    Time complexity:
        append:       O(1)
        prepend:      O(1)
        insert:       O(n/2)
        remove:       O(n/2)
        index:        O(n)
        clear:        O(1)
        copy:         O(n)
        __getitem__:  O(n/2)
        __setitem__:  O(n/2)
        __len__:      O(1)
        __bool__:     O(1)
        __iter__:     O(n)
        __reversed__: O(n) — traverses from tail using prev pointers
        __contains__: O(n)
        __repr__:     O(n)
    """

    __slots__ = ("_head", "_tail", "_size")

    def __init__(self, *args) -> None:
        """
        Creates a circular doubly linked list with optional initial values.

        Args:
            *args: Optional initial values, appended in order.

        Examples:
            lst = CircularDoublyLinkedList()           # empty
            lst = CircularDoublyLinkedList(1, 2, 3)    # ... <-> 1 <-> 2 <-> 3 <-> ...
        """
        self._head: Optional[DoubleNode] = None
        self._tail: Optional[DoubleNode] = None
        self._size: int = 0

        for val in args:
            self.append(val)

    # -------------------------------------------------------------------------
    # Internal helpers

    def _get_node(self, index: int) -> DoubleNode:
        """
        Traverses the list and returns the node at given index.
        Supports negative indexing. Starts from tail if index is closer to it.

        Time complexity: O(n/2)

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range.
        """
        index = validate_index(index, self._size)
        if index < self._size // 2:
            current = self._head
            for _ in range(index):
                current = current.next  # type: ignore[union-attr]
        else:
            current = self._tail
            for _ in range(self._size - 1 - index):
                current = current.prev  # type: ignore[union-attr]
        return current  # type: ignore[union-attr]

    def _set_node(self, index: int, value: Any) -> None:
        """
        Sets value of the node at given index using _get_node.
        Supports negative indexing.

        Time complexity: O(n/2)

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range.
        """
        self._get_node(index).value = value

    def _append_to_empty(self, node: DoubleNode) -> None:
        """
        Initializes head and tail when the list is empty.
        Node points to itself in both directions to maintain the circular invariant.

        Time complexity: O(1)
        """
        node.next = node
        node.prev = node
        self._head = node
        self._tail = node

    def _link_nodes(self, a: DoubleNode, b: DoubleNode) -> None:
        """
        Links two adjacent nodes: sets a.next = b and b.prev = a.

        Time complexity: O(1)
        """
        a.next = b
        b.prev = a

    def _unlink_node(self, node: DoubleNode) -> None:
        """
        Bridges over a node by reconnecting its neighbors directly.
        Safe to call here because in a circular list every node always has
        valid prev and next — neither is ever None.
        Does not update head or tail — caller is responsible for that.

        Time complexity: O(1)
        """
        node.prev.next = node.next  # type: ignore[union-attr]
        node.next.prev = node.prev  # type: ignore[union-attr]

    # -------------------------------------------------------------------------
    # Core operations

    def append(self, value: Any) -> None:
        """
        Appends a new node with given value to the end of the list.
        Maintains circular invariant: tail.next = head, head.prev = tail.

        Time complexity: O(1)
        """
        node = DoubleNode(value)
        if self._size == 0:
            self._append_to_empty(node)
        else:
            self._link_nodes(self._tail, node)  # type: ignore[union-attr]
            self._link_nodes(node, self._head)  # type: ignore[union-attr]
            self._tail = node
        self._size += 1

    def prepend(self, value: Any) -> None:
        """
        Prepends a new node with given value to the front of the list.
        Maintains circular invariant: tail.next = head, head.prev = tail.

        Time complexity: O(1)
        """
        node = DoubleNode(value)
        if self._size == 0:
            self._append_to_empty(node)
        else:
            self._link_nodes(self._tail, node)  # type: ignore[union-attr]
            self._link_nodes(node, self._head)  # type: ignore[union-attr]
            self._head = node
        self._size += 1

    def insert(self, index: int, value: Any) -> None:
        """
        Inserts a new node with given value at given index.
        Supports negative indexing. Allows index == size (insert at end).

        Time complexity: O(n/2)

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range.
        """
        index = validate_insert_index(index, self._size)
        if index == 0:
            self.prepend(value)
            return
        if index == self._size:
            self.append(value)
            return
        node = DoubleNode(value)
        next_node = self._get_node(index)
        prev_node = next_node.prev
        self._link_nodes(prev_node, node)  # type: ignore[union-attr]
        self._link_nodes(node, next_node)
        self._size += 1

    def remove(self, index: int) -> Any:
        """
        Removes and returns the value of the node at given index.
        Restores circular invariant after removal.
        Supports negative indexing.

        Time complexity: O(n/2)

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range or list is empty.
        """
        if self._size == 0:
            raise IndexError("Remove from an empty list")
        target = self._get_node(index)
        value = target.value

        if self._size == 1:
            self._head = None
            self._tail = None
        elif target is self._head:
            self._head = self._head.next  # type: ignore[union-attr]
            self._link_nodes(self._tail, self._head)  # type: ignore[union-attr]
        elif target is self._tail:
            self._tail = self._tail.prev  # type: ignore[union-attr]
            self._link_nodes(self._tail, self._head)  # type: ignore[union-attr]
        else:
            self._unlink_node(target)

        self._size -= 1
        return value

    def index(self, value: Any) -> int:
        """
        Returns the index of the first node whose value equals given value.

        Time complexity: O(n)

        Raises:
            ValueError: If value is not found in the list.
        """
        current = self._head
        for i in range(self._size):
            if current.value == value:  # type: ignore[union-attr]
                return i
            current = current.next  # type: ignore[union-attr]
        raise ValueError(f"{value!r} is not in list")

    def clear(self) -> None:
        """
        Removes all nodes by dropping head and tail references.

        Time complexity: O(1)
        """
        self._head = None
        self._tail = None
        self._size = 0

    def copy(self) -> "CircularDoublyLinkedList":
        """
        Returns a shallow copy of the list preserving order.

        Time complexity: O(n)
        """
        return CircularDoublyLinkedList(*self)

    # -------------------------------------------------------------------------
    # Dunder methods

    def __getitem__(self, index: int) -> Any:
        """
        Returns the value of the node at given index. Supports negative indexing.

        Time complexity: O(n/2)

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range.
        """
        return self._get_node(index).value

    def __setitem__(self, index: int, value: Any) -> None:
        """
        Sets the value of the node at given index. Supports negative indexing.

        Time complexity: O(n/2)

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range.
        """
        self._set_node(index, value)

    def __len__(self) -> int:
        """Returns number of nodes in the list. O(1)"""
        return self._size

    def __bool__(self) -> bool:
        """Returns True if the list is not empty. O(1)"""
        return self._size > 0

    def __iter__(self) -> Iterator[Any]:
        """
        Yields values from head, exactly size steps.
        Uses a counter instead of a None check to handle the circular structure.

        Time complexity: O(n)
        """
        current = self._head
        for _ in range(self._size):
            yield current.value  # type: ignore[union-attr]
            current = current.next  # type: ignore[union-attr]

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields values from tail to head using prev pointers.
        Uses a counter instead of a None check to handle the circular structure.

        Time complexity: O(n)
        """
        current = self._tail
        for _ in range(self._size):
            yield current.value  # type: ignore[union-attr]
            current = current.prev  # type: ignore[union-attr]

    def __contains__(self, value: Any) -> bool:
        """Returns True if any node holds given value. O(n)"""
        try:
            self.index(value)
            return True
        except ValueError:
            return False

    def __repr__(self) -> str:
        """
        Returns string representation of the list.
        Format: CircularDoublyLinkedList(size=3)[... <-> 1 <-> 2 <-> 3 <-> ...]

        Time complexity: O(n)
        """
        elements = " <-> ".join(repr(v) for v in self)
        if self._size > 0:
            return f"CircularDoublyLinkedList(size={self._size})[... <-> {elements} <-> ...]"
        return "CircularDoublyLinkedList(size=0)[]"
