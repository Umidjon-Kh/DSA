# Nodes

Three node types used as building blocks for all linked data structures.

```
nodes/
├── linear.py     # singly linked node (next only)
├── bi_linear.py  # doubly linked node (prev + next)
└── tree_node.py  # binary tree node (left, right, parent)
```

---

## Class Overview

### `LinearNode(value)`

A singly linked node that stores a value and a reference to the next node.
Traversal is forward only. Used by structures that only need to move in one direction.

```python
node = LinearNode(42)
node = LinearNode("hello")
```

Used by:
`SinglyLinkedList`, `CircularSinglyLinkedList`, `DynamicNodeStack`, `NodeQueue`

### `BiLinearNode(value)`

A doubly linked node that stores a value and references to both the previous
and next nodes. Allows traversal in both directions.

```python
node = BiLinearNode(23)
node = BiLinearNode("hi")
```

Used by:
`DoublyLinkedList`, `CircularDoublyLinkedList`, `NodeDeque`

### `TreeNode(value)`

A binary tree node that stores a value and references to its left child,
right child, and parent. The parent reference enables upward traversal
without an external stack.

```python
node = TreeNode(10)
node = TreeNode("root")
```

Used by:
`BinaryTree`, `BinarySearchTree`, `AVLTree`, `RedBlackTree`

---

## Repr Format

Each node's `__repr__` shows the node's own value alongside its neighbors'
values — not just whether neighbors exist.

```python
LinearNode(42) -> 10        # next exists, its value is 10
LinearNode(42) -> None      # no next node

None <-> BiLinearNode(23) <-> 99    # prev=None, next.value=99
10   <-> BiLinearNode(23) <-> None  # prev.value=10, next=None

TreeNode(10) -> (L: 5, R: 15, P: None)   # root node with two children
TreeNode(5)  -> (L: None, R: None, P: 10) # leaf node
```

---

## Supported Operations

| Operation  | LinearNode | BiLinearNode | TreeNode |
| ---------- | ---------- | ------------ | -------- |
| `__init__` | O(1)       | O(1)         | O(1)     |
| `__repr__` | O(1)       | O(1)         | O(1)     |

---

## Key Design Decisions

### `__slots__`

All node classes use `__slots__` to reduce per-instance memory overhead.
This matters when millions of nodes exist simultaneously inside large structures.

### No default neighbor arguments

Nodes are created without neighbors — links are set by the data structure,
not by the node constructor. This keeps the node interface minimal and prevents
accidental shared references between structures.

```python
# Correct — structure sets the links
node = LinearNode(42)
node.next = LinearNode(99)

# There is no LinearNode(42, next=other_node)
```

### `value` lives in `BaseNode`

The `value` slot is defined on `BaseNode` and shared by all subclasses.
Subclasses only declare their own reference slots (`next`, `prev`, `left`, etc.)
and must not redeclare `value` — doing so would duplicate the slot.

### `TreeNode` has no `is_leaf` / `is_root` helpers

Leaf and root checks are the responsibility of the tree structure, not the node.
Keeping the node interface minimal makes it reusable across different tree implementations
that may define "leaf" or "root" differently.
