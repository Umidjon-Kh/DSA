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
