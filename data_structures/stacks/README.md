# Stacks

Ten stack implementations split along three axes: **static vs dynamic**, **typed vs universal**, and **regular vs min**.

```
stacks/
├── array_based/
│   ├── static/
│   │   ├── typed.py      # fixed-size, single dtype
│   │   └── universal.py  # fixed-size, any type
│   └── dynamic/
│       ├── typed.py      # auto-growing, single dtype
│       └── universal.py  # auto-growing, any type
├── node_based/
│   └── node_based.py     # linked nodes, any type, unbounded
└── min_stacks/
    ├── array_based/
    │   ├── static/
    │   │   ├── typed.py      # fixed-size, single dtype, O(1) min
    │   │   └── universal.py  # fixed-size, any type, O(1) min
    │   └── dynamic/
    │       ├── typed.py      # auto-growing, single dtype, O(1) min
    │       └── universal.py  # auto-growing, any type, O(1) min
    └── node_based/
        └── node_based.py     # linked nodes, any type, O(1) min
```

---

## Stack vs Min Stack

A regular stack is a **LIFO** (Last In, First Out) structure — elements are pushed onto the top and popped from the top. Finding the minimum requires scanning every element: **O(n)**.

```
push(3) → [3]
push(1) → [1, 3]
push(2) → [2, 1, 3]
pop()   → 2,  stack: [1, 3]

min?  → must scan [1, 3] → O(n)
```

A **Min Stack** extends the regular stack with a `min()` method that returns the current minimum in **O(1)** at all times — even as elements are pushed and popped. It achieves this by maintaining a second internal structure (`_min_data`) that tracks the running minimum in parallel with the main data.

```
push(3) → main: [3],       min_data: [3]          ← 3 enters min_data (empty)
push(1) → main: [1, 3],    min_data: [1, 3]        ← 1 ≤ 3, enters min_data
push(2) → main: [2, 1, 3], min_data: [1, 3]        ← 2 > 1, skipped
pop()   → 2,   main: [1, 3], min_data: [1, 3]      ← key(2) ≠ key(1), min unchanged
pop()   → 1,   main: [3],    min_data: [3]          ← key(1) == key(1), min also pops

min() → 3   ← O(1), always
```

The rule is simple:

- **push**: value enters `_min_data` only if `key(value) <= key(current_min)`.
- **pop**: if `key(popped) == key(current_min)`, pop from `_min_data` too.
- **min**: always peek at the top of `_min_data`.

This costs one extra pointer or array slot per pushed minimum — memory overhead
is O(n) in the worst case (strictly descending input), O(1) amortized for random data.

### The `key` function

Both regular stacks and min stacks store any comparable value. Min stacks additionally
accept an optional `key` callable that maps each value to a comparable key before any
comparison is made. This lets you track the minimum by any criterion without changing
your data.

```python
# Default: identity — compares values directly
s = NodeMinStack(3, 1, 2)
s.min()  # → 1

# Negative key: treats largest raw value as the "minimum"
s = NodeMinStack(3, 1, 2, key=lambda x: -x)
s.min()  # → 3

# Keyed by second element of a tuple
s = NodeMinStack(("b", 5), ("a", 2), ("c", 8), key=lambda x: x[1])
s.min()  # → ("a", 2)
```

When `key=None` (the default), the identity function `lambda x: x` is used automatically.

---

## Quick Reference

### Regular Stacks

| Class                   | Bounded | Type-safe | Backed by               |
| ----------------------- | ------- | --------- | ----------------------- |
| `StaticUniversalStack`  | ✓       | ✗         | `StaticUniversalArray`  |
| `StaticTypedStack`      | ✓       | ✓         | `StaticTypedArray`      |
| `DynamicUniversalStack` | ✗       | ✗         | `DynamicUniversalArray` |
| `DynamicTypedStack`     | ✗       | ✓         | `DynamicTypedArray`     |
| `NodeStack`             | ✗       | ✗         | `LinearNode` chain      |

### Min Stacks

| Class                      | Bounded | Type-safe | Backed by                    |
| -------------------------- | ------- | --------- | ---------------------------- |
| `StaticUniversalMinStack`  | ✓       | ✗         | two `StaticUniversalArray`s  |
| `StaticTypedMinStack`      | ✓       | ✓         | two `StaticTypedArray`s      |
| `DynamicUniversalMinStack` | ✗       | ✗         | two `DynamicUniversalArray`s |
| `DynamicTypedMinStack`     | ✗       | ✓         | two `DynamicTypedArray`s     |
| `NodeMinStack`             | ✗       | ✗         | two `LinearNode` chains      |

---

## Classes

### `NodeStack(*args)`

An unbounded stack backed by a `LinearNode` chain.
Each push allocates a new node; each pop releases it.
No capacity limit, no resize overhead.

```python
s = NodeStack()           # empty
s = NodeStack(1, 2, 3)    # top=3
s.push(4)
s.pop()    # → 4
s.peek()   # → 3
```

---

### `DynamicUniversalStack(*args)`

An unbounded stack backed by `DynamicUniversalArray`.
Accepts any Python type. Grows automatically using CPython's growth formula.

```python
s = DynamicUniversalStack()
s = DynamicUniversalStack(1, "hi", 3.0)  # top=3.0
s.push(True)
s.pop()   # → True
```

---

### `DynamicTypedStack(dtype, *args, str_length=None)`

An unbounded stack backed by `DynamicTypedArray`.
Enforces a single dtype for all elements. Grows automatically.
Supported dtypes: `int`, `float`, `bool`, `str`.

```python
s = DynamicTypedStack(int)
s = DynamicTypedStack(int, 1, 2, 3)  # top=3
s = DynamicTypedStack(str, str_length=50)
s.push(4)
s.pop()   # → 4
```

---

### `StaticUniversalStack(*args, capacity=None)`

A fixed-capacity stack backed by `StaticUniversalArray`.
Accepts any Python type. At least one of `capacity` or `*args` must be provided.

```python
s = StaticUniversalStack(capacity=5)
s = StaticUniversalStack(1, "hi", 3, capacity=5)  # top=3, capacity=5
s.push(4)
s.pop()     # → 4
s.is_full() # → False
```

---

### `StaticTypedStack(dtype, *args, capacity=None, str_length=None)`

A fixed-capacity stack backed by `StaticTypedArray`.
Enforces a single dtype. At least one of `capacity` or `*args` must be provided.

```python
s = StaticTypedStack(int, capacity=5)
s = StaticTypedStack(int, 1, 2, 3, capacity=5)  # top=3
s.push(4)
s.pop()     # → 4
s.is_full() # → False
```

---

### `NodeMinStack(*args, key=None)`

An unbounded min stack backed by two `LinearNode` chains: `_head` (main) and `_min_head` (min).
Accepts any Python type. O(1) on all operations.

```python
s = NodeMinStack()
s = NodeMinStack(3, 1, 2)           # top=2, min=1
s = NodeMinStack(3, 1, 2, key=lambda x: -x)  # max-as-min behaviour
s.push(0)
s.pop()   # → 0
s.min()   # → 1
```

---

### `DynamicUniversalMinStack(*args, key=None)`

An unbounded min stack backed by two `DynamicUniversalArray`s.
Accepts any Python type. Grows automatically.

```python
s = DynamicUniversalMinStack()
s = DynamicUniversalMinStack(3, 1, 2)   # top=2, min=1
s.push(0)
s.min()   # → 0
s.pop()   # → 0
s.min()   # → 1
```

---

### `DynamicTypedMinStack(dtype, *args, str_length=None, key=None)`

An unbounded min stack backed by two `DynamicTypedArray`s.
Enforces a single dtype. Grows automatically.

```python
s = DynamicTypedMinStack(int)
s = DynamicTypedMinStack(int, 3, 1, 2)   # top=2, min=1
s = DynamicTypedMinStack(int, key=lambda x: -x)
s.push(0)
s.min()   # → 0
```

---

### `StaticUniversalMinStack(*args, capacity=None, key=None)`

A fixed-capacity min stack backed by two `StaticUniversalArray`s.
Accepts any Python type. At least one of `capacity` or `*args` must be provided.

```python
s = StaticUniversalMinStack(capacity=5)
s = StaticUniversalMinStack(3, 1, 2, capacity=5)  # top=2, min=1
s.push(0)
s.min()     # → 0
s.is_full() # → False
```

---

### `StaticTypedMinStack(dtype, *args, capacity=None, str_length=None, key=None)`

A fixed-capacity min stack backed by two `StaticTypedArray`s.
Enforces a single dtype. At least one of `capacity` or `*args` must be provided.

```python
s = StaticTypedMinStack(int, capacity=5)
s = StaticTypedMinStack(int, 3, 1, 2, capacity=5)  # top=2, min=1
s.push(0)
s.min()     # → 0
s.is_full() # → False
```

---

## Supported Operations

### Regular Stacks

| Operation      | Node | DynUniv        | DynTyped       | StatUniv | StatTyped |
| -------------- | ---- | -------------- | -------------- | -------- | --------- |
| `push`         | O(1) | O(1) amortized | O(1) amortized | O(1)     | O(1)      |
| `pop`          | O(1) | O(1)           | O(1)           | O(1)     | O(1)      |
| `peek`         | O(1) | O(1)           | O(1)           | O(1)     | O(1)      |
| `clear`        | O(n) | O(n)           | O(n)\*         | O(n)\*   | O(n)\*    |
| `copy`         | O(n) | O(n)           | O(n)           | O(n)     | O(n)      |
| `is_empty`     | O(1) | O(1)           | O(1)           | O(1)     | O(1)      |
| `is_full`      | —    | —              | —              | O(1)     | O(1)      |
| `__len__`      | O(1) | O(1)           | O(1)           | O(1)     | O(1)      |
| `__bool__`     | O(1) | O(1)           | O(1)           | O(1)     | O(1)      |
| `__iter__`     | O(n) | O(n)           | O(n)           | O(n)     | O(n)      |
| `__reversed__` | O(n) | O(n)           | O(n)           | O(n)     | O(n)      |
| `__contains__` | O(n) | O(n)           | O(n)           | O(n)     | O(n)      |
| `__eq__`       | O(n) | O(n)           | O(n)           | O(n)     | O(n)      |
| `__repr__`     | O(n) | O(n)           | O(n)           | O(n)     | O(n)      |

### Min Stacks (same as above plus)

| Operation | All Min Stacks |
| --------- | -------------- |
| `min`     | O(1)           |

\* Typed and static `clear()` reset every slot to the dtype default to keep the
underlying `ctypes` buffer in a consistent state — hence O(n).
`DynamicUniversalStack.clear()` is O(n): only the size counter is reset.

> All stacks yield elements **top to bottom** in `__iter__` and **bottom to top** in `__reversed__`.

---

## Design Decisions

### Static vs Dynamic

Static stacks (backed by `StaticArray`) have a fixed capacity set at construction time.
Pushing onto a full static stack raises `OverflowError`.
Dynamic stacks (backed by `DynamicArray` or `LinearNode`) grow on demand — no overflow.

### Typed vs Universal

Typed stacks enforce a single `dtype` (`int`, `float`, `bool`, or `str`) for every element.
Pushing the wrong type raises `TypeError`. Universal stacks accept any Python object.
Note: `bool` is a subclass of `int` in Python — typed stacks explicitly reject
`bool` values when `dtype=int` and `int` values when `dtype=bool`.

### `NodeStack` vs Array-based stacks

`NodeStack` allocates a new `LinearNode` per element — no preallocated buffer,
no resize. It suits workloads with highly variable depth where capacity is unknown
up front. Array-based stacks have better cache locality and lower per-element overhead.

### `_min_data` sizing (Min Stacks)

Static min stacks allocate a second buffer of the same capacity as `_data`.
In the worst case (strictly descending pushes) every element enters `_min_data`,
so the same capacity is the safe upper bound. Dynamic min stacks grow `_min_data`
on demand in the same way as `_data`.

### `__eq__` in static stacks

Static stacks do not delegate equality to the underlying array's `__eq__` because
`StaticArray.__eq__` checks capacity equality. Two static stacks with the same
elements but different capacities should still be considered equal, so equality
is checked manually up to `_top`.

Dynamic stacks delegate to the array's `__eq__` directly — it already compares
only filled elements and dtype.

---

## `__repr__` Formats

```
NodeStack(size=3)[3, 2, 1]
                  top   bottom

DynamicUniversalStack(size=3)[3, 2, 1]
DynamicTypedStack(int, size=3)[3, 2, 1]

StaticUniversalStack(size=3, capacity=5)[3, 2, 1]
StaticTypedStack(int, size=3, capacity=5)[3, 2, 1]

NodeMinStack(size=3, min=1)[3, 2, 1]
DynamicUniversalMinStack(size=3, min=1)[3, 2, 1]
DynamicTypedMinStack(int, size=3, min=1)[3, 2, 1]

StaticUniversalMinStack(capacity=5, min=1)[3, 2, 1]
StaticTypedMinStack(int, capacity=5, min=1)[3, 2, 1]
```
