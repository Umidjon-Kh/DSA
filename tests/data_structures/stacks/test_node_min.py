import pytest

from data_structures import NodeMinStack

# ── Init ──────────────────────────────────────────────────────────────────────


def test_init_empty() -> None:
    s = NodeMinStack()
    assert s._size == 0
    assert s._min_size == 0
    assert s._head is None
    assert s._min_head is None


def test_init_default_key_is_identity() -> None:
    s = NodeMinStack()
    assert s._key(42) == 42


def test_init_custom_key_stored() -> None:
    s = NodeMinStack(key=lambda x: -x)
    assert s._key(5) == -5


def test_init_non_callable_key_raises() -> None:
    with pytest.raises(TypeError):
        NodeMinStack(key=42)  # type: ignore[arg-type]


def test_init_with_args_sets_size() -> None:
    s = NodeMinStack(3, 1, 2)
    assert s._size == 3


def test_init_with_args_sets_min() -> None:
    s = NodeMinStack(3, 1, 2)
    assert s.min() == 1


def test_init_key_none_treated_as_identity() -> None:
    s = NodeMinStack(key=None)
    s.push(7)
    assert s.min() == 7


# ── Push ──────────────────────────────────────────────────────────────────────


def test_push_first_value_enters_min() -> None:
    s = NodeMinStack()
    s.push(5)
    assert s._min_size == 1
    assert s._min_head.value == 5  # type: ignore[union-attr]


def test_push_lower_value_enters_min() -> None:
    s = NodeMinStack()
    s.push(5)
    s.push(3)
    assert s.min() == 3
    assert s._min_size == 2


def test_push_higher_value_does_not_enter_min() -> None:
    s = NodeMinStack()
    s.push(3)
    s.push(5)
    assert s.min() == 3
    assert s._min_size == 1


def test_push_equal_value_enters_min() -> None:
    s = NodeMinStack()
    s.push(3)
    s.push(3)
    assert s.min() == 3
    assert s._min_size == 2


def test_push_with_key() -> None:
    s = NodeMinStack(key=lambda x: x[1])
    s.push(("a", 5))
    s.push(("b", 2))
    s.push(("c", 8))
    assert s.min() == ("b", 2)
    assert s._min_size == 2


# ── Pop ───────────────────────────────────────────────────────────────────────


def test_pop_returns_top() -> None:
    s = NodeMinStack(1, 2, 3)
    assert s.pop() == 3


def test_pop_non_min_does_not_change_min() -> None:
    s = NodeMinStack(3, 1, 2)
    s.pop()  # pops 2
    assert s.min() == 1
    assert s._min_size == 2


def test_pop_min_removes_from_min_stack() -> None:
    s = NodeMinStack(3, 1, 2)
    s.pop()  # 2
    s.pop()  # 1 — this is min
    assert s.min() == 3
    assert s._min_size == 1


def test_pop_duplicate_min_removes_one() -> None:
    s = NodeMinStack(1, 1)
    s.pop()
    assert s.min() == 1
    assert s._min_size == 1


def test_pop_decrements_size() -> None:
    s = NodeMinStack(1, 2, 3)
    s.pop()
    assert s._size == 2


def test_pop_empty_raises() -> None:
    with pytest.raises(IndexError):
        NodeMinStack().pop()


def test_pop_all_leaves_empty_min() -> None:
    s = NodeMinStack(1, 2, 3)
    s.pop()
    s.pop()
    s.pop()
    assert s._min_size == 0
    assert s._min_head is None


# ── Peek / min ────────────────────────────────────────────────────────────────


def test_peek_returns_top_without_removing() -> None:
    s = NodeMinStack(1, 2, 3)
    assert s.peek() == 3
    assert len(s) == 3


def test_peek_empty_raises() -> None:
    with pytest.raises(IndexError):
        NodeMinStack().peek()


def test_min_returns_without_removing() -> None:
    s = NodeMinStack(3, 1, 2)
    s.min()
    assert len(s) == 3


def test_min_empty_raises() -> None:
    with pytest.raises(IndexError):
        NodeMinStack().min()


def test_min_tracks_correctly_after_sequence() -> None:
    s = NodeMinStack()
    for v in [5, 3, 8, 1, 6]:
        s.push(v)
    assert s.min() == 1
    s.pop()  # 6
    assert s.min() == 1
    s.pop()  # 1 — min
    assert s.min() == 3


# ── clear ─────────────────────────────────────────────────────────────────────


def test_clear_resets_both_stacks() -> None:
    s = NodeMinStack(1, 2, 3)
    s.clear()
    assert s._size == 0
    assert s._min_size == 0
    assert s._head is None
    assert s._min_head is None


# ── copy ──────────────────────────────────────────────────────────────────────


def test_copy_preserves_elements() -> None:
    s = NodeMinStack(3, 1, 2)
    c = s.copy()
    assert list(c) == list(s)


def test_copy_preserves_min() -> None:
    s = NodeMinStack(3, 1, 2)
    assert s.copy().min() == s.min()


def test_copy_preserves_key() -> None:
    s = NodeMinStack(1, 2, 3, key=lambda x: -x)
    c = s.copy()
    assert c._key(5) == -5


def test_copy_is_independent() -> None:
    s = NodeMinStack(3, 1, 2)
    c = s.copy()
    c.push(0)
    assert len(s) == 3
    assert c.min() == 0


# ── is_empty / __bool__ / __len__ ─────────────────────────────────────────────


def test_is_empty_true() -> None:
    assert NodeMinStack().is_empty()


def test_is_empty_false() -> None:
    assert not NodeMinStack(1).is_empty()


def test_bool_empty() -> None:
    assert not bool(NodeMinStack())


def test_bool_not_empty() -> None:
    assert bool(NodeMinStack(1))


def test_len_after_pushes() -> None:
    assert len(NodeMinStack(1, 2, 3)) == 3


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_iter_top_to_bottom() -> None:
    s = NodeMinStack(1, 2, 3)
    assert list(s) == [3, 2, 1]


def test_iter_empty() -> None:
    assert list(NodeMinStack()) == []


def test_reversed_bottom_to_top() -> None:
    s = NodeMinStack(1, 2, 3)
    assert list(reversed(s)) == [1, 2, 3]


def test_iter_does_not_modify() -> None:
    s = NodeMinStack(1, 2, 3)
    _ = list(s)
    assert len(s) == 3


# ── __contains__ ──────────────────────────────────────────────────────────────


def test_contains_existing() -> None:
    assert 2 in NodeMinStack(1, 2, 3)


def test_contains_missing() -> None:
    assert 99 not in NodeMinStack(1, 2, 3)


def test_contains_empty() -> None:
    assert 1 not in NodeMinStack()


# ── __eq__ ────────────────────────────────────────────────────────────────────


def test_eq_equal() -> None:
    assert NodeMinStack(1, 2, 3) == NodeMinStack(1, 2, 3)


def test_eq_both_empty() -> None:
    assert NodeMinStack() == NodeMinStack()


def test_eq_different_elements() -> None:
    assert NodeMinStack(1, 2, 3) != NodeMinStack(1, 2, 9)


def test_eq_different_sizes() -> None:
    assert NodeMinStack(1, 2) != NodeMinStack(1, 2, 3)


def test_eq_not_implemented_for_other_type() -> None:
    assert NodeMinStack(1).__eq__([1]) is NotImplemented


# ── __repr__ ──────────────────────────────────────────────────────────────────


def test_repr_empty() -> None:
    assert repr(NodeMinStack()) == "NodeMinStack(size=0, min=None)[]"


def test_repr_single() -> None:
    assert repr(NodeMinStack(5)) == "NodeMinStack(size=1, min=5)[5]"


def test_repr_multiple() -> None:
    assert repr(NodeMinStack(3, 1, 2)) == "NodeMinStack(size=3, min=1)[2, 1, 3]"
