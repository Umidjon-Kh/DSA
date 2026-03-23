from typing import Any, Optional


def validate_index(index: Any, size: int) -> int:
    """
    Validates nd normalizes index for methods that need index in right format.
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
    Validates and normalizes index for operation that adds value to data structures.
    Allows index == size (insert at end). Valid range: 0 to size.

    Returns normalized index.

    Raises:
        TypeError: if index is not int.
        IndexError: if index is out of range.
    """
    if not isinstance(index, int):
        raise TypeError(f"Index must be integer, got ({type(index).__name__})")
    if index < 0:
        index += size
    if index < 0 or index > size:
        raise IndexError(f"Index ({index}) out of range for size ({size})")
    return index


def validate_capacity(capacity: Optional[Any], *args) -> int:
    """
    Validates and returns computed capacity value for data structures with fixed-size.
    Allows Optional capacity or *args,
    But if does not received at least one argument or capacity value raises TypeError.

    Returns: computed capacity value.

    Raises:
        TypeError: if capcity is provided but not integer.
        ValueError: if both arguments is provided but len(args) is more than capacity.
        ValueError: if capcity is provided but less or equal to 0.
        TypeError: if not provided at least one argument or capacity value.
    """
    if capacity is not None:
        if not isinstance(capacity, int) or isinstance(capacity, bool):
            raise TypeError(f"capacity must be int, got {type(capacity).__name__!r}")
        if capacity <= 0:
            raise ValueError(f"capacity must be >= 1, got {capacity}")
        if capacity < len(args):
            raise ValueError(
                f"Too many initial elemenets: {len(args)} > capacity {capacity}"
            )
        return capacity
    else:
        return len(args)
