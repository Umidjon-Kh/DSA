# first variation: searching item iteratively to avoid recursive error
# But i think with binary serach we never get recursive error even ve use racursively way
# cause its (O log n) not naive checking. It means in every recurse the capacity of items / 2
from collections.abc import Sequence
from typing import Any, Optional


def is_comparable(item: Any) -> bool:
    """
    Determines item is comparable or not.
    Returns True if comparable, otherwise False.
    """
    compare_methos = ("__eq__", "__lt__")

    for method in compare_methos:
        if not hasattr(item, method):
            return False
    else:
        return True


def iterative_binary_search(
    array: Sequence[Any], target: Any, which: Optional[str] = None
) -> int:
    """
    Searchs for received target item in array. Array must be sorted.!
    If array not sorted its not raises Error, it just returns wrong answer.

    Args:
        array  - An Iterable object that contains elements that comparable.
        target - An item to find in received array.

    Returns:
        index - if object if found. otherwise -1

    Raises:
        TypeError: if object is not comparable.
    """
    low = 0
    high = len(array) - 1
    result = -1
    if not is_comparable(target):
        raise TypeError("Array contains item that is not comparable")

    while low <= high:
        mid = (low + high) // 2

        if array[mid] == target:
            result = mid
            if which == "first":
                low = mid + 1
            elif which == "last":
                high = mid - 1
            else:
                return mid

        elif array[mid] < target:
            low = mid + 1

        else:
            high = mid - 1
    else:
        return result


def recursive_binary_search(
    array: Sequence[Any],
    target: Any,
    low: int = 0,
    high: Optional[int] = None,
    which: Optional[str] = None,
    result: int = -1,
) -> int:
    """
    Recursively search for target item in received sequence.
    Also sequence as in iterative binary_serach must be sorted and contain only comparable objects.

    Args:
        array  - A sequnce that contains sorted items from lesser to higher.
        target - A object that needs to find in array.
        low    - index of low point in received array. (It needs cause we search recursively)
        high   - index of high point in received array.
    """
    if high is None:
        high = len(array) - 1
        # I put this condition in this block cause if high is None it means it root function
        # not recursive started yet
        if not is_comparable(target):
            raise TypeError("Array contains item that is not comparable.")

    if low > high:
        return result

    mid = (low + high) // 2

    if array[mid] == target:
        result = mid
        if which == "last":
            return recursive_binary_search(array, target, mid + 1, high, which, result)
        elif which == "first":
            return recursive_binary_search(array, target, low, mid - 1, which, result)
        else:
            return mid

    elif array[mid] < target:
        return recursive_binary_search(array, target, mid + 1, high, which, result)

    else:
        return recursive_binary_search(array, target, low, mid - 1, which, result)
