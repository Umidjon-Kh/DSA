from typing import Any, Generator, Optional

from ..nodes import DoubleNode
from ..tools import validate_index, validate_insert_index


class CircularDoublyLinkedList:
    """
    A circular doubly linked lsit where the tail node's next
    points back to head instead of None and head node's prev points
    to tail instead of None too.
    Build on top of DoubleNode.

    Useful for round-robin scheduling, cyclic buffers,
    and any problem requiring continuous looping over elements.

    Key difference from from CircularSinglyLinkedList:
        head.prev = tail (always, never None)
        Other things are similar to CircularSinglyLinkedList but nodes know
        their previes nodes in the chain.

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
        __contains__:   O(n)
    """

    __slots__ = ("_head", "_tail", "_size")

    def __init__(self, *args) -> None:
        """
        Creates a doubly linked list with optional initial values.

        Args:
            *args: Optional initial values, appended left to right

        Examples:
            lst = CircularDoublyLinkedList()        # empty
            lst = CincularDoublyLinkedList(1, 2, 3)
                    # [tail(3) -><- head(1) -><- 2 -><- tail(3) -><- head(1)]
        """
        self._head: Optional[DoubleNode] = None
        self._tail: Optional[DoubleNode] = None
        self._size = 0
        for item in args:
            self.append(item)

    def append(self, value: Any) -> None:
        """
        Inserts a new node at the end of the list.
        New node's next is set to head and head node's prev set to tail(new_node)
        to maintain circular structure.
        If list is empty - node points to itself
        """
        new_node = DoubleNode(value)
        if self._tail is None:
            self._head = new_node
            self._tail = new_node
            self._tail.next = self._head
            self._head.prev = self._tail
        else:
            new_node.prev = self._tail
            self._tail.next = new_node
            self._tail = new_node
            self._tail.next = self._head
            self._head.prev = self._tail  # type: ignore[union-attr]
        self._size += 1

    def prepend(self, value: Any) -> None:
        """
        Inserts a new node at the beggining of the list.
        New node becomes head. Tail's next is updated to point to new head
        and new head's prev is updated to point to tail.
        If list is empty - node poinst to itself
        """
        new_node = DoubleNode(value)
        if self._head is None:
            self._head = new_node
            self._tail = new_node
            self._tail.next = self._head
            self._head.prev = self._tail
        else:
            new_node.next = self._head
            new_node.prev = self._tail
            self._head.prev = new_node
            self._head = new_node
            self._tail.next = self._head  # type: ignore[union-attr]
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
        node._value = value  # type: ignore[attr-defined]

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
        next_node.prev = new_node  # type: ignore[union-attr]
        self._size += 1

    def remove_head(self) -> Any:
        """
        Removes and returns the value of the head node.
        Tail's next is updated to point to new head and
        new head's prev is updated to point to tail.
        If list becomes empty - head and tail are set to None.

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
            self._tail.next = self._head  # type: ignore[union-attrs]
            self._head.prev = self._tail  # type: ignore[union-attrs]
        self._size -= 1
        return value

    def remove_tail(self) -> Any:
        """
        Removes and returns the value of the tail node.
        Dont need to traverse to find node before tail cause
        tail knows about previous node. That node becomes new tail and its next
        is set to head and updates head's node prev to point to new tail.
        If list becomes empty - head abd tail are set to None.

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
        value = self._tail.value  # type: ignore[union-attr]
        self._tail = self._tail.prev  # type: ignore[union-attr]
        self._tail.next = self._head  # type: ignore[union-attr]
        self._head.prev = self._tail
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

    def copy(self) -> "CircularDoublyLinkedList":
        """
        Creates a shallow copy of Linked List.
        Time complexity: O(n).
        """
        copied = CircularDoublyLinkedList(*self)
        return copied

    def __eq__(self, other: object) -> bool:
        """Checks for equality of all nodes vales in both objects"""
        if not isinstance(other, CircularDoublyLinkedList):
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

    def __reversed__(self) -> Generator[Any, None, None]:
        """Iterates over values of all nodes from tail to head."""
        current = self._tail
        # Why not True: Cause if i write True instead of is not None
        # And if tail is None it raises AttributeError
        while current is not None:
            yield current.value
            if current is self._head:
                break
            current = current.prev

    def __contains__(self, value: Any) -> bool:
        """Returns True if any node in the list holds the given value."""
        return self.find(value) != -1

    def __repr__(self) -> str:
        """
        Returns a string representation of the list.
        Example: CircularDoublyLinkedList([None -><- 1 -><- 2 -><- 3 -><- None])
        """
        nodes = ["(points to tail)"]
        current = self._head
        while current is not None:
            nodes.append(repr(current.value))
            if current is self._tail:
                break
            current = current.next
        nodes.append("(back to head)")
        return f"CircularDoublyLinkedList([{' -><- '.join(nodes)}])"
