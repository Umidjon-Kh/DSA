from typing import Any, Optional


class SingleNode:
    """
    A node for Single Linked List based structures.
    Knows only about next object.
    """

    __slots__ = ("_value", "_next")

    def __init__(self, value: Any) -> None:
        self._value = value
        self._next: Optional["SingleNode"] = None

    @property
    def value(self) -> Any:
        """Returns the value stored in this node"""
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        """Sets the value of node"""
        self._value = value

    @property
    def next(self) -> Optional["SingleNode"]:
        """Returns the next node in the chain"""
        return self._next

    @next.setter
    def next(self, value: Optional["SingleNode"]) -> None:
        """Sets the next node in the chain"""
        self._next = value

    def __eq__(self, other: object) -> bool:
        """Returns True if both nodes are same object or have same attr values."""
        if not isinstance(other, SingleNode):
            return False
        return self._value == other.value
