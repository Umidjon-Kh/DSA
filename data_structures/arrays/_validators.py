from typing import Any


def validate_index(index: Any, size: int) -> int:
    """
    Validates and normalizes index for get, set and remove operations.
    Supports negative indexing. Valid range: 0 to size-1.

    Returns normalized index.

    Raises:
        TypeError: if index is not int.
        IndexError: if index is out of range.
    """
    if not isinstance(index, int):
        raise TypeError(f"Index must be integer, got ({type(index).__name__})")
    if index < 0:
        index += size
    if index < 0 or index >= size:
        raise IndexError(f"Index {index} out of range for size {size}")
    return index


def validate_insert_index(index: Any, size: int) -> int:
    """
    Validates and normalizes index for insert operation.
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
        raise IndexError(f"Index {index} out of range for size {size}")
    return index
