from typing import Any, Iterator, Optional

from ..tools import validate_index, validate_insert_index
from ._nodes import SingleNode


class SinglyLinkedList:
    """
    A singly linked list where each node knows only its next neighbor.
    Maintains references to head and tail for O(1) append.

    Time complexity:
        append:         O(1)
        prepend:        O(1)
        insert:         O(n)
        remove_head:    O(1)
        remove_tail:    O(n) — must traverse to find node before tail
        remove:         O(n)
        find:           O(n)
        get_node:       O(n)
        set_node:       O(n)
        __len__:        O(1)
        __iter__:       O(n)
        __contains__:   O(n)
    """

    __slots__ = ("_head", "_tail", "_size")

    def __init__(self, *args) -> None:
        """
        Creates a singly linked list with optional initial values.

        Args:
            *args: Optional initial values, appended left to right.

        Examples:
            lst = SinglyLinkedList()           # empty
            lst = SinglyLinkedList(1, 2, 3)    # [1 -> 2 -> 3 -> None]
        """
        self._head: Optional[SingleNode] = None
        self._tail: Optional[SingleNode] = None
        self._size: int = 0
        for item in args:
            self.append(item)

    def append(self, value: Any) -> None:
        """
        Inserts a new node with given value at the end of the list.
        If list is empty — new node becomes both head and tail.
        """
        new_node = SingleNode(value)
        if self._tail is None:
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1

    def prepend(self, value: Any) -> None:
        """
        Inserts a new node with given value at the beginning of the list.
        New node becomes head. If list is empty — also becomes tail.
        """
        new_node = SingleNode(value)
        if self._head is None:
            self._head = new_node
            self._tail = new_node
        else:
            new_node.next = self._head
            self._head = new_node
        self._size += 1

    def get_node(self, index: Any) -> SingleNode:
        """
        Traverses the list and returns the node at given index.
        Supports negative indexing.

        Time complexity: O(n)

        Returns:
            SingleNode at given index.

        Raises:
            TypeError:  if index is not int.
            IndexError: if index is out of range.
        """
        index = validate_index(index, self._size)
        current = self._head
        for _ in range(index):
            current = current.next  # type: ignore[union-attr]
        return current  # type: ignore[union-attr]

    def set_node(self, index: Any, value: Any) -> None:
        """
        Replaces value of existing node at given index.
        If index == size — creates a new node and appends it to the end.
        Supports negative indexing (only for existing indices).

        Time complexity: O(n)

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

        Time complexity: O(n)

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
        new_node = SingleNode(value)
        prev = self.get_node(index - 1)
        new_node.next = prev.next
        prev.next = new_node
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
        self._size -= 1
        return value

    def remove_tail(self) -> Any:
        """
        Removes and returns the value of the tail node.
        Must traverse the list to find the node before tail.
        If list becomes empty — head is also set to None.

        Raises:
            IndexError: if list is empty.
        """
        if self._head is None:
            raise IndexError("Remove from empty list")
        if self._head is self._tail:
            value = self._head.value
            self._head = None
            self._tail = None
            self._size -= 1
            return value
        prev = self.get_node(self._size - 2)
        value = self._tail.value  # type: ignore[union-attr]
        prev.next = None
        self._tail = prev
        self._size -= 1
        return value

    def remove(self, index: Any) -> Any:
        """
        Removes and returns the value of the node at given index.
        Index 0 — same as remove_head.
        Index == size - 1 — same as remove_tail.

        Time complexity: O(n)

        Raises:
            TypeError:  if index is not int.
            IndexError: if index is out of range.
        """
        index = validate_index(index, self._size)
        if index == 0:
            return self.remove_head()
        if index == self._size - 1:
            return self.remove_tail()
        prev = self.get_node(index - 1)
        node = prev.next
        prev.next = node.next  # type: ignore[union-attr]
        self._size -= 1
        return node.value  # type: ignore[union-attr]

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

    def __contains__(self, value: Any) -> bool:
        """Returns True if any node in the list holds the given value."""
        return self.find(value) != -1

    def __repr__(self) -> str:
        """
        Returns a string representation of the list.
        Example: SinglyLinkedList([1 -> 2 -> 3 -> None])
        """
        nodes = []
        current = self._head
        while current is not None:
            nodes.append(repr(current.value))
            current = current.next
        nodes.append("None")
        return f"SinglyLinkedList([{' -> '.join(nodes)}])"
