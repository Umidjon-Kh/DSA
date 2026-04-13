"""
Bubble Sort
===========
A family of sorting algorithms that repeatedly step through the sequence,
compare adjacent elements, and swap them if they are in the wrong order.
Larger elements gradually "bubble up" toward the end of the sequence —
hence the name.

Core idea
---------
On each pass through the sequence, every adjacent pair is compared:

    sequence[j] > sequence[j + 1]  →  swap them

After the first pass the largest element is guaranteed to be at the last
position.  After the second pass the second-largest is in its correct spot.
Repeating n - 1 times guarantees a fully sorted sequence.

    Pass 1:  [5, 3, 1, 4, 2]  →  [3, 1, 4, 2, 5]   (5 bubbled to the end)
    Pass 2:  [3, 1, 4, 2, 5]  →  [1, 3, 2, 4, 5]   (4 bubbled to position)
    Pass 3:  [1, 3, 2, 4, 5]  →  [1, 2, 3, 4, 5]   (3 bubbled to position)
    Done.

Requirements
------------
1. Every element must support ``__eq__`` and ``__lt__``.
   Non-comparable elements raise ``TypeError``.

2. Unlike searching algorithms, bubble sort does NOT require the sequence
   to be sorted in advance — sorting is precisely its job.

Functions
---------
    bubble_sort(sequence)            -> list
    bubble_sort_optimized(sequence)  -> list

Variants
--------
    bubble_sort           — classic O(n²) implementation, always runs n-1 passes.
    bubble_sort_optimized — early-exit variant: if a full pass produces no swaps
                            the sequence is already sorted and the algorithm stops.

                            Best case (already sorted input):
                                classic    — O(n²)   still runs all passes
                                optimized  — O(n)    exits after the first pass

Time complexity
---------------
    bubble_sort           : O(n²)  — always, regardless of input order
    bubble_sort_optimized : O(n²)  — worst / average case (random input)
                            O(n)   — best case (already sorted input)

Space complexity
----------------
    Both variants: O(1) — sorting is done in-place; only a few scalar
                          variables are allocated regardless of input size.
"""

from collections.abc import Sequence
from typing import Any

from .._tools import is_comparable

# ─────────────────────────────────────────────────────────────────────────────
#  1. Classic bubble sort
# ─────────────────────────────────────────────────────────────────────────────


def bubble_sort(sequence: Sequence[Any]) -> list:
    """
    Sorts *sequence* in ascending order using the classic bubble sort algorithm.

    On every outer iteration ``i``, the inner loop runs from the start up to
    the last unsorted position (``n - i - 1``).  After iteration ``i``, the
    ``i`` largest elements are already in their final positions at the tail of
    the list, so the inner loop shrinks by one each time.

    How it works
    ------------
    Two nested loops drive the sort:

        outer loop (i):  counts completed passes; after pass i, the last i
                         elements are in their final sorted positions.

        inner loop (j):  walks adjacent pairs in the unsorted prefix and
                         swaps whenever the left neighbour is greater:

                             sequence[j] > sequence[j + 1]  →  swap

    After n - 1 outer iterations every element is in its correct position.

    Args:
        sequence: Any sequence whose elements support == and <.

    Returns:
        A new sorted list.  The original sequence is not modified.

    Raises:
        TypeError: If any element does not support == and < operators.

    Examples:
        >>> bubble_sort([5, 3, 1, 4, 2])
        [1, 2, 3, 4, 5]
        >>> bubble_sort([1])
        [1]
        >>> bubble_sort([])
        []
        >>> bubble_sort([3, 3, 1, 2])
        [1, 2, 3, 3]

    Time complexity:  O(n²)
    Space complexity: O(1)
    """
    result = list(sequence)
    n = len(result)

    for i in range(n):
        # The last i elements are already in their final positions
        for j in range(0, n - i - 1):
            if not is_comparable(result[j]):
                raise TypeError(
                    f"Elements must support == and < operators, "
                    f"got {type(result[j]).__name__!r}."
                )
            if result[j] > result[j + 1]:
                # Swap adjacent elements that are out of order
                result[j], result[j + 1] = result[j + 1], result[j]

    return result


# ─────────────────────────────────────────────────────────────────────────────
#  2. Optimized bubble sort  (early exit)
# ─────────────────────────────────────────────────────────────────────────────


def bubble_sort_optimized(sequence: Sequence[Any]) -> list:
    """
    Sorts *sequence* in ascending order using an optimized bubble sort that
    exits early when the sequence is already sorted.

    Identical to :func:`bubble_sort` in structure, but tracks whether any
    swap occurred during the inner loop.  If a complete inner pass finishes
    with zero swaps, the sequence is fully sorted and the algorithm stops
    immediately — no further passes are needed.

    How it works
    ------------
    Same two-loop structure as the classic variant, with one addition:

        ``swapped`` flag — reset to False at the start of each outer pass.

        If the inner loop completes and ``swapped`` is still False, every
        adjacent pair was already in order → the sequence is sorted → break.

    This optimisation does not help in the average case (random data) but
    makes an enormous difference on nearly-sorted or already-sorted inputs,
    reducing work from O(n²) to O(n).

    Args:
        sequence: Any sequence whose elements support == and <.

    Returns:
        A new sorted list.  The original sequence is not modified.

    Raises:
        TypeError: If any element does not support == and < operators.

    Examples:
        >>> bubble_sort_optimized([5, 3, 1, 4, 2])
        [1, 2, 3, 4, 5]
        >>> bubble_sort_optimized([1, 2, 3, 4, 5])   # already sorted -> O(n)
        [1, 2, 3, 4, 5]
        >>> bubble_sort_optimized([])
        []
        >>> bubble_sort_optimized([3, 3, 1, 2])
        [1, 2, 3, 3]

    Time complexity:  O(n²) worst/average case, O(n) best case (sorted input)
    Space complexity: O(1)
    """
    result = list(sequence)
    n = len(result)

    for i in range(n):
        swapped = False

        # The last i elements are already in their final positions
        for j in range(0, n - i - 1):
            if not is_comparable(result[j]):
                raise TypeError(
                    f"Elements must support == and < operators, "
                    f"got {type(result[j]).__name__!r}."
                )
            if result[j] > result[j + 1]:
                # Swap adjacent elements that are out of order
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True

        if not swapped:
            # No swaps in this pass — sequence is fully sorted, stop early
            break

    return result
