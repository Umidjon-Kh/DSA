from typing import Any, Callable, Optional


def validate_index(index: Any, size: int) -> int:
    """
    Validates and normalizes index for methods that need index in right format.
    Supports negative indexing. Valid range: 0 to size-1.

    Returns: normalized index.

    Raises:
        TypeError: if index is not integer.
        IndexError: if index is out of range.
    """
    if not isinstance(index, int) or isinstance(index, bool):
        raise TypeError(f"Index must be integer, got ({type(index).__name__})")
    if index < 0:
        index += size
    if index < 0 or index >= size:
        raise IndexError(f"Index ({index}) is out of range for size ({size})")
    return index


def validate_insert_index(index: Any, size: int) -> int:
    """
    Validates and normalizes index for operations that adds value to data structures.
    Allows index == size (insert at end). Valid range: 0 to size.

    Returns: normalized index.

    Raises:
        TypeError: if index is not integer.
        IndexError: if index is out of range.
    """
    if not isinstance(index, int) or isinstance(index, bool):
        raise TypeError(f"Index must be integer, got ({type(index).__name__})")
    if index < 0:
        index += size
    if index < 0 or index > size:
        raise IndexError(f"Index ({index}) out of range for size ({size})")
    return index


def validate_capacity(capacity: Optional[int], args_length: int, structure: str) -> int:
    """
    Validates and returns computed capacity value for data structures with fixed-size.
    Allows Optional capacity or args_length,
    But if does not received at least one argument or capacity value raises TypeError.

    Returns: computed capacity value.

    Raises:
        TypeError: if capacity is provided but not integer.
        OverflowError: if both argument is provided but args_length is more than capacity.
        ValueError: if capacity is provided but less than or equal to 0.
        TypeError: if not provided at least one argument or capacity value.
    """
    if capacity is not None:
        if not isinstance(capacity, int) or isinstance(capacity, bool):
            raise TypeError(f"Capacity must be int, got ({type(capacity).__name__!r})")
        if capacity <= 0:
            raise ValueError(f"capacity must be >= 1, got ({capacity})")
        if capacity < args_length:
            raise OverflowError(
                f"Too many initial elements: {args_length} > capacity {capacity}"
            )
        return capacity
    elif args_length != 0:
        return args_length
    else:
        raise TypeError(
            f"{structure} requires at least one of: capacity or initial elements"
        )


def validate_key_function(key: Optional[Callable]) -> Callable:
    """
    Validates and returns computed key function for all MinStacks
    variations. Key argument is optional cause if user not provided
    key function it uses default function (lambda x: x).

    Returns: computed callable for key function.

    Raises:
        TypeError: If key is provided but not callable.
    """
    if key is not None:
        if not callable(key):
            raise TypeError(f"Key must be callable, got ({type(key).__name__})")
        return key
    else:
        return lambda x: x


def validate_value_type(value: Any, dtype: type) -> None:
    """
    Validates that value matches the structure
    storing data type, if matches returns True otherwise
    raises TypeError.

    Raises:
        TypeError: if value not matches data type.
    """
    if not isinstance(value, dtype) or dtype is int and isinstance(value, bool):
        raise TypeError(f"Expected {dtype.__name__}, got ({type(value).__name__!r})")
