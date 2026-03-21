# Arrays

From-scratch implementation of static and dynamic arrays in Python using `ctypes` for low-level memory management.

---

## Structure

```
arrays/
├── static_universal.py   # Fixed-size array, any type (ctypes.py_object)
├── static_typed.py       # Fixed-size array, single dtype (ctypes C types)
├── dynamic_universal.py  # Auto-resizing array, any type
├── dynamic_typed.py      # Auto-resizing array, single dtype
└── _validators.py        # Shared index validation logic
```

---

## Classes

| Class                   | Type                                         | Resizable | Backend                |
| ----------------------- | -------------------------------------------- | --------- | ---------------------- |
| `StaticUniversalArray`  | Any Python object                            | ❌        | `ctypes.py_object`     |
| `StaticTypedArray`      | Single dtype (`int`, `float`, `bool`, `str`) | ❌        | `ctypes` C types       |
| `DynamicUniversalArray` | Any Python object                            | ✅        | `StaticUniversalArray` |
| `DynamicTypedArray`     | Single dtype                                 | ✅        | `StaticTypedArray`     |

---

## Time Complexity

| Operation     | Static | Dynamic        |
| ------------- | ------ | -------------- |
| `__getitem__` | O(1)   | O(1)           |
| `__setitem__` | O(1)   | O(1)           |
| `append`      | —      | O(1) amortized |
| `insert`      | —      | O(n)           |
| `remove`      | —      | O(n)           |
| `_resize`     | —      | O(n)           |
| `copy`        | O(n)   | O(n)           |

---

## Growth Formula (Dynamic arrays)

Same formula as CPython list internals:

```python
new_capacity = capacity + (capacity >> 3) + (3 if capacity < 9 else 6)
```

Initial capacity: `max(4, len(args))`

---

## Usage

```python
from data_structures.arrays import (
    StaticUniversalArray,
    StaticTypedArray,
    DynamicUniversalArray,
    DynamicTypedArray,
)

# Fixed-size, any type
arr = StaticUniversalArray(5)
arr[0] = 42
arr[1] = "hello"

# Fixed-size, typed (raw C values in memory)
arr = StaticTypedArray(5, dtype=int)
arr[0] = 10

# String arrays require str_length (default 20)
arr = StaticTypedArray(5, dtype=str, str_length=50)
arr[0] = "hello"

# Dynamic, any type
arr = DynamicUniversalArray(1, 2, 3)
arr.append(4)
arr.insert(0, 99)
removed = arr.remove(0)  # returns 99

# Dynamic, typed
arr = DynamicTypedArray(float, 1.1, 2.2, 3.3)
arr.append(4.4)
arr.insert(0, 0.0)
removed = arr.remove(-1)  # supports negative indexing
```

---

## Design Decisions

**Why ctypes?**
`StaticUniversalArray` uses `ctypes.py_object` — stores PyObject pointers the same way CPython stores items in a list internally. `StaticTypedArray` uses typed C arrays (`c_long`, `c_double`, etc.) for lower memory overhead — no PyObject wrapper per element.

**Why Universal and Typed separately?**
To reflect the same trade-off as Python's own `list` vs `array.array` — flexibility vs memory efficiency.

**Why Dynamic builds on Static?**
`DynamicUniversalArray` wraps `StaticUniversalArray`, and `DynamicTypedArray` wraps `StaticTypedArray`. Each layer has a single responsibility.
