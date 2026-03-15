from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass(slots=True)
class SingleNode:
    """
    A node for Singly Linked List based structures.
    Knows only the next node, not the previous one.
    Used in: Stack, SimpleQueue, CircularQueue
    """

    _value: Any
    _next: Optional['SingleNode'] = field(init=False, default=None)

    @property
    def value(self) -> Any:
        """Returns the value stored in this node."""
        return self._value

    @property
    def next(self) -> Optional['SingleNode']:
        """Returns the next node in the chain."""
        return self._next

    @next.setter
    def next(self, node: Optional['SingleNode']) -> None:
        """Sets the next node in the chain."""
        self._next = node
