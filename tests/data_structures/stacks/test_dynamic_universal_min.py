import pytest

from data_structures import DynamicUniversalMinStack

# ── Init ──────────────────────────────────────────────────────────────────────


def test_init_empty() -> None:
    s = DynamicUniversalMinStack()
    assert len(s) == 0
    assert s.is_empty()


def test_init_default_key_is_identity() -> None:
    s = DynamicUniversalMinStack()
    assert s._key(10) == 10


def test_init_custom_key_stored() -> None:
    s = DynamicUniversalMinStack(key=lambda x: -x)
    assert s._key(5) == -5


def test_init_non_callable_key_raises() -> None:
    with pytest.raises(TypeError):
        DynamicUniversalMinStack(key=42)  # type: ignore[arg-type]


def test_init_with_args() -> None:
    s = DynamicUniversalMinStack(3, 1, 2)
    assert len(s) == 3
    assert s.peek() == 2


def test_init_with_args_sets_min() -> None:
    s = DynamicUniversalMinStack(3, 1, 2)
    assert s.min() == 1


# ── Push ──────────────────────────────────────────────────────────────────────


def test_push_first_enters_min() -> None:
    s = DynamicUniversalMinStack()
    s.push(5)
    assert s.min() == 5
    assert len(s._min_data) == 1


def test_push_lower_enters_min() -> None:
    s = DynamicUniversalMinStack()
    s.push(5)
    s.push(3)
    assert s.min() == 3
    assert len(s._min_data) == 2


def test_push_higher_does_not_enter_min() -> None:
    s = DynamicUniversalMinStack()
    s.push(3)
    s.push(5)
    assert s.min() == 3
    assert len(s._min_data) == 1


def test_push_equal_enters_min() -> None:
    s = DynamicUniversalMinStack()
    s.push(3)
    s.push(3)
    assert s.min() == 3
    assert len(s._min_data) == 2


def test_push_triggers_resize() -> None:
    s = DynamicUniversalMinStack()
    for i in range(20):
        s.push(i)
    assert len(s) == 20
    assert s.min() == 0


def test_push_with_custom_key() -> None:
    s = DynamicUniversalMinStack(key=lambda x: -x)
    s.push(3)
    s.push(7)
    s.push(1)
    # key=-x so largest raw value is "min"
    assert s.min() == 7


# ── Pop ───────────────────────────────────────────────────────────────────────


def test_pop_returns_top() -> None:
    s = DynamicUniversalMinStack(1, 2, 3)
    assert s.pop() == 3


def test_pop_non_min_leaves_min_intact() -> None:
    s = DynamicUniversalMinStack(3, 1, 2)
    s.pop()  # pops 2
    assert s.min() == 1


def test_pop_min_value_updates_min() -> None:
    s = DynamicUniversalMinStack(3, 1, 2)
    s.pop()  # 2
    s.pop()  # 1
    assert s.min() == 3


def test_pop_duplicate_min_removes_one() -> None:
    s = DynamicUniversalMinStack(1, 1)
    s.pop()
    assert s.min() == 1
    assert len(s._min_data) == 1


def test_pop_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicUniversalMinStack().pop()


def test_pop_all_drains_min_data() -> None:
    s = DynamicUniversalMinStack(1, 2, 3)
    s.pop()
    s.pop()
    s.pop()
    assert len(s._min_data) == 0


# ── Peek / min ────────────────────────────────────────────────────────────────


def test_peek_returns_top_without_removing() -> None:
    s = DynamicUniversalMinStack(1, 2, 3)
    assert s.peek() == 3
    assert len(s) == 3


def test_peek_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicUniversalMinStack().peek()


def test_min_returns_without_removing() -> None:
    s = DynamicUniversalMinStack(3, 1, 2)
    s.min()
    assert len(s) == 3


def test_min_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicUniversalMinStack().min()


def test_min_sequence() -> None:
    s = DynamicUniversalMinStack()
    for v in [5, 3, 8, 1, 6]:
        s.push(v)
    assert s.min() == 1
    s.pop()  # 6
    assert s.min() == 1
    s.pop()  # 1
    assert s.min() == 3


# ── clear ─────────────────────────────────────────────────────────────────────


def test_clear_resets_both_arrays() -> None:
    s = DynamicUniversalMinStack(1, 2, 3)
    s.clear()
    assert len(s._data) == 0
    assert len(s._min_data) == 0


# ── copy ──────────────────────────────────────────────────────────────────────


def test_copy_preserves_elements() -> None:
    s = DynamicUniversalMinStack(3, 1, 2)
    c = s.copy()
    assert list(c) == list(s)


def test_copy_preserves_min() -> None:
    s = DynamicUniversalMinStack(3, 1, 2)
    assert s.copy().min() == s.min()


def test_copy_preserves_key() -> None:
    s = DynamicUniversalMinStack(5, 3, 8, key=lambda x: -x)
    c = s.copy()
    assert c._key(5) == -5


def test_copy_is_independent() -> None:
    s = DynamicUniversalMinStack(1, 2, 3)
    c = s.copy()
    c.push(0)
    assert len(s) == 3


# ── is_empty / __bool__ / __len__ ─────────────────────────────────────────────


def test_is_empty_true() -> None:
    assert DynamicUniversalMinStack().is_empty()


def test_is_empty_false() -> None:
    assert not DynamicUniversalMinStack(1).is_empty()


def test_bool_empty() -> None:
    assert not bool(DynamicUniversalMinStack())


def test_bool_not_empty() -> None:
    assert bool(DynamicUniversalMinStack(1))


def test_len_grows() -> None:
    s = DynamicUniversalMinStack(1, 2, 3)
    assert len(s) == 3


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_iter_top_to_bottom() -> None:
    s = DynamicUniversalMinStack(1, 2, 3)
    assert list(s) == [3, 2, 1]


def test_iter_empty() -> None:
    assert list(DynamicUniversalMinStack()) == []


def test_reversed_bottom_to_top() -> None:
    s = DynamicUniversalMinStack(1, 2, 3)
    assert list(reversed(s)) == [1, 2, 3]


def test_iter_does_not_modify() -> None:
    s = DynamicUniversalMinStack(1, 2, 3)
    _ = list(s)
    assert len(s) == 3


# ── __contains__ ──────────────────────────────────────────────────────────────


def test_contains_existing() -> None:
    assert 2 in DynamicUniversalMinStack(1, 2, 3)


def test_contains_missing() -> None:
    assert 99 not in DynamicUniversalMinStack(1, 2, 3)


# ── __eq__ ────────────────────────────────────────────────────────────────────


def test_eq_equal() -> None:
    assert DynamicUniversalMinStack(1, 2, 3) == DynamicUniversalMinStack(1, 2, 3)


def test_eq_both_empty() -> None:
    assert DynamicUniversalMinStack() == DynamicUniversalMinStack()


def test_eq_different_elements() -> None:
    assert DynamicUniversalMinStack(1, 2) != DynamicUniversalMinStack(1, 9)


def test_eq_not_implemented_for_other_type() -> None:
    assert DynamicUniversalMinStack(1).__eq__([1]) is NotImplemented


# ── __repr__ ──────────────────────────────────────────────────────────────────


def test_repr_empty() -> None:
    assert (
        repr(DynamicUniversalMinStack())
        == "DynamicUniversalMinStack(size=0, min=None)[]"
    )


def test_repr_multiple() -> None:
    s = DynamicUniversalMinStack(1, 2, 3)
    assert repr(s) == "DynamicUniversalMinStack(size=3, min=1)[3, 2, 1]"
