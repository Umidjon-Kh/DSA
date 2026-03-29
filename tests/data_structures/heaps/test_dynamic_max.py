import pytest

from data_structures.heaps import DynamicTypedMaxHeap, DynamicUniversalMaxHeap

# ══════════════════════════════════════════════════════════════════════════════
# DynamicTypedMaxHeap
# ══════════════════════════════════════════════════════════════════════════════

# ── Init ──────────────────────────────────────────────────────────────────────


def test_typed_init_empty() -> None:
    h = DynamicTypedMaxHeap(int)
    assert len(h) == 0
    assert h.is_empty()


def test_typed_init_with_args() -> None:
    h = DynamicTypedMaxHeap(int, 1, 3, 5)
    assert h.peek() == 5
    assert len(h) == 3


def test_typed_init_wrong_type_raises() -> None:
    with pytest.raises(TypeError):
        DynamicTypedMaxHeap(int, 1, "x")


# ── Push ──────────────────────────────────────────────────────────────────────


def test_typed_push_larger_becomes_root() -> None:
    h = DynamicTypedMaxHeap(int)
    h.push(3)
    h.push(9)
    assert h.peek() == 9


def test_typed_push_smaller_does_not_change_root() -> None:
    h = DynamicTypedMaxHeap(int)
    h.push(9)
    h.push(1)
    assert h.peek() == 9


def test_typed_push_grows_without_overflow() -> None:
    h = DynamicTypedMaxHeap(int)
    for i in range(100):
        h.push(i)
    assert len(h) == 100
    assert h.peek() == 99


def test_typed_push_wrong_type_raises() -> None:
    h = DynamicTypedMaxHeap(int)
    with pytest.raises(TypeError):
        h.push("x")


def test_typed_push_bool_rejected_for_int() -> None:
    h = DynamicTypedMaxHeap(int)
    with pytest.raises(TypeError):
        h.push(True)


# ── Pop ───────────────────────────────────────────────────────────────────────


def test_typed_pop_returns_maximum() -> None:
    h = DynamicTypedMaxHeap(int, 5, 3, 8, 1)
    assert h.pop() == 8


def test_typed_pop_reduces_size() -> None:
    h = DynamicTypedMaxHeap(int, 1, 2)
    h.pop()
    assert len(h) == 1


def test_typed_pop_sequence_reverse_sorted() -> None:
    h = DynamicTypedMaxHeap(int, 5, 3, 8, 1, 4)
    result = [h.pop() for _ in range(5)]
    assert result == sorted(result, reverse=True)


def test_typed_pop_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicTypedMaxHeap(int).pop()


def test_typed_pop_single_element() -> None:
    h = DynamicTypedMaxHeap(int)
    h.push(7)
    assert h.pop() == 7
    assert h.is_empty()


# ── Peek ──────────────────────────────────────────────────────────────────────


def test_typed_peek_does_not_remove() -> None:
    h = DynamicTypedMaxHeap(int, 1, 2, 3)
    h.peek()
    assert len(h) == 3


def test_typed_peek_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicTypedMaxHeap(int).peek()


# ── Heapify ───────────────────────────────────────────────────────────────────


def test_typed_heapify_sets_correct_root() -> None:
    h = DynamicTypedMaxHeap(int)
    h.heapify([9, 4, 7, 2, 6])
    assert h.peek() == 9


def test_typed_heapify_appends_to_existing() -> None:
    h = DynamicTypedMaxHeap(int)
    h.push(10)
    h.heapify([5, 3])
    assert len(h) == 3
    assert h.peek() == 10


def test_typed_heapify_wrong_type_raises() -> None:
    h = DynamicTypedMaxHeap(int)
    with pytest.raises(TypeError):
        h.heapify([1, 2, "x"])


def test_typed_heapify_not_iterable_raises() -> None:
    h = DynamicTypedMaxHeap(int)
    with pytest.raises(TypeError):
        h.heapify(123)  # type: ignore[arg-type]


# ── Ordered ───────────────────────────────────────────────────────────────────


def test_typed_ordered_yields_reverse_sorted() -> None:
    h = DynamicTypedMaxHeap(int, 5, 3, 8, 1, 4)
    assert list(h.ordered()) == [8, 5, 4, 3, 1]


def test_typed_ordered_does_not_modify_heap() -> None:
    h = DynamicTypedMaxHeap(int, 3, 1, 2)
    list(h.ordered())
    assert len(h) == 3
    assert h.peek() == 3


# ── Clear / copy ──────────────────────────────────────────────────────────────


def test_typed_clear_empties_heap() -> None:
    h = DynamicTypedMaxHeap(int, 1, 2, 3)
    h.clear()
    assert h.is_empty()


def test_typed_copy_is_equal() -> None:
    h = DynamicTypedMaxHeap(int, 3, 1, 2)
    assert h.copy() == h


def test_typed_copy_is_independent() -> None:
    h = DynamicTypedMaxHeap(int, 1, 2)
    c = h.copy()
    c.push(99)
    assert len(h) == 2


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_typed_iter_root_first() -> None:
    h = DynamicTypedMaxHeap(int, 3, 1, 5)
    assert list(h)[0] == 5


def test_typed_iter_does_not_modify() -> None:
    h = DynamicTypedMaxHeap(int, 1, 2, 3)
    list(h)
    assert len(h) == 3


# ── __contains__ / __eq__ / __repr__ ─────────────────────────────────────────


def test_typed_contains_existing() -> None:
    assert 8 in DynamicTypedMaxHeap(int, 5, 3, 8)


def test_typed_contains_missing() -> None:
    assert 99 not in DynamicTypedMaxHeap(int, 1, 2, 3)


def test_typed_contains_wrong_type_false() -> None:
    assert "x" not in DynamicTypedMaxHeap(int, 1)


def test_typed_eq_equal() -> None:
    a = DynamicTypedMaxHeap(int, 1, 2, 3)
    b = DynamicTypedMaxHeap(int, 1, 2, 3)
    assert a == b


def test_typed_eq_not_implemented() -> None:
    h = DynamicTypedMaxHeap(int, 1)
    assert h.__eq__([1]) is NotImplemented


def test_typed_repr_empty() -> None:
    h = DynamicTypedMaxHeap(int)
    assert repr(h) == "DynamicTypedMaxHeap(int, size=0)[]"


# ══════════════════════════════════════════════════════════════════════════════
# DynamicUniversalMaxHeap
# ══════════════════════════════════════════════════════════════════════════════

# ── Init ──────────────────────────────────────────────────────────────────────


def test_universal_init_empty() -> None:
    h = DynamicUniversalMaxHeap()
    assert h.is_empty()


def test_universal_init_with_args() -> None:
    h = DynamicUniversalMaxHeap(1, 3, 5)
    assert h.peek() == 5


# ── Push ──────────────────────────────────────────────────────────────────────


def test_universal_push_larger_becomes_root() -> None:
    h = DynamicUniversalMaxHeap()
    h.push(3)
    h.push(9)
    assert h.peek() == 9


def test_universal_push_grows_without_limit() -> None:
    h = DynamicUniversalMaxHeap()
    for i in range(100):
        h.push(i)
    assert h.peek() == 99


# ── Pop ───────────────────────────────────────────────────────────────────────


def test_universal_pop_returns_maximum() -> None:
    h = DynamicUniversalMaxHeap(5, 3, 8, 1)
    assert h.pop() == 8


def test_universal_pop_sequence_reverse_sorted() -> None:
    h = DynamicUniversalMaxHeap(5, 3, 8, 1, 4)
    result = [h.pop() for _ in range(5)]
    assert result == sorted(result, reverse=True)


def test_universal_pop_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicUniversalMaxHeap().pop()


def test_universal_pop_single_element() -> None:
    h = DynamicUniversalMaxHeap()
    h.push(7)
    assert h.pop() == 7
    assert h.is_empty()


# ── Heapify ───────────────────────────────────────────────────────────────────


def test_universal_heapify_correct_root() -> None:
    h = DynamicUniversalMaxHeap()
    h.heapify([1, 4, 7, 9, 2])
    assert h.peek() == 9


def test_universal_heapify_appends_to_existing() -> None:
    h = DynamicUniversalMaxHeap()
    h.push(10)
    h.heapify([5, 3])
    assert len(h) == 3
    assert h.peek() == 10


def test_universal_heapify_not_iterable_raises() -> None:
    with pytest.raises(TypeError):
        DynamicUniversalMaxHeap().heapify(42)  # type: ignore[arg-type]


# ── Ordered ───────────────────────────────────────────────────────────────────


def test_universal_ordered_reverse_sorted() -> None:
    h = DynamicUniversalMaxHeap(5, 3, 8, 1, 4)
    assert list(h.ordered()) == [8, 5, 4, 3, 1]


def test_universal_ordered_does_not_modify() -> None:
    h = DynamicUniversalMaxHeap(3, 1, 2)
    list(h.ordered())
    assert len(h) == 3


# ── Clear / copy ──────────────────────────────────────────────────────────────


def test_universal_clear() -> None:
    h = DynamicUniversalMaxHeap(1, 2, 3)
    h.clear()
    assert h.is_empty()


def test_universal_copy_equal() -> None:
    h = DynamicUniversalMaxHeap(3, 1, 2)
    assert h.copy() == h


def test_universal_copy_independent() -> None:
    h = DynamicUniversalMaxHeap(1, 2)
    c = h.copy()
    c.push(99)
    assert len(h) == 2


# ── __contains__ / __eq__ / __repr__ ─────────────────────────────────────────


def test_universal_contains_existing() -> None:
    assert 8 in DynamicUniversalMaxHeap(5, 3, 8)


def test_universal_contains_missing() -> None:
    assert 99 not in DynamicUniversalMaxHeap(1, 2, 3)


def test_universal_eq_equal() -> None:
    a = DynamicUniversalMaxHeap(1, 2, 3)
    b = DynamicUniversalMaxHeap(1, 2, 3)
    assert a == b


def test_universal_eq_not_implemented() -> None:
    h = DynamicUniversalMaxHeap(1)
    assert h.__eq__([1]) is NotImplemented


def test_universal_repr_empty() -> None:
    h = DynamicUniversalMaxHeap()
    assert repr(h) == "DynamicUniversalMaxHeap(size=0)[]"
