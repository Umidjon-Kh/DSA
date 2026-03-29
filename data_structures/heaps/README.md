# Heaps

A heap is a **complete binary tree** that satisfies the heap property — every
parent compares correctly with its children. This module provides ten heap
classes across three backends and two ordering modes.

---

## Heap property

**Min-heap** — every parent is ≤ its children. The root is always the minimum.

**Max-heap** — every parent is ≥ its children. The root is always the maximum.

Siblings have no guaranteed ordering between each other — only the
parent-to-child relationship is enforced.

---

## Complete binary tree

A complete binary tree fills every level from left to right with no gaps.
This shape is what makes the array representation work: the position of a
node's parent and children can be computed from its index alone.

```
Level 0:              1          ← root (index 0)
Level 1:          3       2      ← indices 1, 2
Level 2:        7   5   4        ← indices 3, 4, 5
```

For a node at index `i`:

```
parent       = (i - 1) // 2
left child   = 2 * i + 1
right child  = 2 * i + 2
```

---

## Core operations

### push — O(log n)

1. Place the new value at the end of the structure (next leaf position).
2. Call `_sift_up`: compare with parent, swap while the heap property is
   violated, move up. Stops at the root or when no swap is needed.

```
Insert 1 into min-heap [3, 5, 4, 7, 8]:

       3                  3                  1
     /   \              /   \              /   \
    5     4    →       1     4    →       3     4
   / \               / \               / \
  7   8             7   8             7   8
  ↑ inserted     sift_up: 1<5       sift_up: 1<3
```

### pop — O(log n)

1. Save the root value (the answer).
2. Move the last element to the root position.
3. Remove the last slot.
4. Call `_sift_down`: compare with children, swap with the more extreme
   child while the heap property is violated, move down. Stops at a leaf
   or when no swap is needed.

```
Pop from min-heap [1, 3, 4, 7, 8]:

       1                  8                  3
     /   \              /   \              /   \
    3     4    →       3     4    →       7     4
   / \               /                 /
  7   8             7               8 removed, sift_down: 8>3 → swap with 3
  root removed   last→root          then 8>7 → swap with 7
```

### peek — O(1)

Returns `array[0]` (array-based) or `root.value` (node-based) without
removing it. The root is always the extreme element.

### heapify — O(n) for array-based, O(n log n) for node-based

**Array-based** uses Floyd's algorithm — load all values into the array
first, then call `_sift_down` from the last non-leaf node up to the root.
This runs in O(n) because most nodes are near the bottom and sift only a
short distance.

```
Last non-leaf index = size // 2 - 1

[9, 4, 7, 1, 3, 2]  →  sift_down from index 2 backwards to 0
    ↑ start here        result: [1, 3, 2, 9, 4, 7]
```

**Node-based** uses repeated `push()` calls because random index access
is not available. Each push costs O(log n), giving O(n log n) total.

`heapify` does **not** replace existing elements — it appends to the
current heap. Call `clear()` first if you want a fresh heap.

### ordered — O(n log n)

Yields all elements in sorted order by repeatedly popping from a copy.
The original heap is not modified. For unsorted internal order use
`__iter__` instead.

```python
h = StaticTypedMinHeap(int, 5, 3, 8, 1, capacity=5)
list(h)            # [1, 3, 8, 5] — internal array order, not sorted
list(h.ordered())  # [1, 3, 5, 8] — fully sorted
```

---

## Backends

### Array-based static

Backed by `StaticTypedArray` or `StaticUniversalArray`. Fixed capacity set
at construction. Raises `OverflowError` when full. Inherits `BaseBoundedHeap`
which adds `is_full()`.

```python
h = StaticTypedMinHeap(int, capacity=10)
h = StaticUniversalMaxHeap(1, 5, 3, capacity=5)
```

### Array-based dynamic

Backed by `DynamicTypedArray` or `DynamicUniversalArray`. Grows automatically
using CPython's growth formula. No capacity argument, no `is_full()`.
Inherits `BaseHeap`.

```python
h = DynamicTypedMinHeap(int)
h = DynamicUniversalMaxHeap(1, 5, 3)
```

### Node-based

Backed by `TreeNode` with `left`, `right`, and `parent` pointers. No
internal array — the tree lives as linked nodes in memory.

The key challenge is finding where to insert the next node without
iterating the entire tree. This is solved with a **bit-path trick**:

In a 1-based complete binary tree the binary representation of a
position encodes the path from root to that node. Stripping the leading
`1` bit (via `bin(position)[3:]`) gives turn-by-turn directions:

```
'0' → go left
'1' → go right

position = 6  →  bin(6) = '0b110'  →  [3:] = '10'  →  right, left
position = 5  →  bin(5) = '0b101'  →  [3:] = '01'  →  left, right
```

This finds any node in `floor(log2(n))` steps — at one billion nodes
that is about 30 steps, never more.

```python
h = NodeMinHeap(5, 3, 1)
h = NodeMaxHeap()
h.push(7)
```

---

## Typed vs Universal

**Typed** (`*Typed*`) — enforces a single dtype for all elements.
Supported dtypes: `int`, `float`, `bool`, `str`.
Raises `TypeError` on wrong type. Uses `_raw_get`/`_raw_set` internally
for zero-overhead element access in the static backend.

**Universal** (`*Universal*`) — accepts any Python object.
No type restriction. Elements are compared with `<` or `>` directly,
so values must be mutually comparable at runtime.

---

## Available classes

### Min-heaps (root = minimum)

| Class                     | Backend                 | Capacity |
| ------------------------- | ----------------------- | -------- |
| `StaticTypedMinHeap`      | `StaticTypedArray`      | fixed    |
| `StaticUniversalMinHeap`  | `StaticUniversalArray`  | fixed    |
| `DynamicTypedMinHeap`     | `DynamicTypedArray`     | grows    |
| `DynamicUniversalMinHeap` | `DynamicUniversalArray` | grows    |
| `NodeMinHeap`             | `TreeNode`              | grows    |

### Max-heaps (root = maximum)

| Class                     | Backend                 | Capacity |
| ------------------------- | ----------------------- | -------- |
| `StaticTypedMaxHeap`      | `StaticTypedArray`      | fixed    |
| `StaticUniversalMaxHeap`  | `StaticUniversalArray`  | fixed    |
| `DynamicTypedMaxHeap`     | `DynamicTypedArray`     | grows    |
| `DynamicUniversalMaxHeap` | `DynamicUniversalArray` | grows    |
| `NodeMaxHeap`             | `TreeNode`              | grows    |

---

## Time complexity summary

| Operation      | Array-based                 | Node-based |
| -------------- | --------------------------- | ---------- |
| `push`         | O(log n)                    | O(log n)   |
| `pop`          | O(log n)                    | O(log n)   |
| `peek`         | O(1)                        | O(1)       |
| `heapify`      | O(n)                        | O(n log n) |
| `ordered`      | O(n log n)                  | O(n log n) |
| `clear`        | O(n) typed / O(1) universal | O(1)       |
| `copy`         | O(n)                        | O(n log n) |
| `__iter__`     | O(n)                        | O(n)       |
| `__contains__` | O(n)                        | O(n)       |
| `__len__`      | O(1)                        | O(1)       |

---

## `__repr__` formats

```
StaticTypedMinHeap(int, size=3, capacity=5)[1, 3, 2]
StaticUniversalMinHeap(size=3, capacity=5)[1, 3, 2]
StaticTypedMaxHeap(int, size=3, capacity=5)[5, 3, 1]
StaticUniversalMaxHeap(size=3, capacity=5)[5, 3, 1]

DynamicTypedMinHeap(int, size=3)[1, 3, 2]
DynamicUniversalMinHeap(size=3)[1, 3, 2]
DynamicTypedMaxHeap(int, size=3)[5, 3, 1]
DynamicUniversalMaxHeap(size=3)[5, 3, 1]

NodeMinHeap(size=4)[1, 3, 2, 7]
NodeMaxHeap(size=4)[7, 5, 4, 1]
```

Elements are shown in internal order (root first), not sorted.
For node-based heaps the order is level-order (BFS).

---

## Usage examples

```python
from data_structures.heaps import (
    StaticTypedMinHeap,
    DynamicUniversalMaxHeap,
    NodeMinHeap,
)

# Static typed min-heap
h = StaticTypedMinHeap(int, 5, 3, 8, 1, capacity=10)
h.peek()            # 1
h.pop()             # 1
list(h.ordered())   # [3, 5, 8]

# Dynamic universal max-heap
h = DynamicUniversalMaxHeap(4, 1, 7, 2)
h.push(9)
h.peek()            # 9
h.pop()             # 9

# Node-based min-heap with heapify
h = NodeMinHeap()
h.heapify([6, 2, 8, 1, 4])
h.peek()            # 1
list(h.ordered())   # [1, 2, 4, 6, 8]
```
