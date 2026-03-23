from typing import Any, Iterator, Optional

from ...nodes import SingleNode
from ...tools import validate_index, validate_insert_index


class SinglyLinkedList:
    """
    A singly linked list backed by SingleNode.
    Each node holds a value and a reference to the next node only.

    Supports O(1) prepend/append and O(n) insert/remove/find.
    Traversal is forward-only — reversed() builds a temporary reversed chain.

    Time complexity:
        append:       O(1)
        prepend:      O(1)
        insert:       O(n)
        remove:       O(n)
        find:         O(n)
        __getitem__:  O(n)
        __setitem__:  O(n)
        __len__:      O(1)
        __iter__:     O(n)
        __reversed__: O(n*2) — builds a temp reversed chain, then traverses it
        __contains__: O(n)
        __repr__:     O(n)
    """

    __slots__ = ("_head", "_tail", "_size")

    def __init__(self, *args) -> None:
        """
        Creates a singly linked list with optional initial values.

        Args:
            *args: Optional initial values, appended in order.

        Examples:
            lst = SinglyLinkedList()           # empty
            lst = SinglyLinkedList(1, 2, 3)    # 1 -> 2 -> 3
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
        Used by append, prepend, and insert to avoid duplicating this logic.

        Time complexity: O(1)
        """
        self._head = node
        self._tail = node

    # -------------------------------------------------------------------------
    # Core operations

    def append(self, value: Any) -> None:
        """
        Appends a new node with given value to the end of the list.

        Time complexity: O(1)
        """
        node = SingleNode(value)
        if self._size == 0:
            self._append_to_empty(node)
        else:
            self._tail.next = node  # type: ignore[union-attr]
            self._tail = node
        self._size += 1

    def prepend(self, value: Any) -> None:
        """
        Prepends a new node with given value to the front of the list.

        Time complexity: O(1)
        """
        node = SingleNode(value)
        if self._size == 0:
            self._append_to_empty(node)
        else:
            node.next = self._head
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
        Supports negative indexing.

        Time complexity: O(n)

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range or list is empty.
        """
        if self._size == 0:
            raise IndexError("Remove from an empty list")
        index = validate_index(index, self._size)

        if index == 0:
            value = self._head.value  # type: ignore[union-attr]
            self._head = self._head.next  # type: ignore[union-attr]
            if self._size == 1:
                self._tail = None
            self._size -= 1
            return value

        prev = self._get_node(index - 1)
        target = prev.next
        value = target.value  # type: ignore[union-attr]
        prev.next = target.next  # type: ignore[union-attr]
        if target.next is None:  # type: ignore[union-attr]
            self._tail = prev
        self._size -= 1
        return value

    def find(self, value: Any) -> int:
        """
        Returns the index of the first node whose value equals given value.
        Returns -1 if no such node exists.

        Time complexity: O(n)
        """
        current = self._head
        for i in range(self._size):
            if current.value == value:  # type: ignore[union-attr]
                return i
            current = current.next  # type: ignore[union-attr]
        return -1

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

    def __iter__(self) -> Iterator[Any]:
        """Yields values from head to tail. O(n)"""
        current = self._head
        while current is not None:
            yield current.value
            current = current.next

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields values from tail to head.
        Builds a temporary reversed SingleNode chain, then traverses it.

        Time complexity: O(n*2)
        """
        temp_head: Optional[SingleNode] = None
        current = self._head
        while current is not None:
            temp = SingleNode(current.value)
            temp.next = temp_head
            temp_head = temp
            current = current.next
        current = temp_head
        while current is not None:
            yield current.value
            current = current.next

    def __contains__(self, value: Any) -> bool:
        """Returns True if any node holds given value. O(n)"""
        return self.find(value) != -1

    def __repr__(self) -> str:
        """
        Returns string representation of the list.
        Format: SinglyLinkedList(size=3)[1 -> 2 -> 3]

        Time complexity: O(n)
        """
        elements = " -> ".join(repr(v) for v in self)
        return f"SinglyLinkedList(size={self._size})[{elements}]"
