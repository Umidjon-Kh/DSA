from abc import abstractmethod
from typing import Any, Iterator

from .base_collection import BaseCollection


class BaseTree(BaseCollection):
    """
    Abstract base class for all binary tree types.

    Defines the shared interface for BST, AVL, and other binary tree
    implementations. Extends BaseCollection with tree-specific operations:
    insertion, removal, search, traversals, and structural queries.

    All traversal methods are generators — they yield values lazily.

    Subclasses:
        BST     — unbalanced binary search tree
        AVLTree — self-balancing binary search tree

    Required to implement (in addition to BaseCollection):
        insert, remove, search, min, max, height,
        inorder, preorder, postorder, level_order
    """

    __slots__ = ()

    @abstractmethod
    def insert(self, value: Any) -> None:
        """
        Inserts value into the tree, maintaining BST property.

        Duplicate values are ignored.

        Time complexity: O(log n) average — O(n) worst case for unbalanced trees.

        Raises:
            TypeError: If value is not comparable.
        """
        ...

    @abstractmethod
    def remove(self, value: Any) -> None:
        """
        Removes value from the tree, maintaining BST property.

        If value is not found, does nothing.

        Time complexity: O(log n) average — O(n) worst case for unbalanced trees.
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
    def min(self) -> Any:
        """
        Returns the minimum value in the tree (leftmost node).

        Time complexity: O(log n) average.

        Raises:
            IndexError: If the tree is empty.
        """
        ...

    @abstractmethod
    def max(self) -> Any:
        """
        Returns the maximum value in the tree (rightmost node).

        Time complexity: O(log n) average.

        Raises:
            IndexError: If the tree is empty.
        """
        ...

    @abstractmethod
    def height(self) -> int:
        """
        Returns the height of the tree.

        Height is defined as the number of edges on the longest path
        from root to a leaf. An empty tree has height -1. A single
        node has height 0.

        Time complexity: O(1) for AVL (stored), O(n) for BST (computed).
        """
        ...

    @abstractmethod
    def inorder(self) -> Iterator[Any]:
        """
        Yields values in inorder (left, node, right).

        For a BST this always produces a sorted sequence.

        Time complexity: O(n)
        """
        ...

    @abstractmethod
    def preorder(self) -> Iterator[Any]:
        """
        Yields values in preorder (node, left, right).

        Useful for copying or serializing the tree — root comes first,
        so reinserting in this order reconstructs the same structure.

        Time complexity: O(n)
        """
        ...

    @abstractmethod
    def postorder(self) -> Iterator[Any]:
        """
        Yields values in postorder (left, right, node).

        Useful for deletion or computing subtree sizes — children
        are always processed before their parent.

        Time complexity: O(n)
        """
        ...

    @abstractmethod
    def level_order(self) -> Iterator[Any]:
        """
        Yields values level by level, left to right.

        Uses an internal queue — no recursion.

        Time complexity: O(n)
        """
        ...
