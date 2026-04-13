"""
Selection Sort
==============
A simple comparison-based sorting algorithm that divides the sequence into
two parts: a sorted part (at the beginning) and an unsorted part (at the end).
On each iteration, the algorithm finds the minimum element in the unsorted
part and moves it to the end of the sorted part.

Core idea
---------
On each pass through the remaining unsorted portion, find the element with
the minimum value and move it to its correct position in the sorted portion:

    for each position i:
        find minimum in unsorted part (from i to end)
        swap minimum with sequence[i]

After the first pass, the smallest element is in position 0.  After the
second pass, the second-smallest is in position 1.  Repeating n - 1 times
guarantees a fully sorted sequence.

    Pass 1:  [64, 25, 12, 22, 11]  →  [11, 25, 12, 22, 64]   (11 is minimum)
    Pass 2:  [11, 25, 12, 22, 64]  →  [11, 12, 25, 22, 64]   (12 is minimum)
    Pass 3:  [11, 12, 25, 22, 64]  →  [11, 12, 22, 25, 64]   (22 is minimum)
    Pass 4:  [11, 12, 22, 25, 64]  →  [11, 12, 22, 25, 64]   (25 is minimum)
    Done.

Requirements
------------
1. Every element must support ``__eq__`` and ``__lt__``.
   Non-comparable elements raise ``TypeError``.

2. Unlike searching algorithms, selection sort does NOT require the sequence
   to be sorted in advance — sorting is precisely its job.

Functions
---------
    selection_sort(sequence)  -> list

Time complexity
---------------
    O(n²) — always, regardless of input order.

    Why always O(n²)?
        • Outer loop runs n - 1 times
        • Inner loop (finding minimum) runs (n - 1), (n - 2), ..., 1 times
        • Total comparisons: (n-1) + (n-2) + ... + 1 = n*(n-1)/2 = O(n²)

    This is constant regardless of whether data is sorted, reverse-sorted,
    or random.  Selection sort cannot take advantage of pre-sorted input.

Space complexity
----------------
    O(1) — sorting is done in-place; only a few scalar variables are
           allocated regardless of input size.

Stability
---------
    Selection sort is NOT stable.  When you find the minimum and swap it
    with position i, you might move an element past other equal elements,
    changing their relative order.

Advantages
----------
- Simple to understand and implement
- In-place — requires only O(1) extra space
- Minimal number of swaps — exactly n - 1 swaps (best for write-heavy media)
- Predictable O(n²) always — no best/average/worst case variance

Disadvantages
-----------
- Very slow for large datasets — O(n²) always
- Not stable — equal elements may change relative order
- Not adaptive — cannot take advantage of partially sorted input
- Not used in production code (use Timsort, Quicksort, or Mergesort instead)

Examples
--------
    >>> selection_sort([64, 25, 12, 22, 11])
    [11, 12, 22, 25, 64]

    >>> selection_sort([1])
    [1]

    >>> selection_sort([])
    []

    >>> selection_sort([3, 3, 1, 2])
    [1, 2, 3, 3]
"""

from collections.abc import Sequence
from typing import Any

from .._tools import is_comparable

# ─────────────────────────────────────────────────────────────────────────────
#  Selection sort
# ─────────────────────────────────────────────────────────────────────────────


def selection_sort(sequence: Sequence[Any]) -> list:
    """
    Sorts *sequence* in ascending order using the selection sort algorithm.

    On every outer iteration ``i``, the inner loop finds the minimum element
    in the remaining unsorted portion (from position ``i`` to the end) and
    swaps it with the element at position ``i``.  After iteration ``i``, the
    first ``i`` elements are sorted and in their final positions.

    How it works
    ------------
    Two nested loops drive the sort:

        outer loop (i):  represents the current position where the next
                         smallest element should be placed.  After iteration i,
                         the first i elements are sorted.

        inner loop (j):  scans the unsorted suffix (from i+1 to end) to find
                         the index of the minimum element. Comparability is
                         checked during this scan.

    The minimum element found in the inner loop is swapped with the element
    at position i.  After n - 1 outer iterations, the entire sequence is
    sorted and all elements are in their correct positions.

    Args:
        sequence: Any sequence whose elements support == and <.

    Returns:
        A new sorted list.  The original sequence is not modified.

    Raises:
        TypeError: If any element does not support == and < operators.

    Examples:
        >>> selection_sort([64, 25, 12, 22, 11])
        [11, 12, 22, 25, 64]

        >>> selection_sort([5, 3, 1, 4, 2])
        [1, 2, 3, 4, 5]

        >>> selection_sort([1])
        [1]

        >>> selection_sort([])
        []

        >>> selection_sort([3, 3, 1, 2])
        [1, 2, 3, 3]

    Time complexity:  O(n²)  — always, regardless of input order
    Space complexity: O(1)   — in-place sorting
    """
    result = list(sequence)
    n = len(result)

    # Outer loop: iterate through each position where we place the next minimum
    for i in range(n):
        # Find the index of the minimum element in the unsorted portion
        min_index = i

        # Inner loop: scan from i+1 to the end to find the minimum
        for j in range(i + 1, n):
            if not is_comparable(result[j]):
                raise TypeError(
                    f"Elements must support == and < operators, "
                    f"got {type(result[j]).__name__!r}."
                )
            if result[j] < result[min_index]:
                min_index = j

        # Swap the minimum element with the element at position i
        result[i], result[min_index] = result[min_index], result[i]

    return result
