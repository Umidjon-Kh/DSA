"""
Sliding Window
==============
A technique that maintains a contiguous sub-sequence (the "window") as it
slides from left to right across a sequence, updating a running aggregate
instead of recomputing it from scratch on every step.

Core idea
---------
A naive approach to subarray problems uses two nested loops — for every
starting position, scan the entire window again.  Cost: O(n * k).

Sliding Window avoids this by keeping a running value (sum, count, etc.)
and updating it in O(1) as the window moves one step right:

    new_value = old_value - element_leaving_left + element_entering_right

One pass through the sequence → O(n) total, regardless of window size.

Visual
------
    sequence = [1, 3, 5, 2, 8, 4, 6],  k = 3

    window      elements      sum
    ────────    ──────────    ───
    [0, 2]      1  3  5        9
    [1, 3]      3  5  2       10      (9 - 1 + 2)
    [2, 4]      5  2  8       15     (10 - 3 + 8)
    [3, 5]      2  8  4       14     (15 - 5 + 4)
    [4, 6]      8  4  6       18  ← maximum  (14 - 2 + 6)

Two window types
----------------
    FIXED    — window size is constant (given as parameter *k*).
               The window moves exactly one step right per iteration.
               Use when the subarray length is known upfront.

    VARIABLE — window grows or shrinks depending on a condition.
               ``right`` always advances; ``left`` shrinks the window
               when a constraint is violated.
               Use when you are looking for the shortest / longest
               subarray that satisfies some property.

    This module implements the fixed-size variant.
    Variable-size windows follow the same left/right pointer idea
    but add a shrink step — a natural extension once the fixed
    pattern is solid.

Comparison with Two Pointers
-----------------------------
Both techniques use a left and right index, but they differ in movement:

    Two Pointers   — pointers can move toward each other or independently.
    Sliding Window — the window only moves rightward; left never passes right.

Requirements
------------
    Elements must support + and - (``__add__`` and ``__sub__``).
    Strings, for example, support + but not - and cannot be used here.
    Use ``is_addable()`` from ``_tools.validators`` to check before passing
    custom objects.

Functions
---------
    max_sum_subarray(sequence, k)  -> Any

Time complexity
---------------
    max_sum_subarray : O(n) — single pass after O(k) initialisation.

Space complexity
----------------
    max_sum_subarray : O(1) — only a few scalar variables.
"""

from collections.abc import Sequence
from typing import Any

from .._tools import is_addable, is_comparable

# ─────────────────────────────────────────────────────────────────────────────
#  Fixed sliding window
# ─────────────────────────────────────────────────────────────────────────────


def max_sum_subarray(sequence: Sequence[Any], k: int) -> Any:
    """
    Finds the maximum sum of any contiguous subarray of length *k*.

    How it works
    ------------
    Phase 1 — build the first window by summing ``sequence[0:k]``.
    Phase 2 — slide the window one step at a time:

        window_sum = window_sum - sequence[right - k] + sequence[right]

    Subtracting the element that leaves the left edge and adding the
    element that enters the right edge keeps the sum current in O(1).
    Track the maximum seen so far and return it at the end.

    Args:
        sequence: A sequence of elements that support + and -.
        k:        Window size (must be ≥ 1 and ≤ len(sequence)).

    Returns:
        The maximum subarray sum found across all windows of size *k*.

    Raises:
        ValueError: If *k* is less than 1 or greater than len(sequence).
        TypeError: if item in provided sequnce is not addable.

    Examples:
        >>> max_sum_subarray([1, 3, 5, 2, 8, 4, 6], 3)
        18
        >>> max_sum_subarray([1, 3, 5, 2, 8, 4, 6], 1)
        8
        >>> max_sum_subarray([4, 4, 4, 4], 2)
        8
        >>> max_sum_subarray([-3, -1, -2, -5], 2)
        -3

    Time complexity:  O(n)  — one pass after O(k) window initialisation
    Space complexity: O(1)  — three scalar variables
    """
    n = len(sequence)

    if k < 1 or k > n:
        raise ValueError(
            f"Window size k={k} is out of range for a sequence of length {n}. "
            f"k must be between 1 and {n} inclusive."
        )

    # ── Phase 1: build the initial window sum ─────────────────────────────────
    # Start with the first element and add the rest one by one.
    # Avoids creating a temporary slice (which would cost O(k) extra memory).
    window_sum = sequence[0]

    # Validate it for support operands(+,-) and comparsion protocol
    if not is_addable(window_sum) or not is_comparable(window_sum):
        raise TypeError(
            "Sequence must contain only items that support operands('+','-') "
            "and comparison protocol."
        )
    for idx in range(1, k):
        window_sum += sequence[idx]

    max_sum = window_sum

    # ── Phase 2: slide the window across the rest of the sequence ─────────────
    for right in range(k, n):
        # Subtract the element leaving the left edge of the window
        window_sum -= sequence[right - k]
        # Add the element entering the right edge of the window
        window_sum += sequence[right]

        if window_sum > max_sum:
            max_sum = window_sum

    return max_sum
