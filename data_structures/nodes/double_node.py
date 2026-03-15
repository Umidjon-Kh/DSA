from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass(slots=True)
class DoubleNode:
    """
    A node for Double Linked List based structures.
    Knows about previous and next object.
    Used in: Dequeue, DoubleLinked List
    """

    _value: Any
    _next: Optional['DoubleNode'] = field(init=False, default=None)
    _prev: Optional['DoubleNode'] = field(init=False, default=None)

    @property
    def value(self) -> Any:
        """Returns the value stored in this node"""
        return self._value

    @property
    def next(self) -> Optional['DoubleNode']:
        """Returns the next node in the chain"""
        return self._next

    @next.setter
    def next(self, node: Optional['DoubleNode']) -> None:
        """Sets the nex node in the chain"""
        self._next = node

    @property
    def prev(self) -> Optional['DoubleNode']:
        """Retunrs the previous node in the chain"""
        return self._prev

    @prev.setter
    def prev(self, node: Optional['DoubleNode']) -> None:
        """Sets the previous node in the chain"""
        self._prev = node
