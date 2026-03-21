from typing import Any, Iterator, Optional

from ..nodes import DoubleNode
from ..tools import validate_index, validate_insert_index


class DoublyLinkedList:
    """
    A doubly linked list where each node knows both its next and previous neighbor.
    Maintains references to head and tail.
    Supports traversal in both directions.

    Compared to SinglyLinkedList:
        remove_tail:  O(1) — tail.prev gives direct access to previous node
        __reversed__: O(n) — can traverse backwards

    Time complexity:
        append:         O(1)
        prepend:        O(1)
        insert:         O(n/2)
        remove_head:    O(1)
        remove_tail:    O(1)
        remove:         O(n/2)
        find:           O(n)
        get_node:       O(n) — O(n/2) due to bidirectional traversal
        set_node:       O(n/2)
        __len__:        O(1)
        __iter__:       O(n)
        __reversed__:   O(n)
        __contains__:   O(n)
    """

    __slots__ = ("_head", "_tail", "_size")

    def __init__(self, *args) -> None:
        """
        Creates a doubly linked list with optional initial values.

        Args:
            *args: Optional initial values, appended left to right.

        Examples:
            lst = DoublyLinkedList()           # empty
            lst = DoublyLinkedList(1, 2, 3)    # [None -><- 1 -><- 2 -><- 3 -><- None]
        """
        self._head: Optional[DoubleNode] = None
        self._tail: Optional[DoubleNode] = None
        self._size: int = 0
        for item in args:
            self.append(item)

    def append(self, value: Any) -> None:
        """
        Inserts a new node with given value at the end of the list.
        If list is empty — new node becomes both head and tail.
        """
        new_node = DoubleNode(value)
        if self._tail is None:
            self._head = new_node
            self._tail = new_node
        else:
            new_node.prev = self._tail
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1

    def prepend(self, value: Any) -> None:
        """
        Inserts a new node with given value at the beginning of the list.
        New node becomes head. If list is empty — also becomes tail.
        """
        new_node = DoubleNode(value)
        if self._head is None:
            self._head = new_node
            self._tail = new_node
        else:
            self._head.prev = new_node
            new_node.next = self._head
            self._head = new_node
        self._size += 1

    def get_node(self, index: Any) -> DoubleNode:
        """
        Traverses the list and returns the node at given index.
        Supports negative indexing.
        If index is in the second half — traverses backwards from tail.

        Time complexity: O(n/2)

        Returns:
            DoubleNode at given index.

        Raises:
            TypeError:  if index is not int.
            IndexError: if index is out of range.
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
        return current  # type: ignore[return-value]

    def set_node(self, index: Any, value: Any) -> None:
        """
        Replaces value of existing node at given index.
        If index == size — creates a new node and appends it to the end.
        Supports negative indexing (only for existing indices).

        Time complexity: O(n/2)

        Raises:
            TypeError:  if index is not int.
            IndexError: if index is out of range.
        """
        index = validate_insert_index(index, self._size)
        if index == self._size:
            self.append(value)
            return
        node = self.get_node(index)
        node.value = value  # type: ignore[attr-defined]

    def insert(self, index: Any, value: Any) -> None:
        """
        Inserts a new node with given value at the given index.
        Shifts all subsequent nodes forward.
        Index 0 — same as prepend.
        Index == size — same as append.

        Time complexity: O(n/2)

        Raises:
            TypeError:  if index is not int.
            IndexError: if index is out of range.
        """
        index = validate_insert_index(index, self._size)
        if index == 0:
            self.prepend(value)
            return
        if index == self._size:
            self.append(value)
            return
        new_node = DoubleNode(value)
        prev = self.get_node(index - 1)
        next_node = prev.next
        new_node.next = next_node
        new_node.prev = prev
        prev.next = new_node
        if next_node is not None:
            next_node.prev = new_node
        self._size += 1

    def remove_head(self) -> Any:
        """
        Removes and returns the value of the head node.
        Next node becomes the new head.
        If list becomes empty — tail is also set to None.

        Raises:
            IndexError: if list is empty.
        """
        if self._head is None:
            raise IndexError("Remove from empty list")
        value = self._head.value
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        else:
            self._head.prev = None
        self._size -= 1
        return value

    def remove_tail(self) -> Any:
        """
        Removes and returns the value of the tail node.
        Uses tail.prev for O(1) access — no traversal needed.
        If list becomes empty — head is also set to None.

        Raises:
            IndexError: if list is empty.
        """
        if self._tail is None:
            raise IndexError("Remove from empty list")
        value = self._tail.value
        self._tail = self._tail.prev
        if self._tail is None:
            self._head = None
        else:
            self._tail.next = None
        self._size -= 1
        return value

    def remove(self, index: Any) -> Any:
        """
        Removes and returns the value of the node at given index.
        Index 0 — same as remove_head.
        Index == size - 1 — same as remove_tail.

        Time complexity: O(n/2)

        Raises:
            TypeError:  if index is not int.
            IndexError: if index is out of range.
        """
        index = validate_index(index, self._size)
        if index == 0:
            return self.remove_head()
        if index == self._size - 1:
            return self.remove_tail()
        node = self.get_node(index)
        node.prev.next = node.next  # type: ignore[union-attr]
        node.next.prev = node.prev  # type: ignore[union-attr]
        self._size -= 1
        return node.value

    def find(self, value: Any) -> int:
        """
        Returns the index of the first node with given value.
        Returns -1 if value is not found.

        Time complexity: O(n)
        """
        current = self._head
        index = 0
        while current is not None:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return -1

    def __len__(self) -> int:
        """Returns the number of nodes in the list."""
        return self._size

    def __iter__(self) -> Iterator[Any]:
        """Iterates over values of all nodes from head to tail."""
        current = self._head
        while current is not None:
            yield current.value
            current = current.next

    def __reversed__(self) -> Iterator[Any]:
        """Iterates over values of all nodes from tail to head."""
        current = self._tail
        while current is not None:
            yield current.value
            current = current.prev

    def __contains__(self, value: Any) -> bool:
        """Returns True if any node in the list holds the given value."""
        return self.find(value) != -1

    def __repr__(self) -> str:
        """
        Returns a string representation of the list.
        Example: DoublyLinkedList([None -><- 1 -><- 2 -><- 3 -><- None])
        """
        nodes = ["None"]
        current = self._head
        while current is not None:
            nodes.append(repr(current.value))
            current = current.next
        nodes.append("None")
        return f"DoublyLinkedList([{' -><- '.join(nodes)}])"
