from typing import Any, Optional

from .._base import BaseNode


class LinearNode(BaseNode):
    """
    A Linear node for use in singly linked data structures.
    stores a value and reference to the next node only.
    Used by structures like:
        SinglyLinkedList, CircularSinglyLinkedList,
        DynamicNodeStack, NodeQueue and other simple node based structures.
    """

    __slots__ = ("next",)

    def __init__(self, value) -> None:
        """
        Creates a node with given value and no next reference.

        Args:
            value: Any value to store in this node.

        Examples:
            node = LinearNode(42)
            node = LinearNode("hello")
        """
        self.value: Any = value
        self.next: Optional["LinearNode"] = None

    def __repr__(self) -> str:
        """
        Returns a string representation of the node.
        Format:
            LinearNode(42) -> 10
            LinearNode(42) -> None
        """
        next_val = self.next.value if self.next is not None else None
        return f"LinearNode({self.value}) -> {next_val!r}"
