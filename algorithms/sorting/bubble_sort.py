"""
Bubble Sort
===========
A simple comparison-based sorting algorithm that repeatedly steps through the
list, compares adjacent elements, and swaps them if they are in the wrong order.
The algorithm gets its name because smaller elements "bubble" to the top
(beginning) of the list with each pass.

Core idea
---------
On each pass through the sequence, we compare every adjacent pair and swap if
the left element is greater than the right:

    for each pass:
        for each adjacent pair:
            if left > right:
                swap(left, right)

After the first pass, the largest element is guaranteed to be in its final
position at the end. After the second pass, the second-largest is in place.
Each pass places one more element in its final position.

Visual example (ascending order)
--------------------------------
Initial:      [5, 3, 8, 4, 2]

Pass 1:       5 > 3 → swap   [3, 5, 8, 4, 2]
              5 < 8 → no swap [3, 5, 8, 4, 2]
              8 > 4 → swap    [3, 5, 4, 8, 2]
              8 > 2 → swap    [3, 5, 4, 2, 8]  ← 8 is now in final position

Pass 2:       3 < 5 → no swap [3, 5, 4, 2, 8]
              5 > 4 → swap    [3, 4, 5, 2, 8]
              5 > 2 → swap    [3, 4, 2, 5, 8]  ← 5 is now in final position

Pass 3:       3 < 4 → no swap [3, 4, 2, 5, 8]
              4 > 2 → swap    [3, 2, 4, 5, 8]  ← 4 is now in final position

Pass 4:       3 > 2 → swap    [2, 3, 4, 5, 8]  ← sorted!

Requirements
------------
1. Every element must support the comparison operators ``__lt__`` (less than)
   and ``__gt__`` (greater than).  Non-comparable elements raise ``TypeError``.

2. The sequence must be a mutable list (not a tuple or string).
   Bubble sort works by modifying elements in-place.

Functions
---------
    bubble_sort(array)              -> None
    bubble_sort_optimized(array)    -> None

Advantages
----------
- Simple to understand and implement
- Stable — maintains relative order of equal elements
- In-place — requires only O(1) extra space
- Useful for nearly-sorted data (optimized version)

Disadvantages
-----------
- Very slow for large datasets — O(n²) comparisons and swaps
- Performs many unnecessary swaps
- Not used in production code (use Timsort, Quicksort, or Mergesort instead)

Time complexity
---------------
    Worst case (reverse sorted)  : O(n²)  — n² comparisons and swaps
    Average case                 : O(n²)  — random order still requires many passes
    Best case (already sorted)   : O(n)   — optimized version with early exit

Space complexity
----------------
    Both variants : O(1)  — only a few temporary variables (no recursion)

Stability
---------
    Bubble sort IS stable.  Equal elements maintain their relative order
    because we only swap when left > right (never when left == right).
"""

from typing import Any, List

# ─────────────────────────────────────────────────────────────────────────────
#  Basic bubble sort
# ─────────────────────────────────────────────────────────────────────────────


def bubble_sort(array: List[Any]) -> None:
    """
    Sorts *array* in-place in ascending order using the bubble sort algorithm.

    On each pass, adjacent elements are compared and swapped if they are out
    of order. After n passes, the array is guaranteed to be sorted.

    How it works
    ------------
    Outer loop runs n times (n = length of array).
    Inner loop compares every adjacent pair and swaps if needed.
    After pass i, the last i elements are in their final positions.

        Pass 1: compare all pairs                  → largest element moves to end
        Pass 2: compare all but last pair          → second-largest moves to end - 1
        ...
        Pass n: compare first two elements         → array is sorted

    Args:
        array: A mutable list of comparable elements (support < and >).

    Returns:
        None — the list is sorted in-place.

    Raises:
        TypeError: If any element does not support < and >.

    Examples:
        >>> arr = [64, 34, 25, 12, 22, 11, 90]
        >>> bubble_sort(arr)
        >>> arr
        [11, 12, 22, 25, 34, 64, 90]

        >>> arr = [5, 2, 8, 1, 9]
        >>> bubble_sort(arr)
        >>> arr
        [1, 2, 5, 8, 9]

        >>> arr = [3, 3, 1, 2]
        >>> bubble_sort(arr)
        >>> arr
        [1, 2, 3, 3]

        >>> arr = [1]
        >>> bubble_sort(arr)
        >>> arr
        [1]

        >>> arr = []
        >>> bubble_sort(arr)
        >>> arr
        []

    Time complexity:  O(n²)  — always n² comparisons regardless of input
    Space complexity: O(1)   — in-place sorting
    """
    n = len(array)

    # Outer loop: each pass places one element in its final position
    for i in range(n):
        # Inner loop: compare adjacent elements from start to (n - i - 1)
        # After i passes, the last i elements are already sorted
        for j in range(n - i - 1):
            # Swap if the current element is greater than the next
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]


# ─────────────────────────────────────────────────────────────────────────────
#  Optimized bubble sort with early termination
# ─────────────────────────────────────────────────────────────────────────────


def bubble_sort_optimized(array: List[Any]) -> None:
    """
    Sorts *array* in-place using bubble sort with early termination.

    If the array becomes sorted before all n passes are complete, this
    version detects it and stops early. This makes the best-case time
    complexity O(n) instead of O(n²) for nearly-sorted data.

    How it works
    ------------
    Same as basic bubble sort, but we track whether any swaps occurred
    during a pass.  If no swaps happened, the array is sorted and we can
    stop immediately.

    Optimization rationale
    ----------------------
    On each pass, if no swaps occur:
        1. Every pair was already in correct order (left <= right)
        2. The array is sorted
        3. No future pass will change anything
        4. Exit immediately — saves remaining passes

    This makes the algorithm adaptive — it takes advantage of partially
    sorted or already-sorted input.

    Args:
        array: A mutable list of comparable elements (support < and >).

    Returns:
        None — the list is sorted in-place.

    Raises:
        TypeError: If any element does not support < and >.

    Examples:
        >>> arr = [1, 2, 3, 4, 5]  # already sorted
        >>> bubble_sort_optimized(arr)
        >>> arr
        [1, 2, 3, 4, 5]

        >>> arr = [5, 1, 2, 3, 4]  # nearly sorted
        >>> bubble_sort_optimized(arr)
        >>> arr
        [1, 2, 3, 4, 5]

        >>> arr = [64, 34, 25, 12, 22, 11, 90]
        >>> bubble_sort_optimized(arr)
        >>> arr
        [11, 12, 22, 25, 34, 64, 90]

        >>> arr = []
        >>> bubble_sort_optimized(arr)
        >>> arr
        []

    Time complexity:
        Best case (already sorted)   : O(n)   — one pass, no swaps
        Average case                 : O(n²)  — mostly random data
        Worst case (reverse sorted)  : O(n²)  — every comparison requires swap

    Space complexity: O(1)   — in-place sorting
    """
    n = len(array)

    # Outer loop: each pass potentially places one element in final position
    for i in range(n):
        # Track whether a swap occurred in this pass
        swapped = False

        # Inner loop: compare adjacent elements
        for j in range(n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                swapped = True

        # If no swaps occurred, the array is already sorted
        if not swapped:
            break
