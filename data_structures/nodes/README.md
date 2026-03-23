# Nodes

Two node types used as building blocks for all linked data structures.

```
nodes/
├── single.py   # SingleNode — holds value + next
└── double.py   # DoubleNode — holds value + next + prev
```

---

## Class Overview

### `SingleNode(value)`
A node with a reference to the next node only.
Used by: `SinglyLinkedList`, `CircularSinglyLinkedList`, node-based stacks and queues.

```python
node = SingleNode(42)
node = SingleNode("hello")

a = SingleNode(1)
b = SingleNode(2)
a.next = b          # 1 -> 2
```

**Attributes:**
- `value` — any Python object
- `next` — next `SingleNode` or `None`

**`__repr__` format:**
```
SingleNode(42) -> None
SingleNode(42) -> 10     # when next is set
```

### `DoubleNode(value)`
A node with references to both next and previous nodes.
Used by: `DoublyLinkedList`, `CircularDoublyLinkedList`, node-based deques.

```python
node = DoubleNode(42)

a = DoubleNode(1)
b = DoubleNode(2)
a.next = b
b.prev = a          # 1 <-> 2
```

**Attributes:**
- `value` — any Python object
- `next` — next `DoubleNode` or `None`
- `prev` — previous `DoubleNode` or `None`

**`__repr__` format:**
```
None <-> DoubleNode(42) <-> None
1 <-> DoubleNode(42) <-> None     # when prev is set
None <-> DoubleNode(42) <-> 99    # when next is set
1 <-> DoubleNode(42) <-> 99       # when both are set
```

---

## Time Complexity

| Method     | Complexity |
|------------|------------|
| `__init__` | O(1)       |
| `__repr__` | O(1)       |

---

## Notes

- Both nodes use `__slots__` for lower memory overhead.
- Nodes themselves do not validate their `next` / `prev` references —
  that responsibility belongs to the data structure using them.
- `value` accepts any Python object including `None`.