# Queues

Seventeen queue implementations organized into four families: **simple**, **circular**, **deque**, and **priority**.

```
queues/
├── simple/
│   ├── array_based/
│   │   ├── static/
│   │   │   ├── typed.py      # fixed-size, single dtype, O(n) dequeue
│   │   │   └── universal.py  # fixed-size, any type, O(n) dequeue
│   │   └── dynamic/
│   │       ├── typed.py      # auto-growing, single dtype, O(n) dequeue
│   │       └── universal.py  # auto-growing, any type, O(n) dequeue
│   └── node_based/
│       └── node_based.py     # linked nodes, any type, O(1) enqueue/dequeue
├── circular/
│   ├── array_based/
│   │   └── static/
│   │       ├── typed.py      # fixed-size, single dtype, O(1) enqueue/dequeue
│   │       └── universal.py  # fixed-size, any type, O(1) enqueue/dequeue
│   └── node_based/
│       └── node_based.py     # linked nodes, circular chain, O(1) enqueue/dequeue
├── deque/
│   ├── array_based/
│   │   ├── static/
│   │   │   ├── typed.py              # fixed-size, typed, O(n) front ops
│   │   │   ├── universal.py          # fixed-size, universal, O(n) front ops
│   │   │   ├── circular_typed.py     # fixed-size, typed, O(1) both ends
│   │   │   └── circular_universal.py # fixed-size, universal, O(1) both ends
│   │   └── dynamic/
│   │       ├── typed.py      # auto-growing, typed, O(n) front ops
│   │       └── universal.py  # auto-growing, universal, O(n) front ops
│   └── node_based/
│       ├── node_based.py          # doubly linked, O(1) both ends
│       └── circular_node_based.py # sentinel circular, O(1) both ends
└── priority/
    ├── max_priority.py   # highest priority number dequeues first
    └── min_priority.py   # lowest priority number dequeues first
```

---

## Simple vs Circular vs Deque vs Priority

**Simple Queue** is a basic FIFO structure. Enqueue adds to the rear, dequeue removes from the front. In array-based implementations the front is always index 0 — every dequeue requires shifting all remaining elements left: **O(n)**.

```
enqueue(1) → [1]
enqueue(2) → [1, 2]
enqueue(3) → [1, 2, 3]
dequeue()  → 1,  queue: [2, 3]  ← all elements shifted left: O(n)
```

**Circular Queue** solves the shifting problem by using two pointers (`_front`, `_rear`) that advance with modulo arithmetic over a fixed buffer. Both enqueue and dequeue are **O(1)** — no element shifting ever occurs.

```
capacity=5, after enqueue(1, 2, 3) then dequeue():
    buffer:  [_, 2, 3, _, _]
    _front=1, _rear=3, _size=2
    next enqueue → index 3, next dequeue → index 1
```

**Deque** (Double-Ended Queue) allows insertion and removal from **both** the front and the rear. Circular deques achieve O(1) on all four operations. Non-circular static deques achieve O(1) on rear operations but O(n) on front operations (element shifting).

```
enqueue_front(0) → [0, 1, 2, 3]
enqueue_rear(4)  → [0, 1, 2, 3, 4]
dequeue_front()  → 0,  deque: [1, 2, 3, 4]
dequeue_rear()   → 4,  deque: [1, 2, 3]
```

**Priority Queue** orders elements by a numeric priority rather than insertion order. `MaxPriorityQueue` dequeues the element with the **highest** priority number first; `MinPriorityQueue` dequeues the element with the **lowest** priority number first. Both are heap-backed and grow automatically.

```python
q = MaxPriorityQueue()
q.enqueue("low",  priority=1)
q.enqueue("high", priority=10)
q.dequeue()  # → "high"   (priority=10 comes out first)

q = MinPriorityQueue()
q.enqueue("urgent", priority=1)
q.enqueue("later",  priority=5)
q.dequeue()  # → "urgent"  (priority=1 comes out first)
```

---

## Quick Reference

### Simple Queues

| Class                   | Bounded | Type-safe | Backed by               | dequeue |
| ----------------------- | ------- | --------- | ----------------------- | ------- |
| `StaticUniversalQueue`  | ✓       | ✗         | `StaticUniversalArray`  | O(n)    |
| `StaticTypedQueue`      | ✓       | ✓         | `StaticTypedArray`      | O(n)    |
| `DynamicUniversalQueue` | ✗       | ✗         | `DynamicUniversalArray` | O(n)    |
| `DynamicTypedQueue`     | ✗       | ✓         | `DynamicTypedArray`     | O(n)    |
| `NodeQueue`             | ✗       | ✗         | `LinearNode` chain      | O(1)    |

### Circular Queues

| Class                          | Bounded | Type-safe | Backed by              | dequeue |
| ------------------------------ | ------- | --------- | ---------------------- | ------- |
| `StaticUniversalCircularQueue` | ✓       | ✗         | `StaticUniversalArray` | O(1)    |
| `StaticTypedCircularQueue`     | ✓       | ✓         | `StaticTypedArray`     | O(1)    |
| `NodeCircularQueue`            | ✗       | ✗         | `LinearNode` chain     | O(1)    |

### Deques

| Class                          | Bounded | Type-safe | Circular | Backed by                 |
| ------------------------------ | ------- | --------- | -------- | ------------------------- |
| `StaticUniversalDeque`         | ✓       | ✗         | ✗        | `StaticUniversalArray`    |
| `StaticTypedDeque`             | ✓       | ✓         | ✗        | `StaticTypedArray`        |
| `StaticUniversalCircularDeque` | ✓       | ✗         | ✓        | `StaticUniversalArray`    |
| `StaticTypedCircularDeque`     | ✓       | ✓         | ✓        | `StaticTypedArray`        |
| `DynamicUniversalDeque`        | ✗       | ✗         | ✗        | `DynamicUniversalArray`   |
| `DynamicTypedDeque`            | ✗       | ✓         | ✗        | `DynamicTypedArray`       |
| `NodeDeque`                    | ✗       | ✗         | ✗        | `BiLinearNode` chain      |
| `CircularNodeDeque`            | ✗       | ✗         | ✓        | `BiLinearNode` + sentinel |

### Priority Queues

| Class              | Order                | Backed by                 |
| ------------------ | -------------------- | ------------------------- |
| `MaxPriorityQueue` | Highest number first | `DynamicUniversalMaxHeap` |
| `MinPriorityQueue` | Lowest number first  | `DynamicUniversalMinHeap` |

---

## Classes

### `NodeQueue(*args)`

An unbounded queue backed by a `LinearNode` chain.
Each enqueue allocates a new node at the rear; each dequeue releases the front node.
O(1) on all operations. No capacity limit.

```python
q = NodeQueue()
q = NodeQueue(1, 2, 3)  # front=1, rear=3
q.enqueue(4)
q.dequeue()  # → 1
q.peek()     # → 2
```

---

### `DynamicUniversalQueue(*args)`

An unbounded queue backed by `DynamicUniversalArray`. Accepts any Python type.
Front is always index 0 — dequeue shifts all elements left: **O(n)**.

```python
q = DynamicUniversalQueue()
q = DynamicUniversalQueue(1, "hi", 3.0)  # front=1
q.enqueue("new")
q.dequeue()  # → 1
```

---

### `DynamicTypedQueue(dtype, *args, str_length=None)`

An unbounded queue backed by `DynamicTypedArray`. Enforces a single dtype.
Supported dtypes: `int`, `float`, `bool`, `str`.

```python
q = DynamicTypedQueue(int)
q = DynamicTypedQueue(int, 1, 2, 3)       # front=1
q = DynamicTypedQueue(str, str_length=50)
q.enqueue(4)
q.dequeue()  # → 1
```

---

### `StaticUniversalQueue(*args, capacity=None)`

A fixed-capacity queue backed by `StaticUniversalArray`. Accepts any Python type.
At least one of `capacity` or `*args` must be provided.

```python
q = StaticUniversalQueue(capacity=5)
q = StaticUniversalQueue(1, 2, 3, capacity=5)  # front=1, capacity=5
q.enqueue(4)
q.dequeue()   # → 1
q.is_full()   # → False
```

---

### `StaticTypedQueue(dtype, *args, capacity=None, str_length=None)`

A fixed-capacity queue backed by `StaticTypedArray`. Enforces a single dtype.
At least one of `capacity` or `*args` must be provided.

```python
q = StaticTypedQueue(int, capacity=5)
q = StaticTypedQueue(int, 1, 2, 3, capacity=5)  # front=1
q.enqueue(4)
q.dequeue()   # → 1
q.is_full()   # → False
```

---

### `StaticUniversalCircularQueue(*args, capacity=None)`

A fixed-capacity circular queue backed by `StaticUniversalArray`.
Uses modulo arithmetic — both enqueue and dequeue are **O(1)**.
At least one of `capacity` or `*args` must be provided.

```python
q = StaticUniversalCircularQueue(capacity=5)
q = StaticUniversalCircularQueue(1, 2, 3, capacity=5)  # front=1
q.enqueue(4)
q.dequeue()  # → 1   (O(1), no shifting)
```

---

### `StaticTypedCircularQueue(dtype, *args, capacity=None, str_length=None)`

A fixed-capacity circular queue backed by `StaticTypedArray`. Enforces a single dtype.
Both enqueue and dequeue are **O(1)**.

```python
q = StaticTypedCircularQueue(int, capacity=5)
q = StaticTypedCircularQueue(int, 1, 2, 3, capacity=5)  # front=1
q.enqueue(4)
q.dequeue()  # → 1   (O(1), no shifting)
```

---

### `NodeCircularQueue(*args)`

A dynamic circular queue backed by a `LinearNode` chain.
Uses a single `_rear` pointer — `_rear.next` is always the front.
Both enqueue and dequeue are **O(1)**.

```python
q = NodeCircularQueue()
q = NodeCircularQueue(1, 2, 3)  # front=1, rear=3
q.enqueue(4)
q.dequeue()  # → 1
q.peek()     # → 2
```

---

### `NodeDeque(*args)`

A dynamic deque backed by a `BiLinearNode` doubly-linked chain.
All four operations (enqueue/dequeue front/rear) are **O(1)**.
No capacity limit.

```python
d = NodeDeque()
d = NodeDeque(1, 2, 3)   # front=1, rear=3
d.enqueue_front(0)
d.enqueue_rear(4)
d.dequeue_front()   # → 0
d.dequeue_rear()    # → 4
d.peek_front()      # → 1
d.peek_rear()       # → 3
```

---

### `CircularNodeDeque(*args)`

A dynamic circular deque backed by a `BiLinearNode` chain with a sentinel node.
The sentinel eliminates all empty-state edge cases — insertion and removal
logic is identical regardless of the number of elements.
All four operations are **O(1)**.

```python
d = CircularNodeDeque()
d = CircularNodeDeque(1, 2, 3)  # front=1, rear=3
d.enqueue_front(0)
d.dequeue_rear()   # → 3
d.peek_front()     # → 0
```

---

### `DynamicUniversalDeque(*args)`

An unbounded deque backed by `DynamicUniversalArray`. Accepts any Python type.
Rear operations are O(1) amortized; front operations require shifting: **O(n)**.

```python
d = DynamicUniversalDeque()
d = DynamicUniversalDeque(1, "hi", 3.0)  # front=1
d.enqueue_rear(4)
d.dequeue_front()   # → 1
```

---

### `DynamicTypedDeque(dtype, *args, str_length=None)`

An unbounded deque backed by `DynamicTypedArray`. Enforces a single dtype.
Supported dtypes: `int`, `float`, `bool`, `str`.

```python
d = DynamicTypedDeque(int)
d = DynamicTypedDeque(int, 1, 2, 3)  # front=1
d.enqueue_rear(4)
d.dequeue_front()   # → 1
```

---

### `StaticUniversalDeque(*args, capacity=None)`

A fixed-capacity deque backed by `StaticUniversalArray`. Non-circular.
Rear operations are O(1); front operations shift elements: **O(n)**.
At least one of `capacity` or `*args` must be provided.

```python
d = StaticUniversalDeque(capacity=5)
d = StaticUniversalDeque(1, 2, 3, capacity=5)  # front=1
d.enqueue_rear(4)
d.dequeue_front()   # → 1
d.is_full()         # → False
```

---

### `StaticTypedDeque(dtype, *args, capacity=None, str_length=None)`

A fixed-capacity deque backed by `StaticTypedArray`. Non-circular. Enforces a single dtype.
At least one of `capacity` or `*args` must be provided.

```python
d = StaticTypedDeque(int, capacity=5)
d = StaticTypedDeque(int, 1, 2, 3, capacity=5)  # front=1
d.enqueue_rear(4)
d.dequeue_front()   # → 1
d.is_full()         # → False
```

---

### `StaticUniversalCircularDeque(*args, capacity=None)`

A fixed-capacity circular deque backed by `StaticUniversalArray`.
Uses modulo arithmetic — all four operations are **O(1)**.
At least one of `capacity` or `*args` must be provided.

```python
d = StaticUniversalCircularDeque(capacity=5)
d = StaticUniversalCircularDeque(1, 2, 3, capacity=5)  # front=1
d.enqueue_front(0)
d.dequeue_rear()    # → 3   (O(1), no shifting)
```

---

### `StaticTypedCircularDeque(dtype, *args, capacity=None, str_length=None)`

A fixed-capacity circular deque backed by `StaticTypedArray`. Enforces a single dtype.
All four operations are **O(1)**.

```python
d = StaticTypedCircularDeque(int, capacity=5)
d = StaticTypedCircularDeque(int, 1, 2, 3, capacity=5)  # front=1
d.enqueue_front(0)
d.dequeue_rear()    # → 3   (O(1), no shifting)
```

---

### `MaxPriorityQueue(*args)`

A dynamic priority queue backed by `DynamicUniversalMaxHeap`.
Elements with the **highest** priority number dequeue first.
Values are wrapped in a `PriorityObject` internally — the caller never sees the wrapper.

```python
q = MaxPriorityQueue()
q = MaxPriorityQueue(("low", 1), ("high", 10))
q.enqueue("medium", priority=5)
q.dequeue()        # → "high"    (priority=10)
q.peek()           # → "medium"  (priority=5)
q.peek_priority()  # → 5
```

---

### `MinPriorityQueue(*args)`

A dynamic priority queue backed by `DynamicUniversalMinHeap`.
Elements with the **lowest** priority number dequeue first.

```python
q = MinPriorityQueue()
q = MinPriorityQueue(("send email", 2), ("fix bug", 1))
q.enqueue("meeting", priority=3)
q.dequeue()        # → "fix bug"     (priority=1)
q.peek()           # → "send email"  (priority=2)
q.peek_priority()  # → 2
```

---

## Supported Operations

### Simple Queues

| Operation      | NodeQueue | DynUniv        | DynTyped       | StatUniv | StatTyped |
| -------------- | --------- | -------------- | -------------- | -------- | --------- |
| `enqueue`      | O(1)      | O(1) amortized | O(1) amortized | O(1)     | O(1)      |
| `dequeue`      | O(1)      | O(n)           | O(n)           | O(n)     | O(n)      |
| `peek`         | O(1)      | O(1)           | O(1)           | O(1)     | O(1)      |
| `clear`        | O(1)      | O(1)\*         | O(n)           | O(n)     | O(n)      |
| `copy`         | O(n)      | O(n)           | O(n)           | O(n)     | O(n)      |
| `is_empty`     | O(1)      | O(1)           | O(1)           | O(1)     | O(1)      |
| `is_full`      | —         | —              | —              | O(1)     | O(1)      |
| `__len__`      | O(1)      | O(1)           | O(1)           | O(1)     | O(1)      |
| `__bool__`     | O(1)      | O(1)           | O(1)           | O(1)     | O(1)      |
| `__iter__`     | O(n)      | O(n)           | O(n)           | O(n)     | O(n)      |
| `__reversed__` | O(n)      | O(n)           | O(n)           | O(n)     | O(n)      |
| `__contains__` | O(n)      | O(n)           | O(n)           | O(n)     | O(n)      |
| `__eq__`       | O(n)      | O(n)           | O(n)           | O(n)     | O(n)      |
| `__repr__`     | O(n)      | O(n)           | O(n)           | O(n)     | O(n)      |

### Circular Queues

| Operation      | NodeCircular | StatUnivCircular | StatTypedCircular |
| -------------- | ------------ | ---------------- | ----------------- |
| `enqueue`      | O(1)         | O(1)             | O(1)              |
| `dequeue`      | O(1)         | O(1)             | O(1)              |
| `peek`         | O(1)         | O(1)             | O(1)              |
| `clear`        | O(1)         | O(n)             | O(n)              |
| `copy`         | O(n)         | O(n)             | O(n)              |
| `is_empty`     | O(1)         | O(1)             | O(1)              |
| `is_full`      | —            | O(1)             | O(1)              |
| `__iter__`     | O(n)         | O(n)             | O(n)              |
| `__reversed__` | O(n)         | O(n)             | O(n)              |
| `__contains__` | O(n)         | O(n)             | O(n)              |
| `__eq__`       | O(n)         | O(n)             | O(n)              |
| `__repr__`     | O(n)         | O(n)             | O(n)              |

### Deques

| Operation       | NodeDeque | CircNodeDeque | DynUniv        | DynTyped       | StatUniv | StatTyped | StatUnivCirc | StatTypedCirc |
| --------------- | --------- | ------------- | -------------- | -------------- | -------- | --------- | ------------ | ------------- |
| `enqueue_front` | O(1)      | O(1)          | O(n)           | O(n)           | O(n)     | O(n)      | O(1)         | O(1)          |
| `enqueue_rear`  | O(1)      | O(1)          | O(1) amortized | O(1) amortized | O(1)     | O(1)      | O(1)         | O(1)          |
| `dequeue_front` | O(1)      | O(1)          | O(n)           | O(n)           | O(n)     | O(n)      | O(1)         | O(1)          |
| `dequeue_rear`  | O(1)      | O(1)          | O(1)           | O(1)           | O(1)     | O(1)      | O(1)         | O(1)          |
| `peek_front`    | O(1)      | O(1)          | O(1)           | O(1)           | O(1)     | O(1)      | O(1)         | O(1)          |
| `peek_rear`     | O(1)      | O(1)          | O(1)           | O(1)           | O(1)     | O(1)      | O(1)         | O(1)          |
| `clear`         | O(1)      | O(1)          | O(1)\*         | O(n)           | O(n)     | O(n)      | O(n)         | O(n)          |
| `copy`          | O(n)      | O(n)          | O(n)           | O(n)           | O(n)     | O(n)      | O(n)         | O(n)          |
| `is_full`       | —         | —             | —              | —              | O(1)     | O(1)      | O(1)         | O(1)          |

### Priority Queues

| Operation       | MaxPriorityQueue | MinPriorityQueue |
| --------------- | ---------------- | ---------------- |
| `enqueue`       | O(log n)         | O(log n)         |
| `dequeue`       | O(log n)         | O(log n)         |
| `peek`          | O(1)             | O(1)             |
| `peek_priority` | O(1)             | O(1)             |
| `clear`         | O(1)             | O(1)             |
| `copy`          | O(n log n)       | O(n log n)       |
| `is_empty`      | O(1)             | O(1)             |
| `__iter__`      | O(n)             | O(n)             |
| `__reversed__`  | O(n)             | O(n)             |
| `__contains__`  | O(n)             | O(n)             |
| `__eq__`        | O(n)             | O(n)             |
| `__repr__`      | O(n)             | O(n)             |

\* `DynamicUniversalQueue.clear()` and `DynamicUniversalDeque.clear()` are O(1) — only the size counter is reset.
Typed and static `clear()` reset every slot to the dtype default to keep the underlying `ctypes` buffer consistent — hence O(n).

> All queues yield elements **front to rear** in `__iter__` and **rear to front** in `__reversed__`.
> Priority queue `__iter__` yields `(value, priority)` tuples in internal heap order — **not** sorted by priority.

---

## Design Decisions

### Simple vs Circular (array-based)

Simple queues pin the front at index 0. After each dequeue, every remaining element shifts one position left — **O(n)**. This is simple to implement but wasteful for high-throughput use.

Circular queues use two integer pointers (`_front`, `_rear`) that advance with `% capacity`. No shifting ever occurs — both enqueue and dequeue are **O(1)**. The trade-off is a fixed capacity: the buffer cannot grow.

### Non-circular vs Circular Deques

Non-circular static deques pin the rear at the end of the buffer. `enqueue_rear` and `dequeue_rear` are O(1); `enqueue_front` and `dequeue_front` require shifting: **O(n)**. Circular deques wrap both ends with modulo — all four operations are **O(1)**.

### `NodeCircularQueue` pointer invariant

`NodeCircularQueue` uses a single `_rear` pointer. The circular invariant is that `_rear.next` is always the front. Enqueue inserts a new node between `_rear` and `_rear.next` then advances `_rear`; dequeue removes `_rear.next`. This gives O(1) access to both ends through just one pointer.

### `CircularNodeDeque` sentinel

`CircularNodeDeque` uses a permanent sentinel node that is never removed. The sentinel's `next` always points to the front and its `prev` always points to the rear. An empty deque has the sentinel pointing to itself on both sides. The sentinel eliminates all `None` checks from insertion and removal code — the logic is the same regardless of whether the deque has zero or a thousand elements.

### `PriorityObject` and heap ordering

`MaxPriorityQueue` and `MinPriorityQueue` wrap each `(value, priority)` pair in a `PriorityObject` before pushing it onto a `DynamicUniversalMaxHeap` or `DynamicUniversalMinHeap`. `PriorityObject` defines `__gt__` and `__lt__` based solely on the priority number — the heap never compares values directly. The wrapper is stripped before returning from `dequeue()` and `peek()`, so callers always receive the raw value.

### `__eq__` in priority queues

Two priority queues built from the same elements in different insertion orders may produce different internal heap arrangements. `__eq__` compares internal positions, not logical dequeue order.

---

## `__repr__` Formats

```
NodeQueue(size=3)[1, 2, 3]
                  front  rear

DynamicUniversalQueue(size=3)[1, 'hi', 3.0]
DynamicTypedQueue(int, size=3)[1, 2, 3]

StaticUniversalQueue(size=3, capacity=5)[1, 2, 3]
StaticTypedQueue(int, size=3, capacity=5)[1, 2, 3]

NodeCircularQueue(size=3)[1, 2, 3]
StaticUniversalCircularQueue(size=3, capacity=5)[1, 2, 3]
StaticTypedCircularQueue(int, size=3, capacity=5)[1, 2, 3]

NodeDeque(size=3)[1, 2, 3]
CircularNodeDeque(size=3)[1, 2, 3]
DynamicUniversalDeque(size=3)[1, 2, 3]
DynamicTypedDeque(int, size=3)[1, 2, 3]

StaticUniversalDeque(size=3, capacity=5)[1, 2, 3]
StaticTypedDeque(int, size=3, capacity=5)[1, 2, 3]
StaticUniversalCircularDeque(size=3, capacity=5)[1, 2, 3]
StaticTypedCircularDeque(int, size=3, capacity=5)[1, 2, 3]

MaxPriorityQueue(size=2)[(value='high', priority=10), (value='low', priority=1)]
MinPriorityQueue(size=2)[(value='urgent', priority=1), (value='later', priority=5)]
```
