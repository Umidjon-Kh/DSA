from typing import Any


class PriorityObject:
    """
    A wrapper object used as the element type for all priority queues.

    Priority queues in this library are backed by heaps. Heap operations
    rely on comparison between elements — push uses __lt__ or __gt__ to
    sift elements into the correct position. A plain value carries no
    priority information, so a wrapper is needed.

    PriorityObject bundles a value with a numeric priority. Comparisons
    are performed on priority alone — the stored value is never compared.
    This means any value type is supported regardless of whether it is
    comparable itself.

    ── Fields ───────────────────────────────────────────────────────────────
        value    — the payload to store. Any Python object.
        priority — a numeric key that determines ordering.
                   Lower number = higher urgency in a min-heap.
                   Higher number = higher urgency in a max-heap.

    ── Comparison behaviour ─────────────────────────────────────────────────
        obj_a < obj_b   →  obj_a.priority <  obj_b.priority
        obj_a <= obj_b  →  obj_a.priority <= obj_b.priority
        obj_a > obj_b   →  obj_a.priority >  obj_b.priority
        obj_a >= obj_b  →  obj_a.priority >= obj_b.priority
        obj_a == obj_b  →  obj_a.priority == obj_b.priority
                           and obj_a.value == obj_b.value

    ── Usage ────────────────────────────────────────────────────────────────
        item = PriorityObject("task", priority=1)
        heap.push(item)
        heap.peek().value   # → "task"

    Time complexity:
        __init__: O(1)
        __repr__: O(1)
        __eq__:   O(1)
        __lt__:   O(1)
        __le__:   O(1)
        __gt__:   O(1)
        __ge__:   O(1)
    """

    __slots__ = ("value", "priority")

    def __init__(self, value: Any, priority: int | float) -> None:
        """
        Creates a PriorityObject with a given value and priority.

        Args:
            value:    Any Python object to store as the payload.
            priority: A numeric key used for ordering. Supports int and float.

        Raises:
            TypeError: If priority is not int or float.

        Examples:
            obj = PriorityObject("send email", priority=2)
            obj = PriorityObject({"id": 1}, priority=0.5)
        """
        if not isinstance(priority, (int, float)) or isinstance(priority, bool):
            raise TypeError(
                f"Priority must be int or float, got ({type(priority).__name__!r})"
            )
        self.value: Any = value
        self.priority: int | float = priority

    # -------------------------------------------------------------------------
    # Comparison methods

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both priority and value are equal.
        Comparing with a non-PriorityObject returns NotImplemented.
        """
        if not isinstance(other, PriorityObject):
            return NotImplemented
        return self.priority == other.priority and self.value == other.value

    def __lt__(self, other: "PriorityObject") -> bool:
        """Returns True if this object's priority is less than other's."""
        if not isinstance(other, PriorityObject):
            return NotImplemented
        return self.priority < other.priority

    def __le__(self, other: "PriorityObject") -> bool:
        """Returns True if this object's priority is less than or equal to other's."""
        if not isinstance(other, PriorityObject):
            return NotImplemented
        return self.priority <= other.priority

    def __gt__(self, other: "PriorityObject") -> bool:
        """Returns True if this object's priority is greater than other's."""
        if not isinstance(other, PriorityObject):
            return NotImplemented
        return self.priority > other.priority

    def __ge__(self, other: "PriorityObject") -> bool:
        """Returns True if this object's priority is greater than or equal to other's."""
        if not isinstance(other, PriorityObject):
            return NotImplemented
        return self.priority >= other.priority

    # -------------------------------------------------------------------------
    # Dunder methods

    def __repr__(self) -> str:
        """
        Returns string representation of the object.
        Format: PriorityObject(value='task', priority=1)
        """
        return f"PriorityObject(value={self.value!r}, priority={self.priority!r})"
