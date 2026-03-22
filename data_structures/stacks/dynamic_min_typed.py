from typing import Any, Callable, Generator, Optional

from ..arrays import DynamicTypedArray


class DynamicTypedMinStack:
    """
    Creates two dynamic stacks that grows automatically when capacity is exceeded.
    Build on top of DynamicTypedArray - enforces a single type for all elemenets.
    Follows LIFO (Last In, First Out) by DynamicTypedArray principle.

    Compared to StaticTypedMinStack and DynamicUniversalMinStack:
        1) Never raises OverflowsError.
        2) Stores all objects in raw C values.

    Raises IndexError on pop/peek when empty.
    Raises TypeError if key function is provided but not callable.
    Raises TypeError if pushed object is not initialized data type.
    Raises TypeError if str_length is provided but not positive integer.
    Raises ValueError if str_length less than or equal to 0.

    Time complexity:
        push:     O(1) amortized — O(n) on resize
        pop:      O(1)
        peek:     O(1)
        get_min:  O(1)
        is_empty: O(1)
        __len__:  O(1)
        __iter__: O(n) — from top to bottom
        copy:     O(n)
    """

    __slots__ = (
        "_main_data",
        "_min_data",
        "_key",
        "_dtype",
    )

    def __init__(
        self, *args, dtype: type, str_length: Any = None, key: Optional[Callable] = None
    ) -> None:
        """
        Creates two dynamic typed stack with optional initial values.

        Args:
            *args:      Optional initial values pushed bottom to top. Must match dtype.
            dtype:      Element type. Supported: int, float, bool, str.
            str_length: Max string length for dtype=str (default 20).

        Raises:
            TypeError: if key function is provided but not callable.
            TypeError: if pushed value is not initialized data type.
            TypeError: if str_length is provided but not positive integer.
            ValueError: if str_length less than or equal to 0
        """
        # Validating key function
        if key is not None:
            if not callable(key):
                raise TypeError(f"Key must be callable, got ({type(key).__name__})")
            self._key = key
        else:
            self._key = lambda x: x
        # Initializing data type
        self._dtype = dtype
        # Creating both structures
        self._main_data = DynamicTypedArray(dtype=self._dtype, str_length=str_length)
        self._min_data = DynamicTypedArray(dtype=self._dtype, str_length=str_length)
        # Pushing args to both datas
        for item in args:
            self.push(item)

    def push(self, value: Any) -> None:
        """
        Adds object to main stack and computes minimal
        using key function to get minimum object and adds it to
        min data. Value must match dtype.

        Raises:
            TypeError:     if value does not match dtype.
        """
        self._main_data.append(value)
        if len(self._min_data) == 0 or self._key(value) <= self._key(
            self._min_data[-1]
        ):
            self._min_data.append(value)

    def is_empty(self) -> bool:
        """Returns True if stack has no elements."""
        return len(self._main_data) == 0

    def pop(self) -> Any:
        """
        Removes and returns object from the top of the main data.
        If main data top object and min data top object
        computed minimal value is equal clears top of slot of min data too.

        Returns:
            Value at the top.

        Raises:
            IndexError: if stack is empty.
        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        removed = self._main_data.remove(-1)
        if self._key(removed) == self._key(self._min_data[-1]):
            self._min_data.remove(-1)
        return removed

    def peek(self) -> Any:
        """
        Returns value at the top without removing it.

        Returns:
            Value at the top.

        Raises:
            IndexError: if stack is empty.
        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._main_data[-1]

    def get_min(self) -> Any:
        """
        Returns the actual minimal object in the stack.(min_data top)
        """
        return self._min_data[-1]

    def copy(self) -> "DynamicTypedMinStack":
        """
        Creates a shallow copy of the stack.
        Returned stack has same attrs and data structures.
        """
        copied = DynamicTypedMinStack(key=self._key, dtype=self._dtype)
        copied._main_data = self._main_data.copy()
        copied._min_data = self._min_data.copy()
        return copied

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both stacks have same elements in same order.
        """
        if not isinstance(other, DynamicTypedMinStack):
            return False
        if self._dtype != other._dtype:
            return False
        return list(other._main_data) == list(self._main_data) and list(
            other._min_data
        ) == list(self._min_data)

    def __len__(self) -> int:
        """Returns number of elements in the stack."""
        return len(self._main_data)

    def __iter__(self) -> Generator[Any, None, None]:
        """
        Iterates over values from top to bottom.
        Does not modify the stack.
        """
        current = len(self._main_data) - 1
        while current >= 0:
            yield self._main_data[current]
            current -= 1

    def __repr__(self) -> str:
        """
        Returns string representation of the stack.
        Example: DynamicTypedMinStack(dtype=int, top=[3, 2, 1], min=1)
        """
        items = list(self)
        current_min = self._min_data[-1] if len(self._min_data) > 0 else None
        return f"DynamicTypedMinStack(dtype={self._dtype.__name__}, top={items}, min={current_min})"
