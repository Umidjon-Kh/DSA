import pytest

from data_structures import AVLTree

# ── Init ──────────────────────────────────────────────────────────────────────


def test_init_empty() -> None:
    t = AVLTree()
    assert len(t) == 0
    assert t._root is None


def test_init_with_args() -> None:
    t = AVLTree(5, 3, 7)
    assert len(t) == 3


def test_init_duplicates_ignored() -> None:
    t = AVLTree(5, 5, 5)
    assert len(t) == 1


def test_init_sorted_order_stays_balanced() -> None:
    t = AVLTree(1, 2, 3, 4, 5)
    assert t.height() <= 3


# ── Insert ────────────────────────────────────────────────────────────────────


def test_insert_single() -> None:
    t = AVLTree()
    t.insert(10)
    assert t._root.value == 10  # type: ignore[union-attr-assigment]


def test_insert_duplicate_ignored() -> None:
    t = AVLTree(10)
    t.insert(10)
    assert len(t) == 1


def test_insert_increases_size() -> None:
    t = AVLTree()
    for v in [5, 3, 7]:
        t.insert(v)
    assert len(t) == 3


def test_insert_sorted_stays_balanced() -> None:
    t = AVLTree()
    for v in range(1, 8):
        t.insert(v)
    assert t.height() <= 3


def test_insert_reverse_sorted_stays_balanced() -> None:
    t = AVLTree()
    for v in range(7, 0, -1):
        t.insert(v)
    assert t.height() <= 3


def test_insert_triggers_rotate_left() -> None:
    t = AVLTree(1, 2, 3)
    assert t._root.value == 2  # type: ignore[union-attr-assigment]
    assert t.height() == 1


def test_insert_triggers_rotate_right() -> None:
    t = AVLTree(3, 2, 1)
    assert t._root.value == 2  # type: ignore[union-attr-assigment]
    assert t.height() == 1


def test_insert_triggers_left_right_rotation() -> None:
    t = AVLTree(3, 1, 2)
    assert t._root.value == 2  # type: ignore[union-attr-assigment]
    assert t.height() == 1


def test_insert_triggers_right_left_rotation() -> None:
    t = AVLTree(1, 3, 2)
    assert t._root.value == 2  # type: ignore[union-attr-assigment]
    assert t.height() == 1


# ── Balance factor invariant ──────────────────────────────────────────────────


def _check_balance(node) -> bool:
    if node is None:
        return True
    bf = (node.left.height if node.left else -1) - (
        node.right.height if node.right else -1
    )
    if abs(bf) > 1:
        return False
    return _check_balance(node.left) and _check_balance(node.right)


def test_balance_after_many_inserts() -> None:
    t = AVLTree()
    for v in [10, 5, 15, 3, 7, 12, 20, 1, 4]:
        t.insert(v)
    assert _check_balance(t._root)


def test_balance_after_inserts_and_removes() -> None:
    t = AVLTree()
    for v in range(1, 16):
        t.insert(v)
    for v in [3, 7, 11, 14]:
        t.remove(v)
    assert _check_balance(t._root)


# ── Remove ────────────────────────────────────────────────────────────────────


def test_remove_leaf() -> None:
    t = AVLTree(5, 3, 7)
    t.remove(3)
    assert 3 not in t
    assert len(t) == 2


def test_remove_node_with_two_children() -> None:
    t = AVLTree(5, 3, 7, 1, 4)
    t.remove(3)
    assert list(t) == [1, 4, 5, 7]


def test_remove_root() -> None:
    t = AVLTree(5, 3, 7)
    t.remove(5)
    assert list(t) == [3, 7]


def test_remove_not_found_does_nothing() -> None:
    t = AVLTree(5, 3, 7)
    t.remove(99)
    assert len(t) == 3


def test_remove_rebalances() -> None:
    t = AVLTree(1, 2, 3, 4, 5, 6, 7)
    t.remove(7)
    t.remove(6)
    assert _check_balance(t._root)


def test_remove_all_one_by_one() -> None:
    t = AVLTree(5, 3, 7)
    for v in [5, 3, 7]:
        t.remove(v)
    assert len(t) == 0
    assert t._root is None


# ── Search ────────────────────────────────────────────────────────────────────


def test_search_existing() -> None:
    assert AVLTree(5, 3, 7).search(3) is True


def test_search_missing() -> None:
    assert AVLTree(5, 3, 7).search(99) is False


def test_search_empty() -> None:
    assert AVLTree().search(1) is False


# ── Min / Max ─────────────────────────────────────────────────────────────────


def test_min_returns_smallest() -> None:
    assert AVLTree(5, 3, 7, 1, 4).min() == 1


def test_max_returns_largest() -> None:
    assert AVLTree(5, 3, 7, 1, 4).max() == 7


def test_min_empty_raises() -> None:
    with pytest.raises(IndexError):
        AVLTree().min()


def test_max_empty_raises() -> None:
    with pytest.raises(IndexError):
        AVLTree().max()


# ── Height ────────────────────────────────────────────────────────────────────


def test_height_empty() -> None:
    assert AVLTree().height() == -1


def test_height_single() -> None:
    assert AVLTree(5).height() == 0


def test_height_three_nodes() -> None:
    assert AVLTree(5, 3, 7).height() == 1


def test_height_is_o1() -> None:
    t = AVLTree()
    for v in range(1000):
        t.insert(v)
    assert t.height() == t._root.height  # type: ignore[union-attr-assigment]


# ── Traversals ────────────────────────────────────────────────────────────────


def test_inorder_sorted() -> None:
    t = AVLTree(5, 3, 7, 1, 4)
    assert list(t.inorder()) == [1, 3, 4, 5, 7]


def test_inorder_empty() -> None:
    assert list(AVLTree().inorder()) == []


def test_preorder_root_first() -> None:
    t = AVLTree(5, 3, 7)
    assert list(t.preorder())[0] == t._root.value  # type: ignore[union-attr-assigment]


def test_postorder_root_last() -> None:
    t = AVLTree(5, 3, 7)
    assert list(t.postorder())[-1] == t._root.value  # type: ignore[union-attr-assigment]


def test_level_order_root_first() -> None:
    t = AVLTree(5, 3, 7)
    assert list(t.level_order())[0] == t._root.value  # type: ignore[union-attr-assigment]


def test_all_traversals_contain_same_elements() -> None:
    t = AVLTree(5, 3, 7, 1, 4)
    elements = {1, 3, 4, 5, 7}
    assert set(t.inorder()) == elements
    assert set(t.preorder()) == elements
    assert set(t.postorder()) == elements
    assert set(t.level_order()) == elements


# ── clear / copy ──────────────────────────────────────────────────────────────


def test_clear_empties_tree() -> None:
    t = AVLTree(5, 3, 7)
    t.clear()
    assert len(t) == 0
    assert t._root is None


def test_copy_preserves_elements() -> None:
    t = AVLTree(5, 3, 7)
    assert list(t.copy()) == list(t)


def test_copy_preserves_structure() -> None:
    t = AVLTree(5, 3, 7)
    assert t.copy() == t


def test_copy_is_independent() -> None:
    t = AVLTree(5, 3, 7)
    c = t.copy()
    c.insert(99)
    assert len(t) == 3


# ── is_empty / __len__ / __bool__ ─────────────────────────────────────────────


def test_is_empty_true() -> None:
    assert AVLTree().is_empty()


def test_is_empty_false() -> None:
    assert not AVLTree(1).is_empty()


def test_bool_empty() -> None:
    assert not bool(AVLTree())


def test_bool_not_empty() -> None:
    assert bool(AVLTree(1))


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_iter_sorted() -> None:
    t = AVLTree(5, 3, 7, 1, 4)
    assert list(t) == [1, 3, 4, 5, 7]


def test_iter_empty() -> None:
    assert list(AVLTree()) == []


def test_reversed_descending() -> None:
    t = AVLTree(5, 3, 7)
    assert list(reversed(t)) == sorted([5, 3, 7], reverse=True)


def test_reversed_empty() -> None:
    assert list(reversed(AVLTree())) == []


# ── __contains__ ──────────────────────────────────────────────────────────────


def test_contains_existing() -> None:
    assert 3 in AVLTree(5, 3, 7)


def test_contains_missing() -> None:
    assert 99 not in AVLTree(5, 3, 7)


# ── __eq__ ────────────────────────────────────────────────────────────────────


def test_eq_same() -> None:
    a = AVLTree(5, 3, 7)
    b = AVLTree(5, 3, 7)
    assert a == b


def test_eq_different_elements() -> None:
    a = AVLTree(5, 3, 7)
    b = AVLTree(5, 3, 9)
    assert a != b


def test_eq_not_implemented_for_other_type() -> None:
    assert AVLTree(1).__eq__([1]) is NotImplemented


# ── __repr__ ──────────────────────────────────────────────────────────────────


def test_repr_empty() -> None:
    assert repr(AVLTree()) == "AVLTree(size=0, height=-1)[]"


def test_repr_with_elements() -> None:
    t = AVLTree(5, 3, 7)
    assert repr(t) == "AVLTree(size=3, height=1)[3, 5, 7]"
