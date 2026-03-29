import pytest

from data_structures.heaps import StaticTypedMinHeap, StaticUniversalMinHeap

# ══════════════════════════════════════════════════════════════════════════════
# StaticTypedMinHeap
# ══════════════════════════════════════════════════════════════════════════════

# ── Init ──────────────────────────────────────────────────────────────────────


def test_typed_init_empty() -> None:
    h = StaticTypedMinHeap(int, capacity=5)
    assert len(h) == 0
    assert h.is_empty()


def test_typed_init_with_args() -> None:
    h = StaticTypedMinHeap(int, 5, 3, 1, capacity=5)
    assert len(h) == 3
    assert h.peek() == 1


def test_typed_init_no_capacity_no_args_raises() -> None:
    with pytest.raises(TypeError):
        StaticTypedMinHeap(int)


def test_typed_init_zero_capacity_raises() -> None:
    with pytest.raises(ValueError):
        StaticTypedMinHeap(int, capacity=0)


def test_typed_init_too_many_args_raises() -> None:
    with pytest.raises(OverflowError):
        StaticTypedMinHeap(int, 1, 2, 3, capacity=2)


def test_typed_init_wrong_type_raises() -> None:
    with pytest.raises(TypeError):
        StaticTypedMinHeap(int, 1, "x", capacity=5)


# ── Push ──────────────────────────────────────────────────────────────────────


def test_typed_push_single() -> None:
    h = StaticTypedMinHeap(int, capacity=5)
    h.push(10)
    assert h.peek() == 10
    assert len(h) == 1


def test_typed_push_smaller_becomes_root() -> None:
    h = StaticTypedMinHeap(int, capacity=5)
    h.push(5)
    h.push(1)
    assert h.peek() == 1


def test_typed_push_larger_does_not_change_root() -> None:
    h = StaticTypedMinHeap(int, capacity=5)
    h.push(1)
    h.push(9)
    assert h.peek() == 1


def test_typed_push_equal_values() -> None:
    h = StaticTypedMinHeap(int, capacity=5)
    h.push(3)
    h.push(3)
    assert h.peek() == 3
    assert len(h) == 2


def test_typed_push_full_raises() -> None:
    h = StaticTypedMinHeap(int, 1, 2, capacity=2)
    with pytest.raises(OverflowError):
        h.push(3)


def test_typed_push_wrong_type_raises() -> None:
    h = StaticTypedMinHeap(int, capacity=5)
    with pytest.raises(TypeError):
        h.push("x")


def test_typed_push_bool_rejected_for_int() -> None:
    h = StaticTypedMinHeap(int, capacity=5)
    with pytest.raises(TypeError):
        h.push(True)


# ── Pop ───────────────────────────────────────────────────────────────────────


def test_typed_pop_returns_minimum() -> None:
    h = StaticTypedMinHeap(int, 5, 3, 8, 1, capacity=5)
    assert h.pop() == 1


def test_typed_pop_reduces_size() -> None:
    h = StaticTypedMinHeap(int, 1, 2, capacity=3)
    h.pop()
    assert len(h) == 1


def test_typed_pop_sequence_sorted() -> None:
    h = StaticTypedMinHeap(int, 5, 3, 8, 1, 4, capacity=5)
    result = [h.pop() for _ in range(5)]
    assert result == sorted(result)


def test_typed_pop_empty_raises() -> None:
    h = StaticTypedMinHeap(int, capacity=3)
    with pytest.raises(IndexError):
        h.pop()


def test_typed_pop_single_element() -> None:
    h = StaticTypedMinHeap(int, capacity=1)
    h.push(7)
    assert h.pop() == 7
    assert h.is_empty()


# ── Peek ──────────────────────────────────────────────────────────────────────


def test_typed_peek_does_not_remove() -> None:
    h = StaticTypedMinHeap(int, 1, 2, 3, capacity=5)
    h.peek()
    assert len(h) == 3


def test_typed_peek_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticTypedMinHeap(int, capacity=3).peek()


def test_typed_peek_always_minimum() -> None:
    h = StaticTypedMinHeap(int, capacity=10)
    for v in [9, 4, 7, 2, 6]:
        h.push(v)
    assert h.peek() == 2


# ── Heapify ───────────────────────────────────────────────────────────────────


def test_typed_heapify_sets_correct_root() -> None:
    h = StaticTypedMinHeap(int, capacity=10)
    h.heapify([9, 4, 7, 2, 6])
    assert h.peek() == 2


def test_typed_heapify_appends_to_existing() -> None:
    h = StaticTypedMinHeap(int, capacity=10)
    h.push(1)
    h.heapify([5, 3])
    assert len(h) == 3
    assert h.peek() == 1


def test_typed_heapify_overflow_raises() -> None:
    h = StaticTypedMinHeap(int, capacity=3)
    with pytest.raises(OverflowError):
        h.heapify([1, 2, 3, 4])


def test_typed_heapify_wrong_type_raises() -> None:
    h = StaticTypedMinHeap(int, capacity=5)
    with pytest.raises(TypeError):
        h.heapify([1, 2, "x"])


def test_typed_heapify_not_iterable_raises() -> None:
    h = StaticTypedMinHeap(int, capacity=5)
    with pytest.raises(TypeError):
        h.heapify(123)  # type: ignore[arg-type]


# ── Ordered ───────────────────────────────────────────────────────────────────


def test_typed_ordered_yields_sorted() -> None:
    h = StaticTypedMinHeap(int, 5, 3, 8, 1, 4, capacity=5)
    assert list(h.ordered()) == [1, 3, 4, 5, 8]


def test_typed_ordered_does_not_modify_heap() -> None:
    h = StaticTypedMinHeap(int, 3, 1, 2, capacity=5)
    list(h.ordered())
    assert len(h) == 3
    assert h.peek() == 1


# ── Clear / copy ──────────────────────────────────────────────────────────────


def test_typed_clear_empties_heap() -> None:
    h = StaticTypedMinHeap(int, 1, 2, 3, capacity=5)
    h.clear()
    assert len(h) == 0
    assert h.is_empty()


def test_typed_copy_is_equal() -> None:
    h = StaticTypedMinHeap(int, 3, 1, 2, capacity=5)
    assert h.copy() == h


def test_typed_copy_is_independent() -> None:
    h = StaticTypedMinHeap(int, 1, 2, capacity=5)
    c = h.copy()
    c.push(0)
    assert len(h) == 2


def test_typed_copy_preserves_dtype() -> None:
    h = StaticTypedMinHeap(int, 1, capacity=3)
    assert h.copy()._dtype is int


# ── is_empty / is_full ────────────────────────────────────────────────────────


def test_typed_is_empty_true() -> None:
    assert StaticTypedMinHeap(int, capacity=3).is_empty()


def test_typed_is_empty_false() -> None:
    assert not StaticTypedMinHeap(int, 1, capacity=3).is_empty()


def test_typed_is_full_true() -> None:
    assert StaticTypedMinHeap(int, 1, 2, 3, capacity=3).is_full()


def test_typed_is_full_false() -> None:
    assert not StaticTypedMinHeap(int, 1, capacity=3).is_full()


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_typed_iter_root_first() -> None:
    h = StaticTypedMinHeap(int, 3, 1, 2, capacity=5)
    values = list(h)
    assert values[0] == 1


def test_typed_iter_does_not_modify() -> None:
    h = StaticTypedMinHeap(int, 1, 2, 3, capacity=5)
    list(h)
    assert len(h) == 3


def test_typed_reversed_last_to_first() -> None:
    h = StaticTypedMinHeap(int, 3, 1, 2, capacity=5)
    fwd = list(h)
    rev = list(reversed(h))
    assert fwd == list(reversed(rev))


# ── __contains__ ──────────────────────────────────────────────────────────────


def test_typed_contains_existing() -> None:
    assert 3 in StaticTypedMinHeap(int, 1, 2, 3, capacity=5)


def test_typed_contains_missing() -> None:
    assert 99 not in StaticTypedMinHeap(int, 1, 2, 3, capacity=5)


def test_typed_contains_wrong_type_false() -> None:
    h = StaticTypedMinHeap(int, 1, capacity=3)
    assert "x" not in h


# ── __eq__ ────────────────────────────────────────────────────────────────────


def test_typed_eq_equal() -> None:
    a = StaticTypedMinHeap(int, 1, 2, 3, capacity=5)
    b = StaticTypedMinHeap(int, 1, 2, 3, capacity=5)
    assert a == b


def test_typed_eq_different_elements() -> None:
    a = StaticTypedMinHeap(int, 1, 2, capacity=3)
    b = StaticTypedMinHeap(int, 1, 9, capacity=3)
    assert a != b


def test_typed_eq_different_capacity_same_data() -> None:
    a = StaticTypedMinHeap(int, 1, 2, capacity=2)
    b = StaticTypedMinHeap(int, 1, 2, capacity=5)
    assert a == b


def test_typed_eq_not_implemented_for_other_type() -> None:
    h = StaticTypedMinHeap(int, 1, capacity=3)
    assert h.__eq__([1]) is NotImplemented


# ── __repr__ ──────────────────────────────────────────────────────────────────


def test_typed_repr_empty() -> None:
    h = StaticTypedMinHeap(int, capacity=3)
    assert repr(h) == "StaticTypedMinHeap(int, size=0, capacity=3)[]"


def test_typed_repr_partial() -> None:
    h = StaticTypedMinHeap(int, capacity=5)
    h.push(1)
    assert "StaticTypedMinHeap(int" in repr(h)
    assert "1" in repr(h)


# ══════════════════════════════════════════════════════════════════════════════
# StaticUniversalMinHeap
# ══════════════════════════════════════════════════════════════════════════════

# ── Init ──────────────────────────────────────────────────────────────────────


def test_universal_init_empty() -> None:
    h = StaticUniversalMinHeap(capacity=5)
    assert len(h) == 0
    assert h.is_empty()


def test_universal_init_with_args() -> None:
    h = StaticUniversalMinHeap(5, 3, 1, capacity=5)
    assert h.peek() == 1


def test_universal_init_no_args_no_capacity_raises() -> None:
    with pytest.raises(TypeError):
        StaticUniversalMinHeap()


def test_universal_init_zero_capacity_raises() -> None:
    with pytest.raises(ValueError):
        StaticUniversalMinHeap(capacity=0)


def test_universal_init_too_many_args_raises() -> None:
    with pytest.raises(OverflowError):
        StaticUniversalMinHeap(1, 2, 3, capacity=2)


# ── Push ──────────────────────────────────────────────────────────────────────


def test_universal_push_smaller_becomes_root() -> None:
    h = StaticUniversalMinHeap(capacity=5)
    h.push(5)
    h.push(1)
    assert h.peek() == 1


def test_universal_push_full_raises() -> None:
    h = StaticUniversalMinHeap(1, 2, capacity=2)
    with pytest.raises(OverflowError):
        h.push(3)


def test_universal_push_mixed_types() -> None:
    h = StaticUniversalMinHeap(capacity=5)
    h.push(3)
    h.push(1)
    assert h.peek() == 1


# ── Pop ───────────────────────────────────────────────────────────────────────


def test_universal_pop_returns_minimum() -> None:
    h = StaticUniversalMinHeap(5, 3, 8, 1, capacity=5)
    assert h.pop() == 1


def test_universal_pop_sequence_sorted() -> None:
    h = StaticUniversalMinHeap(5, 3, 8, 1, 4, capacity=5)
    result = [h.pop() for _ in range(5)]
    assert result == sorted(result)


def test_universal_pop_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticUniversalMinHeap(capacity=3).pop()


def test_universal_pop_clears_slot() -> None:
    h = StaticUniversalMinHeap(1, 2, capacity=3)
    h.pop()
    assert h._data[1] is None


# ── Heapify ───────────────────────────────────────────────────────────────────


def test_universal_heapify_appends_to_existing() -> None:
    h = StaticUniversalMinHeap(capacity=10)
    h.push(1)
    h.heapify([5, 3])
    assert len(h) == 3
    assert h.peek() == 1


def test_universal_heapify_overflow_raises() -> None:
    h = StaticUniversalMinHeap(capacity=2)
    with pytest.raises(OverflowError):
        h.heapify([1, 2, 3])


# ── Ordered ───────────────────────────────────────────────────────────────────


def test_universal_ordered_yields_sorted() -> None:
    h = StaticUniversalMinHeap(5, 3, 8, 1, 4, capacity=5)
    assert list(h.ordered()) == [1, 3, 4, 5, 8]


def test_universal_ordered_does_not_modify() -> None:
    h = StaticUniversalMinHeap(3, 1, 2, capacity=5)
    list(h.ordered())
    assert len(h) == 3


# ── Clear / copy ──────────────────────────────────────────────────────────────


def test_universal_clear() -> None:
    h = StaticUniversalMinHeap(1, 2, 3, capacity=5)
    h.clear()
    assert h.is_empty()


def test_universal_copy_equal() -> None:
    h = StaticUniversalMinHeap(3, 1, 2, capacity=5)
    assert h.copy() == h


def test_universal_copy_independent() -> None:
    h = StaticUniversalMinHeap(1, 2, capacity=5)
    c = h.copy()
    c.push(0)
    assert len(h) == 2


# ── __contains__ / __eq__ / __repr__ ─────────────────────────────────────────


def test_universal_contains_existing() -> None:
    assert 3 in StaticUniversalMinHeap(1, 2, 3, capacity=5)


def test_universal_contains_missing() -> None:
    assert 99 not in StaticUniversalMinHeap(1, 2, 3, capacity=5)


def test_universal_eq_equal() -> None:
    a = StaticUniversalMinHeap(1, 2, 3, capacity=5)
    b = StaticUniversalMinHeap(1, 2, 3, capacity=5)
    assert a == b


def test_universal_eq_not_implemented() -> None:
    h = StaticUniversalMinHeap(1, capacity=3)
    assert h.__eq__([1]) is NotImplemented


def test_universal_repr_empty() -> None:
    h = StaticUniversalMinHeap(capacity=3)
    assert repr(h) == "StaticUniversalMinHeap(size=0, capacity=3)[]"
