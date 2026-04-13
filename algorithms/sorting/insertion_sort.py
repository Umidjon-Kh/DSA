"""
Insertion Sort
==============
A simple comparison-based sorting algorithm that builds a sorted sequence
one element at a time by inserting each new element into its correct position
within the already-sorted portion.

Core idea
---------
Iterate through the sequence starting from the second element. For each
element, find its correct position in the already-sorted left portion and
insert it there by shifting larger elements one position to the right.

    for each position i (starting from 1):
        take element at i
        find correct position in sorted portion (0 to i-1)
        shift all larger elements right by one
        insert element at correct position

After each iteration, the sorted portion grows by one element. After n - 1
iterations, the entire sequence is sorted.

    Pass 1:  [5] | 2 8 1 9  →  [2, 5] | 8 1 9      (insert 2 into [5])
    Pass 2:  [2, 5] | 8 1 9  →  [2, 5, 8] | 1 9    (8 already in place)
    Pass 3:  [2, 5, 8] | 1 9  →  [1, 2, 5, 8] | 9  (insert 1 at start)
    Pass 4:  [1, 2, 5, 8] | 9  →  [1, 2, 5, 8, 9]  (9 already in place)
    Done.

Requirements
------------
1. Every element must support ``__eq__`` and ``__lt__``.
   Non-comparable elements raise ``TypeError``.

2. Unlike searching algorithms, insertion sort does NOT require the sequence
   to be sorted in advance — sorting is precisely its job.

Functions
---------
    insertion_sort(sequence) -> list

Time complexity
---------------
    Best case (already sorted)    : O(n)   — inner while loop never executes
    Average case (random input)   : O(n²)  — typical random permutation
    Worst case (reverse sorted)   : O(n²)  — minimum element at the end
                                             must shift all other elements

    Why worst case is bad:
        When the array is reverse-sorted [5, 4, 3, 2, 1], each new element
        must shift past ALL previously processed elements:
            • 4 shifts past 5: 1 shift
            • 3 shifts past 5, 4: 2 shifts
            • 2 shifts past 5, 4, 3: 3 shifts
            • 1 shifts past 5, 4, 3, 2: 4 shifts
            Total: 1 + 2 + 3 + 4 = 10 shifts = O(n²)

Space complexity
----------------
    O(1) — sorting is done in-place; only a few scalar variables are
           allocated regardless of input size.

Stability
---------
    Insertion sort IS stable.  When inserting an element, we only shift
    past elements that are strictly greater (not equal).  Equal elements
    maintain their relative order because we stop shifting once we find
    an element that is not greater.

    Example:
        Input:  [(5, 'a'), (3, 'b'), (5, 'c')]
        After sorting by first element:
                [(3, 'b'), (5, 'a'), (5, 'c')]

        Notice: the two 5s kept their original order (5,'a') before (5,'c')

Advantages
----------
- Stable — maintains relative order of equal elements
- In-place — requires only O(1) extra space
- Adaptive — O(n) for nearly-sorted data
- Simple implementation — easy to understand and debug
- Efficient for small datasets — low overhead compared to Quick/Merge Sort
- Online — can sort as data arrives (useful for streams)

Disadvantages
-----------
- Very slow for large datasets — O(n²) in average/worst case
- Many shifts can be expensive on arrays with large elements
- Not used in production for large data (use Timsort, Quicksort, Mergesort)

When to use
-----------
- Sorting small arrays (< 50 elements)
- Nearly-sorted data
- Online sorting (data arrives one element at a time)
- Teaching/learning algorithm fundamentals
- Part of Timsort in Python for small subarrays

Examples
--------
    >>> insertion_sort([5, 2, 8, 1, 9])
    [1, 2, 5, 8, 9]

    >>> insertion_sort([1, 2, 3, 4, 5])  # already sorted
    [1, 2, 3, 4, 5]

    >>> insertion_sort([5, 4, 3, 2, 1])  # reverse sorted - worst case
    [1, 2, 3, 4, 5]

    >>> insertion_sort([1])
    [1]

    >>> insertion_sort([])
    []

    >>> insertion_sort([3, 3, 1, 2])
    [1, 2, 3, 3]
"""

from collections.abc import Sequence
from typing import Any

from .._tools import is_comparable

# ─────────────────────────────────────────────────────────────────────────────
#  Insertion sort
# ─────────────────────────────────────────────────────────────────────────────


def insertion_sort(sequence: Sequence[Any]) -> list:
    """
    Sorts *sequence* in ascending order using the insertion sort algorithm.

    Builds the sorted sequence incrementally.  On each iteration ``i``, the
    element at position ``i`` is inserted into its correct position within
    the already-sorted portion (indices 0 to i-1).  Larger elements are
    shifted one position to the right to make room.

    How it works
    ------------
    Two nested structures drive the sort:

        outer loop (i):  iterates through each element starting from index 1.
                         After iteration i, the first i+1 elements are sorted.

        inner while (j): scans backwards through the sorted portion to find
                         the correct insertion point. Stops when it finds an
                         element that is not greater than the current element.

    Shifting and insertion happen in the inner loop:
        • If array[j] > current, shift array[j] one position right
        • Continue until finding the insertion point
        • Place current at array[j + 1]

    This is exactly how humans sort playing cards in their hand.

    Args:
        sequence: Any sequence whose elements support == and <.

    Returns:
        A new sorted list.  The original sequence is not modified.

    Raises:
        TypeError: If any element does not support == and < operators.

    Examples:
        >>> insertion_sort([5, 2, 8, 1, 9])
        [1, 2, 5, 8, 9]

        >>> insertion_sort([1, 2, 3, 4, 5])
        [1, 2, 3, 4, 5]

        >>> insertion_sort([5, 4, 3, 2, 1])
        [1, 2, 3, 4, 5]

        >>> insertion_sort([1])
        [1]

        >>> insertion_sort([])
        []

        >>> insertion_sort([3, 3, 1, 2])
        [1, 2, 3, 3]

    Time complexity:
        Best case (already sorted)    : O(n)   — inner while never executes
        Average case (random)         : O(n²)  — typical random permutation
        Worst case (reverse sorted)   : O(n²)  — each element shifts past all others

    Space complexity: O(1)   — in-place sorting
    """
    result = list(sequence)
    n = len(result)

    # Start from the second element (index 1)
    # First element is already considered "sorted"
    for i in range(1, n):
        current = result[i]

        if not is_comparable(current):
            raise TypeError(
                f"Elements must support == and < operators, "
                f"got {type(current).__name__!r}."
            )

        j = i - 1

        # Shift all elements greater than current one position to the right
        # Continue until we find the correct insertion point
        while j >= 0 and result[j] > current:
            result[j + 1] = result[j]
            j -= 1

        # Insert current at its correct position
        result[j + 1] = current

    return result
