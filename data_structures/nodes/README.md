# Nodes

Collection of lightweight node implementations used as building blocks for
linked data structures and tree-based containers.

Each node is optimized for:

- minimal memory usage (`__slots__`)
- O(1) access to neighbors
- clear debug-friendly `__repr__`

All nodes inherit from `BaseNode`.

---

## Available Nodes

### LinearNode

Singly-linked node.

value -> next

Used in:

- SinglyLinkedList
- CircularSinglyLinkedList
- NodeStack
- NodeQueue

Example:

```python
node1 = LinearNode(10)
node2 = LinearNode(20)

node1.next = node2
print(node1)
# LinearNode(10) -> 20
```

### BiLinearNode

Doubly-linked node.

prev <-> value <-> next

Used in:

- DoublyLinkedList
- CircularDoublyLinkedList
- NodeDeque

Example:

```python
a = BiLinearNode(1)
b = BiLinearNode(2)

a.next = b
b.prev = a

print(b)
# 1 <-> BiLinearNode(2) <-> None
```

### TreeNode

Binary tree node with parent pointer.

        parent
        /    \
     left   right

Used in:

- BinaryTree
- BinarySearchTree
- AVLTree
- RedBlackTree

Example:

```python
root = TreeNode(10)
left = TreeNode(5)
right = TreeNode(15)

root.left = left
root.right = right

left.parent = root
right.parent = root

print(root)
# TreeNode(10) -> (L: 5, R: 15, P: None)
```

## Design Principles

- All nodes use **slots** to reduce memory overhead
- No logic inside nodes (data containers only)
- O(1) initialization
- O(1) neighbor updates
- Debug-friendly representations
- Type-hinted references

## Complexity

| Operation        | Complexity |
| ---------------- | ---------- |
| create node      | O(1)       |
| assign neighbors | O(1)       |
| repr             | O(1)       |

## File Structure

```
nodes/
│
├── linear_node.py
├── bi_linear_node.py
├── tree_node.py
├── quad_node.py (reserved)
└── **init**.py
```

## Notes

- Nodes are intentionally minimal
- No validation is performed
- Containers are responsible for maintaining structure integrity
- quad_node.py reserved for future graph/grid structures
