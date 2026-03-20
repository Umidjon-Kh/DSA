import ctypes
from typing import Any, Iterator

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

    Supported dtypes: int, float, bool

    Time complexity:
        __getitem__: O(1)
        __setitem__: O(1)
        __iter__:    O(n)
        __len__:     O(1)
    """

    __slots__ = ("_capacity", "_data", "_dtype", "_ctype", "_str_length")

    def __init__(self, capacity: Any, dtype: type, str_length: Any = None) -> None:
        """
        Creates data structure array
        with received data type and capacity and
        allocates it to memory
        """
        # ---------- Validating Received Values ---------
        # Checking capacity for type and for value
        if not isinstance(capacity, int):
            raise TypeError(
                f"Capacity value must be positive integer, got ({type(capacity).__name__})"
            )
        if capacity <= 0:
            raise ValueError(f"Capacity value must be more than 0, got ({capacity})")

        self._capacity = capacity

        # Checking data type for matching _TYPE_MAP
        if dtype not in _TYPE_MAP:
            raise TypeError(
                f"Unsupported data type: {dtype.__name__}"
                f"Supported: {[t.__name__ for t in _TYPE_MAP]}"
            )

        self._dtype = dtype
        self._ctype = _TYPE_MAP[dtype]

        # If data type is str checks value of str_length too
        if self._dtype == str:  # noqa
            self._str_length = 20
            if str_length is not None:
                if not isinstance(str_length, int):
                    raise TypeError(
                        f"Str length value must be positive integer, got ({type(str_length).__name__})"
                    )
                if str_length <= 0:
                    raise ValueError(
                        f"Str length must be more than 0, got ({str_length})"
                    )
                self._str_length = str_length

            # Allocating str values data array to memory ()
            self._data = ((self._ctype * self._str_length) * self._capacity)()
        # Otherwise if dtype is not str
        else:
            if str_length is not None:
                raise ValueError("Str length only valid for dtype=str")
            self._data = (self._ctype * self._capacity)()
            self._str_length = 0

    def __getitem__(self, index: Any) -> Any:
        """Returns value at given index."""
        # Checking type of received index
        if not isinstance(index, int):
            raise TypeError(
                f"Index must be positive integer, got ({type(index).__name__})"
            )
            # Converting index if its negative integer
        if index < 0:
            index += self._capacity
        # Checking value of received index
        if index < 0 or index >= self._capacity:
            raise ValueError(
                f"Index {index} out of range for capacity {self._capacity}"
            )

        value = self._data[index]
        # If data type is str we need to decode it
        if self._dtype == str:  # noqa
            return bytes(self._data[index]).rstrip(b"\x00").decode()
        return value

    def __setitem__(self, index: Any, value: Any) -> None:
        """Sets value to given index."""
        # Checking type of received index
        if not isinstance(index, int):
            raise TypeError(
                f"Index must be positive integer, got ({type(index).__name__})"
            )
        # Converting index if its negative integer
        if index < 0:
            index += self._capacity
        # Checking value of received index
        if index < 0 or index >= self._capacity:
            raise IndexError(
                f"Index {index} out of range for capacity {self._capacity}"
            )
        # Checking value is instance of data type or not
        if not isinstance(value, self._dtype):
            raise TypeError(f"Expected {self._dtype}, got ({type(value).__name__})")

        # If data type is str we need to encode value before setting
        if self._dtype == str:  # noqa
            encoded = value.encode()
            # Checking encoded value for lenght
            if len(encoded) > self._str_length:
                raise ValueError(
                    f"String too long: max ({self._str_length}) chars, got ({len(encoded)})"
                )
            self._data[index] = (ctypes.c_char * self._str_length)(*encoded)
        # Otherwise just set it to given index
        else:
            self._data[index] = value

    def __len__(self) -> int:
        """Returns length of data array"""
        return self._capacity

    def __iter__(self) -> Iterator[Any]:
        """Iterates the total capacity of the Array, not the number of filled slots"""
        for index in range(self._capacity):
            yield self._data[index]

    def __repr__(self) -> str:
        """Returns Representation instance of StaticTypedlArray"""
        items = [self._data[i] for i in range(self._capacity)]
        return f"StaticTypedArray(data_type={self._dtype} ,capacity={self._capacity}, slots={items})"
