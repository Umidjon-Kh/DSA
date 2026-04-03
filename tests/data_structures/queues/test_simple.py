import pytest

from data_structures import (
    DynamicTypedQueue,
    DynamicUniversalQueue,
    NodeQueue,
    StaticTypedQueue,
    StaticUniversalQueue,
)

# ==============================================================================
# NodeQueue
# ==============================================================================

# ── Init ──────────────────────────────────────────────────────────────────────


def test_node_init_empty() -> None:
    q = NodeQueue()
    assert q._size == 0
    assert q._front is None
    assert q._rear is None


def test_node_init_with_args() -> None:
    q = NodeQueue(1, 2, 3)
    assert q._size == 3
    assert q.peek() == 1


def test_node_init_single_arg() -> None:
    q = NodeQueue(42)
    assert len(q) == 1
    assert q.peek() == 42


def test_node_init_mixed_types() -> None:
    q = NodeQueue(1, "hi", 3.0)
    assert q.peek() == 1
    assert len(q) == 3


# ── Enqueue ───────────────────────────────────────────────────────────────────


def test_node_enqueue_increments_size() -> None:
    q = NodeQueue()
    q.enqueue(1)
    q.enqueue(2)
    assert q._size == 2


def test_node_enqueue_first_sets_front_and_rear() -> None:
    q = NodeQueue()
    q.enqueue(99)
    assert q._front is q._rear
    assert q._front.value == 99  # type: ignore[union-attr]


def test_node_enqueue_updates_rear() -> None:
    q = NodeQueue()
    q.enqueue(1)
    q.enqueue(2)
    assert q._rear.value == 2  # type: ignore[union-attr]


def test_node_enqueue_none_value() -> None:
    q = NodeQueue()
    q.enqueue(None)
    assert q.peek() is None
    assert len(q) == 1


# ── Dequeue ───────────────────────────────────────────────────────────────────


def test_node_dequeue_returns_front() -> None:
    q = NodeQueue(1, 2, 3)
    assert q.dequeue() == 1


def test_node_dequeue_decrements_size() -> None:
    q = NodeQueue(1, 2, 3)
    q.dequeue()
    assert q._size == 2


def test_node_dequeue_order_is_fifo() -> None:
    q = NodeQueue(1, 2, 3)
    assert [q.dequeue(), q.dequeue(), q.dequeue()] == [1, 2, 3]


def test_node_dequeue_last_clears_rear() -> None:
    q = NodeQueue(1)
    q.dequeue()
    assert q._front is None
    assert q._rear is None


def test_node_dequeue_empty_raises() -> None:
    with pytest.raises(IndexError):
        NodeQueue().dequeue()


# ── Peek ──────────────────────────────────────────────────────────────────────


def test_node_peek_returns_front_without_removing() -> None:
    q = NodeQueue(1, 2, 3)
    assert q.peek() == 1
    assert len(q) == 3


def test_node_peek_empty_raises() -> None:
    with pytest.raises(IndexError):
        NodeQueue().peek()


# ── clear / copy ──────────────────────────────────────────────────────────────


def test_node_clear_resets_state() -> None:
    q = NodeQueue(1, 2, 3)
    q.clear()
    assert q._size == 0
    assert q._front is None
    assert q._rear is None


def test_node_copy_preserves_elements() -> None:
    q = NodeQueue(1, 2, 3)
    c = q.copy()
    assert list(c) == [1, 2, 3]


def test_node_copy_is_independent() -> None:
    q = NodeQueue(1, 2)
    c = q.copy()
    c.enqueue(99)
    assert len(q) == 2


def test_node_copy_empty() -> None:
    assert NodeQueue().copy().is_empty()


# ── is_empty / __bool__ / __len__ ─────────────────────────────────────────────


def test_node_is_empty_true() -> None:
    assert NodeQueue().is_empty()


def test_node_is_empty_false() -> None:
    assert not NodeQueue(1).is_empty()


def test_node_bool_empty() -> None:
    assert not bool(NodeQueue())


def test_node_bool_not_empty() -> None:
    assert bool(NodeQueue(1))


def test_node_len_empty() -> None:
    assert len(NodeQueue()) == 0


def test_node_len_after_enqueues() -> None:
    assert len(NodeQueue(1, 2, 3)) == 3


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_node_iter_front_to_rear() -> None:
    assert list(NodeQueue(1, 2, 3)) == [1, 2, 3]


def test_node_iter_empty() -> None:
    assert list(NodeQueue()) == []


def test_node_reversed_rear_to_front() -> None:
    assert list(reversed(NodeQueue(1, 2, 3))) == [3, 2, 1]


def test_node_iter_does_not_modify() -> None:
    q = NodeQueue(1, 2, 3)
    _ = list(q)
    assert len(q) == 3


# ── __contains__ ──────────────────────────────────────────────────────────────


def test_node_contains_existing() -> None:
    assert 2 in NodeQueue(1, 2, 3)


def test_node_contains_missing() -> None:
    assert 99 not in NodeQueue(1, 2, 3)


def test_node_contains_none() -> None:
    assert None in NodeQueue(None, 1)


# ── __eq__ ────────────────────────────────────────────────────────────────────


def test_node_eq_equal() -> None:
    assert NodeQueue(1, 2, 3) == NodeQueue(1, 2, 3)


def test_node_eq_both_empty() -> None:
    assert NodeQueue() == NodeQueue()


def test_node_eq_different_elements() -> None:
    assert NodeQueue(1, 2, 3) != NodeQueue(1, 2, 9)


def test_node_eq_different_sizes() -> None:
    assert NodeQueue(1, 2) != NodeQueue(1, 2, 3)


def test_node_eq_not_implemented_for_other_type() -> None:
    assert NodeQueue(1).__eq__([1]) is NotImplemented


# ── __repr__ ──────────────────────────────────────────────────────────────────


def test_node_repr_empty() -> None:
    assert repr(NodeQueue()) == "NodeQueue(size=0)[]"


def test_node_repr_elements() -> None:
    assert repr(NodeQueue(1, 2, 3)) == "NodeQueue(size=3)[1, 2, 3]"


# ==============================================================================
# DynamicUniversalQueue
# ==============================================================================

# ── Init ──────────────────────────────────────────────────────────────────────


def test_dyn_univ_init_empty() -> None:
    q = DynamicUniversalQueue()
    assert len(q) == 0


def test_dyn_univ_init_with_args() -> None:
    q = DynamicUniversalQueue(1, 2, 3)
    assert len(q) == 3
    assert q.peek() == 1


def test_dyn_univ_init_mixed_types() -> None:
    q = DynamicUniversalQueue(1, "hi", 3.0)
    assert q.peek() == 1


# ── Enqueue / Dequeue ─────────────────────────────────────────────────────────


def test_dyn_univ_enqueue_adds_to_rear() -> None:
    q = DynamicUniversalQueue(1, 2)
    q.enqueue(3)
    assert list(q) == [1, 2, 3]


def test_dyn_univ_dequeue_returns_front() -> None:
    q = DynamicUniversalQueue(1, 2, 3)
    assert q.dequeue() == 1


def test_dyn_univ_dequeue_shifts_elements() -> None:
    q = DynamicUniversalQueue(1, 2, 3)
    q.dequeue()
    assert q.peek() == 2


def test_dyn_univ_dequeue_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicUniversalQueue().dequeue()


def test_dyn_univ_fifo_order() -> None:
    q = DynamicUniversalQueue(1, 2, 3)
    assert [q.dequeue(), q.dequeue(), q.dequeue()] == [1, 2, 3]


# ── Peek ──────────────────────────────────────────────────────────────────────


def test_dyn_univ_peek_does_not_remove() -> None:
    q = DynamicUniversalQueue(1, 2, 3)
    assert q.peek() == 1
    assert len(q) == 3


def test_dyn_univ_peek_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicUniversalQueue().peek()


# ── clear / copy ──────────────────────────────────────────────────────────────


def test_dyn_univ_clear_empties_queue() -> None:
    q = DynamicUniversalQueue(1, 2, 3)
    q.clear()
    assert q.is_empty()


def test_dyn_univ_copy_preserves_elements() -> None:
    q = DynamicUniversalQueue(1, 2, 3)
    c = q.copy()
    assert list(c) == [1, 2, 3]


def test_dyn_univ_copy_is_independent() -> None:
    q = DynamicUniversalQueue(1, 2)
    c = q.copy()
    c.enqueue(99)
    assert len(q) == 2


# ── __eq__ / __repr__ ─────────────────────────────────────────────────────────


def test_dyn_univ_eq_equal() -> None:
    assert DynamicUniversalQueue(1, 2, 3) == DynamicUniversalQueue(1, 2, 3)


def test_dyn_univ_eq_not_implemented() -> None:
    assert DynamicUniversalQueue(1).__eq__([1]) is NotImplemented


def test_dyn_univ_repr_empty() -> None:
    assert repr(DynamicUniversalQueue()) == "DynamicUniversalQueue(size=0)[]"


def test_dyn_univ_repr_elements() -> None:
    assert (
        repr(DynamicUniversalQueue(1, 2, 3)) == "DynamicUniversalQueue(size=3)[1, 2, 3]"
    )


# ==============================================================================
# DynamicTypedQueue
# ==============================================================================

# ── Init ──────────────────────────────────────────────────────────────────────


def test_dyn_typed_init_empty() -> None:
    q = DynamicTypedQueue(int)
    assert len(q) == 0


def test_dyn_typed_init_with_args() -> None:
    q = DynamicTypedQueue(int, 1, 2, 3)
    assert q.peek() == 1
    assert len(q) == 3


# ── Enqueue / Dequeue ─────────────────────────────────────────────────────────


def test_dyn_typed_enqueue_wrong_type_raises() -> None:
    q = DynamicTypedQueue(int)
    with pytest.raises(TypeError):
        q.enqueue("not an int")


def test_dyn_typed_dequeue_returns_front() -> None:
    q = DynamicTypedQueue(int, 1, 2, 3)
    assert q.dequeue() == 1


def test_dyn_typed_dequeue_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicTypedQueue(int).dequeue()


def test_dyn_typed_fifo_order() -> None:
    q = DynamicTypedQueue(int, 1, 2, 3)
    assert [q.dequeue(), q.dequeue(), q.dequeue()] == [1, 2, 3]


# ── Type enforcement ──────────────────────────────────────────────────────────


def test_dyn_typed_bool_rejected_for_int() -> None:
    q = DynamicTypedQueue(int)
    with pytest.raises(TypeError):
        q.enqueue(True)


def test_dyn_typed_contains_wrong_type_returns_false() -> None:
    q = DynamicTypedQueue(int, 1, 2, 3)
    assert "x" not in q


# ── __eq__ / __repr__ ─────────────────────────────────────────────────────────


def test_dyn_typed_eq_equal() -> None:
    assert DynamicTypedQueue(int, 1, 2, 3) == DynamicTypedQueue(int, 1, 2, 3)


def test_dyn_typed_eq_different_dtype() -> None:
    q1 = DynamicTypedQueue(int)
    q2 = DynamicTypedQueue(float)
    assert q1 != q2


def test_dyn_typed_repr_empty() -> None:
    assert repr(DynamicTypedQueue(int)) == "DynamicTypedQueue(int, size=0)[]"


def test_dyn_typed_repr_elements() -> None:
    assert (
        repr(DynamicTypedQueue(int, 1, 2, 3))
        == "DynamicTypedQueue(int, size=3)[1, 2, 3]"
    )


# ==============================================================================
# StaticUniversalQueue
# ==============================================================================

# ── Init ──────────────────────────────────────────────────────────────────────


def test_stat_univ_init_with_capacity() -> None:
    q = StaticUniversalQueue(capacity=5)
    assert len(q) == 0
    assert q._rear == 0


def test_stat_univ_init_with_args() -> None:
    q = StaticUniversalQueue(1, 2, 3, capacity=5)
    assert len(q) == 3
    assert q.peek() == 1


def test_stat_univ_init_no_args_no_capacity_raises() -> None:
    with pytest.raises(TypeError):
        StaticUniversalQueue()


def test_stat_univ_init_too_many_args_raises() -> None:
    with pytest.raises(OverflowError):
        StaticUniversalQueue(1, 2, 3, capacity=2)


def test_stat_univ_init_zero_capacity_raises() -> None:
    with pytest.raises(ValueError):
        StaticUniversalQueue(capacity=0)


# ── Enqueue / Dequeue ─────────────────────────────────────────────────────────


def test_stat_univ_enqueue_when_full_raises() -> None:
    q = StaticUniversalQueue(1, 2, capacity=2)
    with pytest.raises(OverflowError):
        q.enqueue(3)


def test_stat_univ_dequeue_returns_front() -> None:
    q = StaticUniversalQueue(1, 2, 3, capacity=5)
    assert q.dequeue() == 1


def test_stat_univ_dequeue_shifts_and_clears_slot() -> None:
    q = StaticUniversalQueue(1, 2, 3, capacity=5)
    q.dequeue()
    assert q.peek() == 2
    assert q._data[2] is None


def test_stat_univ_dequeue_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticUniversalQueue(capacity=3).dequeue()


def test_stat_univ_fifo_order() -> None:
    q = StaticUniversalQueue(1, 2, 3, capacity=5)
    assert [q.dequeue(), q.dequeue(), q.dequeue()] == [1, 2, 3]


# ── is_full ───────────────────────────────────────────────────────────────────


def test_stat_univ_is_full_true() -> None:
    assert StaticUniversalQueue(1, 2, capacity=2).is_full()


def test_stat_univ_is_full_false() -> None:
    assert not StaticUniversalQueue(1, capacity=3).is_full()


# ── clear / copy ──────────────────────────────────────────────────────────────


def test_stat_univ_clear_resets_rear() -> None:
    q = StaticUniversalQueue(1, 2, 3, capacity=5)
    q.clear()
    assert q._rear == 0
    assert q.is_empty()


def test_stat_univ_copy_preserves_elements_and_capacity() -> None:
    q = StaticUniversalQueue(1, 2, 3, capacity=5)
    c = q.copy()
    assert list(c) == [1, 2, 3]
    assert len(c._data) == len(q._data)


def test_stat_univ_copy_is_independent() -> None:
    q = StaticUniversalQueue(1, 2, capacity=5)
    c = q.copy()
    c.enqueue(99)
    assert len(q) == 2


# ── __eq__ / __repr__ ─────────────────────────────────────────────────────────


def test_stat_univ_eq_equal() -> None:
    a = StaticUniversalQueue(1, 2, capacity=5)
    b = StaticUniversalQueue(1, 2, capacity=5)
    assert a == b


def test_stat_univ_eq_same_elements_different_capacity() -> None:
    a = StaticUniversalQueue(1, 2, capacity=2)
    b = StaticUniversalQueue(1, 2, capacity=5)
    assert a == b


def test_stat_univ_eq_not_implemented() -> None:
    assert StaticUniversalQueue(1, capacity=3).__eq__([1]) is NotImplemented


def test_stat_univ_repr_empty() -> None:
    q = StaticUniversalQueue(capacity=3)
    assert repr(q) == "StaticUniversalQueue(size=0, capacity=3)[]"


def test_stat_univ_repr_elements() -> None:
    q = StaticUniversalQueue(1, 2, 3, capacity=5)
    assert repr(q) == "StaticUniversalQueue(size=3, capacity=5)[1, 2, 3]"


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_stat_univ_iter_front_to_rear() -> None:
    assert list(StaticUniversalQueue(1, 2, 3, capacity=5)) == [1, 2, 3]


def test_stat_univ_reversed_rear_to_front() -> None:
    assert list(reversed(StaticUniversalQueue(1, 2, 3, capacity=5))) == [3, 2, 1]


def test_stat_univ_contains_existing() -> None:
    assert 2 in StaticUniversalQueue(1, 2, 3, capacity=5)


def test_stat_univ_contains_missing() -> None:
    assert 99 not in StaticUniversalQueue(1, 2, 3, capacity=5)


# ==============================================================================
# StaticTypedQueue
# ==============================================================================

# ── Init ──────────────────────────────────────────────────────────────────────


def test_stat_typed_init_with_capacity() -> None:
    q = StaticTypedQueue(int, capacity=5)
    assert len(q) == 0


def test_stat_typed_init_with_args() -> None:
    q = StaticTypedQueue(int, 1, 2, 3, capacity=5)
    assert q.peek() == 1
    assert len(q) == 3


def test_stat_typed_init_too_many_args_raises() -> None:
    with pytest.raises(OverflowError):
        StaticTypedQueue(int, 1, 2, 3, capacity=2)


def test_stat_typed_init_zero_capacity_raises() -> None:
    with pytest.raises(ValueError):
        StaticTypedQueue(int, capacity=0)


# ── Enqueue / Dequeue ─────────────────────────────────────────────────────────


def test_stat_typed_enqueue_wrong_type_raises() -> None:
    q = StaticTypedQueue(int, capacity=5)
    with pytest.raises(TypeError):
        q.enqueue("x")


def test_stat_typed_enqueue_when_full_raises() -> None:
    q = StaticTypedQueue(int, 1, 2, capacity=2)
    with pytest.raises(OverflowError):
        q.enqueue(3)


def test_stat_typed_dequeue_returns_front() -> None:
    q = StaticTypedQueue(int, 1, 2, 3, capacity=5)
    assert q.dequeue() == 1


def test_stat_typed_dequeue_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticTypedQueue(int, capacity=3).dequeue()


def test_stat_typed_fifo_order() -> None:
    q = StaticTypedQueue(int, 1, 2, 3, capacity=5)
    assert [q.dequeue(), q.dequeue(), q.dequeue()] == [1, 2, 3]


# ── Type enforcement ──────────────────────────────────────────────────────────


def test_stat_typed_bool_rejected_for_int() -> None:
    q = StaticTypedQueue(int, capacity=5)
    with pytest.raises(TypeError):
        q.enqueue(True)


def test_stat_typed_contains_wrong_type_returns_false() -> None:
    q = StaticTypedQueue(int, 1, 2, 3, capacity=5)
    assert "x" not in q


# ── is_full / is_empty ────────────────────────────────────────────────────────


def test_stat_typed_is_full_true() -> None:
    assert StaticTypedQueue(int, 1, 2, capacity=2).is_full()


def test_stat_typed_is_empty_after_clear() -> None:
    q = StaticTypedQueue(int, 1, 2, capacity=5)
    q.clear()
    assert q.is_empty()


# ── __eq__ / __repr__ ─────────────────────────────────────────────────────────


def test_stat_typed_eq_equal() -> None:
    a = StaticTypedQueue(int, 1, 2, capacity=5)
    b = StaticTypedQueue(int, 1, 2, capacity=5)
    assert a == b


def test_stat_typed_eq_different_dtype() -> None:
    a = StaticTypedQueue(int, capacity=5)
    b = StaticTypedQueue(float, capacity=5)
    assert a != b


def test_stat_typed_repr_empty() -> None:
    q = StaticTypedQueue(int, capacity=3)
    assert repr(q) == "StaticTypedQueue(int, size=0, capacity=3)[]"


def test_stat_typed_repr_elements() -> None:
    q = StaticTypedQueue(int, 1, 2, 3, capacity=5)
    assert repr(q) == "StaticTypedQueue(int, size=3, capacity=5)[1, 2, 3]"


# ── copy ──────────────────────────────────────────────────────────────────────


def test_stat_typed_copy_preserves_dtype_and_elements() -> None:
    q = StaticTypedQueue(int, 1, 2, 3, capacity=5)
    c = q.copy()
    assert list(c) == [1, 2, 3]
    assert c._dtype is int


def test_stat_typed_copy_is_independent() -> None:
    q = StaticTypedQueue(int, 1, 2, capacity=5)
    c = q.copy()
    c.enqueue(99)
    assert len(q) == 2
