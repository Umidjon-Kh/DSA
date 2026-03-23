from typing import Any, Optional


class SingleNode:
    """
    A single node for use in singly linked data structures.

    Stores a value and a reference to the next node only.
    Used by: SinglyLinkedList, CircularSinglyLinkedList,
             DynamicNodeStack, NodeQueue, etc.

    Time complexity:
        __init__:  O(1)
        __repr__:  O(1)
    """

    __slots__ = ("value", "next")

    def __init__(self, value: Any) -> None:
        """
        Creates a node with given value and no next reference.

        Args:
            value: Any value to store in this node.

        Examples:
            node = SingleNode(42)
            node = SingleNode("hello")
        """
        self.value: Any = value
        self.next: Optional["SingleNode"] = None

    def __repr__(self) -> str:
        """
        Returns a string representation of the node.
        Format: SingleNode(42) -> 10
                SingleNode(42) -> None

        Time complexity: O(1)
        """
        next_val = self.next.value if self.next is not None else None
        return f"SingleNode({self.value!r}) -> {next_val!r}"
