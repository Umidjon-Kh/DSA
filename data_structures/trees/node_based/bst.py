from typing import Any, Iterator, Optional

from ..._base import BaseTree
from ...nodes import TreeNode


class BST(BaseTree):
    """
    An unbalanced binary search tree backed by TreeNode.

    Maintains BST property: for every node, all values in the left
    subtree are smaller and all values in the right subtree are larger.
    Duplicate values are ignored on insert.

    Performance degrades to O(n) for all operations if elements are
    inserted in sorted order — use AVLTree for guaranteed O(log n).

    Time complexity:
        insert:      O(log n) average — O(n) worst case
        remove:      O(log n) average — O(n) worst case
        search:      O(log n) average — O(n) worst case
        min:         O(log n) average — O(n) worst case
        max:         O(log n) average — O(n) worst case
        height:      O(n)
        inorder:     O(n) — yields sorted order
        preorder:    O(n)
        postorder:   O(n)
        level_order: O(n)
        clear:       O(1)
        copy:        O(n log n)
        __len__:     O(1)
        __bool__:    O(1)
        __iter__:    O(n) — inorder
        __reversed__: O(n) — reverse inorder
        __contains__: O(log n) average
        __eq__:      O(n)
        __repr__:    O(n)
    """

    __slots__ = ("_root", "_size")

    def __init__(self, *args) -> None:
        """
        Creates a BST with optional initial values.

        Args:
            *args: Optional initial values, inserted in order.
                   Duplicates are ignored.

        Examples:
            t = BST()              # empty
            t = BST(5, 3, 7, 1)   # root=5
        """
        self._root: Optional[TreeNode] = None
        self._size: int = 0

        for value in args:
            self.insert(value)

    # -------------------------------------------------------------------------
    # Core operations

    def insert(self, value: Any) -> None:
        """
        Inserts value into the tree maintaining BST property.
        Duplicate values are silently ignored.

        Time complexity: O(log n) average — O(n) worst case
        """
        if self._root is None:
            self._root = TreeNode(value)
            self._size += 1
            return

        current = self._root
        while True:
            if value < current.value:
                if current.left is None:
                    current.left = TreeNode(value)
                    current.left.parent = current
                    self._size += 1
                    return
                current = current.left
            elif value > current.value:
                if current.right is None:
                    current.right = TreeNode(value)
                    current.right.parent = current
                    self._size += 1
                    return
                current = current.right
            else:
                return

    def remove(self, value: Any) -> None:
        """
        Removes value from the tree maintaining BST property.
        If value is not found, does nothing.

        Uses inorder successor strategy for nodes with two children.

        Time complexity: O(log n) average — O(n) worst case
        """
        node = self._find_node(value)
        if node is None:
            return

        self._delete_node(node)
        self._size -= 1

    def _find_node(self, value: Any) -> Optional[TreeNode]:
        """
        Returns the node with given value, or None if not found.

        Time complexity: O(log n) average
        """
        current = self._root
        while current is not None:
            if value == current.value:
                return current
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        return None

    def _delete_node(self, node: TreeNode) -> None:
        """
        Removes the given node from the tree, handling all three cases:
            1. Leaf node — simply detach.
            2. One child — replace node with its child.
            3. Two children — replace value with inorder successor,
               then delete the successor.

        Time complexity: O(log n) average
        """
        # case 3 — two children
        if node.left is not None and node.right is not None:
            successor = self._inorder_successor(node)
            node.value = successor.value
            self._delete_node(successor)
            return

        # case 1 and 2 — zero or one child
        child = node.left if node.right is None else node.right

        if node.parent is None:
            self._root = child
            if child is not None:
                child.parent = None
        elif node.parent.left is node:
            node.parent.left = child
            if child is not None:
                child.parent = node.parent
        else:
            node.parent.right = child
            if child is not None:
                child.parent = node.parent

    def _inorder_successor(self, node: TreeNode) -> TreeNode:
        """
        Returns the inorder successor — the smallest node in the
        right subtree of given node.

        Time complexity: O(log n) average
        """
        current = node.right
        while current.left is not None:  # type: ignore[union-attr]
            current = current.left  # type: ignore[union-attr]
        return current  # type: ignore[return-value]

    def search(self, value: Any) -> bool:
        """
        Returns True if value exists in the tree.

        Time complexity: O(log n) average — O(n) worst case
        """
        return self._find_node(value) is not None

    def min(self) -> Any:
        """
        Returns the minimum value (leftmost node).

        Time complexity: O(log n) average

        Raises:
            IndexError: If the tree is empty.
        """
        if self._root is None:
            raise IndexError("Min from an empty tree")
        current = self._root
        while current.left is not None:
            current = current.left
        return current.value

    def max(self) -> Any:
        """
        Returns the maximum value (rightmost node).

        Time complexity: O(log n) average

        Raises:
            IndexError: If the tree is empty.
        """
        if self._root is None:
            raise IndexError("Max from an empty tree")
        current = self._root
        while current.right is not None:
            current = current.right
        return current.value

    def height(self) -> int:
        """
        Returns the height of the tree.
        Empty tree returns -1. Single node returns 0.

        Time complexity: O(n) — traverses all nodes
        """
        return self._compute_height(self._root)

    def _compute_height(self, node: Optional[TreeNode]) -> int:
        """
        Recursively computes height of the subtree rooted at node.

        Time complexity: O(n)
        """
        if node is None:
            return -1
        left_h = self._compute_height(node.left)
        right_h = self._compute_height(node.right)
        return 1 + max(left_h, right_h)

    # -------------------------------------------------------------------------
    # Traversals

    def inorder(self) -> Iterator[Any]:
        """
        Yields values in inorder (left, node, right) — sorted order.

        Iterative using explicit stack.

        Time complexity: O(n)
        """
        stack = []
        current = self._root
        while current is not None or stack:
            while current is not None:
                stack.append(current)
                current = current.left
            current = stack.pop()
            yield current.value
            current = current.right

    def preorder(self) -> Iterator[Any]:
        """
        Yields values in preorder (node, left, right).

        Iterative using explicit stack.

        Time complexity: O(n)
        """
        if self._root is None:
            return
        stack = [self._root]
        while stack:
            node = stack.pop()
            yield node.value
            if node.right is not None:
                stack.append(node.right)
            if node.left is not None:
                stack.append(node.left)

    def postorder(self) -> Iterator[Any]:
        """
        Yields values in postorder (left, right, node).

        Iterative using two stacks.

        Time complexity: O(n)
        """
        if self._root is None:
            return
        stack = [self._root]
        result = []
        while stack:
            node = stack.pop()
            result.append(node.value)
            if node.left is not None:
                stack.append(node.left)
            if node.right is not None:
                stack.append(node.right)
        yield from reversed(result)

    def level_order(self) -> Iterator[Any]:
        """
        Yields values level by level, left to right.

        Iterative using a queue (list as deque).

        Time complexity: O(n)
        """
        if self._root is None:
            return
        queue = [self._root]
        while queue:
            node = queue.pop(0)
            yield node.value
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)

    # -------------------------------------------------------------------------
    # State checks

    def is_empty(self) -> bool:
        """Returns True if the tree contains no elements. O(1)"""
        return self._size == 0

    # -------------------------------------------------------------------------
    # Dunder methods

    def clear(self) -> None:
        """
        Removes all nodes by dropping the root reference.

        Time complexity: O(1)
        """
        self._root = None
        self._size = 0

    def copy(self) -> "BST":
        """
        Returns a shallow copy preserving structure via preorder insertion.

        Time complexity: O(n log n)
        """
        return BST(*self.preorder())

    def __len__(self) -> int:
        """Returns number of nodes in the tree. O(1)"""
        return self._size

    def __bool__(self) -> bool:
        """Returns True if the tree is not empty. O(1)"""
        return self._size > 0

    def __iter__(self) -> Iterator[Any]:
        """
        Yields values in inorder (sorted) order.

        Time complexity: O(n)
        """
        yield from self.inorder()

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields values in reverse inorder (largest to smallest).

        Iterative — goes right first instead of left.

        Time complexity: O(n)
        """
        stack = []
        current = self._root
        while current is not None or stack:
            while current is not None:
                stack.append(current)
                current = current.right
            current = stack.pop()
            yield current.value
            current = current.left

    def __contains__(self, value: Any) -> bool:
        """Returns True if value exists in the tree. O(log n) average"""
        return self.search(value)

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both trees have identical structure and values.

        Two trees are equal only if every corresponding node has the
        same value and the same child configuration.

        Time complexity: O(n)
        """
        if not isinstance(other, BST):
            return NotImplemented
        return self._equal_nodes(self._root, other._root)

    def _equal_nodes(self, a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
        """
        Recursively checks if two subtrees are structurally identical.

        Time complexity: O(n)
        """
        if a is None and b is None:
            return True
        if a is None or b is None:
            return False
        if a.value != b.value:
            return False
        return self._equal_nodes(a.left, b.left) and self._equal_nodes(a.right, b.right)

    def __repr__(self) -> str:
        """
        Returns string representation of the tree.
        Format: BST(size=4)[1, 3, 5, 7]
                              inorder

        Time complexity: O(n)
        """
        elements = ", ".join(repr(v) for v in self.inorder())
        return f"BST(size={self._size})[{elements}]"
