import pytest

# NOTE: DynamicTypedMinStack.pop() has a SyntaxError (missing colon after if condition,
# line ~4958 in dynamic/typed.py). The entire module fails to import until that is fixed.
# Fix: add `:` at the end of the `if self._key(value) == ...` line.
from data_structures import DynamicTypedMinStack

# ── Init ──────────────────────────────────────────────────────────────────────


def test_init_int_empty() -> None:
    s = DynamicTypedMinStack(int)
    assert len(s) == 0
    assert s._dtype is int


def test_init_default_key_is_identity() -> None:
    s = DynamicTypedMinStack(int)
    assert s._key(10) == 10


def test_init_custom_key_stored() -> None:
    s = DynamicTypedMinStack(int, key=lambda x: -x)
    assert s._key(5) == -5


def test_init_non_callable_key_raises() -> None:
    with pytest.raises(TypeError):
        DynamicTypedMinStack(int, key=42)  # type: ignore[arg-type]


def test_init_with_args_sets_size() -> None:
    s = DynamicTypedMinStack(int, 3, 1, 2)
    assert len(s) == 3


def test_init_with_args_sets_min() -> None:
    s = DynamicTypedMinStack(int, 3, 1, 2)
    assert s.min() == 1


def test_init_unsupported_dtype_raises() -> None:
    with pytest.raises(TypeError):
        DynamicTypedMinStack(list)


# ── Push ──────────────────────────────────────────────────────────────────────


def test_push_correct_type() -> None:
    s = DynamicTypedMinStack(int)
    s.push(5)
    assert s.peek() == 5


def test_push_wrong_type_raises() -> None:
    s = DynamicTypedMinStack(int)
    with pytest.raises(TypeError):
        s.push("hello")


def test_push_bool_into_int_raises() -> None:
    s = DynamicTypedMinStack(int)
    with pytest.raises(TypeError):
        s.push(True)


def test_push_first_enters_min() -> None:
    s = DynamicTypedMinStack(int)
    s.push(5)
    assert s.min() == 5
    assert len(s._min_data) == 1


def test_push_lower_enters_min() -> None:
    s = DynamicTypedMinStack(int)
    s.push(5)
    s.push(3)
    assert s.min() == 3
    assert len(s._min_data) == 2


def test_push_higher_does_not_enter_min() -> None:
    s = DynamicTypedMinStack(int)
    s.push(3)
    s.push(5)
    assert s.min() == 3
    assert len(s._min_data) == 1


def test_push_equal_enters_min() -> None:
    s = DynamicTypedMinStack(int)
    s.push(3)
    s.push(3)
    assert s.min() == 3
    assert len(s._min_data) == 2


def test_push_triggers_resize() -> None:
    s = DynamicTypedMinStack(int)
    for i in range(20):
        s.push(i)
    assert len(s) == 20
    assert s.min() == 0


# ── Pop ───────────────────────────────────────────────────────────────────────


def test_pop_returns_top() -> None:
    s = DynamicTypedMinStack(int, 1, 2, 3)
    assert s.pop() == 3


def test_pop_non_min_leaves_min_intact() -> None:
    s = DynamicTypedMinStack(int, 3, 1, 2)
    s.pop()  # 2
    assert s.min() == 1


def test_pop_min_updates_min() -> None:
    s = DynamicTypedMinStack(int, 3, 1, 2)
    s.pop()  # 2
    s.pop()  # 1
    assert s.min() == 3


def test_pop_duplicate_min_removes_one() -> None:
    s = DynamicTypedMinStack(int, 1, 1)
    s.pop()
    assert s.min() == 1
    assert len(s._min_data) == 1


def test_pop_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicTypedMinStack(int).pop()


def test_pop_all_drains_min_data() -> None:
    s = DynamicTypedMinStack(int, 1, 2, 3)
    s.pop()
    s.pop()
    s.pop()
    assert len(s._min_data) == 0


# ── Peek / min ────────────────────────────────────────────────────────────────


def test_peek_returns_top_without_removing() -> None:
    s = DynamicTypedMinStack(int, 1, 2, 3)
    assert s.peek() == 3
    assert len(s) == 3


def test_peek_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicTypedMinStack(int).peek()


def test_min_returns_without_removing() -> None:
    s = DynamicTypedMinStack(int, 3, 1, 2)
    s.min()
    assert len(s) == 3


def test_min_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicTypedMinStack(int).min()


def test_min_sequence() -> None:
    s = DynamicTypedMinStack(int)
    for v in [5, 3, 8, 1, 6]:
        s.push(v)
    assert s.min() == 1
    s.pop()  # 6
    assert s.min() == 1
    s.pop()  # 1
    assert s.min() == 3


# ── clear / copy ──────────────────────────────────────────────────────────────


def test_clear_resets_both_arrays() -> None:
    s = DynamicTypedMinStack(int, 1, 2, 3)
    s.clear()
    assert len(s._data) == 0
    assert len(s._min_data) == 0


def test_copy_preserves_elements_and_dtype() -> None:
    s = DynamicTypedMinStack(int, 3, 1, 2)
    c = s.copy()
    assert list(c) == list(s)
    assert c._dtype is int


def test_copy_preserves_min() -> None:
    s = DynamicTypedMinStack(int, 3, 1, 2)
    assert s.copy().min() == s.min()


def test_copy_preserves_key() -> None:
    s = DynamicTypedMinStack(int, 1, 2, 3, key=lambda x: -x)
    c = s.copy()
    assert c._key(5) == -5


def test_copy_is_independent() -> None:
    s = DynamicTypedMinStack(int, 1, 2, 3)
    c = s.copy()
    c.push(99)
    assert len(s) == 3


# ── is_empty / __bool__ / __len__ ─────────────────────────────────────────────


def test_is_empty_true() -> None:
    assert DynamicTypedMinStack(int).is_empty()


def test_is_empty_false() -> None:
    assert not DynamicTypedMinStack(int, 1).is_empty()


def test_bool_empty() -> None:
    assert not bool(DynamicTypedMinStack(int))


def test_bool_not_empty() -> None:
    assert bool(DynamicTypedMinStack(int, 1))


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_iter_top_to_bottom() -> None:
    s = DynamicTypedMinStack(int, 1, 2, 3)
    assert list(s) == [3, 2, 1]


def test_reversed_bottom_to_top() -> None:
    s = DynamicTypedMinStack(int, 1, 2, 3)
    assert list(reversed(s)) == [1, 2, 3]


def test_iter_empty() -> None:
    assert list(DynamicTypedMinStack(int)) == []


# ── __contains__ ──────────────────────────────────────────────────────────────


def test_contains_existing() -> None:
    assert 2 in DynamicTypedMinStack(int, 1, 2, 3)


def test_contains_missing() -> None:
    assert 99 not in DynamicTypedMinStack(int, 1, 2, 3)


def test_contains_wrong_type_returns_false() -> None:
    assert "2" not in DynamicTypedMinStack(int, 1, 2, 3)


# ── __eq__ ────────────────────────────────────────────────────────────────────


def test_eq_equal() -> None:
    assert DynamicTypedMinStack(int, 1, 2, 3) == DynamicTypedMinStack(int, 1, 2, 3)


def test_eq_both_empty() -> None:
    assert DynamicTypedMinStack(int) == DynamicTypedMinStack(int)


def test_eq_different_elements() -> None:
    assert DynamicTypedMinStack(int, 1, 2) != DynamicTypedMinStack(int, 1, 9)


def test_eq_not_implemented_for_other_type() -> None:
    assert DynamicTypedMinStack(int, 1).__eq__([1]) is NotImplemented


# ── __repr__ ──────────────────────────────────────────────────────────────────


def test_repr_empty() -> None:
    assert (
        repr(DynamicTypedMinStack(int))
        == "DynamicTypedMinStack(int, size=0, min=None)[]"
    )


def test_repr_multiple() -> None:
    s = DynamicTypedMinStack(int, 1, 2, 3)
    assert repr(s) == "DynamicTypedMinStack(int, size=3, min=1)[3, 2, 1]"
