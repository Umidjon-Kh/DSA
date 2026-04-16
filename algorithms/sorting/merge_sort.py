"""
Merge Sort
==========
A recursive, divide-and-conquer sorting algorithm that splits the sequence
into halves, sorts each half independently, then merges the two sorted halves
back into a single sorted sequence.

Core idea
---------
Instead of sorting the whole sequence at once, merge sort breaks the problem
into smaller and smaller subproblems until each piece is trivially sorted
(a single element or empty), then combines them back in sorted order:

    DIVIDE:   split the sequence in half recursively until every piece
              has at most one element.

    CONQUER:  merge pairs of sorted pieces into larger sorted pieces.

    [5, 3, 1, 4, 2]

            [5, 3, 1, 4, 2]
           /               \\
       [5, 3, 1]         [4, 2]
       /       \\          /   \\
    [5, 3]    [1]       [4]   [2]
    /    \\
  [5]   [3]

  — merge back up —

  [5] + [3]      →  [3, 5]
  [3, 5] + [1]   →  [1, 3, 5]
  [4] + [2]      →  [2, 4]
  [1, 3, 5] + [2, 4]  →  [1, 2, 3, 4, 5]  ✓

The merge step is the heart of the algorithm.  Given two sorted sequences,
it walks both simultaneously, always appending the smaller front element:

    left  = [1, 3, 5]    right = [2, 4]

    1 < 2  →  take 1    result = [1]
    3 > 2  →  take 2    result = [1, 2]
    3 < 4  →  take 3    result = [1, 2, 3]
    5 > 4  →  take 4    result = [1, 2, 3, 4]
    left remains [5]    result = [1, 2, 3, 4, 5]

Requirements
------------
1. Every element must support ``__eq__`` and ``__lt__``.
   Non-comparable elements raise ``TypeError``.

2. Unlike searching algorithms, merge sort does NOT require the sequence
   to be sorted in advance — sorting is precisely its job.

3. Empty sequences are handled gracefully and return an empty list.

Functions
---------
    merge_sort(sequence)  -> list

Time complexity
---------------
    Best case    : O(n log n)  — even on already-sorted input, all splits
                                 and merges still happen.
    Average case : O(n log n)  — typical random permutation.
    Worst case   : O(n log n)  — always, regardless of input order.

    Why O(n log n)?
        Dividing in half repeatedly gives log n levels of recursion.
        At each level, every element is visited once during merging → O(n).
        Total: n work per level × log n levels = O(n log n).

        n = 1 000:
            bubble/insertion/selection  →  1 000 000 operations  (n²)
            merge sort                  →     10 000 operations  (n log n)

        n = 1 000 000:
            bubble/insertion/selection  →  1 000 000 000 000 operations
            merge sort                  →        20 000 000 operations

Space complexity
----------------
    O(n) — merging requires temporary lists to hold the left and right halves.
           Unlike bubble/selection/insertion, merge sort is NOT in-place.

Stability
---------
    Merge sort IS stable.  During merging, when left[i] == right[j], we
    always take from the left half first.  This guarantees that equal
    elements preserve their original relative order.

Advantages
----------
- Guaranteed O(n log n) — no worst-case degradation like Quick Sort
- Stable — maintains relative order of equal elements
- Predictable — performance does not depend on input order
- Parallelisable — independent halves can be sorted concurrently
- Ideal for external sorting (data too large to fit in memory)

Disadvantages
-------------
- O(n) extra space — requires additional memory proportional to input size
- Not in-place — more memory pressure than bubble/selection/insertion
- Recursive — call stack depth is O(log n); negligible for real-world sizes
- Slower than Quick Sort in practice due to memory allocation overhead

When to use
-----------
- Large datasets where O(n log n) guarantee matters
- Sorting linked lists — no random access needed, no extra memory required
- External sorting (files, databases too large for RAM)
- When stability is required and Quick Sort is not an option
- Foundation of Python's Timsort (used for large runs)

Examples
--------
    >>> merge_sort([5, 3, 1, 4, 2])
    [1, 2, 3, 4, 5]

    >>> merge_sort([1, 2, 3, 4, 5])  # already sorted
    [1, 2, 3, 4, 5]

    >>> merge_sort([5, 4, 3, 2, 1])  # reverse sorted
    [1, 2, 3, 4, 5]

    >>> merge_sort([1])
    [1]

    >>> merge_sort([])  # empty sequence handled correctly
    []

    >>> merge_sort([3, 3, 1, 2])
    [1, 2, 3, 3]
"""

from collections.abc import Sequence
from typing import Any

from .._tools import is_comparable

# ─────────────────────────────────────────────────────────────────────────────
#  Merge helper
# ─────────────────────────────────────────────────────────────────────────────


def _merge(left: list, right: list) -> list:
    """
    Merges two sorted lists into a single sorted list.

    Walks both lists simultaneously using two pointers ``i`` and ``j``.
    On each step, the smaller front element is appended to the result and
    its pointer advances. When one list is exhausted, the remainder of
    the other is appended directly — it is already sorted.

    The merge operation preserves stability by always taking from the left
    half when elements are equal, maintaining the original relative order
    of equal elements.

    Args:
        left:  A sorted list.
        right: A sorted list.

    Returns:
        A new sorted list containing all elements from both inputs.

    Time complexity:  O(n)  — each element is visited exactly once.
    Space complexity: O(n)  — a new list of combined size is created.

    Examples:
        >>> _merge([1, 3, 5], [2, 4])
        [1, 2, 3, 4, 5]

        >>> _merge([], [1, 2])
        [1, 2]

        >>> _merge([1, 2], [])
        [1, 2]
    """
    result = []
    i = 0
    j = 0

    # Compare front elements from both lists and take the smaller one
    while i < len(left) and j < len(right):
        # Take from left first on equality — preserves stability
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append remaining elements from left (if any)
    result.extend(left[i:])

    # Append remaining elements from right (if any)
    result.extend(right[j:])

    return result


# ─────────────────────────────────────────────────────────────────────────────
#  Main sorting function
# ─────────────────────────────────────────────────────────────────────────────


def merge_sort(sequence: Sequence[Any]) -> list:
    """
    Sorts *sequence* in ascending order using the merge sort algorithm.

    Recursively divides the sequence in half until every piece contains at
    most one element (which is trivially sorted), then merges the pieces back
    together in sorted order using :func:`_merge`.

    Algorithm overview
    -------------------
    Two phases drive the sort:

        divide phase:  the sequence is split at its midpoint into ``left``
                       and ``right`` halves. Each half is passed recursively
                       to ``merge_sort`` until the base case (length ≤ 1) is
                       reached. This produces a balanced binary tree of
                       recursive calls.

        merge phase:   the two sorted halves returned by the recursive calls
                       are combined by ``_merge``, which walks both halves
                       simultaneously and always picks the smaller front
                       element. This ensures stability and correctness.

    Validation
    ----------
    Element comparability is validated only when a single element is reached
    during recursion. For empty sequences, no validation occurs and an empty
    list is returned immediately. This prevents ``IndexError`` on empty inputs
    while maintaining safety for all other cases.

    Args:
        sequence: Any sequence whose elements support ``==`` and ``<``
                  comparison operators. Can be a list, tuple, or any other
                  sequence type.

    Returns:
        A new sorted list. The original sequence is not modified.

    Raises:
        TypeError: If any element does not support ``==`` and ``<``
                   comparison operators. This is raised when the algorithm
                   reaches a base case with a non-comparable element.

    Examples:
        >>> merge_sort([5, 3, 1, 4, 2])
        [1, 2, 3, 4, 5]

        >>> merge_sort([1, 2, 3, 4, 5])
        [1, 2, 3, 4, 5]

        >>> merge_sort([5, 4, 3, 2, 1])
        [1, 2, 3, 4, 5]

        >>> merge_sort([1])
        [1]

        >>> merge_sort([])
        []

        >>> merge_sort([3, 3, 1, 2])
        [1, 2, 3, 3]

    Time complexity:  O(n log n)  — always, regardless of input order.
    Space complexity: O(n)        — temporary lists created during merging.
    """
    result = list(sequence)

    # Base case: empty or single-element sequences are already sorted
    if len(result) <= 1:
        # Only validate comparability if the sequence is not empty
        if result and not is_comparable(result[0]):
            raise TypeError(
                f"Elements must support == and < operators, "
                f"got {type(result[0]).__name__!r}."
            )
        return result

    # Divide: split the sequence at the midpoint
    mid = len(result) // 2
    left = merge_sort(result[:mid])
    right = merge_sort(result[mid:])

    # Conquer: merge the two sorted halves back together
    return _merge(left, right)
