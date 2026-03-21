from typing import Any, Generator, Optional

from ..nodes import SingleNode
from ..tools import validate_index, validate_insert_index


class CircularSinglyLinkedList:
    """
    A circular singly linked list where the tail node's next
    points back to head instead of None.
    Built on top of SingleNode.

    Useful for round-robin scheduling, cyclic buffers,
    and any problem requiring continuous looping over elements.

    Key difference from SinglyLinkedList:
        tail.next = head  (always, never None)
        __iter__ must stop at head, not at None — otherwise infinite loop

    Time complexity:
        append:         O(1)
        prepend:        O(1)
        insert:         O(n)
        remove_head:    O(1)
        remove_tail:    O(n)
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
            *args: Optional initial values, appended left to right

        Examples:
            lst = CircularSinglyLinkedList()        # empty
            lst = CircularSinglyLinkedList(1, 2, 3)
                                # [head(1) -> 2 -> tail(3) -> head(1)]
        """
        self._head: Optional[SingleNode] = None
        self._tail: Optional[SingleNode] = None
        self._size = 0
        for item in args:
            self.append(item)

    def append(self, value: Any) -> None:
        """
        Inserts a new node at the end of the list.
        New node's next is set to head to maintain circular structure.
        If list is empty — node points to itself.
        """
        new_node = SingleNode(value)
        if self._tail is None:
            self._head = new_node
            self._tail = new_node
            self._tail.next = self._head
        else:
            self._tail.next = new_node
            self._tail = new_node
            self._tail.next = self._head
        self._size += 1

    def prepend(self, value: Any) -> None:
        """
        Inserts a new node at the beginning of the list.
        New node becomes head. Tail's next is updated to point to new head.
        If list is empty — node points to itself.
        """
        new_node = SingleNode(value)
        if self._head is None:
            self._head = new_node
            self._tail = new_node
            self._tail.next = self._head
        else:
            new_node.next = self._head
            self._head = new_node
            self._tail.next = self._head  # type: ignore[union-attr]

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
        Tail's next is updated to point to new head.
        If list becomes empty — head and tail are set to None.

        Raises:
            IndexError: if list is empty.
        """
        if self._head is None:
            raise IndexError("Remove from empty list")
        value = self._head.value
        if self._head is self._tail:
            self._head = None
            self._tail = None
        else:
            self._head = self._head.next
            self._tail.next = self._head  # type: ignore[union attrs]
        self._size -= 1
        return value

    def remove_tail(self) -> Any:
        """
        Removes and returns the value of the tail node.
        Must traverse to find the node before tail.
        That node becomes new tail and its next is set to head.
        If list becomes empty — head and tail are set to None.

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
        self._tail.next = self._head
        self._size -= 1
        return value

    def remove(self, index: Any) -> Any:
        """
        Removes and returns the value of the node at given index.
        Must maintain circular structure after removal.

        Raises:
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
        # Why not True: Cause if i write True instead of is not None
        # And if head is None it raises AttributeError
        while current is not None:
            if current.value == value:
                return index
            if current is self._tail:
                return -1
            current = current.next
            index += 1
        return -1

    def copy(self) -> "CircularSinglyLinkedList":
        """
        Creates a shallow copy of Linked List.
        Time complexity: O(n).
        """
        copied = CircularSinglyLinkedList(*self)
        return copied

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CircularSinglyLinkedList):
            return False
        # Checking length for quick result if not equal
        if len(self) != len(other):
            return False
        # If both empty return True
        if self._size == 0:
            return True
        # Traversing all nodes to check values for equality
        return list(self) == list(other)

    def __len__(self) -> int:
        """Returns the number of nodes in the list."""
        return self._size

    def __iter__(self) -> Generator[Any, None, None]:
        """Iterates over values of all nodes from head to tail."""
        current = self._head
        # Why not True: Cause if i write True instead of is not None
        # And if head is None it raises AttributeError
        while current is not None:
            yield current.value
            if current is self._tail:
                break
            current = current.next

    def __contains__(self, value: Any) -> bool:
        """Returns True if any node in the list holds the given value."""
        return self.find(value) != -1

    def __repr__(self) -> str:
        """
        Returns a string representation of the list.
        Example: CircularSinglyLinkedList([1 -> 2 -> 3 -> None])
        """
        nodes = []
        current = self._head
        # Why not True: Cause if i write True instead of is not None
        # And if head is None it raises AttributeError
        while current is not None:
            nodes.append(repr(current.value))
            if current is self._tail:
                break
            current = current.next
        nodes.append("(back to head)")
        return f"CircularSinglyLinkedList([{' -> '.join(nodes)}])"
