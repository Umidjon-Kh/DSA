import pytest

from data_structures import StaticUniversalMinStack

# ── Init ──────────────────────────────────────────────────────────────────────


def test_init_capacity_only() -> None:
    s = StaticUniversalMinStack(capacity=5)
    assert len(s) == 0
    assert s._top == 0
    assert s._min_top == 0


def test_init_default_key_is_identity() -> None:
    s = StaticUniversalMinStack(capacity=5)
    assert s._key(10) == 10


def test_init_custom_key_stored() -> None:
    s = StaticUniversalMinStack(capacity=5, key=lambda x: -x)
    assert s._key(5) == -5


def test_init_non_callable_key_raises() -> None:
    with pytest.raises(TypeError):
        StaticUniversalMinStack(capacity=5, key=42)  # type: ignore[arg-type]


def test_init_with_args() -> None:
    s = StaticUniversalMinStack(3, 1, 2, capacity=5)
    assert len(s) == 3
    assert s.peek() == 2


def test_init_with_args_sets_min() -> None:
    s = StaticUniversalMinStack(3, 1, 2, capacity=5)
    assert s.min() == 1


def test_init_no_args_no_capacity_raises() -> None:
    with pytest.raises(TypeError):
        StaticUniversalMinStack()


def test_init_too_many_args_raises() -> None:
    with pytest.raises(OverflowError):
        StaticUniversalMinStack(1, 2, 3, capacity=2)


def test_init_zero_capacity_raises() -> None:
    with pytest.raises(ValueError):
        StaticUniversalMinStack(capacity=0)


# ── Push ──────────────────────────────────────────────────────────────────────


def test_push_first_enters_min() -> None:
    s = StaticUniversalMinStack(capacity=5)
    s.push(5)
    assert s._min_top == 1
    assert s._min_data[0] == 5


def test_push_lower_enters_min() -> None:
    # BUG: push() reads self._min_data[self._min_top] instead of [self._min_top - 1].
    # For StaticUniversalArray, that uninitialized slot is None, causing a TypeError
    # on comparison. This test will FAIL until the off-by-one bug is fixed.
    s = StaticUniversalMinStack(capacity=5)
    s.push(5)
    s.push(3)
    assert s.min() == 3
    assert s._min_top == 2


def test_push_higher_does_not_enter_min() -> None:
    s = StaticUniversalMinStack(capacity=5)
    s.push(3)
    s.push(5)
    assert s.min() == 3
    assert s._min_top == 1


def test_push_equal_enters_min() -> None:
    s = StaticUniversalMinStack(capacity=5)
    s.push(3)
    s.push(3)
    assert s.min() == 3
    assert s._min_top == 2


def test_push_when_full_raises() -> None:
    s = StaticUniversalMinStack(1, 2, capacity=2)
    with pytest.raises(OverflowError):
        s.push(3)


def test_push_with_key() -> None:
    s = StaticUniversalMinStack(capacity=5, key=lambda x: -x)
    s.push(3)
    s.push(7)
    s.push(1)
    assert s.min() == 7


# ── Pop ───────────────────────────────────────────────────────────────────────


def test_pop_returns_top() -> None:
    s = StaticUniversalMinStack(1, 2, 3, capacity=5)
    assert s.pop() == 3


def test_pop_non_min_leaves_min_intact() -> None:
    s = StaticUniversalMinStack(3, 1, 2, capacity=5)
    s.pop()  # 2
    assert s.min() == 1


def test_pop_min_updates_min() -> None:
    s = StaticUniversalMinStack(3, 1, 2, capacity=5)
    s.pop()  # 2
    s.pop()  # 1
    assert s.min() == 3


def test_pop_duplicate_min_removes_one() -> None:
    s = StaticUniversalMinStack(1, 1, capacity=5)
    s.pop()
    assert s.min() == 1
    assert s._min_top == 1


def test_pop_clears_main_slot() -> None:
    s = StaticUniversalMinStack(1, 2, capacity=3)
    s.pop()
    assert s._data[1] is None


def test_pop_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticUniversalMinStack(capacity=3).pop()


def test_pop_all_drains_min() -> None:
    s = StaticUniversalMinStack(1, 2, 3, capacity=5)
    s.pop()
    s.pop()
    s.pop()
    assert s._min_top == 0


# ── Peek / min ────────────────────────────────────────────────────────────────


def test_peek_returns_top_without_removing() -> None:
    s = StaticUniversalMinStack(1, 2, 3, capacity=5)
    assert s.peek() == 3
    assert len(s) == 3


def test_peek_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticUniversalMinStack(capacity=3).peek()


def test_min_returns_without_removing() -> None:
    s = StaticUniversalMinStack(3, 1, 2, capacity=5)
    s.min()
    assert len(s) == 3


def test_min_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticUniversalMinStack(capacity=3).min()


def test_min_sequence() -> None:
    s = StaticUniversalMinStack(capacity=10)
    for v in [5, 3, 8, 1, 6]:
        s.push(v)
    assert s.min() == 1
    s.pop()  # 6
    assert s.min() == 1
    s.pop()  # 1
    assert s.min() == 3


# ── clear / copy ──────────────────────────────────────────────────────────────


def test_clear_resets_tops() -> None:
    s = StaticUniversalMinStack(1, 2, 3, capacity=5)
    s.clear()
    assert s._top == 0
    assert s._min_top == 0


def test_copy_preserves_elements_and_capacity() -> None:
    s = StaticUniversalMinStack(3, 1, 2, capacity=5)
    c = s.copy()
    assert list(c) == list(s)
    assert len(c._data) == len(s._data)


def test_copy_preserves_min() -> None:
    s = StaticUniversalMinStack(3, 1, 2, capacity=5)
    assert s.copy().min() == s.min()


def test_copy_preserves_key() -> None:
    s = StaticUniversalMinStack(1, 2, 3, capacity=5, key=lambda x: -x)
    c = s.copy()
    assert c._key(5) == -5


def test_copy_is_independent() -> None:
    s = StaticUniversalMinStack(1, 2, capacity=5)
    c = s.copy()
    c.push(99)
    assert len(s) == 2


# ── is_empty / is_full / __bool__ / __len__ ───────────────────────────────────


def test_is_empty_true() -> None:
    assert StaticUniversalMinStack(capacity=3).is_empty()


def test_is_empty_false() -> None:
    assert not StaticUniversalMinStack(1, capacity=3).is_empty()


def test_is_full_true() -> None:
    assert StaticUniversalMinStack(1, 2, 3, capacity=3).is_full()


def test_is_full_false() -> None:
    assert not StaticUniversalMinStack(1, capacity=3).is_full()


def test_bool_empty() -> None:
    assert not bool(StaticUniversalMinStack(capacity=3))


def test_bool_not_empty() -> None:
    assert bool(StaticUniversalMinStack(1, capacity=3))


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_iter_top_to_bottom() -> None:
    s = StaticUniversalMinStack(1, 2, 3, capacity=5)
    assert list(s) == [3, 2, 1]


def test_iter_empty() -> None:
    assert list(StaticUniversalMinStack(capacity=3)) == []


def test_reversed_bottom_to_top() -> None:
    s = StaticUniversalMinStack(1, 2, 3, capacity=5)
    assert list(reversed(s)) == [1, 2, 3]


def test_iter_does_not_modify() -> None:
    s = StaticUniversalMinStack(1, 2, 3, capacity=5)
    _ = list(s)
    assert len(s) == 3


# ── __contains__ ──────────────────────────────────────────────────────────────


def test_contains_existing() -> None:
    assert 2 in StaticUniversalMinStack(1, 2, 3, capacity=5)


def test_contains_missing() -> None:
    assert 99 not in StaticUniversalMinStack(1, 2, 3, capacity=5)


def test_contains_above_top_not_found() -> None:
    s = StaticUniversalMinStack(1, capacity=5)
    assert None not in s


# ── __eq__ ────────────────────────────────────────────────────────────────────


def test_eq_equal() -> None:
    a = StaticUniversalMinStack(1, 2, 3, capacity=5)
    b = StaticUniversalMinStack(1, 2, 3, capacity=5)
    assert a == b


def test_eq_same_elements_different_capacity() -> None:
    a = StaticUniversalMinStack(1, 2, capacity=2)
    b = StaticUniversalMinStack(1, 2, capacity=5)
    assert a == b


def test_eq_different_elements() -> None:
    a = StaticUniversalMinStack(1, 2, capacity=3)
    b = StaticUniversalMinStack(1, 9, capacity=3)
    assert a != b


def test_eq_not_implemented_for_other_type() -> None:
    assert StaticUniversalMinStack(1, capacity=3).__eq__([1]) is NotImplemented


# ── __repr__ ──────────────────────────────────────────────────────────────────


def test_repr_empty() -> None:
    s = StaticUniversalMinStack(capacity=3)
    assert repr(s) == "StaticUniversalMinStack(capacity=3, min=None)[]"


def test_repr_partial() -> None:
    # BUG: repr reads self._min_data[self._min_top] (off-by-one) and iterates
    # all capacity slots. Both fixed before these tests pass.
    s = StaticUniversalMinStack(3, 1, 2, capacity=5)
    assert repr(s) == "StaticUniversalMinStack(capacity=5, min=1)[2, 1, 3]"
