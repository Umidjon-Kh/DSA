# Arrays

Four array implementations split along two axes: **static vs dynamic** and **typed vs universal**.

```
arrays/
├── static_universal.py   # fixed-size, any type
├── static_typed.py       # fixed-size, single dtype (ctypes buffer)
├── dynamic_universal.py  # auto-growing, any type
└── dynamic_typed.py      # auto-growing, single dtype (ctypes buffer)
```

---

## Class Overview

### `StaticUniversalArray(*args, capacity=None)`

Fixed-size array backed by a `ctypes.py_object` buffer.
Accepts any Python type. All slots default to `None`.
At least one of `capacity` or `*args` must be provided.

```python
arr = StaticUniversalArray(capacity=5)           # [None, None, None, None, None]
arr = StaticUniversalArray(1, "hi", 3)           # [1, 'hi', 3], capacity=3
arr = StaticUniversalArray(1, "hi", capacity=5)  # [1, 'hi', None, None, None]
copy = arr.copy()                                # independent shallow copy
```

### `StaticTypedArray(dtype, *args, capacity=None, str_length=None)`

Fixed-size array backed by a raw `ctypes` buffer.
Enforces a single dtype for all elements — lower memory overhead than universal.
Supported dtypes: `int`, `float`, `bool`, `str`.
At least one of `capacity` or `*args` must be provided.
For `str` dtype, `str_length` sets the max characters per slot (default: **20**).

```python
arr = StaticTypedArray(int, capacity=5)           # [0, 0, 0, 0, 0]
arr = StaticTypedArray(int, 1, 2, 3)              # [1, 2, 3], capacity=3
arr = StaticTypedArray(int, 1, 2, 3, capacity=5)  # [1, 2, 3, 0, 0]
arr = StaticTypedArray(str, capacity=4)           # ['', '', '', ''], str_length=20
arr = StaticTypedArray(str, capacity=4, str_length=8)  # str_length=8
copy = arr.copy()                                 # independent shallow copy
arr.clear()                                       # resets all slots to dtype default
```

### `DynamicUniversalArray(*args)`

Auto-growing array backed by `StaticUniversalArray`.
Accepts any Python type. Grows using CPython's growth formula when capacity is exceeded.
Initial capacity: `max(4, len(args))`.

```python
arr = DynamicUniversalArray()              # empty, capacity=4
arr = DynamicUniversalArray(1, "hi", 3.0)  # [1, 'hi', 3.0], capacity=4
arr.append("new")
arr.insert(0, "first")
arr.remove(1)
arr.clear()                                # size=0, capacity unchanged
copy = arr.copy()                          # independent shallow copy
```

### `DynamicTypedArray(dtype, *args, str_length=20)`

Auto-growing array backed by `StaticTypedArray`.
Enforces a single dtype. Same growth formula as `DynamicUniversalArray`.
For `str` dtype, `str_length` defaults to **20**.

```python
arr = DynamicTypedArray(int)              # empty, capacity=4
arr = DynamicTypedArray(int, 1, 2, 3)    # [1, 2, 3], capacity=4
arr = DynamicTypedArray(str, "hi")       # str_length=20 by default
arr = DynamicTypedArray(str, str_length=50)  # custom str_length
arr.clear()                              # size=0, all filled slots reset to default
copy = arr.copy()                        # independent shallow copy
```

---

## Growth Formula (Dynamic arrays)

Same as CPython's list:

```
new_capacity = capacity + (capacity >> 3) + (3 if capacity < 9 else 6)
```

---

## Supported Operations

| Operation      | Static | Dynamic        |
| -------------- | ------ | -------------- |
| `copy`         | O(n)   | O(n)           |
| `clear`        | O(n)   | O(n) / O(1)\*  |
| `append`       | —      | O(1) amortized |
| `insert`       | —      | O(n)           |
| `remove`       | —      | O(n)           |
| `_resize`      | —      | O(n)           |
| `__getitem__`  | O(1)   | O(1)           |
| `__setitem__`  | O(1)   | O(1)           |
| `__len__`      | O(1)   | O(1)           |
| `__bool__`     | O(1)   | O(1)           |
| `__iter__`     | O(n)   | O(n)           |
| `__reversed__` | O(n)   | O(n)           |
| `__contains__` | O(n)   | O(n)           |
| `__eq__`       | O(n)   | O(n)           |
| `__repr__`     | O(n)   | O(n)           |

\* `DynamicUniversalArray.clear()` is O(1) — only resets the size counter.
`DynamicTypedArray.clear()` and `StaticTypedArray.clear()` are O(n) — they also
reset each slot to the dtype default value so the buffer stays consistent.

Static arrays expose the full capacity via `__len__` and `__iter__`.
Dynamic arrays expose only the filled portion (`size`) via `__len__` and `__iter__`.

---

## Key Design Decisions

### `capacity=None` (Static arrays)

Both static arrays accept `capacity=None`. When omitted, capacity is inferred
from the number of initial elements. At least one of `capacity` or `*args`
must be present — passing neither raises `TypeError`.

```python
StaticTypedArray(int, 1, 2, 3)              # capacity=3, derived from args
StaticTypedArray(int, capacity=5)           # capacity=5, no initial elements
StaticTypedArray(int, 1, 2, 3, capacity=5)  # capacity=5, 3 elements filled
StaticTypedArray(int)                       # TypeError — nothing provided
```

### `str_length` default = 20

Both `StaticTypedArray` and `DynamicTypedArray` default `str_length` to **20**
instead of 1, so strings work out of the box without extra configuration.
Pass `str_length=N` explicitly when you need a different limit.

### `clear()` behaviour

`StaticTypedArray` and `DynamicTypedArray` reset every slot to the dtype default
(`0`, `0.0`, `False`, or `''`). This keeps the ctypes buffer in a predictable
state for further use.

`DynamicUniversalArray.clear()` only resets the `size` counter — it is O(1)
because `None` is already the implicit "empty" value for universal slots.

### `__bool__`

Dynamic arrays return `True` when `size > 0`.
Static arrays return `True` when `capacity > 0` (always `True` for valid arrays).

### `__eq__`

Element-wise comparison. Two arrays are equal when they have the same type,
same size/capacity, and all elements match in order.
Comparing with a non-array type returns `NotImplemented`.

---

## Type Safety Notes

- `bool` is a subclass of `int` in Python. Typed arrays explicitly reject `bool`
  values when `dtype=int`, and reject `int` values when `dtype=bool`.
- `StaticTypedArray` and `DynamicTypedArray` raise `TypeError` for unsupported
  dtypes. The error message uses `repr(dtype)` so it is safe for any input
  including `None`, `42`, or `"int"`.
