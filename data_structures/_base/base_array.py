from abc import abstractmethod
from typing import Any

from .base_collection import BaseCollection


class BaseArray(BaseCollection):
    """
    Abstract base class for all array types.

    Extends BaseCollection with index-based access.
    Both static (fixed-size) and dynamic (resizable) arrays inherit from this.

    Subclasses:
        BaseStaticArray  — adds capacity property and is_full check
        BaseDynamicArray — adds append, insert, remove

    Required to implement (in addition to BaseCollection):
        __getitem__, __setitem__
    """

    __slots__ = ("_capacity",)

    @abstractmethod
    def __getitem__(self, index: int) -> Any:
        """
        Returns element at given index. Supports negative indexing.

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range.
        """
        ...

    @abstractmethod
    def __setitem__(self, index: int, value: Any) -> None:
        """
        Sets element at given index. Supports negative indexing.

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range.
        """
        ...


class BaseDynamicArray(BaseArray):
    """
    Abstract base class for resizable arrays.

    Extends BaseArray with mutation methods that can grow the buffer.
    The internal buffer resizes automatically when capacity is exceeded.

    Required to implement (in addition to BaseArray):
        append, insert, remove
    """

    @abstractmethod
    def append(self, value: Any) -> None:
        """
        Appends value to the end of the array.
        Triggers a resize if size == capacity.

        Time complexity: O(1) amortized — O(n) on resize

        Raises:
            TypeError: If value type does not match the array's dtype (typed only).
        """
        ...

    @abstractmethod
    def insert(self, index: int, value: Any) -> None:
        """
        Inserts value at given index, shifting elements to the right.
        Supports negative indexing. Allows index == size (insert at end).

        Time complexity: O(n)

        Raises:
            TypeError:  If index is not int, or value type is wrong (typed only).
            IndexError: If index is out of range.
        """
        ...

    @abstractmethod
    def remove(self, index: int) -> Any:
        """
        Removes and returns element at given index, shifting elements left.
        Supports negative indexing.

        Time complexity: O(n)

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range or array is empty.
        """
        ...
