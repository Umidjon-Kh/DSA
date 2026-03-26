from typing import Any, Optional


def validate_index(index: Any, size: int) -> int:
    """
    Validates and normalizes index for methods that need index in right format.
    Supports negative indexing. Valid range: 0 to size-1.

    Returns: normalized index.

    Raises:
        TypeError: if index is not integer.
        ValueError: if index is out of range.
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
    Validates and returns computed capacity value for data strucutures with fixed-size.
    Allows Optional capacity or args_length,
    But if does not received at least one argument or capacity value raises TypeError.

    Returns: computed capacity value.

    Raises:
        TypeError: if capacity is provided but not integer.
        ValueError: if both argument is provided but args_length is more than capacity.
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
