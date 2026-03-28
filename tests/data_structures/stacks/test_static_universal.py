import pytest

from data_structures import StaticUniversalStack

# ── Init ──────────────────────────────────────────────────────────────────────


def test_init_capacity_only() -> None:
    s = StaticUniversalStack(capacity=5)
    assert len(s) == 0
    assert s._top == 0


def test_init_with_args() -> None:
    s = StaticUniversalStack(1, 2, 3, capacity=5)
    assert len(s) == 3
    assert s.peek() == 3


def test_init_args_infer_capacity() -> None:
    s = StaticUniversalStack(1, 2, 3)
    assert len(s) == 3
    assert len(s._data) == 3


def test_init_no_args_no_capacity_raises() -> None:
    with pytest.raises(TypeError):
        StaticUniversalStack()


def test_init_too_many_args_raises() -> None:
    with pytest.raises(OverflowError):
        StaticUniversalStack(1, 2, 3, capacity=2)


def test_init_invalid_capacity_type_raises() -> None:
    with pytest.raises(TypeError):
        StaticUniversalStack(capacity="5") # type: ignore[union-attr]


def test_init_zero_capacity_raises() -> None:
    with pytest.raises(ValueError):
        StaticUniversalStack(capacity=0)


# ── Push ──────────────────────────────────────────────────────────────────────


def test_push_any_type() -> None:
    s = StaticUniversalStack(capacity=5)
    s.push(1)
    s.push("hi")
    s.push(3.0)
    assert s.peek() == 3.0
    assert len(s) == 3


def test_push_when_full_raises() -> None:
    s = StaticUniversalStack(1, 2, capacity=2)
    with pytest.raises(OverflowError):
        s.push(3)


def test_push_increments_top() -> None:
    s = StaticUniversalStack(capacity=3)
    s.push(10)
    assert s._top == 1


# ── Pop ───────────────────────────────────────────────────────────────────────


def test_pop_returns_top() -> None:
    s = StaticUniversalStack(1, 2, 3, capacity=5)
    assert s.pop() == 3


def test_pop_clears_slot() -> None:
    s = StaticUniversalStack(1, 2, capacity=3)
    s.pop()
    assert s._data[1] is None


def test_pop_decrements_top() -> None:
    s = StaticUniversalStack(1, 2, 3, capacity=5)
    s.pop()
    assert s._top == 2


def test_pop_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticUniversalStack(capacity=3).pop()


# ── Peek ──────────────────────────────────────────────────────────────────────


def test_peek_returns_top_without_removing() -> None:
    s = StaticUniversalStack(1, 2, 3, capacity=5)
    assert s.peek() == 3
    assert len(s) == 3


def test_peek_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticUniversalStack(capacity=3).peek()


# ── clear / copy ──────────────────────────────────────────────────────────────


def test_clear_resets_top() -> None:
    s = StaticUniversalStack(1, 2, 3, capacity=5)
    s.clear()
    assert s._top == 0
    assert len(s) == 0


def test_copy_preserves_elements_and_capacity() -> None:
    s = StaticUniversalStack(1, 2, 3, capacity=5)
    c = s.copy()
    assert list(c) == list(s)
    assert len(c._data) == len(s._data)


def test_copy_is_independent() -> None:
    s = StaticUniversalStack(1, 2, capacity=5)
    c = s.copy()
    c.push(99)
    assert len(s) == 2
    assert len(c) == 3


# ── is_empty / is_full / __bool__ / __len__ ───────────────────────────────────


def test_is_empty_true() -> None:
    assert StaticUniversalStack(capacity=3).is_empty()


def test_is_empty_false() -> None:
    assert not StaticUniversalStack(1, capacity=3).is_empty()


def test_is_full_true() -> None:
    s = StaticUniversalStack(1, 2, 3, capacity=3)
    assert s.is_full()


def test_is_full_false() -> None:
    assert not StaticUniversalStack(1, capacity=3).is_full()


def test_bool_empty() -> None:
    assert not bool(StaticUniversalStack(capacity=3))


def test_bool_not_empty() -> None:
    assert bool(StaticUniversalStack(1, capacity=3))


def test_len_returns_top() -> None:
    s = StaticUniversalStack(1, 2, 3, capacity=5)
    assert len(s) == 3


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_iter_top_to_bottom() -> None:
    s = StaticUniversalStack(1, 2, 3, capacity=5)
    assert list(s) == [3, 2, 1]


def test_iter_empty() -> None:
    assert list(StaticUniversalStack(capacity=3)) == []


def test_reversed_bottom_to_top() -> None:
    s = StaticUniversalStack(1, 2, 3, capacity=5)
    assert list(reversed(s)) == [1, 2, 3]


def test_iter_does_not_modify() -> None:
    s = StaticUniversalStack(1, 2, 3, capacity=5)
    _ = list(s)
    assert len(s) == 3


# ── __contains__ ──────────────────────────────────────────────────────────────


def test_contains_existing() -> None:
    s = StaticUniversalStack(1, 2, 3, capacity=5)
    assert 2 in s


def test_contains_missing() -> None:
    assert 99 not in StaticUniversalStack(1, 2, 3, capacity=5)


def test_contains_empty_slot_not_accessible() -> None:
    s = StaticUniversalStack(1, capacity=5)
    # slot 1..4 are None but are above _top — should not be found
    assert None not in s


# ── __eq__ ────────────────────────────────────────────────────────────────────


def test_eq_equal() -> None:
    a = StaticUniversalStack(1, 2, 3, capacity=5)
    b = StaticUniversalStack(1, 2, 3, capacity=5)
    assert a == b


def test_eq_same_elements_different_capacity() -> None:
    a = StaticUniversalStack(1, 2, 3, capacity=3)
    b = StaticUniversalStack(1, 2, 3, capacity=5)
    assert a == b  # eq checks only up to _top


def test_eq_different_elements() -> None:
    a = StaticUniversalStack(1, 2, 3, capacity=5)
    b = StaticUniversalStack(1, 2, 9, capacity=5)
    assert a != b


def test_eq_different_sizes() -> None:
    a = StaticUniversalStack(1, 2, capacity=5)
    b = StaticUniversalStack(1, 2, 3, capacity=5)
    assert a != b


def test_eq_not_implemented_for_other_type() -> None:
    s = StaticUniversalStack(1, capacity=3)
    assert s.__eq__([1]) is NotImplemented


# ── __repr__ ──────────────────────────────────────────────────────────────────


def test_repr_empty() -> None:
    s = StaticUniversalStack(capacity=3)
    assert repr(s) == "StaticUniversalStack(size=0, capacity=3)[]"


def test_repr_partial() -> None:
    s = StaticUniversalStack(1, 2, capacity=5)
    assert repr(s) == "StaticUniversalStack(size=2, capacity=5)[2, 1]"


def test_repr_full() -> None:
    s = StaticUniversalStack(1, 2, 3, capacity=3)
    assert repr(s) == "StaticUniversalStack(size=3, capacity=3)[3, 2, 1]"
