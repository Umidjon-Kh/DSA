import pytest

from data_structures import StaticTypedMinStack

# ── Init ──────────────────────────────────────────────────────────────────────


def test_init_capacity_only() -> None:
    s = StaticTypedMinStack(int, capacity=5)
    assert len(s) == 0
    assert s._top == 0
    assert s._min_top == 0
    assert s._dtype is int


def test_init_default_key_is_identity() -> None:
    s = StaticTypedMinStack(int, capacity=5)
    assert s._key(10) == 10


def test_init_custom_key_stored() -> None:
    s = StaticTypedMinStack(int, capacity=5, key=lambda x: -x)
    assert s._key(5) == -5


def test_init_non_callable_key_raises() -> None:
    with pytest.raises(TypeError):
        StaticTypedMinStack(int, capacity=5, key=42)  # type: ignore[arg-type]


def test_init_with_args() -> None:
    s = StaticTypedMinStack(int, 3, 1, 2, capacity=5)
    assert len(s) == 3
    assert s.peek() == 2


def test_init_with_args_sets_min() -> None:
    s = StaticTypedMinStack(int, 3, 1, 2, capacity=5)
    assert s.min() == 1


def test_init_no_args_no_capacity_raises() -> None:
    with pytest.raises(TypeError):
        StaticTypedMinStack(int)


def test_init_too_many_args_raises() -> None:
    with pytest.raises(OverflowError):
        StaticTypedMinStack(int, 1, 2, 3, capacity=2)


def test_init_zero_capacity_raises() -> None:
    with pytest.raises(ValueError):
        StaticTypedMinStack(int, capacity=0)


def test_init_unsupported_dtype_raises() -> None:
    with pytest.raises(TypeError):
        StaticTypedMinStack(list, capacity=3)


def test_init_str_length_stored() -> None:
    s = StaticTypedMinStack(str, capacity=3, str_length=50)
    assert s._str_length == 50


# ── Push ──────────────────────────────────────────────────────────────────────


def test_push_correct_type() -> None:
    s = StaticTypedMinStack(int, capacity=5)
    s.push(42)
    assert s.peek() == 42


def test_push_wrong_type_raises() -> None:
    s = StaticTypedMinStack(int, capacity=5)
    with pytest.raises(TypeError):
        s.push("hello")


def test_push_bool_into_int_raises() -> None:
    s = StaticTypedMinStack(int, capacity=5)
    with pytest.raises(TypeError):
        s.push(True)


def test_push_int_into_bool_raises() -> None:
    s = StaticTypedMinStack(bool, capacity=5)
    with pytest.raises(TypeError):
        s.push(1)


def test_push_when_full_raises() -> None:
    s = StaticTypedMinStack(int, 1, 2, capacity=2)
    with pytest.raises(OverflowError):
        s.push(3)


def test_push_first_enters_min() -> None:
    s = StaticTypedMinStack(int, capacity=5)
    s.push(5)
    assert s._min_top == 1
    assert s._min_data._raw_get(0) == 5


def test_push_lower_enters_min() -> None:
    # BUG: push() reads _raw_get(self._min_top) — off-by-one, reads uninitialized slot.
    # Fix: _raw_get(self._min_top - 1). Test will FAIL until fixed.
    s = StaticTypedMinStack(int, capacity=5)
    s.push(5)
    s.push(3)
    assert s.min() == 3
    assert s._min_top == 2


def test_push_higher_does_not_enter_min() -> None:
    s = StaticTypedMinStack(int, capacity=5)
    s.push(3)
    s.push(5)
    assert s.min() == 3
    assert s._min_top == 1


def test_push_equal_enters_min() -> None:
    s = StaticTypedMinStack(int, capacity=5)
    s.push(3)
    s.push(3)
    assert s.min() == 3
    assert s._min_top == 2


def test_push_with_key() -> None:
    s = StaticTypedMinStack(int, capacity=5, key=lambda x: -x)
    s.push(3)
    s.push(7)
    s.push(1)
    assert s.min() == 7


# ── Pop ───────────────────────────────────────────────────────────────────────


def test_pop_returns_top() -> None:
    s = StaticTypedMinStack(int, 1, 2, 3, capacity=5)
    assert s.pop() == 3


def test_pop_resets_main_slot_to_default() -> None:
    s = StaticTypedMinStack(int, 1, 2, capacity=3)
    s.pop()
    assert s._data._raw_get(1) == 0


def test_pop_non_min_leaves_min_intact() -> None:
    s = StaticTypedMinStack(int, 3, 1, 2, capacity=5)
    s.pop()  # 2
    assert s.min() == 1


def test_pop_min_updates_min() -> None:
    s = StaticTypedMinStack(int, 3, 1, 2, capacity=5)
    s.pop()  # 2
    s.pop()  # 1
    assert s.min() == 3


def test_pop_duplicate_min_removes_one() -> None:
    s = StaticTypedMinStack(int, 1, 1, capacity=5)
    s.pop()
    assert s.min() == 1
    assert s._min_top == 1


def test_pop_decrements_top() -> None:
    s = StaticTypedMinStack(int, 1, 2, 3, capacity=5)
    s.pop()
    assert s._top == 2


def test_pop_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticTypedMinStack(int, capacity=3).pop()


def test_pop_all_drains_min() -> None:
    s = StaticTypedMinStack(int, 1, 2, 3, capacity=5)
    s.pop()
    s.pop()
    s.pop()
    assert s._min_top == 0


# ── Peek / min ────────────────────────────────────────────────────────────────


def test_peek_returns_top_without_removing() -> None:
    s = StaticTypedMinStack(int, 1, 2, 3, capacity=5)
    assert s.peek() == 3
    assert len(s) == 3


def test_peek_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticTypedMinStack(int, capacity=3).peek()


def test_min_returns_without_removing() -> None:
    s = StaticTypedMinStack(int, 3, 1, 2, capacity=5)
    s.min()
    assert len(s) == 3


def test_min_empty_raises() -> None:
    with pytest.raises(IndexError):
        StaticTypedMinStack(int, capacity=3).min()


def test_min_sequence() -> None:
    s = StaticTypedMinStack(int, capacity=10)
    for v in [5, 3, 8, 1, 6]:
        s.push(v)
    assert s.min() == 1
    s.pop()  # 6
    assert s.min() == 1
    s.pop()  # 1
    assert s.min() == 3


# ── clear / copy ──────────────────────────────────────────────────────────────


def test_clear_resets_tops_and_data() -> None:
    s = StaticTypedMinStack(int, 1, 2, 3, capacity=5)
    s.clear()
    assert s._top == 0
    assert s._min_top == 0
    assert s._data._raw_get(0) == 0


def test_copy_preserves_elements_dtype_capacity() -> None:
    s = StaticTypedMinStack(int, 3, 1, 2, capacity=5)
    c = s.copy()
    assert list(c) == list(s)
    assert c._dtype is int
    assert len(c._data) == len(s._data)


def test_copy_preserves_min() -> None:
    s = StaticTypedMinStack(int, 3, 1, 2, capacity=5)
    assert s.copy().min() == s.min()


def test_copy_preserves_key() -> None:
    s = StaticTypedMinStack(int, 1, 2, 3, capacity=5, key=lambda x: -x)
    c = s.copy()
    assert c._key(5) == -5


def test_copy_is_independent() -> None:
    s = StaticTypedMinStack(int, 1, 2, capacity=5)
    c = s.copy()
    c.push(99)
    assert len(s) == 2


# ── is_empty / is_full / __bool__ / __len__ ───────────────────────────────────


def test_is_empty_true() -> None:
    assert StaticTypedMinStack(int, capacity=3).is_empty()


def test_is_empty_false() -> None:
    assert not StaticTypedMinStack(int, 1, capacity=3).is_empty()


def test_is_full_true() -> None:
    assert StaticTypedMinStack(int, 1, 2, 3, capacity=3).is_full()


def test_is_full_false() -> None:
    assert not StaticTypedMinStack(int, 1, capacity=3).is_full()


def test_bool_empty() -> None:
    assert not bool(StaticTypedMinStack(int, capacity=3))


def test_bool_not_empty() -> None:
    assert bool(StaticTypedMinStack(int, 1, capacity=3))


def test_len_returns_top() -> None:
    s = StaticTypedMinStack(int, 1, 2, 3, capacity=5)
    assert len(s) == 3


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_iter_top_to_bottom() -> None:
    s = StaticTypedMinStack(int, 1, 2, 3, capacity=5)
    assert list(s) == [3, 2, 1]


def test_iter_empty() -> None:
    assert list(StaticTypedMinStack(int, capacity=3)) == []


def test_reversed_bottom_to_top() -> None:
    s = StaticTypedMinStack(int, 1, 2, 3, capacity=5)
    assert list(reversed(s)) == [1, 2, 3]


def test_iter_does_not_modify() -> None:
    s = StaticTypedMinStack(int, 1, 2, 3, capacity=5)
    _ = list(s)
    assert len(s) == 3


# ── __contains__ ──────────────────────────────────────────────────────────────


def test_contains_existing() -> None:
    assert 2 in StaticTypedMinStack(int, 1, 2, 3, capacity=5)


def test_contains_missing() -> None:
    assert 99 not in StaticTypedMinStack(int, 1, 2, 3, capacity=5)


def test_contains_wrong_type_returns_false() -> None:
    assert "1" not in StaticTypedMinStack(int, 1, 2, capacity=5)


def test_contains_bool_in_int_stack_returns_false() -> None:
    assert True not in StaticTypedMinStack(int, 1, capacity=3)


def test_contains_above_top_not_found() -> None:
    s = StaticTypedMinStack(int, 1, capacity=5)
    # slots 1..4 hold default 0 but are above _top — should NOT be visible
    assert 0 not in s


# ── __eq__ ────────────────────────────────────────────────────────────────────


def test_eq_equal() -> None:
    a = StaticTypedMinStack(int, 1, 2, 3, capacity=5)
    b = StaticTypedMinStack(int, 1, 2, 3, capacity=5)
    assert a == b


def test_eq_same_elements_different_capacity() -> None:
    a = StaticTypedMinStack(int, 1, 2, capacity=2)
    b = StaticTypedMinStack(int, 1, 2, capacity=5)
    assert a == b


def test_eq_different_dtype() -> None:
    a = StaticTypedMinStack(int, capacity=3)
    b = StaticTypedMinStack(float, capacity=3)
    assert a != b


def test_eq_different_elements() -> None:
    a = StaticTypedMinStack(int, 1, 2, capacity=3)
    b = StaticTypedMinStack(int, 1, 9, capacity=3)
    assert a != b


def test_eq_not_implemented_for_other_type() -> None:
    assert StaticTypedMinStack(int, 1, capacity=3).__eq__([1]) is NotImplemented


# ── __repr__ ──────────────────────────────────────────────────────────────────


def test_repr_empty() -> None:
    s = StaticTypedMinStack(int, capacity=5)
    assert repr(s) == "StaticTypedMinStack(int, capacity=5, min=None)[]"


def test_repr_partial() -> None:
    # BUG: repr reads self._min_data[self._min_top] (off-by-one) and iterates
    # all capacity slots via `for v in self._data`. Both fixed before these pass.
    s = StaticTypedMinStack(int, 3, 1, 2, capacity=5)
    assert repr(s) == "StaticTypedMinStack(int, capacity=5, min=1)[2, 1, 3]"
