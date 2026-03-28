import pytest

from data_structures import DynamicTypedStack

# ── Init ──────────────────────────────────────────────────────────────────────


def test_init_int_empty() -> None:
    s = DynamicTypedStack(int)
    assert len(s) == 0
    assert s._dtype is int


def test_init_float_empty() -> None:
    s = DynamicTypedStack(float)
    assert s._dtype is float


def test_init_str_empty() -> None:
    s = DynamicTypedStack(str)
    assert s._dtype is str


def test_init_with_args() -> None:
    s = DynamicTypedStack(int, 1, 2, 3)
    assert len(s) == 3
    assert s.peek() == 3


def test_init_str_with_args() -> None:
    s = DynamicTypedStack(str, "a", "b")
    assert s.peek() == "b"


def test_init_unsupported_dtype_raises() -> None:
    with pytest.raises(TypeError):
        DynamicTypedStack(list, [1])


# ── Push ──────────────────────────────────────────────────────────────────────


def test_push_correct_type() -> None:
    s = DynamicTypedStack(int)
    s.push(42)
    assert s.peek() == 42


def test_push_wrong_type_raises() -> None:
    s = DynamicTypedStack(int)
    with pytest.raises(TypeError):
        s.push("hello")


def test_push_bool_into_int_raises() -> None:
    s = DynamicTypedStack(int)
    with pytest.raises(TypeError):
        s.push(True)


def test_push_int_into_bool_raises() -> None:
    s = DynamicTypedStack(bool)
    with pytest.raises(TypeError):
        s.push(1)


def test_push_triggers_resize() -> None:
    s = DynamicTypedStack(int)
    for i in range(20):
        s.push(i)
    assert len(s) == 20
    assert s.peek() == 19


# ── Pop ───────────────────────────────────────────────────────────────────────


def test_pop_returns_top() -> None:
    s = DynamicTypedStack(int, 1, 2, 3)
    assert s.pop() == 3


def test_pop_decrements_size() -> None:
    s = DynamicTypedStack(int, 1, 2, 3)
    s.pop()
    assert len(s) == 2


def test_pop_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicTypedStack(int).pop()


# ── Peek ──────────────────────────────────────────────────────────────────────


def test_peek_returns_top_without_removing() -> None:
    s = DynamicTypedStack(int, 1, 2, 3)
    assert s.peek() == 3
    assert len(s) == 3


def test_peek_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicTypedStack(int).peek()


# ── clear / copy ──────────────────────────────────────────────────────────────


def test_clear_resets_size() -> None:
    s = DynamicTypedStack(int, 1, 2, 3)
    s.clear()
    assert len(s) == 0


def test_copy_preserves_elements_and_dtype() -> None:
    s = DynamicTypedStack(int, 1, 2, 3)
    c = s.copy()
    assert list(c) == list(s)
    assert c._dtype is int


def test_copy_is_independent() -> None:
    s = DynamicTypedStack(int, 1, 2, 3)
    c = s.copy()
    c.push(99)
    assert len(s) == 3


# ── is_empty / __bool__ / __len__ ─────────────────────────────────────────────


def test_is_empty_true() -> None:
    assert DynamicTypedStack(int).is_empty()


def test_is_empty_false() -> None:
    assert not DynamicTypedStack(int, 1).is_empty()


def test_bool_empty() -> None:
    assert not bool(DynamicTypedStack(int))


def test_bool_not_empty() -> None:
    assert bool(DynamicTypedStack(int, 1))


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_iter_top_to_bottom() -> None:
    s = DynamicTypedStack(int, 1, 2, 3)
    assert list(s) == [3, 2, 1]


def test_reversed_bottom_to_top() -> None:
    s = DynamicTypedStack(int, 1, 2, 3)
    assert list(reversed(s)) == [1, 2, 3]


def test_iter_empty() -> None:
    assert list(DynamicTypedStack(int)) == []


# ── __contains__ ──────────────────────────────────────────────────────────────


def test_contains_existing() -> None:
    s = DynamicTypedStack(int, 1, 2, 3)
    assert 2 in s


def test_contains_missing() -> None:
    assert 99 not in DynamicTypedStack(int, 1, 2, 3)


def test_contains_wrong_type_returns_false() -> None:
    s = DynamicTypedStack(int, 1, 2, 3)
    assert "1" not in s


def test_contains_bool_in_int_stack_returns_false() -> None:
    s = DynamicTypedStack(int, 1, 2)
    assert True not in s


# ── __eq__ ────────────────────────────────────────────────────────────────────


def test_eq_equal() -> None:
    assert DynamicTypedStack(int, 1, 2, 3) == DynamicTypedStack(int, 1, 2, 3)


def test_eq_both_empty() -> None:
    assert DynamicTypedStack(int) == DynamicTypedStack(int)


def test_eq_different_dtype() -> None:
    a = DynamicTypedStack(int, 1)
    b = DynamicTypedStack(float, 1.0)
    assert a != b


def test_eq_different_elements() -> None:
    assert DynamicTypedStack(int, 1, 2) != DynamicTypedStack(int, 1, 9)


def test_eq_not_implemented_for_other_type() -> None:
    assert DynamicTypedStack(int, 1).__eq__([1]) is NotImplemented


# ── __repr__ ──────────────────────────────────────────────────────────────────


def test_repr_empty() -> None:
    assert repr(DynamicTypedStack(int)) == "DynamicTypedStack(int, size=0)[]"


def test_repr_multiple() -> None:
    assert (
        repr(DynamicTypedStack(int, 1, 2, 3))
        == "DynamicTypedStack(int, size=3)[3, 2, 1]"
    )


def test_repr_float() -> None:
    s = DynamicTypedStack(float, 1.0, 2.0)
    assert repr(s) == "DynamicTypedStack(float, size=2)[2.0, 1.0]"
