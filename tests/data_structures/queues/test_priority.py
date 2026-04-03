import pytest

from data_structures import MaxPriorityQueue, MinPriorityQueue

# ==============================================================================
# MaxPriorityQueue
# ==============================================================================

# ── Init ──────────────────────────────────────────────────────────────────────


def test_max_init_empty() -> None:
    q = MaxPriorityQueue()
    assert len(q) == 0
    assert q.is_empty()


def test_max_init_with_args() -> None:
    q = MaxPriorityQueue(("low", 1), ("high", 10))
    assert len(q) == 2


def test_max_init_args_wrong_format_raises() -> None:
    with pytest.raises((TypeError, AttributeError)):
        MaxPriorityQueue("not_a_tuple")  # type: ignore[arg-type]


def test_max_init_priority_wrong_type_raises() -> None:
    with pytest.raises(TypeError):
        MaxPriorityQueue(("task", "not_a_number"))  # type: ignore[arg-type]


# ── Enqueue ───────────────────────────────────────────────────────────────────


def test_max_enqueue_increases_size() -> None:
    q = MaxPriorityQueue()
    q.enqueue("task", priority=1)
    assert len(q) == 1


def test_max_enqueue_priority_wrong_type_raises() -> None:
    q = MaxPriorityQueue()
    with pytest.raises(TypeError):
        q.enqueue("task", priority="high")  # type: ignore[arg-type]


def test_max_enqueue_float_priority_accepted() -> None:
    q = MaxPriorityQueue()
    q.enqueue("task", priority=1.5)
    assert q.peek_priority() == 1.5


def test_max_enqueue_negative_priority_accepted() -> None:
    q = MaxPriorityQueue()
    q.enqueue("a", priority=-1)
    q.enqueue("b", priority=-5)
    assert q.dequeue() == "a"


# ── Dequeue ───────────────────────────────────────────────────────────────────


def test_max_dequeue_returns_highest_priority() -> None:
    q = MaxPriorityQueue()
    q.enqueue("low", priority=1)
    q.enqueue("mid", priority=5)
    q.enqueue("high", priority=10)
    assert q.dequeue() == "high"


def test_max_dequeue_order_highest_first() -> None:
    q = MaxPriorityQueue(("c", 3), ("a", 1), ("b", 2))
    assert [q.dequeue(), q.dequeue(), q.dequeue()] == ["c", "b", "a"]


def test_max_dequeue_decrements_size() -> None:
    q = MaxPriorityQueue(("x", 1), ("y", 2))
    q.dequeue()
    assert len(q) == 1


def test_max_dequeue_empty_raises() -> None:
    with pytest.raises(IndexError):
        MaxPriorityQueue().dequeue()


def test_max_dequeue_does_not_expose_wrapper() -> None:
    q = MaxPriorityQueue()
    q.enqueue("result", priority=5)
    value = q.dequeue()
    assert value == "result"
    assert not hasattr(value, "priority")


# ── Peek / peek_priority ──────────────────────────────────────────────────────


def test_max_peek_returns_highest_without_removing() -> None:
    q = MaxPriorityQueue()
    q.enqueue("low", priority=1)
    q.enqueue("high", priority=10)
    assert q.peek() == "high"
    assert len(q) == 2


def test_max_peek_priority_returns_highest_number() -> None:
    q = MaxPriorityQueue()
    q.enqueue("low", priority=1)
    q.enqueue("high", priority=10)
    assert q.peek_priority() == 10


def test_max_peek_empty_raises() -> None:
    with pytest.raises(IndexError):
        MaxPriorityQueue().peek()


def test_max_peek_priority_empty_raises() -> None:
    with pytest.raises(IndexError):
        MaxPriorityQueue().peek_priority()


# ── clear / copy ──────────────────────────────────────────────────────────────


def test_max_clear_empties_queue() -> None:
    q = MaxPriorityQueue(("a", 1), ("b", 2))
    q.clear()
    assert q.is_empty()
    assert len(q) == 0


def test_max_copy_preserves_elements() -> None:
    q = MaxPriorityQueue(("low", 1), ("high", 10))
    c = q.copy()
    assert c.dequeue() == "high"
    assert c.dequeue() == "low"


def test_max_copy_is_independent() -> None:
    q = MaxPriorityQueue(("a", 1))
    c = q.copy()
    c.enqueue("b", priority=2)
    assert len(q) == 1


# ── is_empty / __bool__ / __len__ ─────────────────────────────────────────────


def test_max_is_empty_true() -> None:
    assert MaxPriorityQueue().is_empty()


def test_max_is_empty_false() -> None:
    assert not MaxPriorityQueue(("a", 1)).is_empty()


def test_max_bool_empty() -> None:
    assert not bool(MaxPriorityQueue())


def test_max_bool_not_empty() -> None:
    assert bool(MaxPriorityQueue(("a", 1)))


def test_max_len_empty() -> None:
    assert len(MaxPriorityQueue()) == 0


def test_max_len_after_enqueues() -> None:
    q = MaxPriorityQueue()
    q.enqueue("a", 1)
    q.enqueue("b", 2)
    assert len(q) == 2


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_max_iter_yields_value_priority_tuples() -> None:
    q = MaxPriorityQueue()
    q.enqueue("task", priority=5)
    items = list(q)
    assert len(items) == 1
    value, priority = items[0]
    assert value == "task"
    assert priority == 5


def test_max_iter_does_not_modify() -> None:
    q = MaxPriorityQueue(("a", 1), ("b", 2))
    _ = list(q)
    assert len(q) == 2


def test_max_reversed_yields_value_priority_tuples() -> None:
    q = MaxPriorityQueue()
    q.enqueue("task", priority=5)
    items = list(reversed(q))
    assert len(items) == 1


# ── __contains__ ──────────────────────────────────────────────────────────────


def test_max_contains_existing_value() -> None:
    q = MaxPriorityQueue(("a", 1), ("b", 2))
    assert "a" in q


def test_max_contains_missing_value() -> None:
    q = MaxPriorityQueue(("a", 1), ("b", 2))
    assert "z" not in q


def test_max_contains_empty() -> None:
    assert "x" not in MaxPriorityQueue()


def test_max_contains_by_value_not_priority() -> None:
    q = MaxPriorityQueue()
    q.enqueue("task", priority=99)
    assert "task" in q
    assert 99 not in q


# ── __eq__ ────────────────────────────────────────────────────────────────────


def test_max_eq_equal() -> None:
    a = MaxPriorityQueue(("x", 1), ("y", 2))
    b = MaxPriorityQueue(("x", 1), ("y", 2))
    assert a == b


def test_max_eq_empty_both() -> None:
    assert MaxPriorityQueue() == MaxPriorityQueue()


def test_max_eq_different_elements() -> None:
    a = MaxPriorityQueue(("a", 1))
    b = MaxPriorityQueue(("b", 1))
    assert a != b


def test_max_eq_not_implemented_for_other_type() -> None:
    assert MaxPriorityQueue().__eq__([]) is NotImplemented


# ── __repr__ ──────────────────────────────────────────────────────────────────


def test_max_repr_empty() -> None:
    assert repr(MaxPriorityQueue()) == "MaxPriorityQueue(size=0)[]"


def test_max_repr_single() -> None:
    q = MaxPriorityQueue()
    q.enqueue("task", priority=5)
    assert repr(q) == "MaxPriorityQueue(size=1)[(value='task', priority=5)]"


# ==============================================================================
# MinPriorityQueue
# ==============================================================================

# ── Init ──────────────────────────────────────────────────────────────────────


def test_min_init_empty() -> None:
    q = MinPriorityQueue()
    assert len(q) == 0
    assert q.is_empty()


def test_min_init_with_args() -> None:
    q = MinPriorityQueue(("email", 2), ("bug", 1))
    assert len(q) == 2


def test_min_init_priority_wrong_type_raises() -> None:
    with pytest.raises(TypeError):
        MinPriorityQueue(("task", "urgent"))  # type: ignore[arg-type]


# ── Dequeue ───────────────────────────────────────────────────────────────────


def test_min_dequeue_returns_lowest_priority() -> None:
    q = MinPriorityQueue()
    q.enqueue("low", priority=10)
    q.enqueue("mid", priority=5)
    q.enqueue("high", priority=1)
    assert q.dequeue() == "high"


def test_min_dequeue_order_lowest_first() -> None:
    q = MinPriorityQueue(("c", 3), ("a", 1), ("b", 2))
    assert [q.dequeue(), q.dequeue(), q.dequeue()] == ["a", "b", "c"]


def test_min_dequeue_empty_raises() -> None:
    with pytest.raises(IndexError):
        MinPriorityQueue().dequeue()


def test_min_dequeue_does_not_expose_wrapper() -> None:
    q = MinPriorityQueue()
    q.enqueue("result", priority=1)
    value = q.dequeue()
    assert value == "result"
    assert not hasattr(value, "priority")


# ── Peek / peek_priority ──────────────────────────────────────────────────────


def test_min_peek_returns_lowest_without_removing() -> None:
    q = MinPriorityQueue()
    q.enqueue("slow", priority=10)
    q.enqueue("fast", priority=1)
    assert q.peek() == "fast"
    assert len(q) == 2


def test_min_peek_priority_returns_lowest_number() -> None:
    q = MinPriorityQueue()
    q.enqueue("slow", priority=10)
    q.enqueue("fast", priority=1)
    assert q.peek_priority() == 1


def test_min_peek_empty_raises() -> None:
    with pytest.raises(IndexError):
        MinPriorityQueue().peek()


def test_min_peek_priority_empty_raises() -> None:
    with pytest.raises(IndexError):
        MinPriorityQueue().peek_priority()


# ── clear / copy ──────────────────────────────────────────────────────────────


def test_min_clear_empties_queue() -> None:
    q = MinPriorityQueue(("a", 1), ("b", 2))
    q.clear()
    assert q.is_empty()


def test_min_copy_preserves_elements() -> None:
    q = MinPriorityQueue(("bug", 1), ("email", 2))
    c = q.copy()
    assert c.dequeue() == "bug"
    assert c.dequeue() == "email"


def test_min_copy_is_independent() -> None:
    q = MinPriorityQueue(("a", 1))
    c = q.copy()
    c.enqueue("b", priority=0)
    assert len(q) == 1


# ── is_empty / __bool__ / __len__ ─────────────────────────────────────────────


def test_min_is_empty_true() -> None:
    assert MinPriorityQueue().is_empty()


def test_min_is_empty_false() -> None:
    assert not MinPriorityQueue(("a", 1)).is_empty()


def test_min_bool_empty() -> None:
    assert not bool(MinPriorityQueue())


def test_min_bool_not_empty() -> None:
    assert bool(MinPriorityQueue(("a", 1)))


# ── __iter__ / __contains__ ───────────────────────────────────────────────────


def test_min_iter_yields_value_priority_tuples() -> None:
    q = MinPriorityQueue()
    q.enqueue("task", priority=3)
    items = list(q)
    assert len(items) == 1
    value, priority = items[0]
    assert value == "task"
    assert priority == 3


def test_min_contains_existing_value() -> None:
    q = MinPriorityQueue(("a", 1), ("b", 2))
    assert "a" in q


def test_min_contains_missing_value() -> None:
    q = MinPriorityQueue(("a", 1))
    assert "z" not in q


def test_min_contains_by_value_not_priority() -> None:
    q = MinPriorityQueue()
    q.enqueue("task", priority=1)
    assert "task" in q
    assert 1 not in q


# ── __eq__ ────────────────────────────────────────────────────────────────────


def test_min_eq_equal() -> None:
    a = MinPriorityQueue(("x", 1), ("y", 2))
    b = MinPriorityQueue(("x", 1), ("y", 2))
    assert a == b


def test_min_eq_empty_both() -> None:
    assert MinPriorityQueue() == MinPriorityQueue()


def test_min_eq_different_priorities() -> None:
    a = MinPriorityQueue(("a", 1))
    b = MinPriorityQueue(("a", 5))
    assert a != b


def test_min_eq_not_implemented_for_other_type() -> None:
    assert MinPriorityQueue().__eq__([]) is NotImplemented


# ── __repr__ ──────────────────────────────────────────────────────────────────


def test_min_repr_empty() -> None:
    assert repr(MinPriorityQueue()) == "MinPriorityQueue(size=0)[]"


def test_min_repr_single() -> None:
    q = MinPriorityQueue()
    q.enqueue("bug", priority=1)
    assert repr(q) == "MinPriorityQueue(size=1)[(value='bug', priority=1)]"


# ── MaxPriorityQueue vs MinPriorityQueue contrast ─────────────────────────────


def test_max_vs_min_same_input_different_dequeue_order() -> None:
    items = [("a", 1), ("b", 2), ("c", 3)]
    mx = MaxPriorityQueue(*items)
    mn = MinPriorityQueue(*items)
    assert mx.dequeue() == "c"  # highest priority first
    assert mn.dequeue() == "a"  # lowest priority first


def test_max_and_min_not_equal_to_each_other() -> None:
    a = MaxPriorityQueue(("x", 1))
    b = MinPriorityQueue(("x", 1))
    assert a.__eq__(b) is NotImplemented
    assert b.__eq__(a) is NotImplemented
