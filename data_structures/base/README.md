# base/

Abstract base classes for every data structure in this library.

```
base/
├── base_node.py         ← BaseNode
├── base_collection.py   ← BaseCollection  (root of all collections)
├── base_array.py        ← BaseArray, BaseStaticArray, BaseDynamicArray
├── base_stack.py        ← BaseStack, BaseBoundedStack
├── base_queue.py        ← BaseQueue, BaseBoundedQueue
│                           BaseDeque, BaseBoundedDeque
│                           BasePriorityQueue
├── base_linked_list.py  ← BaseLinkedList
├── base_tree.py         ← BaseTree
├── base_graph.py        ← BaseGraph
└── base_heap.py         ← BaseHeap
```

---

## Why ABCs?

Every concrete class in this library inherits from one of these ABCs.
This gives three guarantees:

1. **Interface contract** — if you forget to implement a required method,
   Python raises `TypeError` at instantiation, not at runtime when the method is called.
2. **Consistent API** — all collections share `clear`, `copy`, `__len__`, `__bool__`,
   `__iter__`, `__reversed__`, `__contains__`, `__repr__`.
3. **Type-checking** — `isinstance(obj, BaseStack)` works regardless of which
   stack implementation is behind the facade.

---

## Hierarchy

```
BaseNode
│   value, __repr__
│
├── LinearNode          next
├── BiLinearNode        prev, next
└── TreeNode            left, right, parent


BaseCollection
│   clear, copy
│   __len__, __bool__, __iter__, __reversed__, __contains__, __repr__
│
├── BaseArray
│   │   __getitem__, __setitem__
│   ├── BaseStaticArray    capacity (property), is_full
│   └── BaseDynamicArray   append, insert, remove
│
├── BaseStack
│   │   push, pop, peek, is_empty
│   └── BaseBoundedStack   capacity (property), is_full
│
├── BaseQueue
│   │   enqueue, dequeue, peek, is_empty
│   └── BaseBoundedQueue   capacity (property), is_full
│
├── BaseDeque
│   │   push_front, push_back, pop_front, pop_back
│   │   peek_front, peek_back, is_empty
│   └── BaseBoundedDeque   capacity (property), is_full
│
├── BasePriorityQueue
│       enqueue(value, priority), dequeue, peek, is_empty
│
├── BaseLinkedList
│       append, prepend, insert, remove, index
│       __getitem__, __setitem__
│
├── BaseTree
│       insert, search, delete, height
│
├── BaseGraph
│       add_vertex, add_edge, remove_vertex, remove_edge
│       get_neighbors, has_vertex, has_edge
│
├── BaseHashTable
│       put, get, delete, contains_key
│       __getitem__, __setitem__
│
└── BaseHeap
        push, pop, peek, is_empty
```

---

## BaseNode

Root ABC for all node types. Nodes are the building blocks of linked structures.
Stores a single `value` and defines the `__repr__` contract.

Subclasses add neighbor references and implement `__repr__`:

```python
# nodes/linear_node.py
class LinearNode(BaseNode):
    __slots__ = ("value", "next")
    ...

# nodes/bi_linear_node.py
class BiLinearNode(BaseNode):
    __slots__ = ("value", "prev", "next")
    ...

# nodes/tree_node.py
class TreeNode(BaseNode):
    __slots__ = ("value", "left", "right", "parent")
    ...
```

---

## BaseCollection

Root ABC for all collection types. Every data structure in this library
inherits from `BaseCollection`, directly or through a specialized subclass.

**Required methods:**

| Method         | Description                                    |
| -------------- | ---------------------------------------------- |
| `clear()`      | Removes all elements                           |
| `copy()`       | Returns a shallow copy                         |
| `__len__`      | Number of elements currently in the collection |
| `__bool__`     | `True` if not empty                            |
| `__iter__`     | Yields elements in natural order               |
| `__reversed__` | Yields elements in reverse order               |
| `__contains__` | `True` if value exists                         |
| `__repr__`     | String representation                          |

---

## BaseArray / BaseStaticArray / BaseDynamicArray

Extends `BaseCollection` with index-based access via `__getitem__` and `__setitem__`.

`BaseStaticArray` adds `capacity` property and `is_full()` — for fixed-size buffers.

`BaseDynamicArray` adds `append`, `insert`, `remove` — for resizable buffers.

**Concrete implementations:**

| Class                   | ABC                |
| ----------------------- | ------------------ |
| `StaticUniversalArray`  | `BaseStaticArray`  |
| `StaticTypedArray`      | `BaseStaticArray`  |
| `DynamicUniversalArray` | `BaseDynamicArray` |
| `DynamicTypedArray`     | `BaseDynamicArray` |

---

## BaseStack / BaseBoundedStack

Defines the LIFO interface: `push`, `pop`, `peek`, `is_empty`.

`BaseBoundedStack` adds `capacity` property and `is_full()` for fixed-size stacks.

```python
s = StaticUniversalStack(5)   # inherits BaseBoundedStack
s = NodeStack()               # inherits BaseStack
```

**Concrete implementations:**

| Class                   | ABC                |
| ----------------------- | ------------------ |
| `StaticUniversalStack`  | `BaseBoundedStack` |
| `StaticTypedStack`      | `BaseBoundedStack` |
| `DynamicUniversalStack` | `BaseStack`        |
| `DynamicTypedStack`     | `BaseStack`        |
| `NodeStack`             | `BaseStack`        |

---

## BaseQueue / BaseBoundedQueue / BaseDeque / BasePriorityQueue

`BaseQueue` defines the FIFO interface: `enqueue`, `dequeue`, `peek`, `is_empty`.

`BaseBoundedQueue` adds `capacity` property and `is_full()` for static variants.

`BaseDeque` defines a separate interface for double-ended queues:
`push_front`, `push_back`, `pop_front`, `pop_back`, `peek_front`, `peek_back`.
Deques do not inherit from `BaseQueue` — their interface is different enough.

`BasePriorityQueue` redefines `enqueue(value, priority)` — the signature differs
from `BaseQueue.enqueue(value)`, so it is a separate ABC.

---

## BaseLinkedList

Extends `BaseCollection` with positional access and mutation:
`append`, `prepend`, `insert`, `remove`, `index`, `__getitem__`, `__setitem__`.

**Concrete implementations:**

| Class                      | ABC              |
| -------------------------- | ---------------- |
| `SinglyLinkedList`         | `BaseLinkedList` |
| `DoublyLinkedList`         | `BaseLinkedList` |
| `CircularSinglyLinkedList` | `BaseLinkedList` |
| `CircularDoublyLinkedList` | `BaseLinkedList` |

---

## BaseTree

Extends `BaseCollection` with: `insert`, `search`, `delete`, `height`.
Iteration yields values in **inorder** (left → root → right).

**Concrete implementations:**

| Class        | ABC        |
| ------------ | ---------- |
| `BinaryTree` | `BaseTree` |
| `BST`        | `BaseTree` |
| `AVLTree`    | `BaseTree` |

---

## BaseGraph

Extends `BaseCollection` with:
`add_vertex`, `add_edge`, `remove_vertex`, `remove_edge`,
`get_neighbors`, `has_vertex`, `has_edge`.

Iteration yields all vertices. `__contains__` checks vertex existence.

**Concrete implementations:**

| Class                  | ABC         |
| ---------------------- | ----------- |
| `AdjacencyListGraph`   | `BaseGraph` |
| `AdjacencyMatrixGraph` | `BaseGraph` |

---

## BaseHashTable

Extends `BaseCollection` with:
`put`, `get`, `delete`, `contains_key`, `__getitem__`, `__setitem__`.

Iteration yields all **keys**. `__contains__` checks key existence.

**Concrete implementations:**

| Class                     | ABC             |
| ------------------------- | --------------- |
| `ChainingHashTable`       | `BaseHashTable` |
| `OpenAddressingHashTable` | `BaseHashTable` |

---

## BaseHeap

Extends `BaseCollection` with: `push`, `pop`, `peek`, `is_empty`.
The top element is always the min (min-heap) or max (max-heap).

Iteration yields elements in **heap order** (level-order), not sorted order.
Use `pop()` repeatedly to consume in priority order.

**Concrete implementations:**

| Class     | ABC        |
| --------- | ---------- |
| `MinHeap` | `BaseHeap` |
| `MaxHeap` | `BaseHeap` |

---

## Notes

- All ABCs use only `from abc import ABC, abstractmethod` — no runtime logic.
- No `__slots__` in ABCs — slots are the responsibility of concrete classes.
- `BaseDeque` and `BasePriorityQueue` do **not** inherit from `BaseQueue`
  because their method signatures differ from the standard FIFO interface.
- `isinstance(obj, BaseCollection)` returns `True` for any object in this library.
