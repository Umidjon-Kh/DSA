import ctypes
from typing import Any, Iterator, Optional

from ...._base import BaseArray
from ...._tools import validate_capacity, validate_index, validate_value_type

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

_DEFAULT_STR_LENGTH = 20


class StaticTypedArray(BaseArray):
    """
    A fixed-size array backed by a raw ctypes buffer.
    Enforces a single element type for all items.

    Stores raw C values instead of PyObject pointers —
    less memory overhead per element compared to a universal array.

    Supported dtypes: int, float, bool, str

    For str dtype, each element is a fixed-length character buffer.
    str_length defines the max characters per element (default: 20).

    capacity is optional — if omitted, it is derived from len(args).
    At least one of capacity or *args must be provided.

    Time complexity:
        copy:         O(n)
        clear:        O(n)
        __getitem__:  O(1)
        __setitem__:  O(1)
        __len__:      O(1)
        __bool__:     O(1)
        __iter__:     O(n)
        __reversed__: O(n)
        __contains__: O(n)
        __eq__:       O(n)
        __repr__:     O(n)
    """

    __slots__ = ("_data", "_capacity", "_dtype", "_str_length")

    def __init__(
        self,
        dtype: type,
        *args,
        capacity: Optional[int] = None,
        str_length: Optional[int] = None,
    ) -> None:
        """
        Creates a fixed-size typed array with optional initial elements.

        Args:
            dtype:      Element type. Supported: int, float, bool, str.
            *args:      Optional initial elements. Must all be of type dtype.
            capacity:   Maximum number of elements the array can hold.
                        If omitted, capacity is set to len(args).
                        At least one of capacity or *args must be provided.
            str_length: Max characters per str element (default: 20).
                        Ignored for non-str dtypes.

        Raises:
            TypeError:     If dtype is not a supported type.
            TypeError:     If neither capacity nor args are provided.
            TypeError:     If capacity is provided but not an int.
            ValueError:    If capacity < 1.
            TypeError:     If str_length is provided but not an int.
            ValueError:    If str_length < 1.
            TypeError:     If any element in args is not dtype.
            OverflowError: If len(args) > capacity.

        Examples:
            arr = StaticTypedArray(int, capacity=5)           # [0, 0, 0, 0, 0]
            arr = StaticTypedArray(int, 1, 2, 3)              # [1, 2, 3], capacity=3
            arr = StaticTypedArray(int, 1, 2, 3, capacity=5)  # [1, 2, 3, 0, 0]
            arr = StaticTypedArray(str, capacity=4)           # ['', '', '', ''], str_length=20
            arr = StaticTypedArray(str, capacity=4, str_length=8)  # str_length=8
        """
        if dtype not in _SUPPORTED_DTYPES:
            raise TypeError(
                f"Unsupported dtype: {dtype!r}. "
                f"Supported: {[t.__name__ for t in _SUPPORTED_DTYPES]}"
            )

        self._dtype: type = dtype
        self._capacity: int = validate_capacity(capacity, len(args), "StaticTypedArray")

        # Resolve str_length — use provided value or fall back to default
        resolved_str_length: int = _DEFAULT_STR_LENGTH
        if str_length is not None:
            if not isinstance(str_length, int) or isinstance(str_length, bool):
                raise TypeError(
                    f"str_length must be int, got {type(str_length).__name__!r}"
                )
            if str_length < 1:
                raise ValueError(f"str_length must be >= 1, got {str_length}")
            resolved_str_length = str_length

        self._str_length: int = resolved_str_length

        if dtype is str:
            self._data = (ctypes.c_wchar * self._str_length * self._capacity)()
        else:
            self._data = (_DTYPE_MAP[dtype] * self._capacity)()

        # Fill with type defaults
        default = _DTYPE_DEFAULTS[dtype]
        for index in range(self._capacity):
            self._raw_set(index, default)

        # Set initial elements
        for index, val in enumerate(args):
            self[index] = val

    # -------------------------------------------------------------------------
    # Internal helpers

    def _raw_set(self, index: int, value: Any) -> None:
        """Sets element without type-check. Used internally during init and resize."""
        if self._dtype is str:
            buf = self._data[index]
            for shelf, char in enumerate(value[: self._str_length]):
                buf[shelf] = char
            for shelf in range(len(value), self._str_length):
                buf[shelf] = "\0"
        else:
            self._data[index] = value

    def _raw_get(self, index: int) -> Any:
        """Gets element without bounds-check. Used internally."""
        if self._dtype is str:
            buf = self._data[index]
            return "".join(buf[j] for j in range(self._str_length) if buf[j] != "\0")
        return self._dtype(self._data[index])

    def _set_default(self, index: int) -> None:
        """
        Sets default value in received index for any data type.
        It needs for other structures that backed by StaticTypedArray.
        DRY (Do not Repeat Yourself)
        """
        self._raw_set(index, _DTYPE_DEFAULTS[self._dtype])

    # -------------------------------------------------------------------------
    # Public interface

    def clear(self) -> None:
        """
        Resets all elements to their dtype default value.
        Does not reallocate the buffer.

        Defaults: int -> 0, float -> 0.0, bool -> False, str -> ''

        Time complexity: O(n)
        """
        default = _DTYPE_DEFAULTS[self._dtype]
        for index in range(self._capacity):
            self._raw_set(index, default)

    def copy(self) -> "StaticTypedArray":
        """
        Returns a shallow copy with the same dtype, capacity, str_length and data.

        Time complexity: O(n)
        """
        copied = StaticTypedArray(
            dtype=self._dtype,
            capacity=self._capacity,
            str_length=self._str_length,
        )
        for index in range(self._capacity):
            copied._raw_set(index, self._raw_get(index))
        return copied

    # -------------------------------------------------------------------------
    # Dunder methods

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
        validate_value_type(value, self._dtype)
        self._raw_set(index, value)

    def __len__(self) -> int:
        """Returns the fixed capacity of the array. O(1)"""
        return self._capacity

    def __bool__(self) -> bool:
        """Returns True if capacity is greater than zero. O(1)"""
        return self._capacity > 0

    def __iter__(self) -> Iterator:
        """Yields all elements from index 0 to capacity-1. O(n)"""
        for index in range(self._capacity):
            yield self._raw_get(index)

    def __reversed__(self) -> Iterator[Any]:
        """Yields elements from right to left(back -> start). O(n)"""
        for index in range(self._capacity - 1, -1, -1):
            yield self._raw_get(index)

    def __contains__(self, value: Any) -> bool:
        """
        Returns True if value exists in the array. O(n)
        Returns False instantly if received value type is not match data type.
        """
        try:
            validate_value_type(value, self._dtype)
        except TypeError:
            return False
        for index in range(self._capacity):
            if self._raw_get(index) == value:
                return True
        return False

    def __eq__(self, other: object) -> bool:
        """
        Returns True if other is a StaticTypedArray with the same dtype,
        capacity, and elements in the same order. O(n)
        """
        if not isinstance(other, StaticTypedArray):
            return NotImplemented
        if self._dtype is not other._dtype or self._capacity != other._capacity:
            return False
        for index in range(self._capacity):
            if self._raw_get(index) != other._raw_get(index):
                return False
        return True

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
