from typing import Any, Optional


class DoubleNode:
    """
    A double node for use in doubly linked data structures.

    Stores a value and references to both next and previous nodes.
    Used by: DoublyLinkedList, CircularDoublyLinkedList,
             NodeDeque, etc.

    Time complexity:
        __init__:  O(1)
        __repr__:  O(1)
    """

    __slots__ = ("value", "next", "prev")

    def __init__(self, value: Any) -> None:
        """
        Creates a node with given value and no next/prev references.

        Args:
            value: Any value to store in this node.

        Examples:
            node = DoubleNode(42)
            node = DoubleNode("hello")
        """
        self.value: Any = value
        self.next: Optional["DoubleNode"] = None
        self.prev: Optional["DoubleNode"] = None

    def __repr__(self) -> str:
        """
        Returns a string representation of the node.
        Format: 10 <-> DoubleNode(42) <-> 99
                None <-> DoubleNode(42) <-> None

        Time complexity: O(1)
        """
        prev_val = self.prev.value if self.prev is not None else None
        next_val = self.next.value if self.next is not None else None
        return f"{prev_val!r} <-> DoubleNode({self.value!r}) <-> {next_val!r}"
