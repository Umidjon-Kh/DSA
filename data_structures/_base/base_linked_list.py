from abc import abstractmethod
from typing import Any

from .base_collection import BaseCollection


class BaseLinkedList(BaseCollection):
    """
    Abstract base class for all linked list types.

    Defines the shared interface for singly, doubly, and circular linked lists.
    Extends BaseCollection with positional access and mutation methods.

    Required to implement (in addition to BaseCollection):
        append, prepend, insert, remove, index, __getitem__, __setitem__
    """

    @abstractmethod
    def append(self, value: Any) -> None:
        """
        Appends a new node with given value to the end of the list.

        Time complexity: O(1)
        """
        ...

    @abstractmethod
    def prepend(self, value: Any) -> None:
        """
        Prepends a new node with given value to the front of the list.

        Time complexity: O(1)
        """
        ...

    @abstractmethod
    def insert(self, index: int, value: Any) -> None:
        """
        Inserts a new node with given value at given index.
        Supports negative indexing. Allows index == size (insert at end).

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range.
        """
        ...

    @abstractmethod
    def remove(self, index: int) -> Any:
        """
        Removes and returns the value of the node at given index.
        Supports negative indexing.

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range or list is empty.
        """
        ...

    @abstractmethod
    def index(self, value: Any) -> int:
        """
        Returns the index of the first node whose value equals given value.

        Raises:
            ValueError: If value is not found in the list.
        """
        ...

    @abstractmethod
    def __getitem__(self, index: int) -> Any:
        """
        Returns the value of the node at given index. Supports negative indexing.

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range.
        """
        ...

    @abstractmethod
    def __setitem__(self, index: int, value: Any) -> None:
        """
        Sets the value of the node at given index. Supports negative indexing.

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range.
        """
        ...
