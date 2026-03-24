from typing import Any, Iterator, Optional

from ...nodes import SingleNode
from ...tools import validate_index, validate_insert_index


class CircularSinglyLinkedList:
    """
    A circular singly linked list backed by SingleNode.
    The tail's next always points back to head — there is no None terminator.

    Supports O(1) prepend/append and O(n) insert/remove/index.
    Traversal is forward-only — __reversed__ builds a temporary reversed chain.
    __iter__ and __reversed__ use a step counter instead of a None check
    to avoid infinite loops.

    Time complexity:
        append:       O(1)
        prepend:      O(1)
        insert:       O(n)
        remove:       O(n)
        index:        O(n)
        clear:        O(1)
        copy:         O(n)
        __getitem__:  O(n)
        __setitem__:  O(n)
        __len__:      O(1)
        __bool__:     O(1)
        __iter__:     O(n)
        __reversed__: O(n) — builds a temp reversed chain, then traverses it
        __contains__: O(n)
        __repr__:     O(n)
    """

    __slots__ = ("_head", "_tail", "_size")

    def __init__(self, *args) -> None:
        """
        Creates a circular singly linked list with optional initial values.

        Args:
            *args: Optional initial values, appended in order.

        Examples:
            lst = CircularSinglyLinkedList()           # empty
            lst = CircularSinglyLinkedList(1, 2, 3)    # 1 -> 2 -> 3 -> (head)
        """
        self._head: Optional[SingleNode] = None
        self._tail: Optional[SingleNode] = None
        self._size: int = 0

        for val in args:
            self.append(val)

    # -------------------------------------------------------------------------
    # Internal helpers

    def _get_node(self, index: int) -> SingleNode:
        """
        Traverses the list and returns the node at given index.
        Supports negative indexing. Validates index before traversal.

        Time complexity: O(n)

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range.
        """
        index = validate_index(index, self._size)
        current = self._head
        for _ in range(index):
            current = current.next  # type: ignore[union-attr]
        return current  # type: ignore[union-attr]

    def _set_node(self, index: int, value: Any) -> None:
        """
        Sets value of the node at given index using _get_node.
        Supports negative indexing.

        Time complexity: O(n)

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range.
        """
        self._get_node(index).value = value

    def _append_to_empty(self, node: SingleNode) -> None:
        """
        Initializes head and tail when the list is empty.
        Node points to itself to maintain the circular invariant.

        Time complexity: O(1)
        """
        node.next = node
        self._head = node
        self._tail = node

    # -------------------------------------------------------------------------
    # Core operations

    def append(self, value: Any) -> None:
        """
        Appends a new node with given value to the end of the list.
        Maintains circular invariant: tail.next = head.

        Time complexity: O(1)
        """
        node = SingleNode(value)
        if self._size == 0:
            self._append_to_empty(node)
        else:
            node.next = self._head
            self._tail.next = node  # type: ignore[union-attr]
            self._tail = node
        self._size += 1

    def prepend(self, value: Any) -> None:
        """
        Prepends a new node with given value to the front of the list.
        Maintains circular invariant: tail.next = head.

        Time complexity: O(1)
        """
        node = SingleNode(value)
        if self._size == 0:
            self._append_to_empty(node)
        else:
            node.next = self._head
            self._tail.next = node  # type: ignore[union-attr]
            self._head = node
        self._size += 1

    def insert(self, index: int, value: Any) -> None:
        """
        Inserts a new node with given value at given index.
        Supports negative indexing. Allows index == size (insert at end).

        Time complexity: O(n)

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
        node = SingleNode(value)
        prev = self._get_node(index - 1)
        node.next = prev.next
        prev.next = node
        self._size += 1

    def remove(self, index: int) -> Any:
        """
        Removes and returns the value of the node at given index.
        Maintains circular invariant after removal.
        Supports negative indexing.

        Time complexity: O(n)

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range or list is empty.
        """
        if self._size == 0:
            raise IndexError("Remove from an empty list")
        index = validate_index(index, self._size)

        if self._size == 1:
            value = self._head.value  # type: ignore[union-attr]
            self._head = None
            self._tail = None
            self._size -= 1
            return value

        if index == 0:
            value = self._head.value  # type: ignore[union-attr]
            self._head = self._head.next  # type: ignore[union-attr]
            self._tail.next = self._head  # type: ignore[union-attr]
            self._size -= 1
            return value

        prev = self._get_node(index - 1)
        target = prev.next
        value = target.value  # type: ignore[union-attr]
        prev.next = target.next  # type: ignore[union-attr]
        if index == self._size - 1:
            self._tail = prev
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

    def copy(self) -> "CircularSinglyLinkedList":
        """
        Returns a shallow copy of the list preserving order.

        Time complexity: O(n)
        """
        return CircularSinglyLinkedList(*self)

    # -------------------------------------------------------------------------
    # Dunder methods

    def __getitem__(self, index: int) -> Any:
        """
        Returns the value of the node at given index. Supports negative indexing.

        Time complexity: O(n)

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range.
        """
        return self._get_node(index).value

    def __setitem__(self, index: int, value: Any) -> None:
        """
        Sets the value of the node at given index. Supports negative indexing.

        Time complexity: O(n)

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
        Yields values from tail to head.
        Builds a temporary reversed SingleNode chain, then traverses it.

        Time complexity: O(n)
        """
        temp_head: Optional[SingleNode] = None
        current = self._head
        for _ in range(self._size):
            temp = SingleNode(current.value)  # type: ignore[union-attr]
            temp.next = temp_head
            temp_head = temp
            current = current.next  # type: ignore[union-attr]
        current = temp_head
        while current is not None:
            yield current.value
            current = current.next

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
        Format: CircularSinglyLinkedList(size=3)[1 -> 2 -> 3 -> ...]

        Time complexity: O(n)
        """
        elements = " -> ".join(repr(v) for v in self)
        tail = " -> ..." if self._size > 0 else ""
        return f"CircularSinglyLinkedList(size={self._size})[{elements}{tail}]"
