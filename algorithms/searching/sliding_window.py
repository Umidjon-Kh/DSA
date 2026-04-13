from collections.abc import Sequence
from typing import Any

from typing_extensions import Optional


def max_summary_subarray(sequence: Sequence[Any], array_len: int = 3) -> Optional[Any]:
    """
    Finds the maximum summary of any subarray of size array_len in
    received sequence.

    Args:
        sequence - Sequnce that contains addable  values. "+"
        array_len - Length of subarray to determine maximum.

    Returns:
        max_summary - summary that contains maximum in subarray.

    Raises:
        TypeError: if received items is not addable.
    """

    if len(sequence) < array_len:
        return

    window_sum = sequence[0]

    for idx in range(1, array_len):
        window_sum += sequence[idx]

    max_sum = window_sum

    for right in range(array_len, len(sequence)):
        window_sum -= sequence[right - array_len]
        window_sum += sequence[right]

        if window_sum > max_sum:
            max_sum = window_sum

    return max_sum
