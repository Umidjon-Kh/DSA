from abc import abstractmethod
from typing import Any

from .base_collection import BaseCollection


class BaseTree(BaseCollection):
    """
    Abstract base class for all tree types.

    Defines the shared interface for binary trees, BSTs, and AVL trees.
    Trees are hierarchical structures — iteration order is inorder by default.

    Note: __reversed__ yields inorder traversal in reverse (right → root → left).

    Required to implement (in addition to BaseCollection):
        insert, search, delete, height
    """

    @abstractmethod
    def insert(self, value: Any) -> None:
        """
        Inserts value into the tree following the structure's rules.

        Time complexity: O(log n) average — O(n) worst case for unbalanced trees.

        Raises:
            TypeError: If value is not comparable with existing elements.
        """
        ...

    @abstractmethod
    def search(self, value: Any) -> bool:
        """
        Returns True if value exists in the tree.

        Time complexity: O(log n) average — O(n) worst case for unbalanced trees.
        """
        ...

    @abstractmethod
    def delete(self, value: Any) -> None:
        """
        Removes value from the tree.

        Time complexity: O(log n) average — O(n) worst case for unbalanced trees.

        Raises:
            ValueError: If value is not found in the tree.
        """
        ...

    @abstractmethod
    def height(self) -> int:
        """
        Returns the height of the tree.
        An empty tree has height 0. A tree with one node has height 1.

        Time complexity: O(n)
        """
        ...
