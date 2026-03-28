import pytest

from data_structures import DynamicUniversalStack

# ── Init ──────────────────────────────────────────────────────────────────────


def test_init_empty() -> None:
    s = DynamicUniversalStack()
    assert len(s) == 0
    assert s.is_empty()


def test_init_with_args() -> None:
    s = DynamicUniversalStack(1, 2, 3)
    assert len(s) == 3
    assert s.peek() == 3


def test_init_mixed_types() -> None:
    s = DynamicUniversalStack(1, "hi", 3.0)
    assert s.peek() == 3.0
    assert len(s) == 3


# ── Push ──────────────────────────────────────────────────────────────────────


def test_push_increments_size() -> None:
    s = DynamicUniversalStack()
    s.push(10)
    s.push(20)
    assert len(s) == 2


def test_push_any_type() -> None:
    s = DynamicUniversalStack()
    s.push(None)
    s.push([1, 2])
    s.push({"a": 1})
    assert len(s) == 3
    assert s.peek() == {"a": 1}


def test_push_triggers_resize() -> None:
    s = DynamicUniversalStack()
    for i in range(20):
        s.push(i)
    assert len(s) == 20
    assert s.peek() == 19


# ── Pop ───────────────────────────────────────────────────────────────────────


def test_pop_returns_top() -> None:
    s = DynamicUniversalStack(1, 2, 3)
    assert s.pop() == 3


def test_pop_decrements_size() -> None:
    s = DynamicUniversalStack(1, 2, 3)
    s.pop()
    assert len(s) == 2


def test_pop_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicUniversalStack().pop()


def test_pop_all_leaves_empty() -> None:
    s = DynamicUniversalStack(1, 2)
    s.pop()
    s.pop()
    assert s.is_empty()


# ── Peek ──────────────────────────────────────────────────────────────────────


def test_peek_returns_top_without_removing() -> None:
    s = DynamicUniversalStack(1, 2, 3)
    assert s.peek() == 3
    assert len(s) == 3


def test_peek_empty_raises() -> None:
    with pytest.raises(IndexError):
        DynamicUniversalStack().peek()


# ── clear ─────────────────────────────────────────────────────────────────────


def test_clear_resets_size() -> None:
    s = DynamicUniversalStack(1, 2, 3)
    s.clear()
    assert len(s) == 0
    assert s.is_empty()


def test_clear_empty_is_noop() -> None:
    s = DynamicUniversalStack()
    s.clear()
    assert s.is_empty()


# ── copy ──────────────────────────────────────────────────────────────────────


def test_copy_preserves_elements() -> None:
    s = DynamicUniversalStack(1, 2, 3)
    c = s.copy()
    assert list(c) == list(s)


def test_copy_is_independent() -> None:
    s = DynamicUniversalStack(1, 2, 3)
    c = s.copy()
    c.push(99)
    assert len(s) == 3


def test_copy_empty() -> None:
    assert DynamicUniversalStack().copy().is_empty()


# ── is_empty / __bool__ / __len__ ─────────────────────────────────────────────


def test_is_empty_true() -> None:
    assert DynamicUniversalStack().is_empty()


def test_is_empty_false() -> None:
    assert not DynamicUniversalStack(1).is_empty()


def test_bool_empty() -> None:
    assert not bool(DynamicUniversalStack())


def test_bool_not_empty() -> None:
    assert bool(DynamicUniversalStack(1))


def test_len_grows_with_pushes() -> None:
    s = DynamicUniversalStack()
    for i in range(5):
        s.push(i)
    assert len(s) == 5


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_iter_top_to_bottom() -> None:
    s = DynamicUniversalStack(1, 2, 3)
    assert list(s) == [3, 2, 1]


def test_iter_empty() -> None:
    assert list(DynamicUniversalStack()) == []


def test_reversed_bottom_to_top() -> None:
    s = DynamicUniversalStack(1, 2, 3)
    assert list(reversed(s)) == [1, 2, 3]


def test_iter_does_not_modify() -> None:
    s = DynamicUniversalStack(1, 2, 3)
    _ = list(s)
    assert len(s) == 3


# ── __contains__ ──────────────────────────────────────────────────────────────


def test_contains_existing() -> None:
    s = DynamicUniversalStack(1, 2, 3)
    assert 2 in s


def test_contains_missing() -> None:
    assert 99 not in DynamicUniversalStack(1, 2, 3)


def test_contains_empty() -> None:
    assert 1 not in DynamicUniversalStack()


# ── __eq__ ────────────────────────────────────────────────────────────────────


def test_eq_equal() -> None:
    assert DynamicUniversalStack(1, 2, 3) == DynamicUniversalStack(1, 2, 3)


def test_eq_both_empty() -> None:
    assert DynamicUniversalStack() == DynamicUniversalStack()


def test_eq_different_elements() -> None:
    assert DynamicUniversalStack(1, 2) != DynamicUniversalStack(1, 9)


def test_eq_different_sizes() -> None:
    assert DynamicUniversalStack(1, 2) != DynamicUniversalStack(1, 2, 3)


def test_eq_not_implemented_for_other_type() -> None:
    assert DynamicUniversalStack(1).__eq__([1]) is NotImplemented


# ── __repr__ ──────────────────────────────────────────────────────────────────


def test_repr_empty() -> None:
    assert repr(DynamicUniversalStack()) == "DynamicUniversalStack(size=0)[]"


def test_repr_single() -> None:
    assert repr(DynamicUniversalStack(5)) == "DynamicUniversalStack(size=1)[5]"


def test_repr_multiple() -> None:
    assert (
        repr(DynamicUniversalStack(1, 2, 3)) == "DynamicUniversalStack(size=3)[3, 2, 1]"
    )


def test_repr_with_strings() -> None:
    s = DynamicUniversalStack("a", "b")
    assert repr(s) == "DynamicUniversalStack(size=2)['b', 'a']"
