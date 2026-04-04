from typing import Any, Iterator, Optional

from ..._base import BaseTree
from ...nodes import TreeNode


class AVLTree(BaseTree):
    """
    A self-balancing binary search tree backed by TreeNode.

    Maintains AVL property: for every node, the height difference
    between left and right subtrees (balance factor) is at most 1.
    Balance is restored after every insert and remove via rotations.

    Duplicate values are ignored on insert.

    Time complexity:
        insert:      O(log n)
        remove:      O(log n)
        search:      O(log n)
        min:         O(log n)
        max:         O(log n)
        height:      O(1) — stored in each node
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
        __contains__: O(log n)
        __eq__:      O(n)
        __repr__:    O(n)
    """

    __slots__ = ("_root", "_size")

    def __init__(self, *args) -> None:
        """
        Creates an AVL tree with optional initial values.

        Args:
            *args: Optional initial values, inserted in order.
                   Duplicates are ignored.

        Examples:
            t = AVLTree()              # empty
            t = AVLTree(5, 3, 7, 1)   # balanced, root may vary
        """
        self._root: Optional[TreeNode] = None
        self._size: int = 0

        for value in args:
            self.insert(value)

    # -------------------------------------------------------------------------
    # Internal helpers

    def _height(self, node: Optional[TreeNode]) -> int:
        """Returns stored height of node, or -1 for None. O(1)"""
        return node.height if node is not None else -1

    def _bf(self, node: TreeNode) -> int:
        """
        Returns balance factor of node.
        BF = height(left) - height(right).
        Valid range: [-1, 1]. Outside triggers rebalance.

        O(1)
        """
        return self._height(node.left) - self._height(node.right)

    def _update_height(self, node: TreeNode) -> None:
        """
        Recomputes and stores height of node from its children.
        Must be called bottom-up after structural changes.

        O(1)
        """
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    # -------------------------------------------------------------------------
    # Rotations

    def _rotate_left(self, A: TreeNode) -> TreeNode:
        """
        Performs a left rotation around node A.

        Before:          After:
            A                B
             \\             / \\
              B            A   C
               \\
                C

        Updates heights bottom-up: A first, then B.

        Time complexity: O(1)
        """
        B = A.right  # type: ignore[assignment]
        A.right = B.left  # type: ignore[assignment]
        if B.left is not None:  # type: ignore[union-attr]
            B.left.parent = A  # type: ignore[union-attr]
        B.left = A  # type: ignore[union-attr]
        B.parent = A.parent  # type: ignore[union-attr]
        A.parent = B
        self._update_height(A)
        self._update_height(B)  # type: ignore[union-attr]
        return B  # type: ignore[union-attr]

    def _rotate_right(self, C: TreeNode) -> TreeNode:
        """
        Performs a right rotation around node C.

        Before:          After:
              C              B
             /              / \\
            B              A   C
           /
          A

        Updates heights bottom-up: C first, then B.

        Time complexity: O(1)
        """
        B = C.left  # type: ignore[assignment]
        C.left = B.right  # type: ignore[assigment]
        if B.right is not None:  # type: ignore[union-attr]
            B.right.parent = C  # type: ignore[union-attr]
        B.right = C  # type: ignore[union-attr]
        B.parent = C.parent  # type: ignore[union-attr]
        C.parent = B
        self._update_height(C)
        self._update_height(B)  # type: ignore[union-attr]
        return B  # type: ignore[union-attr]

    def _rebalance(self, node: TreeNode) -> TreeNode:
        """
        Checks balance factor of node and applies the correct rotation.

        Four cases:
            BF = -2, right child BF <= 0  → rotate_left
            BF = -2, right child BF  = 1  → rotate_right(right), rotate_left
            BF =  2, left  child BF >= 0  → rotate_right
            BF =  2, left  child BF = -1  → rotate_left(left), rotate_right

        Time complexity: O(1)
        """
        bf = self._bf(node)

        if bf == -2:
            if self._bf(node.right) == 1:  # type: ignore[arg-type]
                node.right = self._rotate_right(node.right)  # type: ignore[arg-type]
            return self._rotate_left(node)

        if bf == 2:
            if self._bf(node.left) == -1:  # type: ignore[arg-type]
                node.left = self._rotate_left(node.left)  # type: ignore[arg-type]
            return self._rotate_right(node)

        return node

    # -------------------------------------------------------------------------
    # Core operations

    def insert(self, value: Any) -> None:
        """
        Inserts value into the tree and restores AVL balance.

        Traverses down like BST, then walks back up updating heights
        and rebalancing at each ancestor of the inserted node.

        Duplicate values are silently ignored.

        Time complexity: O(log n)
        """
        self._root = self._insert(self._root, value)

    def _insert(self, node: Optional[TreeNode], value: Any) -> TreeNode:
        """
        Recursive insert — returns the (possibly new) root of the subtree.

        Time complexity: O(log n)
        """
        if node is None:
            self._size += 1
            return TreeNode(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
            node.left.parent = node
        elif value > node.value:
            node.right = self._insert(node.right, value)
            node.right.parent = node
        else:
            return node
        self._update_height(node)
        return self._rebalance(node)

    def remove(self, value: Any) -> None:
        """
        Removes value from the tree and restores AVL balance.

        If value is not found, does nothing.
        Unlike BST, may require multiple rebalance steps walking up to root.

        Time complexity: O(log n)
        """
        self._root = self._remove(self._root, value)

    def _remove(self, node: Optional[TreeNode], value: Any) -> Optional[TreeNode]:
        """
        Recursive remove — returns the (possibly new) root of the subtree.

        Time complexity: O(log n)
        """
        if node is None:
            return None
        if value < node.value:
            node.left = self._remove(node.left, value)
            if node.left is not None:
                node.left.parent = node
        elif value > node.value:
            node.right = self._remove(node.right, value)
            if node.right is not None:
                node.right.parent = node
        else:
            self._size -= 1
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = self._inorder_successor(node)
            node.value = successor.value
            self._size += 1
            node.right = self._remove(node.right, successor.value)
            if node.right is not None:
                node.right.parent = node
        self._update_height(node)
        return self._rebalance(node)

    def _inorder_successor(self, node: TreeNode) -> TreeNode:
        """
        Returns the inorder successor — the smallest node in the
        right subtree of given node.

        Time complexity: O(log n)
        """
        current = node.right
        while current.left is not None:  # type: ignore[union-attr]
            current = current.left  # type: ignore[union-attr]
        return current  # type: ignore[return-value]

    def search(self, value: Any) -> bool:
        """
        Returns True if value exists in the tree.

        Time complexity: O(log n)
        """
        current = self._root
        while current is not None:
            if value == current.value:
                return True
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        return False

    def min(self) -> Any:
        """
        Returns the minimum value (leftmost node).

        Time complexity: O(log n)

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

        Time complexity: O(log n)

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

        Time complexity: O(1) — stored in root node.
        """
        return self._height(self._root)

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

        Iterative using a queue.

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

    def copy(self) -> "AVLTree":
        """
        Returns a copy preserving AVL balance via preorder insertion.

        Time complexity: O(n log n)
        """
        return AVLTree(*self.preorder())

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
        """Returns True if value exists in the tree. O(log n)"""
        return self.search(value)

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both trees have identical structure and values.

        Two trees are equal only if every corresponding node has the
        same value and the same child configuration.

        Time complexity: O(n)
        """
        if not isinstance(other, AVLTree):
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
        Format: AVLTree(size=4, height=2)[1, 3, 5, 7]
                                           inorder

        Time complexity: O(n)
        """
        elements = ", ".join(repr(v) for v in self.inorder())
        return f"AVLTree(size={self._size}, height={self.height()})[{elements}]"
