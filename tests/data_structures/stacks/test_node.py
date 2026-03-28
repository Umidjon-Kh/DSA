import pytest

from data_structures import NodeStack

# ── Init ──────────────────────────────────────────────────────────────────────


def test_init_empty() -> None:
    s = NodeStack()
    assert s._size == 0
    assert s._head is None


def test_init_with_args() -> None:
    s = NodeStack(1, 2, 3)
    assert s._size == 3
    assert s.peek() == 3


def test_init_single_arg() -> None:
    s = NodeStack(42)
    assert len(s) == 1
    assert s.peek() == 42


def test_init_mixed_types() -> None:
    s = NodeStack(1, "hi", 3.0)
    assert s.peek() == 3.0
    assert len(s) == 3


# ── Push ──────────────────────────────────────────────────────────────────────


def test_push_increments_size() -> None:
    s = NodeStack()
    s.push(1)
    s.push(2)
    assert s._size == 2


def test_push_updates_head() -> None:
    s = NodeStack()
    s.push(1)
    s.push(2)
    assert s._head.value == 2
    assert s._head.next.value == 1


def test_push_none_value() -> None:
    s = NodeStack()
    s.push(None)
    assert s.peek() is None
    assert len(s) == 1


# ── Pop ───────────────────────────────────────────────────────────────────────


def test_pop_returns_top() -> None:
    s = NodeStack(1, 2, 3)
    assert s.pop() == 3


def test_pop_decrements_size() -> None:
    s = NodeStack(1, 2, 3)
    s.pop()
    assert s._size == 2


def test_pop_updates_head() -> None:
    s = NodeStack(1, 2, 3)
    s.pop()
    assert s._head.value == 2


def test_pop_all_leaves_empty() -> None:
    s = NodeStack(1, 2)
    s.pop()
    s.pop()
    assert s.is_empty()
    assert s._head is None


def test_pop_empty_raises() -> None:
    s = NodeStack()
    with pytest.raises(IndexError):
        s.pop()


def test_pop_single_element() -> None:
    s = NodeStack(99)
    assert s.pop() == 99
    assert s.is_empty()


# ── Peek ──────────────────────────────────────────────────────────────────────


def test_peek_returns_top_without_removing() -> None:
    s = NodeStack(1, 2, 3)
    assert s.peek() == 3
    assert len(s) == 3


def test_peek_empty_raises() -> None:
    s = NodeStack()
    with pytest.raises(IndexError):
        s.peek()


# ── clear ─────────────────────────────────────────────────────────────────────


def test_clear_resets_size_and_head() -> None:
    s = NodeStack(1, 2, 3)
    s.clear()
    assert s._size == 0
    assert s._head is None


def test_clear_empty_is_noop() -> None:
    s = NodeStack()
    s.clear()
    assert s.is_empty()


# ── copy ──────────────────────────────────────────────────────────────────────


def test_copy_preserves_elements() -> None:
    s = NodeStack(1, 2, 3)
    c = s.copy()
    assert list(c) == list(s)


def test_copy_is_independent() -> None:
    s = NodeStack(1, 2, 3)
    c = s.copy()
    c.push(99)
    assert len(s) == 3
    assert len(c) == 4


def test_copy_empty() -> None:
    s = NodeStack()
    c = s.copy()
    assert c.is_empty()


# ── is_empty / __bool__ / __len__ ─────────────────────────────────────────────


def test_is_empty_true() -> None:
    assert NodeStack().is_empty()


def test_is_empty_false() -> None:
    assert not NodeStack(1).is_empty()


def test_bool_empty() -> None:
    assert not bool(NodeStack())


def test_bool_not_empty() -> None:
    assert bool(NodeStack(1))


def test_len_empty() -> None:
    assert len(NodeStack()) == 0


def test_len_after_pushes() -> None:
    s = NodeStack(1, 2, 3)
    assert len(s) == 3


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_iter_top_to_bottom() -> None:
    s = NodeStack(1, 2, 3)
    assert list(s) == [3, 2, 1]


def test_iter_empty() -> None:
    assert list(NodeStack()) == []


def test_reversed_bottom_to_top() -> None:
    s = NodeStack(1, 2, 3)
    assert list(reversed(s)) == [1, 2, 3]


def test_reversed_empty() -> None:
    assert list(reversed(NodeStack())) == []


def test_iter_does_not_modify_stack() -> None:
    s = NodeStack(1, 2, 3)
    _ = list(s)
    assert len(s) == 3


def test_reversed_does_not_modify_stack() -> None:
    s = NodeStack(1, 2, 3)
    _ = list(reversed(s))
    assert len(s) == 3


# ── __contains__ ──────────────────────────────────────────────────────────────


def test_contains_existing() -> None:
    s = NodeStack(1, 2, 3)
    assert 2 in s


def test_contains_missing() -> None:
    s = NodeStack(1, 2, 3)
    assert 99 not in s


def test_contains_empty() -> None:
    assert 1 not in NodeStack()


def test_contains_none() -> None:
    s = NodeStack(None, 1)
    assert None in s


# ── __eq__ ────────────────────────────────────────────────────────────────────


def test_eq_equal_stacks() -> None:
    assert NodeStack(1, 2, 3) == NodeStack(1, 2, 3)


def test_eq_both_empty() -> None:
    assert NodeStack() == NodeStack()


def test_eq_different_elements() -> None:
    assert NodeStack(1, 2, 3) != NodeStack(1, 2, 9)


def test_eq_different_sizes() -> None:
    assert NodeStack(1, 2) != NodeStack(1, 2, 3)


def test_eq_not_implemented_for_other_type() -> None:
    assert NodeStack(1).__eq__([1]) is NotImplemented


# ── __repr__ ──────────────────────────────────────────────────────────────────


def test_repr_empty() -> None:
    assert repr(NodeStack()) == "NodeStack(size=0)[]"


def test_repr_single() -> None:
    assert repr(NodeStack(5)) == "NodeStack(size=1)[5]"


def test_repr_multiple() -> None:
    assert repr(NodeStack(1, 2, 3)) == "NodeStack(size=3)[3, 2, 1]"


def test_repr_with_strings() -> None:
    assert repr(NodeStack("a", "b")) == "NodeStack(size=2)['b', 'a']"
