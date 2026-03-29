from typing import Any, Iterable, Iterator, Optional

from ..._base import BaseHeap
from ...nodes import TreeNode


class NodeMaxHeap(BaseHeap):
    """
    A resizable max-heap backed by TreeNode.
    The root is always the largest element.

    Unlike array-based heaps, this implementation uses real tree nodes
    connected via left, right, and parent pointers (TreeNode). There is
    no internal array — the tree lives in memory as linked nodes.

    ── Structure ────────────────────────────────────────────────────────────
    Logically, the heap is a *complete binary tree*:
      - Every level is fully filled from left to right.
      - The root always holds the maximum value (heap property).
      - Each node is greater than or equal to its children.

    Example with 6 elements [1, 3, 2, 7, 5, 4]:

                    7          ← root (maximum)
                  /   \\
                5       4
               / \\     /
              1   3   2

    ── Difference from NodeMinHeap ──────────────────────────────────────────
    NodeMaxHeap is structurally identical to NodeMinHeap.
    The only difference is the comparison direction:

        NodeMinHeap: parent ≤ children  →  root is minimum
        NodeMaxHeap: parent ≥ children  →  root is maximum

    This means _sift_up swaps while node > parent (instead of <),
    and _sift_down swaps with the *larger* child (instead of smaller).
    All other logic — bit-path traversal, pointer management,
    BFS iteration — is exactly the same.

    ── Finding positions in O(log n) ────────────────────────────────────────
    To insert a new node or find the last node for pop(), we need to
    locate a specific position in the complete binary tree without
    iterating over all nodes. This is done using a bit-path trick:

    In a complete binary tree with n nodes, the binary representation
    of a position (1-based) encodes the path from root to that node.
    Stripping the leading '1' bit (via bin(position)[3:]) gives a
    sequence of '0'/'1' characters:
        '0' → go to left child
        '1' → go to right child

    This finds any node in exactly floor(log2(n)) steps — O(log n).
    At one billion nodes that is about 30 steps.

    ── Time complexity ───────────────────────────────────────────────────────
        push:         O(log n)
        pop:          O(log n)
        peek:         O(1)
        heapify:      O(n log n)  — n pushes, each O(log n)
        ordered:      O(n log n)
        clear:        O(1)
        copy:         O(n log n)
        is_empty:     O(1)
        __len__:      O(1)
        __bool__:     O(1)
        __iter__:     O(n) — level-order (BFS)
        __reversed__: O(n)
        __contains__: O(n)
        __repr__:     O(n)
        __eq__:       O(n)
    """

    __slots__ = ("_root", "_size")

    def __init__(self, *args) -> None:
        """
        Creates a node-based max-heap with optional initial elements.

        If initial elements are provided, they are inserted one by one
        via push(), which establishes the heap property automatically.
        The order of args does not matter — the heap will always
        place the largest value at the root after all insertions.

        Args:
            *args: Optional initial values of any comparable type.

        Examples:
            h = NodeMaxHeap()              # empty heap, root=None
            h = NodeMaxHeap(5, 3, 1, 4)   # root=5
        """
        self._root: Optional[TreeNode] = None
        self._size: int = 0

        if args:
            self.heapify(args)

    # -------------------------------------------------------------------------
    # Internal helpers

    def _find_node(self, position: int) -> TreeNode:
        """
        Locates and returns the node at the given 1-based position
        in the complete binary tree using a bit-path traversal.

        ── How it works ─────────────────────────────────────────────────────
        Every node in a complete binary tree has a unique 1-based index
        in level-order (root=1, its children=2,3, and so on).
        The binary representation of the position encodes the exact path
        from the root. After stripping '0b' and the leading '1' bit
        (bin(position)[3:]), remaining bits are turn-by-turn directions:
            '0' → go to left child
            '1' → go to right child

        Examples:
            position=1  → bin='1'   → [3:]=''   → stay at root
            position=2  → bin='10'  → [3:]='0'  → left
            position=3  → bin='11'  → [3:]='1'  → right
            position=4  → bin='100' → [3:]='00' → left, left
            position=5  → bin='101' → [3:]='01' → left, right
            position=6  → bin='110' → [3:]='10' → right, left
            position=7  → bin='111' → [3:]='11' → right, right

        This always takes exactly floor(log2(position)) steps — O(log n).

        Time complexity: O(log n)

        Args:
            position: 1-based index of the target node in level-order.

        Returns:
            The TreeNode at the given position.
        """
        node = self._root
        for bit in bin(position)[3:]:
            if bit == "0":
                node = node.left  # type: ignore[union-attr]
            else:
                node = node.right  # type: ignore[union-attr]
        return node  # type: ignore[return-value]

    def _swap_values(self, a: TreeNode, b: TreeNode) -> None:
        """
        Swaps the values of two nodes without changing their positions
        or pointer connections in the tree.

        We exchange only the stored values, not the nodes themselves.
        This avoids the complexity of rewiring left, right, and parent
        pointers for both nodes and all their neighbors.

        Time complexity: O(1)

        Args:
            a: First node.
            b: Second node.
        """
        a.value, b.value = b.value, a.value

    # -------------------------------------------------------------------------
    # Heap operations

    def _sift_up(self, node: TreeNode) -> None:
        """
        Restores the heap property by moving a node upward toward the root.

        Called after inserting a new node at the bottom of the tree.
        The new node may be larger than its parent, which would violate
        the max-heap property. This method fixes that by repeatedly
        swapping the node's value with its parent's value while the
        node is larger than its parent.

        ── Step-by-step example ─────────────────────────────────────────────
        Suppose we insert 9 into this heap:

                7
              /   \\
             5     4
            /
           9   ← just inserted here

        Step 1: node=9, parent=5  →  9 > 5  →  swap

                7
              /   \\
             9     4
            /
           5

        Step 2: node=9, parent=7  →  9 > 7  →  swap

                9
              /   \\
             7     4
            /
           5

        Step 3: node=9 is now root, no parent → stop.
        ─────────────────────────────────────────────────────────────────────

        Time complexity: O(log n) — at most the height of the tree swaps.

        Args:
            node: The node to sift upward (usually the newly inserted node).
        """
        while node.parent is not None and node.value > node.parent.value:
            self._swap_values(node, node.parent)
            node = node.parent

    def _sift_down(self, node: TreeNode) -> None:
        """
        Restores the heap property by moving a node downward toward the leaves.

        Called after replacing the root with the last node during pop().
        The replacement node may be smaller than one or both of its children,
        violating the max-heap property. This method fixes that by repeatedly
        swapping the node's value with its larger child's value while the
        node is smaller than at least one child.

        ── Why the larger child? ─────────────────────────────────────────────
        We must swap with the *larger* child, not just any child.
        If we swapped with the smaller child, the larger child would become
        a child of the smaller one, violating the heap property immediately.
        Swapping with the larger child ensures the new parent is larger
        than both its children after the swap.

        ── Step-by-step example ─────────────────────────────────────────────
        After pop(), the last node's value (2) is placed at the root:

                2        ← placed here
              /   \\
             7     6
            / \\
           3   5

        Step 1: node=2, children=7,6  →  largest child=7  →  2 < 7  →  swap

                7
              /   \\
             2     6
            / \\
           3   5

        Step 2: node=2, children=3,5  →  largest child=5  →  2 < 5  →  swap

                7
              /   \\
             5     6
            / \\
           3   2

        Step 3: node=2, no children (leaf) → stop.
        ─────────────────────────────────────────────────────────────────────

        Time complexity: O(log n) — at most the height of the tree swaps.

        Args:
            node: The node to sift downward (usually the root after pop).
        """
        while True:
            largest = node

            if node.left is not None and node.left.value > largest.value:
                largest = node.left
            if node.right is not None and node.right.value > largest.value:
                largest = node.right

            if largest is node:
                break

            self._swap_values(node, largest)
            node = largest

    # -------------------------------------------------------------------------
    # Core operations

    def push(self, value: Any) -> None:
        """
        Inserts a new value into the heap and restores the heap property.

        ── Process ──────────────────────────────────────────────────────────
        1. Increment size. The new node belongs at position `size`
           (1-based) in level-order.
        2. If the heap is empty, the new node becomes the root — done.
        3. Otherwise, find the parent of position `size` using the
           bit-path: _find_node(size >> 1) gives the parent directly
           (integer division by 2 in 1-based indexing).
        4. Create the new TreeNode and attach it as left or right child
           of that parent. Even position → left child. Odd → right child.
        5. Call _sift_up to bubble the new node to its correct position.

        Time complexity: O(log n)

        Args:
            value: Any comparable value to insert.
        """
        self._size += 1
        new_node = TreeNode(value)

        if self._size == 1:
            self._root = new_node
            return

        parent = self._find_node(self._size >> 1)
        new_node.parent = parent

        if self._size % 2 == 0:
            parent.left = new_node
        else:
            parent.right = new_node

        self._sift_up(new_node)

    def pop(self) -> Any:
        """
        Removes and returns the root element (maximum).

        ── Process ──────────────────────────────────────────────────────────
        1. Save the root's value to return later.
        2. If only one node exists, clear the root and return the value.
        3. Find the last node in level-order at position `size` using
           the bit-path.
        4. Copy the last node's value into the root. The root now
           temporarily holds a value that may violate the heap property.
        5. Detach the last node from its parent:
           - If it is the right child → set parent.right = None.
           - Otherwise → set parent.left = None.
           - Clear the last node's parent pointer so it is fully isolated.
        6. Decrement size.
        7. Call _sift_down from the root to restore the heap property.

        ── Why copy the last node's value? ──────────────────────────────────
        Removing the root and rewiring all pointers would be extremely
        complex. Instead we overwrite the root's value with the last node's
        value (O(1)), detach the now-redundant last node, and let
        _sift_down fix the order. The tree shape stays valid throughout.

        Time complexity: O(log n)

        Raises:
            IndexError: If the heap is empty.

        Returns:
            The largest value that was at the root.
        """
        if self.is_empty():
            raise IndexError("Pop from an empty heap")

        root_value = self._root.value  # type: ignore[union-attr]

        if self._size == 1:
            self._root = None
            self._size = 0
            return root_value

        last = self._find_node(self._size)
        self._root.value = last.value  # type: ignore[union-attr]

        if last.parent.right is last:  # type: ignore[union-attr]
            last.parent.right = None  # type: ignore[union-attr]
        else:
            last.parent.left = None  # type: ignore[union-attr]
        last.parent = None

        self._size -= 1
        self._sift_down(self._root)  # type: ignore[arg-type]
        return root_value

    def peek(self) -> Any:
        """
        Returns the root element (maximum) without removing it.

        The root is always the maximum in a max-heap because every
        parent is greater than its children by the heap property.

        Time complexity: O(1)

        Raises:
            IndexError: If the heap is empty.

        Returns:
            The largest value currently in the heap.
        """
        if self.is_empty():
            raise IndexError("Peek from an empty heap")
        return self._root.value  # type: ignore[union-attr]

    def heapify(self, iterable: Iterable[Any]) -> None:
        """
        Inserts all elements from an iterable into the heap.

        Does not replace existing elements — appends to the current heap.
        Each value is inserted via push(), which maintains the heap
        property after every insertion.

        ── Why O(n log n) and not O(n)? ─────────────────────────────────────
        Floyd's O(n) algorithm requires placing all elements first and
        then calling sift_down from the middle index. This relies on
        direct index access — something node-based trees don't support.
        Navigating to any position costs O(log n), making bulk-placement
        without push() impractical. Pushing one by one is the natural
        node-based approach at O(n log n) total.

        Time complexity: O(n log n)

        Args:
            iterable: Any iterable of comparable values.

        Raises:
            TypeError: If iterable is not iterable.
        """
        try:
            values = list(iterable)
        except TypeError:
            raise TypeError(f"Expected an iterable, got ({type(iterable).__name__!r})")
        for value in values:
            self.push(value)

    def clear(self) -> None:
        """
        Removes all nodes by dropping the root reference.

        Once the root is set to None, the entire tree becomes
        unreachable and Python's garbage collector reclaims it.
        No manual traversal needed.

        Time complexity: O(1)
        """
        self._root = None
        self._size = 0

    def copy(self) -> "NodeMaxHeap":
        """
        Returns a shallow copy of the heap with the same elements.

        Builds the copy by iterating in level-order (BFS) and pushing
        each value. The resulting heap satisfies the max-heap property.

        Time complexity: O(n log n)
        """
        new_heap = NodeMaxHeap()
        for value in self:
            new_heap.push(value)
        return new_heap

    def ordered(self) -> Iterator[Any]:
        """
        Yields all elements in sorted order from largest to smallest.

        Works on a copy of the heap — the original is not modified.
        Repeatedly pops from the copy, which always returns the current
        maximum, producing a fully sorted descending sequence.

        For unsorted internal level-order use __iter__ instead.

        Time complexity: O(n log n)
        """
        tmp = self.copy()
        while not tmp.is_empty():
            yield tmp.pop()

    # -------------------------------------------------------------------------
    # State checks

    def is_empty(self) -> bool:
        """Returns True if the heap contains no nodes. O(1)"""
        return self._size == 0

    # -------------------------------------------------------------------------
    # Dunder methods

    def __len__(self) -> int:
        """Returns the number of nodes currently in the heap. O(1)"""
        return self._size

    def __bool__(self) -> bool:
        """Returns True if the heap contains at least one node. O(1)"""
        return self._size > 0

    def __iter__(self) -> Iterator[Any]:
        """
        Yields values in level-order (BFS) from root to last node.

        Uses a queue to visit nodes level by level, left to right.
        The first value yielded is always the maximum (the root).
        The result is NOT sorted — use ordered() for sorted output.

        ── Why BFS and not DFS? ─────────────────────────────────────────────
        BFS (level-order) is the natural traversal for a heap because
        it matches the internal structure — the heap is defined by levels.
        DFS (pre/in/post-order) would yield values in an order that has
        no meaningful relationship to heap priorities.

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

    def __reversed__(self) -> Iterator[Any]:
        """
        Yields values in reverse level-order (last node to root).

        Collects all values via BFS first, then yields them in reverse.
        The last value yielded is the root (maximum).

        Time complexity: O(n)
        """
        values = list(self)
        for value in reversed(values):
            yield value

    def __contains__(self, value: Any) -> bool:
        """
        Returns True if value exists anywhere in the heap.

        Must scan all nodes — there is no ordering between siblings
        or across levels (only parent ≥ children is guaranteed),
        so no early termination is possible.

        Time complexity: O(n)
        """
        for v in self:
            if v == value:
                return True
        return False

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both heaps have the same size and the same values
        in the same level-order positions.

        Two heaps built from the same elements in different insertion
        orders may produce different internal arrangements and thus
        compare as not equal even if their sorted outputs are identical.
        """
        if not isinstance(other, NodeMaxHeap):
            return NotImplemented
        if self._size != other._size:
            return False
        for a, b in zip(self, other):
            if a != b:
                return False
        return True

    def __repr__(self) -> str:
        """
        Returns a string representation of the heap in level-order.

        Format: NodeMaxHeap(size=4)[7, 5, 4, 1]
                                     root

        Time complexity: O(n)
        """
        elements = ", ".join(repr(v) for v in self)
        return f"NodeMaxHeap(size={self._size})[{elements}]"
