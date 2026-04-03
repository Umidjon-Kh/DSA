import pytest

from data_structures import StaticTypedCircularQueue, StaticUniversalCircularQueue
from data_structures.queues.circular import NodeCircularQueue

# ==============================================================================
# StaticUniversalCircularQueue
# ==============================================================================

# ── Init ──────────────────────────────────────────────────────────────────────


def test_univ_init_with_capacity() -> None:
    q = StaticUniversalCircularQueue(capacity=5)
    assert q._size == 0
    assert q._front == 0
    assert q._rear == 0


def test_univ_init_with_args() -> None:
    q = StaticUniversalCircularQueue(1, 2, 3, capacity=5)
    assert q._size == 3
    assert q.peek() == 1


def test_univ_init_no_args_no_capacity_raises() -> None:
    with pytest.raises(TypeError):
        StaticUniversalCircularQueue()


def test_univ_init_too_many_args_raises() -> None:
    with pytest.raises(OverflowError):
        StaticUniversalCircularQueue(1, 2, 3, capacity=2)


def test_univ_init_zero_capacity_raises() -> None:
    with pytest.raises(ValueError):
        StaticUniversalCircularQueue(capacity=0)


# ── Enqueue ───────────────────────────────────────────────────────────────────


def test_univ_enqueue_advances_rear() -> None:
    q = StaticUniversalCircularQueue(capacity=5)
    q.enqueue(1)
    assert q._rear == 1
    assert q._size == 1


def test_univ_enqueue_when_full_raises() -> None:
    q = StaticUniversalCircularQueue(1, 2, capacity=2)
    with pytest.raises(OverflowError):
        q.enqueue(3)


def test_univ_enqueue_wraps_rear_around() -> None:
    q = StaticUniversalCircularQueue(capacity=3)
    q.enqueue(1)
    assert q._rear == 1
    q.enqueue(2)
    assert q._rear == 2
    q.enqueue(3)
    assert q._rear == 0
    q.dequeue()
    q.enqueue(4)
    assert q._rear == 1  # wrapped back to index 0


# ── Dequeue ───────────────────────────────────────────────────────────────────


def test_univ_dequeue_returns_front() -> None:
    q = StaticUniversalCircularQueue(1, 2, 3, capacity=5)
    assert q.dequeue() == 1


def test_univ_dequeue_advances_front() -> None:
    q = StaticUniversalCircularQueue(1, 2, 3, capacity=5)
    q.dequeue()
    assert q._front == 1
    assert q._size == 2


def test_univ_dequeue_clears_slot() -> None:
    q = StaticUniversalCircularQueue(1, 2, capacity=5)
    q.dequeue()
    assert q._data[0] is None


def test_univ_dequeue_wraps_front_around() -> None:
    q = StaticUniversalCircularQueue(capacity=3)
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    q.dequeue()
    q.dequeue()
    q.dequeue()
    assert q._front == 0


def test_univ_dequeue_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticUniversalCircularQueue(capacity=3).dequeue()


def test_univ_fifo_order() -> None:
    q = StaticUniversalCircularQueue(1, 2, 3, capacity=5)
    assert [q.dequeue(), q.dequeue(), q.dequeue()] == [1, 2, 3]


# ── Peek ──────────────────────────────────────────────────────────────────────


def test_univ_peek_returns_front_without_removing() -> None:
    q = StaticUniversalCircularQueue(1, 2, 3, capacity=5)
    assert q.peek() == 1
    assert len(q) == 3


def test_univ_peek_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticUniversalCircularQueue(capacity=3).peek()


# ── is_full / is_empty ────────────────────────────────────────────────────────


def test_univ_is_full_true() -> None:
    assert StaticUniversalCircularQueue(1, 2, capacity=2).is_full()


def test_univ_is_full_false() -> None:
    assert not StaticUniversalCircularQueue(1, capacity=3).is_full()


def test_univ_is_empty_true() -> None:
    assert StaticUniversalCircularQueue(capacity=3).is_empty()


def test_univ_is_empty_false() -> None:
    assert not StaticUniversalCircularQueue(1, capacity=3).is_empty()


# ── clear / copy ──────────────────────────────────────────────────────────────


def test_univ_clear_resets_pointers() -> None:
    q = StaticUniversalCircularQueue(1, 2, 3, capacity=5)
    q.clear()
    assert q._front == 0
    assert q._rear == 0
    assert q._size == 0


def test_univ_copy_preserves_elements_in_order() -> None:
    q = StaticUniversalCircularQueue(1, 2, 3, capacity=5)
    c = q.copy()
    assert list(c) == [1, 2, 3]


def test_univ_copy_after_wrap_preserves_order() -> None:
    q = StaticUniversalCircularQueue(capacity=3)
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    q.dequeue()
    q.enqueue(4)
    c = q.copy()
    assert list(c) == [2, 3, 4]


def test_univ_copy_is_independent() -> None:
    q = StaticUniversalCircularQueue(1, 2, capacity=5)
    c = q.copy()
    c.enqueue(99)
    assert len(q) == 2


def test_univ_copy_preserves_capacity() -> None:
    q = StaticUniversalCircularQueue(1, 2, capacity=5)
    c = q.copy()
    assert len(c._data) == len(q._data)


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_univ_iter_front_to_rear() -> None:
    q = StaticUniversalCircularQueue(1, 2, 3, capacity=5)
    assert list(q) == [1, 2, 3]


def test_univ_iter_wraps_correctly() -> None:
    q = StaticUniversalCircularQueue(capacity=3)
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    q.dequeue()
    q.enqueue(4)
    assert list(q) == [2, 3, 4]


def test_univ_reversed_rear_to_front() -> None:
    q = StaticUniversalCircularQueue(1, 2, 3, capacity=5)
    assert list(reversed(q)) == [3, 2, 1]


def test_univ_iter_does_not_modify() -> None:
    q = StaticUniversalCircularQueue(1, 2, 3, capacity=5)
    _ = list(q)
    assert len(q) == 3


# ── __contains__ ──────────────────────────────────────────────────────────────


def test_univ_contains_existing() -> None:
    assert 2 in StaticUniversalCircularQueue(1, 2, 3, capacity=5)


def test_univ_contains_missing() -> None:
    assert 99 not in StaticUniversalCircularQueue(1, 2, 3, capacity=5)


# ── __eq__ ────────────────────────────────────────────────────────────────────


def test_univ_eq_equal() -> None:
    a = StaticUniversalCircularQueue(1, 2, capacity=5)
    b = StaticUniversalCircularQueue(1, 2, capacity=5)
    assert a == b


def test_univ_eq_different_elements() -> None:
    a = StaticUniversalCircularQueue(1, 2, capacity=5)
    b = StaticUniversalCircularQueue(1, 9, capacity=5)
    assert a != b


def test_univ_eq_same_logical_order_different_physical_layout() -> None:
    a = StaticUniversalCircularQueue(capacity=3)
    a.enqueue(1)
    a.enqueue(2)
    a.dequeue()
    a.enqueue(3)  # _front=1

    b = StaticUniversalCircularQueue(2, 3, capacity=3)  # _front=0
    assert a == b


def test_univ_eq_not_implemented_for_other_type() -> None:
    assert StaticUniversalCircularQueue(1, capacity=3).__eq__([1]) is NotImplemented


# ── __repr__ ──────────────────────────────────────────────────────────────────


def test_univ_repr_empty() -> None:
    q = StaticUniversalCircularQueue(capacity=3)
    assert repr(q) == "StaticUniversalCircularQueue(size=0, capacity=3)[]"


def test_univ_repr_elements() -> None:
    q = StaticUniversalCircularQueue(1, 2, 3, capacity=5)
    assert repr(q) == "StaticUniversalCircularQueue(size=3, capacity=5)[1, 2, 3]"


# ==============================================================================
# StaticTypedCircularQueue
# ==============================================================================

# ── Init ──────────────────────────────────────────────────────────────────────


def test_typed_init_with_capacity() -> None:
    q = StaticTypedCircularQueue(int, capacity=5)
    assert q._size == 0


def test_typed_init_with_args() -> None:
    q = StaticTypedCircularQueue(int, 1, 2, 3, capacity=5)
    assert q.peek() == 1
    assert len(q) == 3


def test_typed_init_too_many_args_raises() -> None:
    with pytest.raises(OverflowError):
        StaticTypedCircularQueue(int, 1, 2, 3, capacity=2)


def test_typed_init_zero_capacity_raises() -> None:
    with pytest.raises(ValueError):
        StaticTypedCircularQueue(int, capacity=0)


# ── Enqueue / Dequeue ─────────────────────────────────────────────────────────


def test_typed_enqueue_wrong_type_raises() -> None:
    q = StaticTypedCircularQueue(int, capacity=5)
    with pytest.raises(TypeError):
        q.enqueue("x")


def test_typed_enqueue_when_full_raises() -> None:
    q = StaticTypedCircularQueue(int, 1, 2, capacity=2)
    with pytest.raises(OverflowError):
        q.enqueue(3)


def test_typed_dequeue_returns_front() -> None:
    q = StaticTypedCircularQueue(int, 1, 2, 3, capacity=5)
    assert q.dequeue() == 1


def test_typed_dequeue_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticTypedCircularQueue(int, capacity=3).dequeue()


def test_typed_fifo_order() -> None:
    q = StaticTypedCircularQueue(int, 1, 2, 3, capacity=5)
    assert [q.dequeue(), q.dequeue(), q.dequeue()] == [1, 2, 3]


# ── Type enforcement ──────────────────────────────────────────────────────────


def test_typed_bool_rejected_for_int() -> None:
    q = StaticTypedCircularQueue(int, capacity=5)
    with pytest.raises(TypeError):
        q.enqueue(True)


def test_typed_contains_wrong_type_returns_false() -> None:
    q = StaticTypedCircularQueue(int, 1, 2, 3, capacity=5)
    assert "x" not in q


# ── Wrap-around ───────────────────────────────────────────────────────────────


def test_typed_wrap_around_enqueue_dequeue() -> None:
    q = StaticTypedCircularQueue(int, capacity=3)
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    q.dequeue()
    q.enqueue(4)
    assert list(q) == [2, 3, 4]


# ── is_full / clear / copy ────────────────────────────────────────────────────


def test_typed_is_full_true() -> None:
    assert StaticTypedCircularQueue(int, 1, 2, capacity=2).is_full()


def test_typed_clear_resets_pointers() -> None:
    q = StaticTypedCircularQueue(int, 1, 2, capacity=5)
    q.clear()
    assert q._size == 0
    assert q._front == 0
    assert q._rear == 0


def test_typed_copy_preserves_dtype_and_elements() -> None:
    q = StaticTypedCircularQueue(int, 1, 2, 3, capacity=5)
    c = q.copy()
    assert list(c) == [1, 2, 3]
    assert c._dtype is int


def test_typed_copy_is_independent() -> None:
    q = StaticTypedCircularQueue(int, 1, 2, capacity=5)
    c = q.copy()
    c.enqueue(99)
    assert len(q) == 2


# ── __eq__ / __repr__ ─────────────────────────────────────────────────────────


def test_typed_eq_equal() -> None:
    a = StaticTypedCircularQueue(int, 1, 2, capacity=5)
    b = StaticTypedCircularQueue(int, 1, 2, capacity=5)
    assert a == b


def test_typed_eq_different_dtype() -> None:
    a = StaticTypedCircularQueue(int, capacity=5)
    b = StaticTypedCircularQueue(float, capacity=5)
    assert a != b


def test_typed_eq_not_implemented_for_other_type() -> None:
    assert StaticTypedCircularQueue(int, 1, capacity=3).__eq__([1]) is NotImplemented


def test_typed_repr_empty() -> None:
    q = StaticTypedCircularQueue(int, capacity=3)
    assert repr(q) == "StaticTypedCircularQueue(int, size=0, capacity=3)[]"


def test_typed_repr_elements() -> None:
    q = StaticTypedCircularQueue(int, 1, 2, 3, capacity=5)
    assert repr(q) == "StaticTypedCircularQueue(int, size=3, capacity=5)[1, 2, 3]"


# ==============================================================================
# NodeCircularQueue
# ==============================================================================

# ── Init ──────────────────────────────────────────────────────────────────────


def test_node_circ_init_empty() -> None:
    q = NodeCircularQueue()
    assert q._size == 0
    assert q._rear is None


def test_node_circ_init_with_args() -> None:
    q = NodeCircularQueue(1, 2, 3)
    assert q._size == 3
    assert q.peek() == 1


def test_node_circ_init_single_arg_points_to_itself() -> None:
    q = NodeCircularQueue(42)
    assert q._rear is q._rear.next  # type: ignore[union-attr]


# ── Enqueue ───────────────────────────────────────────────────────────────────


def test_node_circ_enqueue_increments_size() -> None:
    q = NodeCircularQueue()
    q.enqueue(1)
    assert q._size == 1


def test_node_circ_enqueue_first_makes_self_loop() -> None:
    q = NodeCircularQueue()
    q.enqueue(99)
    assert q._rear.next is q._rear  # type: ignore[union-attr]


def test_node_circ_enqueue_maintains_circular_invariant() -> None:
    q = NodeCircularQueue(1, 2, 3)
    assert q._rear.next.value == 1  # type: ignore[union-attr]  # front is always rear.next


def test_node_circ_enqueue_rear_advances() -> None:
    q = NodeCircularQueue(1, 2)
    q.enqueue(3)
    assert q._rear.value == 3  # type: ignore[union-attr]


# ── Dequeue ───────────────────────────────────────────────────────────────────


def test_node_circ_dequeue_returns_front() -> None:
    q = NodeCircularQueue(1, 2, 3)
    assert q.dequeue() == 1


def test_node_circ_dequeue_decrements_size() -> None:
    q = NodeCircularQueue(1, 2, 3)
    q.dequeue()
    assert q._size == 2


def test_node_circ_dequeue_last_sets_rear_none() -> None:
    q = NodeCircularQueue(1)
    q.dequeue()
    assert q._rear is None


def test_node_circ_dequeue_empty_raises() -> None:
    with pytest.raises(IndexError):
        NodeCircularQueue().dequeue()


def test_node_circ_fifo_order() -> None:
    q = NodeCircularQueue(1, 2, 3)
    assert [q.dequeue(), q.dequeue(), q.dequeue()] == [1, 2, 3]


# ── Peek ──────────────────────────────────────────────────────────────────────


def test_node_circ_peek_returns_front_without_removing() -> None:
    q = NodeCircularQueue(1, 2, 3)
    assert q.peek() == 1
    assert len(q) == 3


def test_node_circ_peek_empty_raises() -> None:
    with pytest.raises(IndexError):
        NodeCircularQueue().peek()


# ── clear / copy ──────────────────────────────────────────────────────────────


def test_node_circ_clear_resets_state() -> None:
    q = NodeCircularQueue(1, 2, 3)
    q.clear()
    assert q._rear is None
    assert q._size == 0


def test_node_circ_copy_preserves_elements() -> None:
    q = NodeCircularQueue(1, 2, 3)
    c = q.copy()
    assert list(c) == [1, 2, 3]


def test_node_circ_copy_is_independent() -> None:
    q = NodeCircularQueue(1, 2)
    c = q.copy()
    c.enqueue(99)
    assert len(q) == 2


# ── is_empty / __bool__ / __len__ ─────────────────────────────────────────────


def test_node_circ_is_empty_true() -> None:
    assert NodeCircularQueue().is_empty()


def test_node_circ_is_empty_false() -> None:
    assert not NodeCircularQueue(1).is_empty()


def test_node_circ_bool_empty() -> None:
    assert not bool(NodeCircularQueue())


def test_node_circ_bool_not_empty() -> None:
    assert bool(NodeCircularQueue(1))


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_node_circ_iter_front_to_rear() -> None:
    assert list(NodeCircularQueue(1, 2, 3)) == [1, 2, 3]


def test_node_circ_iter_empty() -> None:
    assert list(NodeCircularQueue()) == []


def test_node_circ_reversed_rear_to_front() -> None:
    assert list(reversed(NodeCircularQueue(1, 2, 3))) == [3, 2, 1]


def test_node_circ_iter_does_not_modify() -> None:
    q = NodeCircularQueue(1, 2, 3)
    _ = list(q)
    assert len(q) == 3


# ── __contains__ ──────────────────────────────────────────────────────────────


def test_node_circ_contains_existing() -> None:
    assert 2 in NodeCircularQueue(1, 2, 3)


def test_node_circ_contains_missing() -> None:
    assert 99 not in NodeCircularQueue(1, 2, 3)


# ── __eq__ ────────────────────────────────────────────────────────────────────


def test_node_circ_eq_equal() -> None:
    assert NodeCircularQueue(1, 2, 3) == NodeCircularQueue(1, 2, 3)


def test_node_circ_eq_both_empty() -> None:
    assert NodeCircularQueue() == NodeCircularQueue()


def test_node_circ_eq_different_elements() -> None:
    assert NodeCircularQueue(1, 2, 3) != NodeCircularQueue(1, 2, 9)


def test_node_circ_eq_not_implemented_for_other_type() -> None:
    assert NodeCircularQueue(1).__eq__([1]) is NotImplemented


# ── __repr__ ──────────────────────────────────────────────────────────────────


def test_node_circ_repr_empty() -> None:
    assert repr(NodeCircularQueue()) == "NodeCircularQueue(size=0)[]"


def test_node_circ_repr_elements() -> None:
    assert repr(NodeCircularQueue(1, 2, 3)) == "NodeCircularQueue(size=3)[1, 2, 3]"
