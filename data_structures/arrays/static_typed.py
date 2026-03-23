import ctypes
from typing import Any, Iterator

from ..tools import validate_capacity, validate_index

_DTYPE_MAP = {
    int: ctypes.c_long,
    float: ctypes.c_double,
    bool: ctypes.c_bool,
    str: ctypes.c_wchar,
}

_DTYPE_DEFAULTS = {
    int: 0,
    float: 0.0,
    bool: False,
    str: "",
}

_SUPPORTED_DTYPES = frozenset(_DTYPE_MAP)


class StaticTypedArray:
    """
    A fixed-size array backed by a raw ctypes buffer.
    Enforces a single element type for all items.

    Stores raw C values instead of PyObject pointers —
    less memory overhead per element compared to a universal array.

    Supported dtypes: int, float, bool, str

    For str dtype, each element is a fixed-length character buffer.
    str_length defines the max characters per element (default: 1).

    Time complexity:
        __getitem__:  O(1)
        __setitem__:  O(1)
        __len__:      O(1)
        __iter__:     O(n)
        __contains__: O(n)
        __repr__:     O(n)
    """

    __slots__ = ("_data", "_capacity", "_dtype", "_str_length")

    def __init__(self, dtype: type, capacity: int, *args, str_length: int = 1) -> None:
        """
        Creates a fixed-size typed array with optional initial elements.

        Args:
            dtype:      Element type. Supported: int, float, bool, str.
            capacity:   Maximum number of elements the array can hold.
            *args:      Optional initial elements. Must all be of type dtype.
            str_length: Max characters per str element (default: 1). Ignored for other dtypes.

        Raises:
            TypeError:     If dtype is not a supported type.
            TypeError:     If capacity is not an int.
            ValueError:    If capacity < 1.
            TypeError:     If str_length is not an int (str dtype only).
            ValueError:    If str_length < 1 (str dtype only).
            TypeError:     If any element in args is not dtype.
            OverflowError: If len(args) > capacity.

        Examples:
            arr = StaticTypedArray(int, 5)               # [0, 0, 0, 0, 0]
            arr = StaticTypedArray(int, 5, 1, 2, 3)      # [1, 2, 3, 0, 0]
            arr = StaticTypedArray(str, 4, str_length=8)  # ['', '', '', '']
        """
        if dtype not in _SUPPORTED_DTYPES:
            raise TypeError(
                f"Unsupported dtype: {dtype.__name__!r}. "
                f"Supported: {[t.__name__ for t in _SUPPORTED_DTYPES]}"
            )
        self._dtype: type = dtype
        self._capacity: int = validate_capacity(capacity)
        self._str_length: int = str_length

        if dtype is str:
            if not isinstance(str_length, int) or isinstance(str_length, bool):
                raise TypeError(
                    f"str_length must be int, got {type(str_length).__name__!r}"
                )
            if str_length < 1:
                raise ValueError(f"str_length must be >= 1, got {str_length}")
            self._data = (ctypes.c_wchar * str_length * self._capacity)()
        else:
            self._data = (_DTYPE_MAP[dtype] * self._capacity)()

        # Fill with type defaults
        default = _DTYPE_DEFAULTS[dtype]
        for i in range(capacity):
            self._raw_set(i, default)

        # Set initial elements
        for i, val in enumerate(args):
            self[i] = val

    # -------------------------------------------------------------------------
    # Internal helpers

    def _raw_set(self, index: int, value: Any) -> None:
        """Sets element without type-check. Used internally during init and resize."""
        if self._dtype is str:
            buf = self._data[index]
            for j, ch in enumerate(value[: self._str_length]):
                buf[j] = ch
            for j in range(len(value), self._str_length):
                buf[j] = "\0"
        else:
            self._data[index] = value

    def _raw_get(self, index: int) -> Any:
        """Gets element without bounds-check. Used internally."""
        if self._dtype is str:
            buf = self._data[index]
            return "".join(buf[j] for j in range(self._str_length) if buf[j] != "\0")
        return self._dtype(self._data[index])

    # -------------------------------------------------------------------------
    # Public interface

    def __getitem__(self, index: int) -> Any:
        """
        Returns element at given index. Supports negative indexing.

        Time complexity: O(1)

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range.
        """
        index = validate_index(index, self._capacity)
        return self._raw_get(index)

    def __setitem__(self, index: int, value: Any) -> None:
        """
        Sets element at given index. Supports negative indexing.

        Time complexity: O(1)

        Raises:
            TypeError:  If index is not int.
            IndexError: If index is out of range.
            TypeError:  If value is not dtype.
        """
        index = validate_index(index, self._capacity)
        if (
            not isinstance(value, self._dtype)
            or self._dtype is int
            and isinstance(value, bool)
        ):
            raise TypeError(
                f"Expected {self._dtype.__name__}, got {type(value).__name__!r}"
            )
        self._raw_set(index, value)

    def __len__(self) -> int:
        """Returns the fixed capacity of the array. O(1)"""
        return self._capacity

    def __reversed__(self) -> Iterator[Any]:
        """Yields elements from right to left(back -> start). O(n)"""
        for i in range(self._capacity - 1, -1, -1):
            yield self._raw_get(i)

    def __iter__(self) -> Iterator:
        """Yields all elements from index 0 to capacity-1. O(n)"""
        for i in range(self._capacity):
            yield self._raw_get(i)

    def __contains__(self, value: Any) -> bool:
        """
        Returns True if value exists in the array. O(n)
        Returns False instantly if received value type is not matchs data type.
        """
        if (
            not isinstance(value, self._dtype)
            or self._dtype is int
            and isinstance(value, bool)
        ):
            return False
        for i in range(self._capacity):
            if self._raw_get(i) == value:
                return True
        return False

    def __repr__(self) -> str:
        """
        Returns string representation of the array.
        Format: StaticTypedArray(int, capacity=5)[1, 2, 3, 0, 0]

        Time complexity: O(n)
        """
        elements = ", ".join(repr(self._raw_get(i)) for i in range(self._capacity))
        return (
            f"StaticTypedArray({self._dtype.__name__}, capacity={self._capacity})"
            f"[{elements}]"
        )
