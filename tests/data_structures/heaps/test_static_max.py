import pytest

from data_structures.heaps import StaticTypedMaxHeap, StaticUniversalMaxHeap

# ══════════════════════════════════════════════════════════════════════════════
# StaticTypedMaxHeap
# ══════════════════════════════════════════════════════════════════════════════

# ── Init ──────────────────────────────────────────────────────────────────────


def test_typed_init_empty() -> None:
    h = StaticTypedMaxHeap(int, capacity=5)
    assert len(h) == 0
    assert h.is_empty()


def test_typed_init_with_args() -> None:
    h = StaticTypedMaxHeap(int, 1, 3, 5, capacity=5)
    assert h.peek() == 5


def test_typed_init_no_capacity_no_args_raises() -> None:
    with pytest.raises(TypeError):
        StaticTypedMaxHeap(int)


def test_typed_init_zero_capacity_raises() -> None:
    with pytest.raises(ValueError):
        StaticTypedMaxHeap(int, capacity=0)


def test_typed_init_too_many_args_raises() -> None:
    with pytest.raises(OverflowError):
        StaticTypedMaxHeap(int, 1, 2, 3, capacity=2)


def test_typed_init_wrong_type_raises() -> None:
    with pytest.raises(TypeError):
        StaticTypedMaxHeap(int, 1, "x", capacity=5)


# ── Push ──────────────────────────────────────────────────────────────────────


def test_typed_push_larger_becomes_root() -> None:
    h = StaticTypedMaxHeap(int, capacity=5)
    h.push(3)
    h.push(9)
    assert h.peek() == 9


def test_typed_push_smaller_does_not_change_root() -> None:
    h = StaticTypedMaxHeap(int, capacity=5)
    h.push(9)
    h.push(1)
    assert h.peek() == 9


def test_typed_push_equal_values() -> None:
    h = StaticTypedMaxHeap(int, capacity=5)
    h.push(5)
    h.push(5)
    assert h.peek() == 5
    assert len(h) == 2


def test_typed_push_full_raises() -> None:
    h = StaticTypedMaxHeap(int, 1, 2, capacity=2)
    with pytest.raises(OverflowError):
        h.push(3)


def test_typed_push_wrong_type_raises() -> None:
    h = StaticTypedMaxHeap(int, capacity=5)
    with pytest.raises(TypeError):
        h.push("x")


def test_typed_push_bool_rejected_for_int() -> None:
    h = StaticTypedMaxHeap(int, capacity=5)
    with pytest.raises(TypeError):
        h.push(True)


# ── Pop ───────────────────────────────────────────────────────────────────────


def test_typed_pop_returns_maximum() -> None:
    h = StaticTypedMaxHeap(int, 5, 3, 8, 1, capacity=5)
    assert h.pop() == 8


def test_typed_pop_reduces_size() -> None:
    h = StaticTypedMaxHeap(int, 1, 2, capacity=3)
    h.pop()
    assert len(h) == 1


def test_typed_pop_sequence_reverse_sorted() -> None:
    h = StaticTypedMaxHeap(int, 5, 3, 8, 1, 4, capacity=5)
    result = [h.pop() for _ in range(5)]
    assert result == sorted(result, reverse=True)


def test_typed_pop_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticTypedMaxHeap(int, capacity=3).pop()


def test_typed_pop_single_element() -> None:
    h = StaticTypedMaxHeap(int, capacity=1)
    h.push(7)
    assert h.pop() == 7
    assert h.is_empty()


# ── Peek ──────────────────────────────────────────────────────────────────────


def test_typed_peek_does_not_remove() -> None:
    h = StaticTypedMaxHeap(int, 1, 2, 3, capacity=5)
    h.peek()
    assert len(h) == 3


def test_typed_peek_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticTypedMaxHeap(int, capacity=3).peek()


def test_typed_peek_always_maximum() -> None:
    h = StaticTypedMaxHeap(int, capacity=10)
    for v in [9, 4, 7, 2, 6]:
        h.push(v)
    assert h.peek() == 9


# ── Heapify ───────────────────────────────────────────────────────────────────


def test_typed_heapify_sets_correct_root() -> None:
    h = StaticTypedMaxHeap(int, capacity=10)
    h.heapify([9, 4, 7, 2, 6])
    assert h.peek() == 9


def test_typed_heapify_appends_to_existing() -> None:
    h = StaticTypedMaxHeap(int, capacity=10)
    h.push(10)
    h.heapify([5, 3])
    assert len(h) == 3
    assert h.peek() == 10


def test_typed_heapify_overflow_raises() -> None:
    h = StaticTypedMaxHeap(int, capacity=3)
    with pytest.raises(OverflowError):
        h.heapify([1, 2, 3, 4])


def test_typed_heapify_wrong_type_raises() -> None:
    h = StaticTypedMaxHeap(int, capacity=5)
    with pytest.raises(TypeError):
        h.heapify([1, 2, "x"])


def test_typed_heapify_not_iterable_raises() -> None:
    h = StaticTypedMaxHeap(int, capacity=5)
    with pytest.raises(TypeError):
        h.heapify(123)  # type: ignore[arg-type]


# ── Ordered ───────────────────────────────────────────────────────────────────


def test_typed_ordered_yields_reverse_sorted() -> None:
    h = StaticTypedMaxHeap(int, 5, 3, 8, 1, 4, capacity=5)
    assert list(h.ordered()) == [8, 5, 4, 3, 1]


def test_typed_ordered_does_not_modify_heap() -> None:
    h = StaticTypedMaxHeap(int, 3, 1, 2, capacity=5)
    list(h.ordered())
    assert len(h) == 3
    assert h.peek() == 3


# ── Clear / copy ──────────────────────────────────────────────────────────────


def test_typed_clear_empties_heap() -> None:
    h = StaticTypedMaxHeap(int, 1, 2, 3, capacity=5)
    h.clear()
    assert h.is_empty()


def test_typed_copy_is_equal() -> None:
    h = StaticTypedMaxHeap(int, 3, 1, 2, capacity=5)
    assert h.copy() == h


def test_typed_copy_is_independent() -> None:
    h = StaticTypedMaxHeap(int, 1, 2, capacity=5)
    c = h.copy()
    c.push(99)
    assert len(h) == 2


# ── is_empty / is_full ────────────────────────────────────────────────────────


def test_typed_is_full_true() -> None:
    assert StaticTypedMaxHeap(int, 1, 2, 3, capacity=3).is_full()


def test_typed_is_full_false() -> None:
    assert not StaticTypedMaxHeap(int, 1, capacity=3).is_full()


# ── __contains__ / __eq__ / __repr__ ─────────────────────────────────────────


def test_typed_contains_existing() -> None:
    assert 8 in StaticTypedMaxHeap(int, 5, 3, 8, capacity=5)


def test_typed_contains_missing() -> None:
    assert 99 not in StaticTypedMaxHeap(int, 1, 2, 3, capacity=5)


def test_typed_contains_wrong_type_false() -> None:
    h = StaticTypedMaxHeap(int, 1, capacity=3)
    assert "x" not in h


def test_typed_eq_equal() -> None:
    a = StaticTypedMaxHeap(int, 1, 2, 3, capacity=5)
    b = StaticTypedMaxHeap(int, 1, 2, 3, capacity=5)
    assert a == b


def test_typed_eq_not_implemented_for_other_type() -> None:
    h = StaticTypedMaxHeap(int, 1, capacity=3)
    assert h.__eq__([1]) is NotImplemented


def test_typed_repr_empty() -> None:
    h = StaticTypedMaxHeap(int, capacity=3)
    assert repr(h) == "StaticTypedMaxHeap(int, size=0, capacity=3)[]"


# ══════════════════════════════════════════════════════════════════════════════
# StaticUniversalMaxHeap
# ══════════════════════════════════════════════════════════════════════════════

# ── Init ──────────────────────────────────────────────────────────────────────


def test_universal_init_empty() -> None:
    h = StaticUniversalMaxHeap(capacity=5)
    assert h.is_empty()


def test_universal_init_with_args() -> None:
    h = StaticUniversalMaxHeap(1, 3, 5, capacity=5)
    assert h.peek() == 5


def test_universal_init_no_args_no_capacity_raises() -> None:
    with pytest.raises(TypeError):
        StaticUniversalMaxHeap()


def test_universal_init_too_many_args_raises() -> None:
    with pytest.raises(OverflowError):
        StaticUniversalMaxHeap(1, 2, 3, capacity=2)


# ── Push ──────────────────────────────────────────────────────────────────────


def test_universal_push_larger_becomes_root() -> None:
    h = StaticUniversalMaxHeap(capacity=5)
    h.push(3)
    h.push(9)
    assert h.peek() == 9


def test_universal_push_full_raises() -> None:
    h = StaticUniversalMaxHeap(1, 2, capacity=2)
    with pytest.raises(OverflowError):
        h.push(3)


# ── Pop ───────────────────────────────────────────────────────────────────────


def test_universal_pop_returns_maximum() -> None:
    h = StaticUniversalMaxHeap(5, 3, 8, 1, capacity=5)
    assert h.pop() == 8


def test_universal_pop_sequence_reverse_sorted() -> None:
    h = StaticUniversalMaxHeap(5, 3, 8, 1, 4, capacity=5)
    result = [h.pop() for _ in range(5)]
    assert result == sorted(result, reverse=True)


def test_universal_pop_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticUniversalMaxHeap(capacity=3).pop()


def test_universal_pop_clears_slot() -> None:
    h = StaticUniversalMaxHeap(1, 2, capacity=3)
    h.pop()
    assert h._data[1] is None


# ── Heapify ───────────────────────────────────────────────────────────────────


def test_universal_heapify_appends_to_existing() -> None:
    h = StaticUniversalMaxHeap(capacity=10)
    h.push(10)
    h.heapify([5, 3])
    assert len(h) == 3
    assert h.peek() == 10


def test_universal_heapify_overflow_raises() -> None:
    h = StaticUniversalMaxHeap(capacity=2)
    with pytest.raises(OverflowError):
        h.heapify([1, 2, 3])


# ── Ordered ───────────────────────────────────────────────────────────────────


def test_universal_ordered_yields_reverse_sorted() -> None:
    h = StaticUniversalMaxHeap(5, 3, 8, 1, 4, capacity=5)
    assert list(h.ordered()) == [8, 5, 4, 3, 1]


def test_universal_ordered_does_not_modify() -> None:
    h = StaticUniversalMaxHeap(3, 1, 2, capacity=5)
    list(h.ordered())
    assert len(h) == 3


# ── Clear / copy ──────────────────────────────────────────────────────────────


def test_universal_clear() -> None:
    h = StaticUniversalMaxHeap(1, 2, 3, capacity=5)
    h.clear()
    assert h.is_empty()


def test_universal_copy_equal() -> None:
    h = StaticUniversalMaxHeap(3, 1, 2, capacity=5)
    assert h.copy() == h


def test_universal_copy_independent() -> None:
    h = StaticUniversalMaxHeap(1, 2, capacity=5)
    c = h.copy()
    c.push(99)
    assert len(h) == 2


# ── __contains__ / __eq__ / __repr__ ─────────────────────────────────────────


def test_universal_contains_existing() -> None:
    assert 8 in StaticUniversalMaxHeap(5, 3, 8, capacity=5)


def test_universal_contains_missing() -> None:
    assert 99 not in StaticUniversalMaxHeap(1, 2, 3, capacity=5)


def test_universal_eq_equal() -> None:
    a = StaticUniversalMaxHeap(1, 2, 3, capacity=5)
    b = StaticUniversalMaxHeap(1, 2, 3, capacity=5)
    assert a == b


def test_universal_eq_not_implemented() -> None:
    h = StaticUniversalMaxHeap(1, capacity=3)
    assert h.__eq__([1]) is NotImplemented


def test_universal_repr_empty() -> None:
    h = StaticUniversalMaxHeap(capacity=3)
    assert repr(h) == "StaticUniversalMaxHeap(size=0, capacity=3)[]"
