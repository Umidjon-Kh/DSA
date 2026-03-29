import pytest

from data_structures.heaps import DynamicTypedMinHeap, DynamicUniversalMinHeap

# ══════════════════════════════════════════════════════════════════════════════
# DynamicTypedMinHeap
# ══════════════════════════════════════════════════════════════════════════════

# ── Init ──────────────────────────────────────────────────────────────────────


def test_typed_init_empty() -> None:
    h = DynamicTypedMinHeap(int)
    assert len(h) == 0
    assert h.is_empty()


def test_typed_init_with_args() -> None:
    h = DynamicTypedMinHeap(int, 5, 3, 1)
    assert h.peek() == 1
    assert len(h) == 3


def test_typed_init_wrong_type_raises() -> None:
    with pytest.raises(TypeError):
        DynamicTypedMinHeap(int, 1, "x")


# ── Push ──────────────────────────────────────────────────────────────────────


def test_typed_push_smaller_becomes_root() -> None:
    h = DynamicTypedMinHeap(int)
    h.push(5)
    h.push(1)
    assert h.peek() == 1


def test_typed_push_larger_does_not_change_root() -> None:
    h = DynamicTypedMinHeap(int)
    h.push(1)
    h.push(9)
    assert h.peek() == 1


def test_typed_push_grows_without_overflow() -> None:
    h = DynamicTypedMinHeap(int)
    for i in range(100):
        h.push(i)
    assert len(h) == 100
    assert h.peek() == 0


def test_typed_push_wrong_type_raises() -> None:
    h = DynamicTypedMinHeap(int)
    with pytest.raises(TypeError):
        h.push("x")


def test_typed_push_bool_rejected_for_int() -> None:
    h = DynamicTypedMinHeap(int)
    with pytest.raises(TypeError):
        h.push(True)


# ── Pop ───────────────────────────────────────────────────────────────────────


def test_typed_pop_returns_minimum() -> None:
    h = DynamicTypedMinHeap(int, 5, 3, 8, 1)
    assert h.pop() == 1


def test_typed_pop_reduces_size() -> None:
    h = DynamicTypedMinHeap(int, 1, 2)
    h.pop()
    assert len(h) == 1


def test_typed_pop_sequence_sorted() -> None:
    h = DynamicTypedMinHeap(int, 5, 3, 8, 1, 4)
    result = [h.pop() for _ in range(5)]
    assert result == sorted(result)


def test_typed_pop_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicTypedMinHeap(int).pop()


def test_typed_pop_single_element() -> None:
    h = DynamicTypedMinHeap(int)
    h.push(7)
    assert h.pop() == 7
    assert h.is_empty()


# ── Peek ──────────────────────────────────────────────────────────────────────


def test_typed_peek_does_not_remove() -> None:
    h = DynamicTypedMinHeap(int, 1, 2, 3)
    h.peek()
    assert len(h) == 3


def test_typed_peek_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicTypedMinHeap(int).peek()


# ── Heapify ───────────────────────────────────────────────────────────────────


def test_typed_heapify_sets_correct_root() -> None:
    h = DynamicTypedMinHeap(int)
    h.heapify([9, 4, 7, 2, 6])
    assert h.peek() == 2


def test_typed_heapify_appends_to_existing() -> None:
    h = DynamicTypedMinHeap(int)
    h.push(1)
    h.heapify([5, 3])
    assert len(h) == 3
    assert h.peek() == 1


def test_typed_heapify_wrong_type_raises() -> None:
    h = DynamicTypedMinHeap(int)
    with pytest.raises(TypeError):
        h.heapify([1, 2, "x"])


def test_typed_heapify_not_iterable_raises() -> None:
    h = DynamicTypedMinHeap(int)
    with pytest.raises(TypeError):
        h.heapify(123)  # type: ignore[arg-type]


# ── Ordered ───────────────────────────────────────────────────────────────────


def test_typed_ordered_yields_sorted() -> None:
    h = DynamicTypedMinHeap(int, 5, 3, 8, 1, 4)
    assert list(h.ordered()) == [1, 3, 4, 5, 8]


def test_typed_ordered_does_not_modify_heap() -> None:
    h = DynamicTypedMinHeap(int, 3, 1, 2)
    list(h.ordered())
    assert len(h) == 3
    assert h.peek() == 1


# ── Clear / copy ──────────────────────────────────────────────────────────────


def test_typed_clear_empties_heap() -> None:
    h = DynamicTypedMinHeap(int, 1, 2, 3)
    h.clear()
    assert h.is_empty()


def test_typed_copy_is_equal() -> None:
    h = DynamicTypedMinHeap(int, 3, 1, 2)
    assert h.copy() == h


def test_typed_copy_is_independent() -> None:
    h = DynamicTypedMinHeap(int, 1, 2)
    c = h.copy()
    c.push(0)
    assert len(h) == 2


def test_typed_copy_preserves_dtype() -> None:
    h = DynamicTypedMinHeap(float, 1.0)
    assert h.copy()._dtype is float


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_typed_iter_root_first() -> None:
    h = DynamicTypedMinHeap(int, 3, 1, 2)
    assert list(h)[0] == 1


def test_typed_iter_does_not_modify() -> None:
    h = DynamicTypedMinHeap(int, 1, 2, 3)
    list(h)
    assert len(h) == 3


def test_typed_reversed() -> None:
    h = DynamicTypedMinHeap(int, 3, 1, 2)
    fwd = list(h)
    rev = list(reversed(h))
    assert fwd == list(reversed(rev))


# ── __contains__ ──────────────────────────────────────────────────────────────


def test_typed_contains_existing() -> None:
    assert 3 in DynamicTypedMinHeap(int, 1, 2, 3)


def test_typed_contains_missing() -> None:
    assert 99 not in DynamicTypedMinHeap(int, 1, 2, 3)


def test_typed_contains_wrong_type_false() -> None:
    h = DynamicTypedMinHeap(int, 1)
    assert "x" not in h


# ── __eq__ / __repr__ ─────────────────────────────────────────────────────────


def test_typed_eq_equal() -> None:
    a = DynamicTypedMinHeap(int, 1, 2, 3)
    b = DynamicTypedMinHeap(int, 1, 2, 3)
    assert a == b


def test_typed_eq_not_implemented() -> None:
    h = DynamicTypedMinHeap(int, 1)
    assert h.__eq__([1]) is NotImplemented


def test_typed_repr_empty() -> None:
    h = DynamicTypedMinHeap(int)
    assert repr(h) == "DynamicTypedMinHeap(int, size=0)[]"


# ══════════════════════════════════════════════════════════════════════════════
# DynamicUniversalMinHeap
# ══════════════════════════════════════════════════════════════════════════════

# ── Init ──────────────────────────────────────────────────────────────────────


def test_universal_init_empty() -> None:
    h = DynamicUniversalMinHeap()
    assert h.is_empty()


def test_universal_init_with_args() -> None:
    h = DynamicUniversalMinHeap(5, 3, 1)
    assert h.peek() == 1


# ── Push ──────────────────────────────────────────────────────────────────────


def test_universal_push_smaller_becomes_root() -> None:
    h = DynamicUniversalMinHeap()
    h.push(5)
    h.push(1)
    assert h.peek() == 1


def test_universal_push_grows_without_limit() -> None:
    h = DynamicUniversalMinHeap()
    for i in range(100):
        h.push(i)
    assert len(h) == 100
    assert h.peek() == 0


# ── Pop ───────────────────────────────────────────────────────────────────────


def test_universal_pop_returns_minimum() -> None:
    h = DynamicUniversalMinHeap(5, 3, 8, 1)
    assert h.pop() == 1


def test_universal_pop_sequence_sorted() -> None:
    h = DynamicUniversalMinHeap(5, 3, 8, 1, 4)
    result = [h.pop() for _ in range(5)]
    assert result == sorted(result)


def test_universal_pop_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicUniversalMinHeap().pop()


def test_universal_pop_single_element() -> None:
    h = DynamicUniversalMinHeap()
    h.push(7)
    assert h.pop() == 7
    assert h.is_empty()


# ── Heapify ───────────────────────────────────────────────────────────────────


def test_universal_heapify_correct_root() -> None:
    h = DynamicUniversalMinHeap()
    h.heapify([9, 4, 7, 2, 6])
    assert h.peek() == 2


def test_universal_heapify_appends_to_existing() -> None:
    h = DynamicUniversalMinHeap()
    h.push(1)
    h.heapify([5, 3])
    assert len(h) == 3
    assert h.peek() == 1


def test_universal_heapify_not_iterable_raises() -> None:
    with pytest.raises(TypeError):
        DynamicUniversalMinHeap().heapify(42)  # type: ignore[arg-type]


# ── Ordered ───────────────────────────────────────────────────────────────────


def test_universal_ordered_sorted() -> None:
    h = DynamicUniversalMinHeap(5, 3, 8, 1, 4)
    assert list(h.ordered()) == [1, 3, 4, 5, 8]


def test_universal_ordered_does_not_modify() -> None:
    h = DynamicUniversalMinHeap(3, 1, 2)
    list(h.ordered())
    assert len(h) == 3


# ── Clear / copy ──────────────────────────────────────────────────────────────


def test_universal_clear() -> None:
    h = DynamicUniversalMinHeap(1, 2, 3)
    h.clear()
    assert h.is_empty()


def test_universal_copy_equal() -> None:
    h = DynamicUniversalMinHeap(3, 1, 2)
    assert h.copy() == h


def test_universal_copy_independent() -> None:
    h = DynamicUniversalMinHeap(1, 2)
    c = h.copy()
    c.push(0)
    assert len(h) == 2


# ── __contains__ / __eq__ / __repr__ ─────────────────────────────────────────


def test_universal_contains_existing() -> None:
    assert 3 in DynamicUniversalMinHeap(1, 2, 3)


def test_universal_contains_missing() -> None:
    assert 99 not in DynamicUniversalMinHeap(1, 2, 3)


def test_universal_eq_equal() -> None:
    a = DynamicUniversalMinHeap(1, 2, 3)
    b = DynamicUniversalMinHeap(1, 2, 3)
    assert a == b


def test_universal_eq_not_implemented() -> None:
    h = DynamicUniversalMinHeap(1)
    assert h.__eq__([1]) is NotImplemented


def test_universal_repr_empty() -> None:
    h = DynamicUniversalMinHeap()
    assert repr(h) == "DynamicUniversalMinHeap(size=0)[]"
