# Trees

A **tree** is a data structure where each element (called a **node**) can have
multiple "next" elements — unlike a linked list where each node points to only
one next node. Trees are everywhere: your computer's file system is a tree,
HTML pages are trees, and most search engines use trees internally.

This layer implements two binary tree variants:

- **BST** — simple and easy to understand, but can become slow with bad input
- **AVLTree** — always fast, automatically keeps itself balanced

---

## What is a Binary Tree?

A **binary** tree means each node has at most **2 children**: a left child and
a right child. The topmost node is called the **root**. Nodes with no children
are called **leaves**.

```
        10            ← root (no parent)
       /  \
      5    15         ← internal nodes
     / \     \
    2   7     20      ← leaves (no children)
```

**Key vocabulary:**

| Term    | Meaning                                        |
| ------- | ---------------------------------------------- |
| root    | The topmost node — has no parent               |
| leaf    | A node with no children                        |
| height  | Number of levels from root to the deepest leaf |
| depth   | Distance from the root to a specific node      |
| subtree | Any node and all its descendants               |

**Height and log₂:**

A perfectly balanced tree with `n` nodes has height ≈ log₂(n).
This means a balanced tree with **1 000 000 elements** has height ≈ 20.
Searching any element takes at most 20 steps — instead of up to 1 000 000
steps in a plain list.

```
n elements → minimum height

1  → 0
3  → 1
7  → 2
15 → 3
31 → 4
```

Each level doubles the number of nodes. That is the source of O(log n).

---

## BST — Binary Search Tree

A BST adds one rule on top of a plain binary tree:

> For every node: everything to the **left** is **smaller**,
> everything to the **right** is **larger**.

```
          10
         /  \
        5    15
       / \   / \
      2   7 12  20
```

This rule makes searching very fast — at each node you immediately know
whether to go left or right, eliminating half the remaining tree each step.

### Searching for 12

```
Step 1: look at root 10 → 12 > 10 → go right
Step 2: look at 15      → 12 < 15 → go left
Step 3: look at 12      → found!
```

Only 3 steps for 7 elements. A plain list would need up to 7.

### The problem with BST

If you insert elements in sorted order — `1, 2, 3, 4, 5` — the tree
degenerates into a chain:

```
1
 \
  2
   \
    3
     \
      4
       \
        5
```

Height = 4. Search for 5 takes 4 steps instead of 2.
This is called a **degenerate tree** — it has lost all its advantages.

**Use BST when:** you control the insertion order or just want to learn
how trees work. Use AVLTree for real data.

---

## AVLTree — Self-Balancing BST

An AVL tree is a BST that automatically fixes itself after every insert
and remove to stay balanced. It was invented by Adelson-Velsky and Landis
in 1962 — AVL stands for their initials.

### Balance Factor

Every node stores its **height** (how many levels below it).
The **balance factor (BF)** of a node is:

```
BF = height(left subtree) - height(right subtree)
```

AVL rule: every node must have BF in `{-1, 0, 1}`.
If BF reaches `2` or `-2` after an insert/remove — the tree fixes itself.

```
BF =  0 → perfectly balanced
BF =  1 → slightly left-heavy, ok
BF = -1 → slightly right-heavy, ok
BF =  2 → too left-heavy  → rotation needed
BF = -2 → too right-heavy → rotation needed
```

### Rotations

A rotation is a local restructuring of 3 nodes that restores balance
without breaking the BST ordering rule. There are 4 cases:

**Case 1 — everything goes right → rotate left**

```
A                  B
 \                / \
  B       →      A   C
   \
    C
```

**Case 2 — everything goes left → rotate right**

```
    C              B
   /              / \
  B       →      A   C
 /
A
```

**Case 3 — zigzag left-right → rotate left, then rotate right**

```
    C              C              B
   /              /              / \
  A       →      B       →      A   C
   \            /
    B          A
```

**Case 4 — zigzag right-left → rotate right, then rotate left**

```
A              A                  B
 \              \                / \
  C      →       B       →      A   C
 /                \
B                  C
```

All rotations only touch 3 nodes — the rest of the tree is untouched.

### How insert works step by step

Inserting `3, 1, 2` into an empty AVL tree:

```
Insert 3:
    3          height=0, BF=0 ✓

Insert 1:
    3          height(3)=1, BF(3)=1 ✓
   /
  1

Insert 2:
    3          height(3)=2, BF(3)=2 ✗ — violation!
   /
  1
   \
    2

This is a zigzag (Case 3):
  Step 1 — rotate_left around 1:
    3
   /
  2
 /
1

  Step 2 — rotate_right around 3:
  2
 / \
1   3          BF(2)=0 ✓ — balanced!
```

### Why height is stored per node

When going back up after an insert, AVL needs to know the height of each
node's children instantly — O(1). If height were computed on the fly it
would require traversing the entire subtree each time — O(n).
Storing `height` in the node makes the check O(1) at the cost of one
extra integer per node.

---

## Quick Reference

```
arrays/
├── static_universal.py   # fixed-size, any type
├── static_typed.py       # fixed-size, single dtype (ctypes buffer)
```

```
trees/
└── node_based/
    ├── bst.py     # unbalanced, simple
    └── avl.py     # self-balancing, always O(log n)
```

| Class     | Balanced | insert                    | remove                    | search                    |
| --------- | -------- | ------------------------- | ------------------------- | ------------------------- |
| `BST`     | ✗        | O(log n) avg / O(n) worst | O(log n) avg / O(n) worst | O(log n) avg / O(n) worst |
| `AVLTree` | ✓        | O(log n)                  | O(log n)                  | O(log n)                  |

---

## Classes

### `BST(*args)`

An unbalanced binary search tree. Simple and easy to understand.
Accepts any comparable Python objects.

```python
t = BST()                    # empty
t = BST(5, 3, 7, 1, 4)      # root=5

t.insert(6)                  # insert
t.remove(3)                  # remove
t.search(7)                  # → True
t.min()                      # → 1
t.max()                      # → 7
t.height()                   # → height of tree

list(t)                      # → [1, 4, 5, 6, 7]  (sorted, inorder)
list(reversed(t))            # → [7, 6, 5, 4, 1]  (reverse sorted)

list(t.inorder())            # → [1, 4, 5, 6, 7]
list(t.preorder())           # → [5, 4, 1, 7, 6]
list(t.postorder())          # → [1, 4, 6, 7, 5]
list(t.level_order())        # → [5, 4, 7, 1, 6]

6 in t                       # → True
len(t)                       # → 5
bool(t)                      # → True

copy = t.copy()              # independent copy, same structure
t.clear()                    # empty the tree
```

---

### `AVLTree(*args)`

A self-balancing BST. Guaranteed O(log n) for all operations regardless
of insertion order. Accepts any comparable Python objects.

```python
t = AVLTree()                # empty
t = AVLTree(1, 2, 3, 4, 5)  # inserts in sorted order — stays balanced!

t.insert(6)
t.remove(3)
t.search(4)                  # → True
t.min()                      # → 1
t.max()                      # → 6
t.height()                   # → O(1) — stored in root node

list(t)                      # → [1, 2, 4, 5, 6]  (sorted)
list(reversed(t))            # → [6, 5, 4, 2, 1]

list(t.inorder())            # → [1, 2, 4, 5, 6]
list(t.preorder())           # → root first
list(t.postorder())          # → root last
list(t.level_order())        # → level by level

copy = t.copy()              # independent copy
t.clear()
```

---

## Traversals explained

All four traversals visit every node exactly once — O(n).
They differ only in **when** each node is processed relative to its children.

### Inorder — left, node, right

Always produces a **sorted sequence** for a BST. This is the default
iteration order (`for v in tree`).

```
        5
       / \
      3   7       →   3, 5, 7
```

### Preorder — node, left, right

The **root always comes first**. Reinserting elements in this order into
a new empty BST reconstructs the exact same tree structure.

```
        5
       / \
      3   7       →   5, 3, 7
```

### Postorder — left, right, node

The **root always comes last**. Useful when you need to process children
before their parent — for example when computing subtree sizes or
deleting an entire tree safely.

```
        5
       / \
      3   7       →   3, 7, 5
```

### Level order — level by level

Visits nodes from top to bottom, left to right within each level.
Uses a **queue** internally (not a stack like the others).

```
        5
       / \
      3   7       →   5, 3, 7

        5
       / \
      3   7       →   5, 3, 7, 1, 4
     / \
    1   4
```

---

## Supported Operations

### BST

| Operation      | Time         | Description                           |
| -------------- | ------------ | ------------------------------------- |
| `insert`       | O(log n) avg | Insert value, ignore duplicates       |
| `remove`       | O(log n) avg | Remove value, do nothing if not found |
| `search`       | O(log n) avg | Return True if value exists           |
| `min`          | O(log n) avg | Return smallest value                 |
| `max`          | O(log n) avg | Return largest value                  |
| `height`       | O(n)         | Height of tree, -1 if empty           |
| `inorder`      | O(n)         | Yield sorted values                   |
| `preorder`     | O(n)         | Yield root-first values               |
| `postorder`    | O(n)         | Yield root-last values                |
| `level_order`  | O(n)         | Yield level by level                  |
| `clear`        | O(1)         | Remove all nodes                      |
| `copy`         | O(n log n)   | Independent copy, same structure      |
| `is_empty`     | O(1)         | True if no elements                   |
| `__len__`      | O(1)         | Number of nodes                       |
| `__bool__`     | O(1)         | True if not empty                     |
| `__iter__`     | O(n)         | Inorder iteration                     |
| `__reversed__` | O(n)         | Reverse inorder                       |
| `__contains__` | O(log n) avg | `value in tree`                       |
| `__eq__`       | O(n)         | Same structure and values             |
| `__repr__`     | O(n)         | `BST(size=3)[1, 2, 3]`                |

### AVLTree

Same as BST with these differences:

| Operation  | Time     | Note                                 |
| ---------- | -------- | ------------------------------------ |
| `insert`   | O(log n) | Guaranteed — rebalances after insert |
| `remove`   | O(log n) | Guaranteed — rebalances after remove |
| `search`   | O(log n) | Guaranteed                           |
| `height`   | O(1)     | Stored in root node, not computed    |
| `__repr__` | O(n)     | `AVLTree(size=3, height=1)[1, 2, 3]` |

---

## Design Decisions

### Why no typed (dtype) variant?

Typed arrays use a `ctypes` buffer which only works with fixed-size
memory blocks. TreeNode uses Python object references — there is no
buffer to type-restrict. Both BST and AVLTree accept any comparable
Python type naturally.

### Why iterative traversals instead of recursive?

Recursive traversals are simpler to read but have a hard limit — Python's
default recursion limit is ~1000. A degenerate BST with 2000 nodes would
crash with `RecursionError`. Iterative traversals using an explicit stack
have no such limit.

AVL `_insert` and `_remove` use recursion safely because the tree is
always balanced — maximum depth is O(log n), never more than ~60 levels
for any realistic input.

### Why does `copy` use preorder insertion?

Preorder always yields the root first. Inserting elements in preorder
order into a new empty tree reconstructs the exact same structure because
the root is inserted before its children — the BST ordering rule places
every subsequent element in the correct position.

### Why does `height` cost O(n) in BST but O(1) in AVL?

AVL stores `height` in every node and updates it after each rotation.
BST does not track height — computing it requires traversing the entire
tree. This is an intentional trade-off: BST is simpler with less overhead
per node.

### `__eq__` compares structure, not just elements

Two trees with the same elements but different structures are not equal:

```python
a = BST(5, 3, 7)
b = BST(3, 5, 7)   # different insertion order → different structure

list(a) == list(b)  # → True  (same elements in inorder)
a == b              # → False (different structure)
```

If you only care about elements use `list(a) == list(b)`.

---

## `__repr__` Formats

```
BST(size=4)[1, 3, 5, 7]
             inorder

AVLTree(size=4, height=2)[1, 3, 5, 7]
                           inorder
```
