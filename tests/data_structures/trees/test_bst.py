import pytest

from data_structures import BST

# ── Init ──────────────────────────────────────────────────────────────────────


def test_init_empty() -> None:
    t = BST()
    assert len(t) == 0
    assert t._root is None


def test_init_with_args() -> None:
    t = BST(5, 3, 7)
    assert len(t) == 3


def test_init_duplicates_ignored() -> None:
    t = BST(5, 5, 5)
    assert len(t) == 1


def test_init_sorted_order() -> None:
    t = BST(1, 2, 3, 4, 5)
    assert list(t) == [1, 2, 3, 4, 5]


# ── Insert ────────────────────────────────────────────────────────────────────


def test_insert_single() -> None:
    t = BST()
    t.insert(10)
    assert t._root.value == 10  # type: ignore[union-attr-assigment]


def test_insert_left() -> None:
    t = BST(10)
    t.insert(5)
    assert t._root.left.value == 5  # type: ignore[union-attr-assigment]


def test_insert_right() -> None:
    t = BST(10)
    t.insert(15)
    assert t._root.right.value == 15  # type: ignore[union-attr-assigment]


def test_insert_duplicate_ignored() -> None:
    t = BST(10)
    t.insert(10)
    assert len(t) == 1


def test_insert_sets_parent() -> None:
    t = BST(10)
    t.insert(5)
    assert t._root.left.parent is t._root  # type: ignore[union-attr-assigment]


def test_insert_increases_size() -> None:
    t = BST()
    for v in [5, 3, 7]:
        t.insert(v)
    assert len(t) == 3


# ── Remove ────────────────────────────────────────────────────────────────────


def test_remove_leaf() -> None:
    t = BST(5, 3, 7)
    t.remove(3)
    assert t._root.left is None  # type: ignore[union-attr-assigment]
    assert len(t) == 2


def test_remove_node_with_left_child() -> None:
    t = BST(5, 3, 7, 1)
    t.remove(3)
    assert t._root.left.value == 1  # type: ignore[union-attr-assigment]


def test_remove_node_with_right_child() -> None:
    t = BST(5, 3, 7, 4)
    t.remove(3)
    assert t._root.left.value == 4  # type: ignore[union-attr-assigment]


def test_remove_node_with_two_children() -> None:
    t = BST(5, 3, 7, 1, 4)
    t.remove(3)
    assert list(t) == [1, 4, 5, 7]  # type: ignore[union-attr-assigment]


def test_remove_root_no_children() -> None:
    t = BST(5)
    t.remove(5)
    assert t._root is None
    assert len(t) == 0


def test_remove_root_with_children() -> None:
    t = BST(5, 3, 7)
    t.remove(5)
    assert list(t) == [3, 7]


def test_remove_not_found_does_nothing() -> None:
    t = BST(5, 3, 7)
    t.remove(99)
    assert len(t) == 3


def test_remove_decreases_size() -> None:
    t = BST(5, 3, 7)
    t.remove(3)
    assert len(t) == 2


# ── Search ────────────────────────────────────────────────────────────────────


def test_search_existing() -> None:
    t = BST(5, 3, 7)
    assert t.search(3) is True


def test_search_missing() -> None:
    t = BST(5, 3, 7)
    assert t.search(99) is False


def test_search_empty() -> None:
    assert BST().search(1) is False


def test_search_root() -> None:
    t = BST(5)
    assert t.search(5) is True


# ── Min / Max ─────────────────────────────────────────────────────────────────


def test_min_returns_smallest() -> None:
    t = BST(5, 3, 7, 1, 4)
    assert t.min() == 1


def test_max_returns_largest() -> None:
    t = BST(5, 3, 7, 1, 4)
    assert t.max() == 7


def test_min_single_node() -> None:
    assert BST(5).min() == 5


def test_max_single_node() -> None:
    assert BST(5).max() == 5


def test_min_empty_raises() -> None:
    with pytest.raises(IndexError):
        BST().min()


def test_max_empty_raises() -> None:
    with pytest.raises(IndexError):
        BST().max()


# ── Height ────────────────────────────────────────────────────────────────────


def test_height_empty() -> None:
    assert BST().height() == -1


def test_height_single() -> None:
    assert BST(5).height() == 0


def test_height_balanced() -> None:
    t = BST(5, 3, 7)
    assert t.height() == 1


def test_height_degenerate() -> None:
    t = BST(1, 2, 3, 4, 5)
    assert t.height() == 4


# ── Traversals ────────────────────────────────────────────────────────────────


def test_inorder_sorted() -> None:
    t = BST(5, 3, 7, 1, 4)
    assert list(t.inorder()) == [1, 3, 4, 5, 7]


def test_inorder_empty() -> None:
    assert list(BST().inorder()) == []


def test_preorder_root_first() -> None:
    t = BST(5, 3, 7)
    result = list(t.preorder())
    assert result[0] == 5


def test_preorder_empty() -> None:
    assert list(BST().preorder()) == []


def test_postorder_root_last() -> None:
    t = BST(5, 3, 7)
    result = list(t.postorder())
    assert result[-1] == 5


def test_postorder_empty() -> None:
    assert list(BST().postorder()) == []


def test_level_order_root_first() -> None:
    t = BST(5, 3, 7)
    result = list(t.level_order())
    assert result[0] == 5


def test_level_order_by_levels() -> None:
    t = BST(5, 3, 7)
    assert list(t.level_order()) == [5, 3, 7]


def test_level_order_empty() -> None:
    assert list(BST().level_order()) == []


def test_preorder_reconstructs_structure() -> None:
    t = BST(5, 3, 7, 1, 4)
    copy = BST(*t.preorder())
    assert t == copy


# ── clear / copy ──────────────────────────────────────────────────────────────


def test_clear_empties_tree() -> None:
    t = BST(5, 3, 7)
    t.clear()
    assert len(t) == 0
    assert t._root is None


def test_copy_preserves_elements() -> None:
    t = BST(5, 3, 7)
    c = t.copy()
    assert list(c) == list(t)


def test_copy_preserves_structure() -> None:
    t = BST(5, 3, 7)
    assert t.copy() == t


def test_copy_is_independent() -> None:
    t = BST(5, 3, 7)
    c = t.copy()
    c.insert(99)
    assert len(t) == 3


# ── is_empty / __len__ / __bool__ ─────────────────────────────────────────────


def test_is_empty_true() -> None:
    assert BST().is_empty()


def test_is_empty_false() -> None:
    assert not BST(1).is_empty()


def test_bool_empty() -> None:
    assert not bool(BST())


def test_bool_not_empty() -> None:
    assert bool(BST(1))


# ── __iter__ / __reversed__ ───────────────────────────────────────────────────


def test_iter_sorted() -> None:
    t = BST(5, 3, 7, 1, 4)
    assert list(t) == [1, 3, 4, 5, 7]


def test_iter_empty() -> None:
    assert list(BST()) == []


def test_reversed_descending() -> None:
    t = BST(5, 3, 7)
    assert list(reversed(t)) == [7, 5, 3]


def test_reversed_empty() -> None:
    assert list(reversed(BST())) == []


# ── __contains__ ──────────────────────────────────────────────────────────────


def test_contains_existing() -> None:
    assert 3 in BST(5, 3, 7)


def test_contains_missing() -> None:
    assert 99 not in BST(5, 3, 7)


# ── __eq__ ────────────────────────────────────────────────────────────────────


def test_eq_same_structure() -> None:
    a = BST(5, 3, 7)
    b = BST(5, 3, 7)
    assert a == b


def test_eq_different_structure() -> None:
    a = BST(5, 3, 7)
    b = BST(3, 5, 7)
    assert a != b


def test_eq_different_elements() -> None:
    a = BST(5, 3, 7)
    b = BST(5, 3, 9)
    assert a != b


def test_eq_not_implemented_for_other_type() -> None:
    assert BST(1).__eq__([1]) is NotImplemented


# ── __repr__ ──────────────────────────────────────────────────────────────────


def test_repr_empty() -> None:
    assert repr(BST()) == "BST(size=0)[]"


def test_repr_with_elements() -> None:
    t = BST(5, 3, 7)
    assert repr(t) == "BST(size=3)[3, 5, 7]"
