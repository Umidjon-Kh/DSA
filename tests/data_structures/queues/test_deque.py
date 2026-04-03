import pytest

from data_structures import (
    CircularNodeDeque,
    DynamicTypedDeque,
    DynamicUniversalDeque,
    NodeDeque,
    StaticTypedCircularDeque,
    StaticTypedDeque,
    StaticUniversalCircularDeque,
    StaticUniversalDeque,
)

# ==============================================================================
# NodeDeque
# ==============================================================================

# ── Init ──────────────────────────────────────────────────────────────────────


def test_node_init_empty() -> None:
    d = NodeDeque()
    assert d._size == 0
    assert d._front is None
    assert d._rear is None


def test_node_init_with_args() -> None:
    d = NodeDeque(1, 2, 3)
    assert d._size == 3
    assert d.peek_front() == 1
    assert d.peek_rear() == 3


# ── Enqueue front / rear ──────────────────────────────────────────────────────


def test_node_enqueue_front_prepends() -> None:
    d = NodeDeque(2, 3)
    d.enqueue_front(1)
    assert list(d) == [1, 2, 3]


def test_node_enqueue_rear_appends() -> None:
    d = NodeDeque(1, 2)
    d.enqueue_rear(3)
    assert list(d) == [1, 2, 3]


def test_node_enqueue_front_on_empty_sets_both_ends() -> None:
    d = NodeDeque()
    d.enqueue_front(1)
    assert d._front is d._rear


def test_node_enqueue_rear_on_empty_sets_both_ends() -> None:
    d = NodeDeque()
    d.enqueue_rear(1)
    assert d._front is d._rear


# ── Dequeue front / rear ──────────────────────────────────────────────────────


def test_node_dequeue_front_returns_front() -> None:
    d = NodeDeque(1, 2, 3)
    assert d.dequeue_front() == 1


def test_node_dequeue_rear_returns_rear() -> None:
    d = NodeDeque(1, 2, 3)
    assert d.dequeue_rear() == 3


def test_node_dequeue_front_advances_front() -> None:
    d = NodeDeque(1, 2, 3)
    d.dequeue_front()
    assert d.peek_front() == 2


def test_node_dequeue_rear_retreats_rear() -> None:
    d = NodeDeque(1, 2, 3)
    d.dequeue_rear()
    assert d.peek_rear() == 2


def test_node_dequeue_front_last_element_clears_both() -> None:
    d = NodeDeque(1)
    d.dequeue_front()
    assert d._front is None
    assert d._rear is None


def test_node_dequeue_rear_last_element_clears_both() -> None:
    d = NodeDeque(1)
    d.dequeue_rear()
    assert d._front is None
    assert d._rear is None


def test_node_dequeue_front_empty_raises() -> None:
    with pytest.raises(IndexError):
        NodeDeque().dequeue_front()


def test_node_dequeue_rear_empty_raises() -> None:
    with pytest.raises(IndexError):
        NodeDeque().dequeue_rear()


# ── Peek front / rear ─────────────────────────────────────────────────────────


def test_node_peek_front_without_removing() -> None:
    d = NodeDeque(1, 2, 3)
    assert d.peek_front() == 1
    assert len(d) == 3


def test_node_peek_rear_without_removing() -> None:
    d = NodeDeque(1, 2, 3)
    assert d.peek_rear() == 3
    assert len(d) == 3


def test_node_peek_front_empty_raises() -> None:
    with pytest.raises(IndexError):
        NodeDeque().peek_front()


def test_node_peek_rear_empty_raises() -> None:
    with pytest.raises(IndexError):
        NodeDeque().peek_rear()


# ── clear / copy ──────────────────────────────────────────────────────────────


def test_node_clear_resets_state() -> None:
    d = NodeDeque(1, 2, 3)
    d.clear()
    assert d._size == 0
    assert d._front is None
    assert d._rear is None


def test_node_copy_preserves_elements() -> None:
    d = NodeDeque(1, 2, 3)
    c = d.copy()
    assert list(c) == [1, 2, 3]


def test_node_copy_is_independent() -> None:
    d = NodeDeque(1, 2)
    c = d.copy()
    c.enqueue_rear(99)
    assert len(d) == 2


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_node_iter_front_to_rear() -> None:
    assert list(NodeDeque(1, 2, 3)) == [1, 2, 3]


def test_node_reversed_rear_to_front() -> None:
    assert list(reversed(NodeDeque(1, 2, 3))) == [3, 2, 1]


def test_node_iter_does_not_modify() -> None:
    d = NodeDeque(1, 2, 3)
    _ = list(d)
    assert len(d) == 3


# ── __eq__ / __repr__ ─────────────────────────────────────────────────────────


def test_node_eq_equal() -> None:
    assert NodeDeque(1, 2, 3) == NodeDeque(1, 2, 3)


def test_node_eq_different_elements() -> None:
    assert NodeDeque(1, 2, 3) != NodeDeque(1, 2, 9)


def test_node_eq_not_implemented_for_other_type() -> None:
    assert NodeDeque(1).__eq__([1]) is NotImplemented


def test_node_repr_empty() -> None:
    assert repr(NodeDeque()) == "NodeDeque(size=0)[]"


def test_node_repr_elements() -> None:
    assert repr(NodeDeque(1, 2, 3)) == "NodeDeque(size=3)[1, 2, 3]"


# ==============================================================================
# CircularNodeDeque
# ==============================================================================

# ── Init ──────────────────────────────────────────────────────────────────────


def test_circ_node_init_empty() -> None:
    d = CircularNodeDeque()
    assert d._size == 0
    assert d._sentinel.next is d._sentinel
    assert d._sentinel.prev is d._sentinel


def test_circ_node_init_with_args() -> None:
    d = CircularNodeDeque(1, 2, 3)
    assert d._size == 3
    assert d.peek_front() == 1
    assert d.peek_rear() == 3


# ── Enqueue front / rear ──────────────────────────────────────────────────────


def test_circ_node_enqueue_front_prepends() -> None:
    d = CircularNodeDeque(2, 3)
    d.enqueue_front(1)
    assert list(d) == [1, 2, 3]


def test_circ_node_enqueue_rear_appends() -> None:
    d = CircularNodeDeque(1, 2)
    d.enqueue_rear(3)
    assert list(d) == [1, 2, 3]


def test_circ_node_sentinel_stays_consistent_after_enqueue() -> None:
    d = CircularNodeDeque(1, 2, 3)
    assert d._sentinel.next.value == 1  # type: ignore[union-attr]
    assert d._sentinel.prev.value == 3  # type: ignore[union-attr]


# ── Dequeue front / rear ──────────────────────────────────────────────────────


def test_circ_node_dequeue_front_returns_front() -> None:
    d = CircularNodeDeque(1, 2, 3)
    assert d.dequeue_front() == 1


def test_circ_node_dequeue_rear_returns_rear() -> None:
    d = CircularNodeDeque(1, 2, 3)
    assert d.dequeue_rear() == 3


def test_circ_node_dequeue_front_empty_raises() -> None:
    with pytest.raises(IndexError):
        CircularNodeDeque().dequeue_front()


def test_circ_node_dequeue_rear_empty_raises() -> None:
    with pytest.raises(IndexError):
        CircularNodeDeque().dequeue_rear()


def test_circ_node_dequeue_last_restores_sentinel_self_loop() -> None:
    d = CircularNodeDeque(1)
    d.dequeue_front()
    assert d._sentinel.next is d._sentinel
    assert d._sentinel.prev is d._sentinel


# ── is_empty / clear / copy ───────────────────────────────────────────────────


def test_circ_node_is_empty_checks_sentinel() -> None:
    assert CircularNodeDeque().is_empty()
    assert not CircularNodeDeque(1).is_empty()


def test_circ_node_clear_resets_sentinel() -> None:
    d = CircularNodeDeque(1, 2, 3)
    d.clear()
    assert d._size == 0
    assert d._sentinel.next is d._sentinel


def test_circ_node_copy_preserves_elements() -> None:
    d = CircularNodeDeque(1, 2, 3)
    c = d.copy()
    assert list(c) == [1, 2, 3]


def test_circ_node_copy_is_independent() -> None:
    d = CircularNodeDeque(1, 2)
    c = d.copy()
    c.enqueue_rear(99)
    assert len(d) == 2


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_circ_node_iter_front_to_rear() -> None:
    assert list(CircularNodeDeque(1, 2, 3)) == [1, 2, 3]


def test_circ_node_reversed_rear_to_front() -> None:
    assert list(reversed(CircularNodeDeque(1, 2, 3))) == [3, 2, 1]


# ── __eq__ / __repr__ ─────────────────────────────────────────────────────────


def test_circ_node_eq_equal() -> None:
    assert CircularNodeDeque(1, 2, 3) == CircularNodeDeque(1, 2, 3)


def test_circ_node_eq_not_implemented_for_other_type() -> None:
    assert CircularNodeDeque(1).__eq__([1]) is NotImplemented


def test_circ_node_repr_empty() -> None:
    assert repr(CircularNodeDeque()) == "CircularNodeDeque(size=0)[]"


def test_circ_node_repr_elements() -> None:
    assert repr(CircularNodeDeque(1, 2, 3)) == "CircularNodeDeque(size=3)[1, 2, 3]"


# ==============================================================================
# DynamicUniversalDeque
# ==============================================================================

# ── Init ──────────────────────────────────────────────────────────────────────


def test_dyn_univ_init_empty() -> None:
    d = DynamicUniversalDeque()
    assert len(d) == 0


def test_dyn_univ_init_with_args() -> None:
    d = DynamicUniversalDeque(1, 2, 3)
    assert d.peek_front() == 1
    assert d.peek_rear() == 3


# ── Enqueue / Dequeue ─────────────────────────────────────────────────────────


def test_dyn_univ_enqueue_front_prepends() -> None:
    d = DynamicUniversalDeque(2, 3)
    d.enqueue_front(1)
    assert list(d) == [1, 2, 3]


def test_dyn_univ_enqueue_rear_appends() -> None:
    d = DynamicUniversalDeque(1, 2)
    d.enqueue_rear(3)
    assert list(d) == [1, 2, 3]


def test_dyn_univ_dequeue_front_returns_front() -> None:
    d = DynamicUniversalDeque(1, 2, 3)
    assert d.dequeue_front() == 1


def test_dyn_univ_dequeue_rear_returns_rear() -> None:
    d = DynamicUniversalDeque(1, 2, 3)
    assert d.dequeue_rear() == 3


def test_dyn_univ_dequeue_front_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicUniversalDeque().dequeue_front()


def test_dyn_univ_dequeue_rear_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicUniversalDeque().dequeue_rear()


# ── Peek / clear / copy ───────────────────────────────────────────────────────


def test_dyn_univ_peek_front_without_removing() -> None:
    d = DynamicUniversalDeque(1, 2, 3)
    assert d.peek_front() == 1
    assert len(d) == 3


def test_dyn_univ_peek_rear_without_removing() -> None:
    d = DynamicUniversalDeque(1, 2, 3)
    assert d.peek_rear() == 3
    assert len(d) == 3


def test_dyn_univ_clear_empties() -> None:
    d = DynamicUniversalDeque(1, 2, 3)
    d.clear()
    assert d.is_empty()


def test_dyn_univ_copy_is_independent() -> None:
    d = DynamicUniversalDeque(1, 2)
    c = d.copy()
    c.enqueue_rear(99)
    assert len(d) == 2


# ── __eq__ / __repr__ ─────────────────────────────────────────────────────────


def test_dyn_univ_eq_equal() -> None:
    assert DynamicUniversalDeque(1, 2, 3) == DynamicUniversalDeque(1, 2, 3)


def test_dyn_univ_repr_empty() -> None:
    assert repr(DynamicUniversalDeque()) == "DynamicUniversalDeque(size=0)[]"


def test_dyn_univ_repr_elements() -> None:
    assert (
        repr(DynamicUniversalDeque(1, 2, 3)) == "DynamicUniversalDeque(size=3)[1, 2, 3]"
    )


# ==============================================================================
# DynamicTypedDeque
# ==============================================================================

# ── Init ──────────────────────────────────────────────────────────────────────


def test_dyn_typed_init_empty() -> None:
    d = DynamicTypedDeque(int)
    assert len(d) == 0


def test_dyn_typed_init_with_args() -> None:
    d = DynamicTypedDeque(int, 1, 2, 3)
    assert d.peek_front() == 1
    assert d.peek_rear() == 3


# ── Enqueue / Dequeue ─────────────────────────────────────────────────────────


def test_dyn_typed_enqueue_front_wrong_type_raises() -> None:
    d = DynamicTypedDeque(int)
    with pytest.raises(TypeError):
        d.enqueue_front("x")


def test_dyn_typed_enqueue_rear_wrong_type_raises() -> None:
    d = DynamicTypedDeque(int)
    with pytest.raises(TypeError):
        d.enqueue_rear("x")


def test_dyn_typed_dequeue_front_returns_front() -> None:
    d = DynamicTypedDeque(int, 1, 2, 3)
    assert d.dequeue_front() == 1


def test_dyn_typed_dequeue_rear_returns_rear() -> None:
    d = DynamicTypedDeque(int, 1, 2, 3)
    assert d.dequeue_rear() == 3


def test_dyn_typed_dequeue_front_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicTypedDeque(int).dequeue_front()


def test_dyn_typed_dequeue_rear_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicTypedDeque(int).dequeue_rear()


def test_dyn_typed_bool_rejected_for_int() -> None:
    d = DynamicTypedDeque(int)
    with pytest.raises(TypeError):
        d.enqueue_rear(True)


# ── __eq__ / __repr__ ─────────────────────────────────────────────────────────


def test_dyn_typed_eq_equal() -> None:
    assert DynamicTypedDeque(int, 1, 2, 3) == DynamicTypedDeque(int, 1, 2, 3)


def test_dyn_typed_eq_different_dtype() -> None:
    assert DynamicTypedDeque(int) != DynamicTypedDeque(float)


def test_dyn_typed_repr_empty() -> None:
    assert repr(DynamicTypedDeque(int)) == "DynamicTypedDeque(int, size=0)[]"


def test_dyn_typed_repr_elements() -> None:
    assert (
        repr(DynamicTypedDeque(int, 1, 2, 3))
        == "DynamicTypedDeque(int, size=3)[1, 2, 3]"
    )


# ==============================================================================
# StaticUniversalDeque
# ==============================================================================

# ── Init ──────────────────────────────────────────────────────────────────────


def test_stat_univ_init_with_capacity() -> None:
    d = StaticUniversalDeque(capacity=5)
    assert len(d) == 0


def test_stat_univ_init_with_args() -> None:
    d = StaticUniversalDeque(1, 2, 3, capacity=5)
    assert d.peek_front() == 1
    assert d.peek_rear() == 3


def test_stat_univ_init_no_args_no_capacity_raises() -> None:
    with pytest.raises(TypeError):
        StaticUniversalDeque()


def test_stat_univ_init_too_many_args_raises() -> None:
    with pytest.raises(OverflowError):
        StaticUniversalDeque(1, 2, 3, capacity=2)


# ── Enqueue / Dequeue ─────────────────────────────────────────────────────────


def test_stat_univ_enqueue_front_prepends() -> None:
    d = StaticUniversalDeque(2, 3, capacity=5)
    d.enqueue_front(1)
    assert list(d) == [1, 2, 3]


def test_stat_univ_enqueue_rear_appends() -> None:
    d = StaticUniversalDeque(1, 2, capacity=5)
    d.enqueue_rear(3)
    assert list(d) == [1, 2, 3]


def test_stat_univ_enqueue_rear_when_full_raises() -> None:
    d = StaticUniversalDeque(1, 2, capacity=2)
    with pytest.raises(OverflowError):
        d.enqueue_rear(3)


def test_stat_univ_dequeue_front_returns_front() -> None:
    d = StaticUniversalDeque(1, 2, 3, capacity=5)
    assert d.dequeue_front() == 1


def test_stat_univ_dequeue_rear_returns_rear() -> None:
    d = StaticUniversalDeque(1, 2, 3, capacity=5)
    assert d.dequeue_rear() == 3


def test_stat_univ_dequeue_front_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticUniversalDeque(capacity=3).dequeue_front()


def test_stat_univ_dequeue_rear_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticUniversalDeque(capacity=3).dequeue_rear()


# ── is_full / clear / copy ────────────────────────────────────────────────────


def test_stat_univ_is_full_true() -> None:
    assert StaticUniversalDeque(1, 2, capacity=2).is_full()


def test_stat_univ_clear_empties() -> None:
    d = StaticUniversalDeque(1, 2, 3, capacity=5)
    d.clear()
    assert d.is_empty()


def test_stat_univ_copy_preserves_elements_and_capacity() -> None:
    d = StaticUniversalDeque(1, 2, 3, capacity=5)
    c = d.copy()
    assert list(c) == [1, 2, 3]
    assert len(c._data) == len(d._data)


def test_stat_univ_copy_is_independent() -> None:
    d = StaticUniversalDeque(1, 2, capacity=5)
    c = d.copy()
    c.enqueue_rear(99)
    assert len(d) == 2


# ── __eq__ / __repr__ ─────────────────────────────────────────────────────────


def test_stat_univ_eq_equal() -> None:
    a = StaticUniversalDeque(1, 2, capacity=5)
    b = StaticUniversalDeque(1, 2, capacity=5)
    assert a == b


def test_stat_univ_repr_empty() -> None:
    d = StaticUniversalDeque(capacity=3)
    assert repr(d) == "StaticUniversalDeque(size=0, capacity=3)[]"


def test_stat_univ_repr_elements() -> None:
    d = StaticUniversalDeque(1, 2, 3, capacity=5)
    assert repr(d) == "StaticUniversalDeque(size=3, capacity=5)[1, 2, 3]"


# ==============================================================================
# StaticTypedDeque
# ==============================================================================

# ── Init ──────────────────────────────────────────────────────────────────────


def test_stat_typed_init_with_capacity() -> None:
    d = StaticTypedDeque(int, capacity=5)
    assert len(d) == 0


def test_stat_typed_init_with_args() -> None:
    d = StaticTypedDeque(int, 1, 2, 3, capacity=5)
    assert d.peek_front() == 1
    assert d.peek_rear() == 3


def test_stat_typed_init_too_many_args_raises() -> None:
    with pytest.raises(OverflowError):
        StaticTypedDeque(int, 1, 2, 3, capacity=2)


# ── Enqueue / Dequeue ─────────────────────────────────────────────────────────


def test_stat_typed_enqueue_wrong_type_raises() -> None:
    d = StaticTypedDeque(int, capacity=5)
    with pytest.raises(TypeError):
        d.enqueue_rear("x")


def test_stat_typed_enqueue_rear_when_full_raises() -> None:
    d = StaticTypedDeque(int, 1, 2, capacity=2)
    with pytest.raises(OverflowError):
        d.enqueue_rear(3)


def test_stat_typed_dequeue_front_returns_front() -> None:
    d = StaticTypedDeque(int, 1, 2, 3, capacity=5)
    assert d.dequeue_front() == 1


def test_stat_typed_dequeue_rear_returns_rear() -> None:
    d = StaticTypedDeque(int, 1, 2, 3, capacity=5)
    assert d.dequeue_rear() == 3


def test_stat_typed_dequeue_front_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticTypedDeque(int, capacity=3).dequeue_front()


def test_stat_typed_bool_rejected_for_int() -> None:
    d = StaticTypedDeque(int, capacity=5)
    with pytest.raises(TypeError):
        d.enqueue_rear(True)


# ── __eq__ / __repr__ ─────────────────────────────────────────────────────────


def test_stat_typed_eq_equal() -> None:
    a = StaticTypedDeque(int, 1, 2, capacity=5)
    b = StaticTypedDeque(int, 1, 2, capacity=5)
    assert a == b


def test_stat_typed_eq_different_dtype() -> None:
    a = StaticTypedDeque(int, capacity=5)
    b = StaticTypedDeque(float, capacity=5)
    assert a != b


def test_stat_typed_repr_empty() -> None:
    d = StaticTypedDeque(int, capacity=3)
    assert repr(d) == "StaticTypedDeque(int, size=0, capacity=3)[]"


def test_stat_typed_repr_elements() -> None:
    d = StaticTypedDeque(int, 1, 2, 3, capacity=5)
    assert repr(d) == "StaticTypedDeque(int, size=3, capacity=5)[1, 2, 3]"


# ==============================================================================
# StaticUniversalCircularDeque
# ==============================================================================

# ── Init ──────────────────────────────────────────────────────────────────────


def test_stat_univ_circ_init_with_capacity() -> None:
    d = StaticUniversalCircularDeque(capacity=5)
    assert d._size == 0


def test_stat_univ_circ_init_with_args() -> None:
    d = StaticUniversalCircularDeque(1, 2, 3, capacity=5)
    assert d.peek_front() == 1
    assert d.peek_rear() == 3


def test_stat_univ_circ_init_too_many_args_raises() -> None:
    with pytest.raises(OverflowError):
        StaticUniversalCircularDeque(1, 2, 3, capacity=2)


# ── Enqueue / Dequeue O(1) both ends ─────────────────────────────────────────


def test_stat_univ_circ_enqueue_front_prepends() -> None:
    d = StaticUniversalCircularDeque(2, 3, capacity=5)
    d.enqueue_front(1)
    assert list(d) == [1, 2, 3]


def test_stat_univ_circ_enqueue_rear_appends() -> None:
    d = StaticUniversalCircularDeque(1, 2, capacity=5)
    d.enqueue_rear(3)
    assert list(d) == [1, 2, 3]


def test_stat_univ_circ_dequeue_front_returns_front() -> None:
    d = StaticUniversalCircularDeque(1, 2, 3, capacity=5)
    assert d.dequeue_front() == 1


def test_stat_univ_circ_dequeue_rear_returns_rear() -> None:
    d = StaticUniversalCircularDeque(1, 2, 3, capacity=5)
    assert d.dequeue_rear() == 3


def test_stat_univ_circ_enqueue_when_full_raises() -> None:
    d = StaticUniversalCircularDeque(1, 2, capacity=2)
    with pytest.raises(OverflowError):
        d.enqueue_rear(3)


def test_stat_univ_circ_dequeue_front_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticUniversalCircularDeque(capacity=3).dequeue_front()


def test_stat_univ_circ_dequeue_rear_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticUniversalCircularDeque(capacity=3).dequeue_rear()


# ── Wrap-around ───────────────────────────────────────────────────────────────


def test_stat_univ_circ_wrap_around_enqueue_front() -> None:
    d = StaticUniversalCircularDeque(2, 3, 4, capacity=5)
    d.enqueue_front(1)
    d.enqueue_front(0)
    assert list(d) == [0, 1, 2, 3, 4]


def test_stat_univ_circ_wrap_around_mixed_ops() -> None:
    d = StaticUniversalCircularDeque(1, 2, 3, capacity=5)
    d.dequeue_front()
    d.enqueue_rear(4)
    d.enqueue_rear(5)
    assert list(d) == [2, 3, 4, 5]


# ── is_full / clear / copy ────────────────────────────────────────────────────


def test_stat_univ_circ_is_full_true() -> None:
    assert StaticUniversalCircularDeque(1, 2, capacity=2).is_full()


def test_stat_univ_circ_clear_resets() -> None:
    d = StaticUniversalCircularDeque(1, 2, 3, capacity=5)
    d.clear()
    assert d._size == 0
    assert d.is_empty()


def test_stat_univ_circ_copy_preserves_elements() -> None:
    d = StaticUniversalCircularDeque(1, 2, 3, capacity=5)
    c = d.copy()
    assert list(c) == [1, 2, 3]


def test_stat_univ_circ_copy_is_independent() -> None:
    d = StaticUniversalCircularDeque(1, 2, capacity=5)
    c = d.copy()
    c.enqueue_rear(99)
    assert len(d) == 2


# ── __eq__ / __repr__ ─────────────────────────────────────────────────────────


def test_stat_univ_circ_eq_equal() -> None:
    a = StaticUniversalCircularDeque(1, 2, capacity=5)
    b = StaticUniversalCircularDeque(1, 2, capacity=5)
    assert a == b


def test_stat_univ_circ_repr_empty() -> None:
    d = StaticUniversalCircularDeque(capacity=3)
    assert repr(d) == "StaticUniversalCircularDeque(size=0, capacity=3)[]"


def test_stat_univ_circ_repr_elements() -> None:
    d = StaticUniversalCircularDeque(1, 2, 3, capacity=5)
    assert repr(d) == "StaticUniversalCircularDeque(size=3, capacity=5)[1, 2, 3]"


# ==============================================================================
# StaticTypedCircularDeque
# ==============================================================================

# ── Init ──────────────────────────────────────────────────────────────────────


def test_stat_typed_circ_init_with_capacity() -> None:
    d = StaticTypedCircularDeque(int, capacity=5)
    assert d._size == 0


def test_stat_typed_circ_init_with_args() -> None:
    d = StaticTypedCircularDeque(int, 1, 2, 3, capacity=5)
    assert d.peek_front() == 1
    assert d.peek_rear() == 3


def test_stat_typed_circ_init_too_many_args_raises() -> None:
    with pytest.raises(OverflowError):
        StaticTypedCircularDeque(int, 1, 2, 3, capacity=2)


# ── Enqueue / Dequeue ─────────────────────────────────────────────────────────


def test_stat_typed_circ_enqueue_wrong_type_raises() -> None:
    d = StaticTypedCircularDeque(int, capacity=5)
    with pytest.raises(TypeError):
        d.enqueue_rear("x")


def test_stat_typed_circ_enqueue_when_full_raises() -> None:
    d = StaticTypedCircularDeque(int, 1, 2, capacity=2)
    with pytest.raises(OverflowError):
        d.enqueue_rear(3)


def test_stat_typed_circ_dequeue_front_returns_front() -> None:
    d = StaticTypedCircularDeque(int, 1, 2, 3, capacity=5)
    assert d.dequeue_front() == 1


def test_stat_typed_circ_dequeue_rear_returns_rear() -> None:
    d = StaticTypedCircularDeque(int, 1, 2, 3, capacity=5)
    assert d.dequeue_rear() == 3


def test_stat_typed_circ_dequeue_front_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticTypedCircularDeque(int, capacity=3).dequeue_front()


def test_stat_typed_circ_bool_rejected_for_int() -> None:
    d = StaticTypedCircularDeque(int, capacity=5)
    with pytest.raises(TypeError):
        d.enqueue_rear(True)


# ── Wrap-around ───────────────────────────────────────────────────────────────


def test_stat_typed_circ_wrap_around() -> None:
    d = StaticTypedCircularDeque(int, capacity=3)
    d.enqueue_rear(1)
    d.enqueue_rear(2)
    d.enqueue_rear(3)
    d.dequeue_front()
    d.enqueue_rear(4)
    assert list(d) == [2, 3, 4]


# ── is_full / clear / copy ────────────────────────────────────────────────────


def test_stat_typed_circ_is_full_true() -> None:
    assert StaticTypedCircularDeque(int, 1, 2, capacity=2).is_full()


def test_stat_typed_circ_clear_resets() -> None:
    d = StaticTypedCircularDeque(int, 1, 2, capacity=5)
    d.clear()
    assert d.is_empty()


def test_stat_typed_circ_copy_preserves_dtype_and_elements() -> None:
    d = StaticTypedCircularDeque(int, 1, 2, 3, capacity=5)
    c = d.copy()
    assert list(c) == [1, 2, 3]
    assert c._dtype is int


def test_stat_typed_circ_copy_is_independent() -> None:
    d = StaticTypedCircularDeque(int, 1, 2, capacity=5)
    c = d.copy()
    c.enqueue_rear(99)
    assert len(d) == 2


# ── __eq__ / __repr__ ─────────────────────────────────────────────────────────


def test_stat_typed_circ_eq_equal() -> None:
    a = StaticTypedCircularDeque(int, 1, 2, capacity=5)
    b = StaticTypedCircularDeque(int, 1, 2, capacity=5)
    assert a == b


def test_stat_typed_circ_eq_different_dtype() -> None:
    a = StaticTypedCircularDeque(int, capacity=5)
    b = StaticTypedCircularDeque(float, capacity=5)
    assert a != b


def test_stat_typed_circ_repr_empty() -> None:
    d = StaticTypedCircularDeque(int, capacity=3)
    assert repr(d) == "StaticTypedCircularDeque(int, size=0, capacity=3)[]"


def test_stat_typed_circ_repr_elements() -> None:
    d = StaticTypedCircularDeque(int, 1, 2, 3, capacity=5)
    assert repr(d) == "StaticTypedCircularDeque(int, size=3, capacity=5)[1, 2, 3]"
