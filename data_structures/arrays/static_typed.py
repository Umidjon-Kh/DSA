import ctypes
from typing import Any, Iterator

from ._validators import validate_index

_TYPE_MAP = {
    int: ctypes.c_long,
    float: ctypes.c_double,
    bool: ctypes.c_bool,
    str: ctypes.c_char,
}


class StaticTypedArray:
    """
    A fixed-size array that enforces a single type for all elements.
    Built on top of ctypes typed arrays — elements are stored as raw
    C values in contiguous memory, not as PyObject pointers.

    Unlike StaticUniversalArray:
    - Only accepts elements of the declared dtype
    - Stores raw values, not pointers — less memory overhead
    - No PyObject overhead per element

    Supported dtypes: int, float, bool, str
    For dtype str: must provide fixed str_length (default 20).
    Strings longer than str_length will raise ValueError.

    Time complexity:
        __getitem__: O(1)
        __setitem__: O(1)
        __iter__:    O(n)
        __len__:     O(1)
    """

    __slots__ = ("_capacity", "_data", "_dtype", "_ctype", "_str_length")

    def __init__(self, capacity: Any, dtype: type, str_length: Any = None) -> None:
        """
        Creates typed array with received capacity and dtype.
        Allocates fixed memory block via ctypes.
        """
        if not isinstance(capacity, int):
            raise TypeError(
                f"Capacity value must be positive integer, got ({type(capacity).__name__})"
            )
        if capacity <= 0:
            raise ValueError(f"Capacity value must be more than 0, got ({capacity})")

        self._capacity = capacity

        if dtype not in _TYPE_MAP:
            raise TypeError(
                f"Unsupported data type: {dtype.__name__}. "
                f"Supported: {[t.__name__ for t in _TYPE_MAP]}"
            )

        self._dtype = dtype
        self._ctype = _TYPE_MAP[dtype]

        if self._dtype == str:  # noqa
            self._str_length = 20
            if str_length is not None:
                if not isinstance(str_length, int):
                    raise TypeError(
                        f"Str length must be positive integer, got ({type(str_length).__name__})"
                    )
                if str_length <= 0:
                    raise ValueError(
                        f"Str length must be more than 0, got ({str_length})"
                    )
                self._str_length = str_length
            self._data = ((self._ctype * self._str_length) * self._capacity)()
        else:
            if str_length is not None:
                raise ValueError("str_length is only valid for dtype=str")
            self._data = (self._ctype * self._capacity)()
            self._str_length = 0

    def __getitem__(self, index: Any) -> Any:
        """Returns value at given index. Decodes bytes to str for dtype=str."""
        index = validate_index(index, self._capacity)
        if self._dtype == str:  # noqa
            return bytes(self._data[index]).rstrip(b"\x00").decode()
        return self._data[index]

    def __setitem__(self, index: Any, value: Any) -> None:
        """
        Sets value at given index.
        Validates value type against dtype.
        Encodes str to bytes for dtype=str.
        """
        index = validate_index(index, self._capacity)
        if not isinstance(value, self._dtype):
            raise TypeError(
                f"Expected {self._dtype.__name__}, got ({type(value).__name__})"
            )
        if self._dtype == str:  # noqa
            encoded = value.encode()
            if len(encoded) > self._str_length:
                raise ValueError(
                    f"String too long: max ({self._str_length}) chars, got ({len(encoded)})"
                )
            self._data[index] = (ctypes.c_char * self._str_length)(*encoded)
        else:
            self._data[index] = value

    def __len__(self) -> int:
        """Returns capacity of array."""
        return self._capacity

    def __iter__(self) -> Iterator[Any]:
        """Iterates all slots."""
        for index in range(self._capacity):
            yield self._data[index]

    def __repr__(self) -> str:
        items = [self._data[i] for i in range(self._capacity)]
        return f"StaticTypedArray(data_type={self._dtype}, capacity={self._capacity}, slots={items})"
