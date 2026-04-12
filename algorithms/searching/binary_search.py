"""
Binary Search
=============
A family of search algorithms that operate on **sorted** sequences by
repeatedly halving the search space until the target is found or the
search space is exhausted.

Core idea
---------
Instead of scanning every element (O(n)), binary search jumps to the
middle of the current search space and asks one question:
    "Is the target less than, equal to, or greater than this element?"

That single comparison eliminates half the remaining elements.
Repeating this gives O(log n) — a sorted array of 1 000 000 000 elements
requires at most ~30 comparisons.

    Array size      Max comparisons
    ----------      ---------------
    100             7
    10 000          14
    1 000 000       20
    1 000 000 000   30

Requirements
------------
1. The sequence must be **sorted in ascending order**.
   Passing an unsorted sequence does NOT raise an error — the function
   simply returns a wrong answer silently.

2. Every element (and the target itself) must support ``__eq__`` and
   ``__lt__``.  Non-comparable elements raise ``TypeError``.

Functions
---------
    is_comparable(item)                          -> bool
    iterative_binary_search(array, target, mode) -> int
    recursive_binary_search(array, target, mode) -> int

Modes (SearchMode enum)
-----------------------
    None              — return any matching index  (default)
    SearchMode.FIRST  — return the FIRST (leftmost) occurrence
    SearchMode.LAST   — return the LAST  (rightmost) occurrence

    Useful when the array contains duplicates:

        arr = [1, 3, 3, 3, 7]

        iterative_binary_search(arr, 3)                    # → 2 (any)
        iterative_binary_search(arr, 3, SearchMode.FIRST)  # → 1
        iterative_binary_search(arr, 3, SearchMode.LAST)   # → 3

Time complexity
---------------
    iterative_binary_search : O(log n)  — no call-stack overhead
    recursive_binary_search : O(log n)  — each call halves the space;
                                          depth never exceeds ~log₂(n)
                                          so Python's recursion limit
                                          (default 1 000) is never reached
                                          for any real-world array size.

Space complexity
----------------
    iterative : O(1)       — three integer variables
    recursive : O(log n)   — one stack frame per recursion level
"""

from collections.abc import Sequence
from enum import Enum
from typing import Any, Optional

# ─────────────────────────────────────────────────────────────────────────────
#  Search mode
# ─────────────────────────────────────────────────────────────────────────────


class SearchMode(Enum):
    """
    Controls which occurrence is returned when duplicates are present.

    Attributes:
        FIRST: Return the index of the leftmost (first) matching element.
        LAST:  Return the index of the rightmost (last) matching element.
    """

    FIRST = "first"
    LAST = "last"


# ─────────────────────────────────────────────────────────────────────────────
#  Helper
# ─────────────────────────────────────────────────────────────────────────────


def is_comparable(item: Any) -> bool:
    """
    Returns True if *item* supports the minimum comparison protocol
    required by binary search (``__eq__`` and ``__lt__``).

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


# ─────────────────────────────────────────────────────────────────────────────
#  Iterative binary search
# ─────────────────────────────────────────────────────────────────────────────


def iterative_binary_search(
    array: Sequence[Any],
    target: Any,
    mode: Optional[SearchMode] = None,
) -> int:
    """
    Searches *array* for *target* using an iterative approach.

    Iterative binary search is the preferred production variant — it uses
    O(1) extra space and avoids any call-stack overhead.

    How it works
    ------------
    Two pointers, ``low`` and ``high``, mark the current search window.
    On every iteration the midpoint ``mid`` is computed and compared with
    the target:

        array[mid] == target  →  match found (behaviour depends on *mode*)
        array[mid]  < target  →  target is in the RIGHT half → low  = mid + 1
        array[mid]  > target  →  target is in the LEFT  half → high = mid - 1

    The loop ends when ``low > high`` (search space exhausted).

    Args:
        array:  A sorted sequence whose elements support == and <.
        target: The value to search for.
        mode:   SearchMode.FIRST  — find the leftmost occurrence.
                SearchMode.LAST   — find the rightmost occurrence.
                None (default)    — return any matching index immediately.

    Returns:
        The index of the matching element, or -1 if not found.

    Raises:
        TypeError: If *target* does not support == and <.

    Examples:
        >>> iterative_binary_search([1, 3, 5, 7, 9], 7)
        3
        >>> iterative_binary_search([1, 3, 5, 7, 9], 4)
        -1
        >>> iterative_binary_search([1, 3, 3, 3, 7], 3, SearchMode.FIRST)
        1
        >>> iterative_binary_search([1, 3, 3, 3, 7], 3, SearchMode.LAST)
        3

    Time complexity:  O(log n)
    Space complexity: O(1)
    """
    if not is_comparable(target):
        raise TypeError(
            f"Target must support == and < operators, got {type(target).__name__!r}."
        )

    low = 0
    high = len(array) - 1
    result = -1  # -1 means "not found yet"

    while low <= high:
        # Integer midpoint — avoids float division and potential overflow
        # (in Python ints are arbitrary precision so overflow isn't an issue,
        #  but this form is the standard convention and maps cleanly to C/Java)
        mid = (low + high) // 2

        if array[mid] == target:
            result = mid

            if mode is SearchMode.FIRST:
                # Match found — but keep searching LEFT for an earlier one
                high = mid - 1

            elif mode is SearchMode.LAST:
                # Match found — but keep searching RIGHT for a later one
                low = mid + 1

            else:
                # No mode — return immediately (first match we find is fine)
                return mid

        elif array[mid] < target:
            # Mid value is too small — target must be to the RIGHT
            low = mid + 1

        else:
            # Mid value is too large — target must be to the LEFT
            high = mid - 1

    # Loop ended: either not found (result == -1) or best match stored
    return result


# ─────────────────────────────────────────────────────────────────────────────
#  Recursive binary search
# ─────────────────────────────────────────────────────────────────────────────


def recursive_binary_search(
    array: Sequence[Any],
    target: Any,
    low: int = 0,
    high: Optional[int] = None,
    mode: Optional[SearchMode] = None,
    result: int = -1,
) -> int:
    """
    Searches *array* for *target* using a recursive approach.

    Each call works on the sub-array ``array[low:high+1]``.
    The base case is ``low > high`` — the search space is empty.

    Compared with the iterative version this uses O(log n) stack space
    (one frame per recursion level), but is often easier to reason about
    when first learning the algorithm.

    Note on recursion depth
    -----------------------
    Because the search space halves on every call, the maximum depth is
    ⌈log₂(n)⌉.  For Python's default limit of 1 000 that would require
    an array with 2^1000 elements — effectively impossible in practice.

    Args:
        array:  A sorted sequence whose elements support == and <.
        target: The value to search for.
        low:    Left boundary of the current search window (default 0).
        high:   Right boundary of the current search window
                (default: last index, set automatically on first call).
        mode:   SearchMode.FIRST  — find the leftmost occurrence.
                SearchMode.LAST   — find the rightmost occurrence.
                None (default)    — return any matching index immediately.
        result: Accumulator that carries the best match found so far
                across recursive calls (default -1 = not found).

    Returns:
        The index of the matching element, or -1 if not found.

    Raises:
        TypeError: If *target* does not support == and <.

    Examples:
        >>> recursive_binary_search([1, 3, 5, 7, 9], 7)
        3
        >>> recursive_binary_search([1, 3, 5, 7, 9], 4)
        -1
        >>> recursive_binary_search([1, 3, 3, 3, 7], 3, mode=SearchMode.FIRST)
        1
        >>> recursive_binary_search([1, 3, 3, 3, 7], 3, mode=SearchMode.LAST)
        3

    Time complexity:  O(log n)
    Space complexity: O(log n)  — recursion depth
    """
    # ── First call only: set defaults and validate ────────────────────────────
    if high is None:
        high = len(array) - 1

        # Comparable check only on the first call — target type does not
        # change between recursive calls, so checking once is enough.
        if not is_comparable(target):
            raise TypeError(
                f"Target must support == and < operators, got {type(target).__name__!r}."
            )

    # ── Base case: search space is empty ─────────────────────────────────────
    if low > high:
        return result

    mid = (low + high) // 2

    # ── Compare and recurse ───────────────────────────────────────────────────
    if array[mid] == target:
        result = mid

        if mode is SearchMode.FIRST:
            # Keep searching LEFT — maybe there's an earlier occurrence
            return recursive_binary_search(array, target, low, mid - 1, mode, result)

        elif mode is SearchMode.LAST:
            # Keep searching RIGHT — maybe there's a later occurrence
            return recursive_binary_search(array, target, mid + 1, high, mode, result)

        else:
            # No mode — found it, stop immediately
            return mid

    elif array[mid] < target:
        # Target is in the RIGHT half
        return recursive_binary_search(array, target, mid + 1, high, mode, result)

    else:
        # Target is in the LEFT half
        return recursive_binary_search(array, target, low, mid - 1, mode, result)
