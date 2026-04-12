"""
Two Pointers
============
A technique that uses two index variables — ``left`` and ``right`` — to
traverse a sequence in a single pass, avoiding the O(n²) cost of nested loops.

Core idea
---------
Instead of checking every possible pair with two nested loops, two pointers
exploit some property of the data (sorted order, symmetry, uniqueness) to
know which pointer to move after each comparison.  One comparison → one
pointer moves → search space shrinks.  Total cost: O(n).

Pointer movement patterns
-------------------------
There are two fundamental patterns, each suited to different problems:

    1. CONVERGING  — pointers start at opposite ends and move toward each other.
                     Used when the answer involves a pair of elements.

            [1, 3, 5, 7, 9]
             ↑           ↑
            left        right
                  → ← (moving inward)

    2. FAST / SLOW — both pointers start at the left and move rightward,
                     but at different speeds.  Used when rewriting a sequence
                     in-place or detecting a structural property.

            [1, 1, 2, 3, 3]
             ↑  ↑
            slow fast
                  → → (both moving right, fast leads)

Functions
---------
    pair_sum_search(sequence, target)  -> Tuple[int, int]   [converging]
    is_palindrome(sequence)            -> bool               [converging]
    remove_duplicates(sequence)        -> int                [fast / slow]

When NOT to use Two Pointers
-----------------------------
- Unsorted data where pair_sum_search is needed (use a hash set instead).
- Problems that genuinely require all O(n²) pairs — two pointers cannot
  help when every combination must be examined.
- In Python, remove_duplicates on a plain list is usually just
  ``list(dict.fromkeys(seq))`` — the manual two-pointer version is here
  to demonstrate the pattern, not as a production utility.

Time complexity
---------------
    All three functions: O(n) — single pass through the sequence.

Space complexity
----------------
    pair_sum_search  : O(1) — two index variables only.
    is_palindrome    : O(1) — two index variables only.
    remove_duplicates: O(1) — in-place rewrite, no extra allocation.
"""

from collections.abc import Sequence
from typing import Any, Tuple

# ─────────────────────────────────────────────────────────────────────────────
#  1. Pair sum search  (converging pointers — sorted sequence required)
# ─────────────────────────────────────────────────────────────────────────────


def pair_sum_search(sequence: Sequence[Any], target: Any) -> Tuple[int, int]:
    """
    Finds the indices of two elements that add up to *target*.

    Uses converging pointers on a **sorted** sequence.  Starting from both
    ends, the current sum decides which pointer moves:

        sum == target  →  found, return indices
        sum  < target  →  sum is too small  → move left  pointer right (+1)
        sum  > target  →  sum is too large  → move right pointer left  (-1)

    Because the sequence is sorted, moving left right increases the sum and
    moving right left decreases it — so every step makes meaningful progress.

    Args:
        sequence: A sorted sequence of elements that support + and ==.
        target:   The desired sum.

    Returns:
        (left_index, right_index) of the matching pair, or (-1, -1) if none.

    Note:
        Passing an unsorted sequence does NOT raise an error — the function
        will silently return a wrong answer (same caveat as binary search).

    Examples:
        >>> pair_sum_search([1, 3, 5, 7, 9], 12)
        (2, 4)
        >>> pair_sum_search([1, 3, 5, 7, 9], 100)
        (-1, -1)
        >>> pair_sum_search([1, 3, 5, 7, 9], 8)
        (0, 3)

    Time complexity:  O(n)
    Space complexity: O(1)
    """
    left = 0
    right = len(sequence) - 1

    while left < right:
        current_sum = sequence[left] + sequence[right]

        if current_sum == target:
            return (left, right)

        elif current_sum < target:
            # Sum too small — need a larger left element
            left += 1

        else:
            # Sum too large — need a smaller right element
            right -= 1

    # Pointers met without finding a valid pair
    return (-1, -1)


# ─────────────────────────────────────────────────────────────────────────────
#  2. Palindrome check  (converging pointers — works on any sequence)
# ─────────────────────────────────────────────────────────────────────────────


def is_palindrome(sequence: Sequence[Any]) -> bool:
    """
    Returns True if *sequence* reads the same forwards and backwards.

    Uses converging pointers: ``left`` starts at index 0, ``right`` at the
    last index.  On each step both elements are compared:

        sequence[left] != sequence[right]  →  not a palindrome, stop immediately
        sequence[left] == sequence[right]  →  move both pointers inward

    The loop ends either when a mismatch is found (False) or when the
    pointers meet/cross — meaning every pair matched (True).

    Works on strings, lists, tuples, or any subscriptable sequence whose
    elements support ==.  No sorting required.

    Args:
        sequence: Any sequence that supports indexing and ==.

    Returns:
        True if the sequence is a palindrome, False otherwise.

    Examples:
        >>> is_palindrome("racecar")
        True
        >>> is_palindrome("hello")
        False
        >>> is_palindrome([1, 2, 3, 2, 1])
        True
        >>> is_palindrome([])
        True
        >>> is_palindrome("a")
        True

    Time complexity:  O(n)
    Space complexity: O(1)
    """
    left = 0
    right = len(sequence) - 1

    while left < right:
        if sequence[left] != sequence[right]:
            # Mismatch found — cannot be a palindrome
            return False

        # Characters / elements match — move both pointers inward
        left += 1
        right -= 1

    # All pairs matched
    return True


# ─────────────────────────────────────────────────────────────────────────────
#  3. Remove duplicates in-place  (fast / slow pointers — sorted sequence)
# ─────────────────────────────────────────────────────────────────────────────


def remove_duplicates(sequence: list) -> int:
    """
    Removes duplicate elements from a **sorted** list in-place and returns
    the count of unique elements.

    Uses a fast/slow pointer pair — both move rightward but at different speeds:

        ``slow`` — marks the boundary of the unique section built so far.
        ``fast`` — scans ahead looking for values not yet seen.

        sequence[fast] != sequence[slow]
            →  new unique element found
            →  slow advances by one
            →  sequence[slow] = sequence[fast]   (write it into the unique section)

        sequence[fast] == sequence[slow]
            →  duplicate — fast keeps moving, slow stays

    After the loop, ``sequence[:slow + 1]`` contains all unique elements in
    their original order.  The rest of the list is irrelevant garbage — only
    the returned count matters.

    Args:
        sequence: A sorted list (mutated in-place).

    Returns:
        The number of unique elements.  The first *k* positions of *sequence*
        hold those unique elements after the call.

    Note:
        In everyday Python code ``list(dict.fromkeys(seq))`` or
        ``sorted(set(seq))`` are cleaner choices.  This function exists to
        demonstrate the fast/slow pointer pattern explicitly.

    Examples:
        >>> seq = [1, 1, 2, 3, 3, 4]
        >>> k = remove_duplicates(seq)
        >>> k
        4
        >>> seq[:k]
        [1, 2, 3, 4]

        >>> seq = [1, 1, 1, 1]
        >>> k = remove_duplicates(seq)
        >>> k
        1
        >>> seq[:k]
        [1]

    Time complexity:  O(n)
    Space complexity: O(1)  — in-place, no extra list created
    """
    if not sequence:
        return 0

    # slow points to the last confirmed unique element
    slow = 0

    for fast in range(1, len(sequence)):
        if sequence[fast] != sequence[slow]:
            # New unique value discovered — extend the unique section
            slow += 1
            sequence[slow] = sequence[fast]

    # slow is the index of the last unique element → count = slow + 1
    return slow + 1
