from typing import Any, Optional


class DoubleNode:
    """
    A node for Double Linked List based structures.
    Knows about previous and next object.
    """

    __slots__ = ("_value", "_next", "_prev")

    def __init__(self, value: Any) -> None:
        self._value = value
        self._next: Optional["DoubleNode"] = None
        self._prev: Optional["DoubleNode"] = None

    @property
    def value(self) -> Any:
        """Returns the value stored in this node"""
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        """Sets value for node"""
        self._value = value

    @property
    def prev(self) -> Optional["DoubleNode"]:
        """Returns the previous node in the chain"""
        return self._prev

    @prev.setter
    def prev(self, value: Optional["DoubleNode"]) -> None:
        """Sets the previous node in the chain"""
        self._prev = value

    @property
    def next(self) -> Optional["DoubleNode"]:
        """Returns the next node in the chain"""
        return self._next

    @next.setter
    def next(self, value: Optional["DoubleNode"]) -> None:
        """Sets the next node in the chain"""
        self._next = value

    def __eq__(self, other: object) -> bool:
        """Returns True if both nodes are same object or have same attr values."""
        if not isinstance(other, DoubleNode):
            return False
        return self._value == other._value
