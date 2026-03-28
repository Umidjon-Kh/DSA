import pytest

from data_structures import StaticTypedStack

# ── Init ──────────────────────────────────────────────────────────────────────


def test_init_int_capacity_only() -> None:
    s = StaticTypedStack(int, capacity=5)
    assert len(s) == 0
    assert s._dtype is int


def test_init_with_args() -> None:
    s = StaticTypedStack(int, 1, 2, 3, capacity=5)
    assert len(s) == 3
    assert s.peek() == 3


def test_init_infer_capacity_from_args() -> None:
    s = StaticTypedStack(int, 1, 2, 3)
    assert len(s) == 3
    assert len(s._data) == 3


def test_init_no_args_no_capacity_raises() -> None:
    with pytest.raises(TypeError):
        StaticTypedStack(int)


def test_init_too_many_args_raises() -> None:
    with pytest.raises(OverflowError):
        StaticTypedStack(int, 1, 2, 3, capacity=2)


def test_init_zero_capacity_raises() -> None:
    with pytest.raises(ValueError):
        StaticTypedStack(int, capacity=0)


def test_init_unsupported_dtype_raises() -> None:
    with pytest.raises(TypeError):
        StaticTypedStack(list, capacity=3)


def test_init_str_length_stored() -> None:
    s = StaticTypedStack(str, capacity=3, str_length=50)
    assert s._str_length == 50


# ── Push ──────────────────────────────────────────────────────────────────────


def test_push_correct_type() -> None:
    s = StaticTypedStack(int, capacity=5)
    s.push(42)
    assert s.peek() == 42


def test_push_wrong_type_raises() -> None:
    s = StaticTypedStack(int, capacity=5)
    with pytest.raises(TypeError):
        s.push("hello")


def test_push_bool_into_int_raises() -> None:
    s = StaticTypedStack(int, capacity=5)
    with pytest.raises(TypeError):
        s.push(True)


def test_push_int_into_bool_raises() -> None:
    s = StaticTypedStack(bool, capacity=5)
    with pytest.raises(TypeError):
        s.push(1)


def test_push_when_full_raises() -> None:
    s = StaticTypedStack(int, 1, 2, capacity=2)
    with pytest.raises(OverflowError):
        s.push(3)


def test_push_increments_top() -> None:
    s = StaticTypedStack(int, capacity=5)
    s.push(1)
    assert s._top == 1


# ── Pop ───────────────────────────────────────────────────────────────────────


def test_pop_returns_top() -> None:
    s = StaticTypedStack(int, 1, 2, 3, capacity=5)
    assert s.pop() == 3


def test_pop_resets_slot_to_default() -> None:
    s = StaticTypedStack(int, 1, 2, capacity=3)
    s.pop()
    assert s._data._raw_get(1) == 0


def test_pop_decrements_top() -> None:
    s = StaticTypedStack(int, 1, 2, 3, capacity=5)
    s.pop()
    assert s._top == 2


def test_pop_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticTypedStack(int, capacity=3).pop()


# ── Peek ──────────────────────────────────────────────────────────────────────


def test_peek_returns_top_without_removing() -> None:
    s = StaticTypedStack(int, 1, 2, 3, capacity=5)
    assert s.peek() == 3
    assert len(s) == 3


def test_peek_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticTypedStack(int, capacity=3).peek()


# ── clear / copy ──────────────────────────────────────────────────────────────


def test_clear_resets_top_and_data() -> None:
    s = StaticTypedStack(int, 1, 2, 3, capacity=5)
    s.clear()
    assert s._top == 0
    assert s._data._raw_get(0) == 0


def test_copy_preserves_elements_dtype_capacity() -> None:
    s = StaticTypedStack(int, 1, 2, 3, capacity=5)
    c = s.copy()
    assert list(c) == list(s)
    assert c._dtype is int
    assert len(c._data) == len(s._data)


def test_copy_is_independent() -> None:
    s = StaticTypedStack(int, 1, 2, capacity=5)
    c = s.copy()
    c.push(99)
    assert len(s) == 2


# ── is_empty / is_full / __bool__ ─────────────────────────────────────────────


def test_is_empty_true() -> None:
    assert StaticTypedStack(int, capacity=3).is_empty()


def test_is_empty_false() -> None:
    assert not StaticTypedStack(int, 1, capacity=3).is_empty()


def test_is_full_true() -> None:
    assert StaticTypedStack(int, 1, 2, 3, capacity=3).is_full()


def test_is_full_false() -> None:
    assert not StaticTypedStack(int, 1, capacity=3).is_full()


def test_bool_empty() -> None:
    assert not bool(StaticTypedStack(int, capacity=3))


def test_bool_not_empty() -> None:
    assert bool(StaticTypedStack(int, 1, capacity=3))


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_iter_top_to_bottom() -> None:
    s = StaticTypedStack(int, 1, 2, 3, capacity=5)
    assert list(s) == [3, 2, 1]


def test_iter_empty() -> None:
    assert list(StaticTypedStack(int, capacity=3)) == []


def test_reversed_bottom_to_top() -> None:
    s = StaticTypedStack(int, 1, 2, 3, capacity=5)
    assert list(reversed(s)) == [1, 2, 3]


# ── __contains__ ──────────────────────────────────────────────────────────────


def test_contains_existing() -> None:
    s = StaticTypedStack(int, 1, 2, 3, capacity=5)
    assert 2 in s


def test_contains_missing() -> None:
    assert 99 not in StaticTypedStack(int, 1, 2, 3, capacity=5)


def test_contains_wrong_type_returns_false() -> None:
    s = StaticTypedStack(int, 1, 2, capacity=5)
    assert "1" not in s


def test_contains_bool_in_int_stack_returns_false() -> None:
    s = StaticTypedStack(int, 1, capacity=3)
    assert True not in s


# ── __eq__ ────────────────────────────────────────────────────────────────────


def test_eq_equal() -> None:
    a = StaticTypedStack(int, 1, 2, 3, capacity=5)
    b = StaticTypedStack(int, 1, 2, 3, capacity=5)
    assert a == b


def test_eq_same_elements_different_capacity() -> None:
    a = StaticTypedStack(int, 1, 2, capacity=2)
    b = StaticTypedStack(int, 1, 2, capacity=5)
    assert a == b


def test_eq_different_dtype() -> None:
    a = StaticTypedStack(int, capacity=3)
    b = StaticTypedStack(float, capacity=3)
    assert a != b


def test_eq_different_elements() -> None:
    a = StaticTypedStack(int, 1, 2, capacity=3)
    b = StaticTypedStack(int, 1, 9, capacity=3)
    assert a != b


def test_eq_not_implemented_for_other_type() -> None:
    assert StaticTypedStack(int, 1, capacity=3).__eq__([1]) is NotImplemented


# ── __repr__ ──────────────────────────────────────────────────────────────────


def test_repr_empty() -> None:
    s = StaticTypedStack(int, capacity=5)
    assert repr(s) == "StaticTypedStack(int, size=0, capacity=5)[]"


def test_repr_partial() -> None:
    s = StaticTypedStack(int, 1, 2, capacity=5)
    assert repr(s) == "StaticTypedStack(int, size=2, capacity=5)[2, 1]"


def test_repr_full() -> None:
    s = StaticTypedStack(int, 1, 2, 3, capacity=3)
    assert repr(s) == "StaticTypedStack(int, size=3, capacity=3)[3, 2, 1]"
