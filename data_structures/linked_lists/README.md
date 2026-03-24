# Linked Lists

Four linked list implementations split along two axes: **singly vs doubly** linked
and **linear vs circular**.

```
linked_lists/
├── single/
│   └── single.py            # SinglyLinkedList
├── double/
│   └── double.py            # DoublyLinkedList
└── circular/
    ├── single.py            # CircularSinglyLinkedList
    └── double.py            # CircularDoublyLinkedList
```

---

## Class Overview

### `SinglyLinkedList(*args)`

Linear list. Each node holds `value` and `next`.
`__reversed__` builds a temporary reversed `SingleNode` chain, then traverses it.

```python
lst = SinglyLinkedList()           # empty
lst = SinglyLinkedList(1, 2, 3)    # 1 -> 2 -> 3
```

### `DoublyLinkedList(*args)`

Linear list. Each node holds `value`, `next`, and `prev`.
`_get_node` starts from `tail` when the index is closer to the end — O(n/2).
`__reversed__` traverses from `tail` using `prev` pointers — no extra memory.

```python
lst = DoublyLinkedList()           # empty
lst = DoublyLinkedList(1, 2, 3)    # 1 <-> 2 <-> 3
```

### `CircularSinglyLinkedList(*args)`

Circular list. `tail.next` always points back to `head` — no `None` terminator.
`__iter__` and `__reversed__` use a step counter instead of a `None` check to
avoid infinite loops.

```python
lst = CircularSinglyLinkedList()           # empty
lst = CircularSinglyLinkedList(1, 2, 3)    # 1 -> 2 -> 3 -> (head)
```

### `CircularDoublyLinkedList(*args)`

Circular list. `tail.next → head` and `head.prev → tail` at all times.
`_get_node` starts from `tail` when the index is closer to the end — O(n/2).
`__reversed__` traverses from `tail` using `prev` pointers with a step counter.

```python
lst = CircularDoublyLinkedList()           # empty
lst = CircularDoublyLinkedList(1, 2, 3)    # ... <-> 1 <-> 2 <-> 3 <-> ...
```

---

## Supported Operations

All four classes expose the same public interface:

| Operation      | Singly | Doubly | Circ. Singly | Circ. Doubly |
| -------------- | ------ | ------ | ------------ | ------------ |
| `append`       | O(1)   | O(1)   | O(1)         | O(1)         |
| `prepend`      | O(1)   | O(1)   | O(1)         | O(1)         |
| `insert`       | O(n)   | O(n/2) | O(n)         | O(n/2)       |
| `remove`       | O(n)   | O(n/2) | O(n)         | O(n/2)       |
| `index`        | O(n)   | O(n)   | O(n)         | O(n)         |
| `clear`        | O(1)   | O(1)   | O(1)         | O(1)         |
| `copy`         | O(n)   | O(n)   | O(n)         | O(n)         |
| `__getitem__`  | O(n)   | O(n/2) | O(n)         | O(n/2)       |
| `__setitem__`  | O(n)   | O(n/2) | O(n)         | O(n/2)       |
| `__len__`      | O(1)   | O(1)   | O(1)         | O(1)         |
| `__bool__`     | O(1)   | O(1)   | O(1)         | O(1)         |
| `__iter__`     | O(n)   | O(n)   | O(n)         | O(n)         |
| `__reversed__` | O(n)   | O(n)   | O(n)         | O(n)         |
| `__contains__` | O(n)   | O(n)   | O(n)         | O(n)         |
| `__repr__`     | O(n)   | O(n)   | O(n)         | O(n)         |

---

## Internal Helpers

| Helper                    | Singly  | Doubly    | Circ. Singly | Circ. Doubly |
| ------------------------- | ------- | --------- | ------------ | ------------ |
| `_get_node(index)`        | ✅ O(n) | ✅ O(n/2) | ✅ O(n)      | ✅ O(n/2)    |
| `_set_node(index, value)` | ✅      | ✅        | ✅           | ✅           |
| `_append_to_empty(node)`  | ✅      | ✅        | ✅ circular  | ✅ circular  |
| `_link_nodes(a, b)`       | —       | ✅        | —            | ✅           |
| `_unlink_node(node)`      | —       | ✅        | —            | ✅           |

`_append_to_empty` in circular variants additionally sets `node.next = node`
(singly) or `node.next = node.prev = node` (doubly) to establish the circular
invariant from the start.

`_unlink_node` in `DoublyLinkedList` guards against `None` prev/next.
In `CircularDoublyLinkedList` no guard is needed — every node always has
valid `prev` and `next` references.

---

## `index(value) -> int`

Returns the index of the first node whose value equals `value`.
Raises `ValueError` if no such node exists — same as Python's built-in `list.index()`.

```python
lst = SinglyLinkedList(10, 20, 30)
lst.index(20)   # → 1
lst.index(99)   # → raises ValueError: 99 is not in list
```

`__contains__` delegates to `index()` internally via try/except.

---

## `clear()`

Removes all nodes by dropping head and tail references.
O(1) — no traversal needed.

```python
lst = DoublyLinkedList(1, 2, 3)
lst.clear()
len(lst)   # → 0
bool(lst)  # → False
```

---

## `copy() -> SameType`

Returns a shallow copy of the list preserving order.
The copy is a fully independent new instance — modifying it does not affect the original.
For circular variants, the circular invariant is maintained in the copy.

```python
lst = CircularSinglyLinkedList(1, 2, 3)
c = lst.copy()
c.append(4)
len(lst)  # → 3  (original unchanged)
```

---

## Negative Indexing

All methods that accept an index support negative indexing via `validate_index`
and `validate_insert_index` from `data_structures.tools`.

```python
lst = DoublyLinkedList(1, 2, 3)
lst[-1]             # → 3
lst.remove(-1)      # removes 3
lst.insert(-1, 99)  # inserts before the last element
```

---

## `__repr__` Formats

```
SinglyLinkedList(size=3)[1 -> 2 -> 3]
DoublyLinkedList(size=3)[1 <-> 2 <-> 3]
CircularSinglyLinkedList(size=3)[1 -> 2 -> 3 -> ...]
CircularDoublyLinkedList(size=3)[... <-> 1 <-> 2 <-> 3 <-> ...]
```
