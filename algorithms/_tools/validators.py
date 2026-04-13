from typing import Any


def is_comparable(item: Any) -> bool:
    """
    Returns true if *item* supports the comparison protocol
    required for algorithmes that needs to compare.

    Args:
        item: Any Python object.

    Returns:
        True  — item can be compared with == and <.
        False — at least one operator is missing.

    Examples:
        >>> is_comparable(42)
        True
        >>> is_comparable("hello")
        True
        >>> is_comparable(object())
        False
    """
    return hasattr(item, "__eq__") and hasattr(item, "__lt__")


def is_addable(item: Any) -> bool:
    """
    Returns True if *item* supports addition and subtraction
    operators required by sliding window and similar algorithms.

    Args:
        item: Any Python object.

    Returns:
        True  — item supports both + and -.
        False — at least one operator is missing.

    Examples:
        >>> is_addable(42)
        True
        >>> is_addable("hello")
        False
        >>> is_addable(object())
        False
    """
    return hasattr(item, "__add__") and hasattr(item, "__sub__")
