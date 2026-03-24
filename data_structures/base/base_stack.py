from abc import abstractmethod
from typing import Any

from .base_collection import BaseCollection


class BaseStack(BaseCollection):
    """
    Abstract base class for all stack types.

    Defines the LIFO (Last In, First Out) interface.
    Both array-based and node-based stacks inherit from this.

    Subclass:
        BaseBoundedStack — adds capacity tracking and is_full check
                           for fixed-size stack implementations

    Required to implement (in addition to BaseCollection):
        push, pop, peek, is_empty
    """

    @abstractmethod
    def push(self, value: Any) -> None:
        """
        Pushes value onto the top of the stack.

        Raises:
            OverflowError: If the stack is full (bounded stacks only).
            TypeError:     If value type does not match dtype (typed stacks only).
        """
        ...

    @abstractmethod
    def pop(self) -> Any:
        """
        Removes and returns the top element.

        Raises:
            IndexError: If the stack is empty.
        """
        ...

    @abstractmethod
    def peek(self) -> Any:
        """
        Returns the top element without removing it.

        Raises:
            IndexError: If the stack is empty.
        """
        ...

    @abstractmethod
    def is_empty(self) -> bool:
        """Returns True if the stack contains no elements."""
        ...


class BaseBoundedStack(BaseStack):
    """
    Abstract base class for fixed-capacity stacks.

    Extends BaseStack with capacity tracking and a fullness check.
    Used by array-based static stack implementations.

    Required to implement (in addition to BaseStack):
        is_full, capacity (property)
    """

    @property
    @abstractmethod
    def capacity(self) -> int:
        """Returns the fixed maximum number of elements the stack can hold."""
        ...

    @abstractmethod
    def is_full(self) -> bool:
        """Returns True if size == capacity."""
        ...
