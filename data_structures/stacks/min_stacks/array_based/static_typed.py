from typing import Any, Iterator

from ....arrays import StaticTypedArray
from ....tools import validate_capacity


class MinStaticTypedStack:
    """
    A fixed-capacity min stack backed by StatictypedArray.
    Tracks the current minimum in O(1) using an auxiliary array.
    Enforces a single element type for all items.
    Follows LIFO (Last In, First Out) principle.

    Supported dtypes: int, float, bool, str

    How MinStack computes minimum when pushing?
     - In Initializing Any Type of MinStack you need to
     provide a key function that computes minimum value and returns an int or
     any other element for comparison. MinStack uses it when you call method push.
     It compares both values and if min_data top value is higher then pushed value or
     min_data is empty, it adds to min_data.
     - MinStack needs a key function that returns element that
     supports comparison operators (<, >) for min tracking.

    How works all basic methods of MinStacks:
        on push(x): if min_data is empty or key(x) < key(min_data[min_top]):
            it pushes to min_data too as current minimum object in stack.
        on pop(): if removal element is equal to current minimum:
            removes current minimum too.
        on get_min(): Only returns current minimum without modifying stack.
        on peek(): Only returns current top of the main_data without modifying.

    Time complexity:
        push:           O(1)
        pop:            O(1)
        peek:           O(1)
        get_min:        O(1)
        clear:          O(1)
        copy:           O(n)
        is_empty:       O(1)
        is_full:        O(1)
        __len__:        O(1)
        __bool__:       O(1)
        __iter__:       O(n) - top to bottom
        __reversed__:   O(n) - bottom to top
        __contains__:   O(n)
        __repr__:       O(n)
    """

    __slots__ = (
        "_data",
        "_min_data",
        "_top",
        "_min_top",
    )

    def __init__(self) -> None:
        pass
