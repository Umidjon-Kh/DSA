import pytest

from data_structures.heaps import NodeMaxHeap, NodeMinHeap

# ══════════════════════════════════════════════════════════════════════════════
# NodeMinHeap
# ══════════════════════════════════════════════════════════════════════════════

# ── Init ──────────────────────────────────────────────────────────────────────


def test_min_init_empty() -> None:
    h = NodeMinHeap()
    assert len(h) == 0
    assert h.is_empty()
    assert h._root is None


def test_min_init_with_args() -> None:
    h = NodeMinHeap(5, 3, 1)
    assert h.peek() == 1
    assert len(h) == 3


def test_min_init_single_arg() -> None:
    h = NodeMinHeap(42)
    assert h._root is not None
    assert h._root.value == 42


# ── Push ──────────────────────────────────────────────────────────────────────


def test_min_push_first_becomes_root() -> None:
    h = NodeMinHeap()
    h.push(7)
    assert h._root is not None
    assert h._root.value == 7


def test_min_push_smaller_becomes_root() -> None:
    h = NodeMinHeap()
    h.push(5)
    h.push(1)
    assert h.peek() == 1


def test_min_push_larger_does_not_change_root() -> None:
    h = NodeMinHeap()
    h.push(1)
    h.push(9)
    assert h.peek() == 1


def test_min_push_increments_size() -> None:
    h = NodeMinHeap()
    h.push(1)
    h.push(2)
    assert len(h) == 2


def test_min_push_parent_pointer_set() -> None:
    h = NodeMinHeap()
    h.push(5)
    h.push(3)
    assert h._root.left is not None  # type: ignore[union-attr]
    assert h._root.left.parent is h._root  # type: ignore[union-attr]


def test_min_push_right_child_on_odd_position() -> None:
    h = NodeMinHeap()
    h.push(5)
    h.push(3)
    h.push(7)
    assert h._root.right is not None  # type: ignore[union-attr]


def test_min_push_grows_large() -> None:
    h = NodeMinHeap()
    for i in range(100):
        h.push(i)
    assert len(h) == 100
    assert h.peek() == 0


# ── Pop ───────────────────────────────────────────────────────────────────────


def test_min_pop_returns_minimum() -> None:
    h = NodeMinHeap(5, 3, 8, 1)
    assert h.pop() == 1


def test_min_pop_reduces_size() -> None:
    h = NodeMinHeap(1, 2)
    h.pop()
    assert len(h) == 1


def test_min_pop_sequence_sorted() -> None:
    h = NodeMinHeap(5, 3, 8, 1, 4)
    result = [h.pop() for _ in range(5)]
    assert result == sorted(result)


def test_min_pop_empty_raises() -> None:
    with pytest.raises(IndexError):
        NodeMinHeap().pop()


def test_min_pop_single_element_clears_root() -> None:
    h = NodeMinHeap()
    h.push(7)
    assert h.pop() == 7
    assert h._root is None
    assert h._size == 0


def test_min_pop_last_node_detached() -> None:
    h = NodeMinHeap(1, 2, 3)
    h.pop()
    assert len(h) == 2
    assert h._root.left is not None  # type: ignore[union-attr]
    assert h._root.right is None  # type: ignore[union-attr]


# ── Peek ──────────────────────────────────────────────────────────────────────


def test_min_peek_does_not_remove() -> None:
    h = NodeMinHeap(1, 2, 3)
    h.peek()
    assert len(h) == 3


def test_min_peek_empty_raises() -> None:
    with pytest.raises(IndexError):
        NodeMinHeap().peek()


def test_min_peek_always_minimum() -> None:
    h = NodeMinHeap()
    for v in [9, 4, 7, 2, 6]:
        h.push(v)
    assert h.peek() == 2


# ── Heapify ───────────────────────────────────────────────────────────────────


def test_min_heapify_sets_correct_root() -> None:
    h = NodeMinHeap()
    h.heapify([9, 4, 7, 2, 6])
    assert h.peek() == 2


def test_min_heapify_appends_to_existing() -> None:
    h = NodeMinHeap()
    h.push(1)
    h.heapify([5, 3])
    assert len(h) == 3
    assert h.peek() == 1


def test_min_heapify_not_iterable_raises() -> None:
    with pytest.raises(TypeError):
        NodeMinHeap().heapify(42)  # type: ignore[arg-type]


# ── Ordered ───────────────────────────────────────────────────────────────────


def test_min_ordered_yields_sorted() -> None:
    h = NodeMinHeap(5, 3, 8, 1, 4)
    assert list(h.ordered()) == [1, 3, 4, 5, 8]


def test_min_ordered_does_not_modify() -> None:
    h = NodeMinHeap(3, 1, 2)
    list(h.ordered())
    assert len(h) == 3
    assert h.peek() == 1


# ── Clear / copy ──────────────────────────────────────────────────────────────


def test_min_clear_drops_root() -> None:
    h = NodeMinHeap(1, 2, 3)
    h.clear()
    assert h._root is None
    assert h._size == 0
    assert h.is_empty()


def test_min_copy_preserves_peek() -> None:
    h = NodeMinHeap(3, 1, 2)
    assert h.copy().peek() == h.peek()


def test_min_copy_is_independent() -> None:
    h = NodeMinHeap(1, 2)
    c = h.copy()
    c.push(0)
    assert len(h) == 2


# ── _find_node (bit-path) ─────────────────────────────────────────────────────


def test_min_find_node_root() -> None:
    h = NodeMinHeap(1)
    assert h._find_node(1) is h._root


def test_min_find_node_left_child() -> None:
    h = NodeMinHeap(1, 2)
    assert h._find_node(2) is h._root.left  # type: ignore[union-attr]


def test_min_find_node_right_child() -> None:
    h = NodeMinHeap(1, 2, 3)
    assert h._find_node(3) is h._root.right  # type: ignore[union-attr]


def test_min_find_node_deeper() -> None:
    h = NodeMinHeap(1, 2, 3, 4, 5)
    node = h._find_node(4)
    assert node is h._root.left.left  # type: ignore[union-attr]


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_min_iter_root_first() -> None:
    h = NodeMinHeap(3, 1, 2)
    assert list(h)[0] == 1


def test_min_iter_bfs_order() -> None:
    h = NodeMinHeap()
    h.push(1)
    h.push(3)
    h.push(2)
    values = list(h)
    assert values[0] == 1


def test_min_iter_empty() -> None:
    assert list(NodeMinHeap()) == []


def test_min_iter_does_not_modify() -> None:
    h = NodeMinHeap(1, 2, 3)
    list(h)
    assert len(h) == 3


def test_min_reversed() -> None:
    h = NodeMinHeap(3, 1, 2)
    fwd = list(h)
    rev = list(reversed(h))
    assert fwd == list(reversed(rev))


# ── __contains__ ──────────────────────────────────────────────────────────────


def test_min_contains_existing() -> None:
    assert 3 in NodeMinHeap(1, 2, 3)


def test_min_contains_missing() -> None:
    assert 99 not in NodeMinHeap(1, 2, 3)


def test_min_contains_empty() -> None:
    assert 1 not in NodeMinHeap()


# ── __eq__ / __repr__ ─────────────────────────────────────────────────────────


def test_min_eq_equal() -> None:
    a = NodeMinHeap(1, 2, 3)
    b = NodeMinHeap(1, 2, 3)
    assert a == b


def test_min_eq_different_size() -> None:
    a = NodeMinHeap(1, 2, 3)
    b = NodeMinHeap(1, 2)
    assert a != b


def test_min_eq_not_implemented() -> None:
    h = NodeMinHeap(1)
    assert h.__eq__([1]) is NotImplemented


def test_min_repr_empty() -> None:
    assert repr(NodeMinHeap()) == "NodeMinHeap(size=0)[]"


def test_min_repr_root_first() -> None:
    h = NodeMinHeap(3, 1, 2)
    r = repr(h)
    assert r.startswith("NodeMinHeap(size=3)[1")


# ══════════════════════════════════════════════════════════════════════════════
# NodeMaxHeap
# ══════════════════════════════════════════════════════════════════════════════

# ── Init ──────────────────────────────────────────────────────────────────────


def test_max_init_empty() -> None:
    h = NodeMaxHeap()
    assert h.is_empty()
    assert h._root is None


def test_max_init_with_args() -> None:
    h = NodeMaxHeap(1, 3, 5)
    assert h.peek() == 5


# ── Push ──────────────────────────────────────────────────────────────────────


def test_max_push_larger_becomes_root() -> None:
    h = NodeMaxHeap()
    h.push(3)
    h.push(9)
    assert h.peek() == 9


def test_max_push_smaller_does_not_change_root() -> None:
    h = NodeMaxHeap()
    h.push(9)
    h.push(1)
    assert h.peek() == 9


def test_max_push_grows_large() -> None:
    h = NodeMaxHeap()
    for i in range(100):
        h.push(i)
    assert len(h) == 100
    assert h.peek() == 99


# ── Pop ───────────────────────────────────────────────────────────────────────


def test_max_pop_returns_maximum() -> None:
    h = NodeMaxHeap(5, 3, 8, 1)
    assert h.pop() == 8


def test_max_pop_sequence_reverse_sorted() -> None:
    h = NodeMaxHeap(5, 3, 8, 1, 4)
    result = [h.pop() for _ in range(5)]
    assert result == sorted(result, reverse=True)


def test_max_pop_empty_raises() -> None:
    with pytest.raises(IndexError):
        NodeMaxHeap().pop()


def test_max_pop_single_element_clears_root() -> None:
    h = NodeMaxHeap()
    h.push(7)
    assert h.pop() == 7
    assert h._root is None
    assert h._size == 0


# ── Peek ──────────────────────────────────────────────────────────────────────


def test_max_peek_does_not_remove() -> None:
    h = NodeMaxHeap(1, 2, 3)
    h.peek()
    assert len(h) == 3


def test_max_peek_empty_raises() -> None:
    with pytest.raises(IndexError):
        NodeMaxHeap().peek()


# ── Heapify ───────────────────────────────────────────────────────────────────


def test_max_heapify_correct_root() -> None:
    h = NodeMaxHeap()
    h.heapify([1, 4, 7, 9, 2])
    assert h.peek() == 9


def test_max_heapify_appends_to_existing() -> None:
    h = NodeMaxHeap()
    h.push(10)
    h.heapify([5, 3])
    assert len(h) == 3
    assert h.peek() == 10


def test_max_heapify_not_iterable_raises() -> None:
    with pytest.raises(TypeError):
        NodeMaxHeap().heapify(42)  # type: ignore[arg-type]


# ── Ordered ───────────────────────────────────────────────────────────────────


def test_max_ordered_reverse_sorted() -> None:
    h = NodeMaxHeap(5, 3, 8, 1, 4)
    assert list(h.ordered()) == [8, 5, 4, 3, 1]


def test_max_ordered_does_not_modify() -> None:
    h = NodeMaxHeap(3, 1, 2)
    list(h.ordered())
    assert len(h) == 3


# ── Clear / copy ──────────────────────────────────────────────────────────────


def test_max_clear_drops_root() -> None:
    h = NodeMaxHeap(1, 2, 3)
    h.clear()
    assert h._root is None
    assert h._size == 0


def test_max_copy_preserves_peek() -> None:
    h = NodeMaxHeap(3, 1, 2)
    assert h.copy().peek() == h.peek()


def test_max_copy_independent() -> None:
    h = NodeMaxHeap(1, 2)
    c = h.copy()
    c.push(99)
    assert len(h) == 2


# ── _find_node (bit-path) ─────────────────────────────────────────────────────


def test_max_find_node_root() -> None:
    h = NodeMaxHeap(1)
    assert h._find_node(1) is h._root


def test_max_find_node_left_child() -> None:
    h = NodeMaxHeap(1, 2)
    assert h._find_node(2) is h._root.left  # type: ignore[union-attr]


def test_max_find_node_right_child() -> None:
    h = NodeMaxHeap(1, 2, 3)
    assert h._find_node(3) is h._root.right  # type: ignore[union-attr]


# ── __contains__ / __eq__ / __repr__ ─────────────────────────────────────────


def test_max_contains_existing() -> None:
    assert 8 in NodeMaxHeap(5, 3, 8)


def test_max_contains_missing() -> None:
    assert 99 not in NodeMaxHeap(1, 2, 3)


def test_max_eq_equal() -> None:
    a = NodeMaxHeap(1, 2, 3)
    b = NodeMaxHeap(1, 2, 3)
    assert a == b


def test_max_eq_not_implemented() -> None:
    h = NodeMaxHeap(1)
    assert h.__eq__([1]) is NotImplemented


def test_max_repr_empty() -> None:
    assert repr(NodeMaxHeap()) == "NodeMaxHeap(size=0)[]"


def test_max_repr_root_first() -> None:
    h = NodeMaxHeap(1, 3, 5)
    r = repr(h)
    assert r.startswith("NodeMaxHeap(size=3)[5")
