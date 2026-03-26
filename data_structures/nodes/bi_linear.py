from typing import Any, Optional

from .._base import BaseNode


class BiLinearNode(BaseNode):
    """
    A BiLinearNode for use in doubly linked data structures.

    Stores a value and references to next and previous nodes.
    Used by:
        DoublyLinkedList, CircularDoublyLinkedList,
        NodeDeque and other structures that need to know about both references.
    """

    __slots__ = ("next", "prev")

    def __init__(self, value) -> None:
        """
        Creates a node with given value and no next/prev references.

        Args:
            value: Any value to store in this node.
        Examples:
            node = BiLinearNode(23)
            node = BiLinearNode("hi")
        """
        super().__init__(value)
        self.next: Optional["BiLinearNode"] = None
        self.prev: Optional["BiLinearNode"] = None

    def __repr__(self) -> str:
        """
        Returns a string representation of the node.
        Format:
            10 <-> BiLinearNode(23) <-> 99
            None <-> BiLinearNode("hi") <-> None
        """
        prev_val = self.prev.value if self.prev is not None else None
        next_val = self.next.value if self.next is not None else None
        return f"{prev_val!r} <-> BiLinearNode({self.value!r}) <-> {next_val!r}"
