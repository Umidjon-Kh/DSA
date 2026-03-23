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

### `StaticUniversalArray(capacity, *args)`

Fixed-size array backed by a `ctypes.py_object` buffer.
Accepts any Python type. All slots default to `None`.

```python
arr = StaticUniversalArray(5)               # [None, None, None, None, None]
arr = StaticUniversalArray(5, 1, "hi", 3)   # [1, 'hi', 3, None, None]
```

### `StaticTypedArray(dtype, capacity, *args, str_length=1)`

Fixed-size array backed by a raw `ctypes` buffer.
Enforces a single dtype for all elements — lower memory overhead than universal.
Supported dtypes: `int`, `float`, `bool`, `str`.
For `str` dtype, `str_length` sets the max characters per slot.

```python
arr = StaticTypedArray(int, 5)               # [0, 0, 0, 0, 0]
arr = StaticTypedArray(int, 5, 1, 2, 3)      # [1, 2, 3, 0, 0]
arr = StaticTypedArray(str, 4, str_length=8)  # ['', '', '', '']
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
```

### `DynamicTypedArray(dtype, *args, str_length=1)`

Auto-growing array backed by `StaticTypedArray`.
Enforces a single dtype. Same growth formula as `DynamicUniversalArray`.

```python
arr = DynamicTypedArray(int)           # empty, capacity=4
arr = DynamicTypedArray(int, 1, 2, 3)  # [1, 2, 3], capacity=4
arr = DynamicTypedArray(int, *range(10))  # grows automatically
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
| `__getitem__`  | O(1)   | O(1)           |
| `__setitem__`  | O(1)   | O(1)           |
| `__len__`      | O(1)   | O(1)           |
| `__iter__`     | O(n)   | O(n)           |
| `__reversed__` | O(n)   | O(n)           |
| `__contains__` | O(n)   | O(n)           |
| `__repr__`     | O(n)   | O(n)           |
| `append`       | —      | O(1) amortized |
| `insert`       | —      | O(n)           |
| `remove`       | —      | O(n)           |
| `_resize`      | —      | O(n)           |

Static arrays expose the full capacity via `__len__` and `__iter__`.
Dynamic arrays expose only the filled portion (`size`) via `__len__` and `__iter__`.

---

## Type Safety Notes

- `bool` is a subclass of `int` in Python. Typed arrays and dynamic typed arrays
  explicitly reject `bool` values when `dtype=int`, and reject `int` values when
  `dtype=bool`.
- `StaticTypedArray` and `DynamicTypedArray` raise `TypeError` for unsupported
  dtypes. The error message uses `repr(dtype)` so it is safe for any input
  including `None`, `42`, or `"int"`.
