from typing import Any, Optional

from .._base import BaseNode


class TreeNode(BaseNode):
    """
    A Tree node for use in binary tree based data structures.
    Stores a value and references to left, right children and parent and
    height for structures that need to know about height for Balance Factor.

    Used by structures like:
        BinaryTree, BinarySearchTree, AVLTree, RedBlackTree and other tree based structures.
    """

    __slots__ = ("left", "right", "parent", "height")

    def __init__(self, value: Any) -> None:
        """
        Creates a node with given value and no child/parent references.

        Args:
            value: Any value to store in this node.

        Examples:
            node = TreeNode(10)
            node = TreeNode("root")
        """
        super().__init__(value)
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None
        self.parent: Optional["TreeNode"] = None
        self.height: int = 0

    def __repr__(self) -> str:
        """
        Returns a string representation of the node.
        Format:
            TreeNode(10) -> (L: 5, R: 15, P: None)
            TreeNode(5)  -> (L: None, R: None, P: 10)
        """
        left_val = self.left.value if self.left is not None else None
        right_val = self.right.value if self.right is not None else None
        parent_val = self.parent.value if self.parent is not None else None

        return f"TreeNode({self.value}) -> (L: {left_val!r}, R: {right_val!r}, P: {parent_val!r})"
