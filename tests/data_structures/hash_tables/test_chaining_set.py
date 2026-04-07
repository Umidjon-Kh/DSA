import pytest

from data_structures import ChainingHashSet

# ══════════════════════════════════════════════════════════════════════════════
# Init
# ══════════════════════════════════════════════════════════════════════════════


def test_init_empty() -> None:
    s = ChainingHashSet()
    assert len(s) == 0
    assert not s


def test_init_with_keys() -> None:
    s = ChainingHashSet("a", "b", "c")
    assert len(s) == 3


def test_init_deduplicates() -> None:
    s = ChainingHashSet(1, 2, 2, 3)
    assert len(s) == 3


def test_init_preserves_all_keys() -> None:
    s = ChainingHashSet("x", "y", "z")
    assert s.contains("x")
    assert s.contains("y")
    assert s.contains("z")


def test_init_mixed_types() -> None:
    s = ChainingHashSet(1, "two", (3, 4))
    assert len(s) == 3


# ══════════════════════════════════════════════════════════════════════════════
# Add
# ══════════════════════════════════════════════════════════════════════════════


def test_add_increases_size() -> None:
    s = ChainingHashSet()
    s.add("key")
    assert len(s) == 1


def test_add_new_key() -> None:
    s = ChainingHashSet()
    s.add("hello")
    assert s.contains("hello")


def test_add_duplicate_does_nothing() -> None:
    s = ChainingHashSet()
    s.add("key")
    s.add("key")
    assert len(s) == 1


def test_add_int_key() -> None:
    s = ChainingHashSet()
    s.add(42)
    assert s.contains(42)


def test_add_tuple_key() -> None:
    s = ChainingHashSet()
    s.add((1, 2))
    assert s.contains((1, 2))


def test_add_unhashable_raises() -> None:
    s = ChainingHashSet()
    with pytest.raises(TypeError):
        s.add([1, 2, 3])


def test_add_triggers_resize() -> None:
    s = ChainingHashSet()
    for i in range(20):
        s.add(i)
    assert len(s) == 20
    for i in range(20):
        assert s.contains(i)


def test_add_bool_key() -> None:
    s = ChainingHashSet()
    s.add(True)
    assert s.contains(True)


# ══════════════════════════════════════════════════════════════════════════════
# Remove
# ══════════════════════════════════════════════════════════════════════════════


def test_remove_existing_key() -> None:
    s = ChainingHashSet("a", "b")
    s.remove("a")
    assert not s.contains("a")
    assert len(s) == 1


def test_remove_decreases_size() -> None:
    s = ChainingHashSet("a")
    s.remove("a")
    assert len(s) == 0


def test_remove_missing_does_nothing() -> None:
    s = ChainingHashSet("a")
    s.remove("missing")
    assert len(s) == 1


def test_remove_only_element() -> None:
    s = ChainingHashSet("only")
    s.remove("only")
    assert not s


def test_remove_does_not_affect_other_keys() -> None:
    s = ChainingHashSet("a", "b", "c")
    s.remove("b")
    assert s.contains("a")
    assert s.contains("c")


# ══════════════════════════════════════════════════════════════════════════════
# Contains
# ══════════════════════════════════════════════════════════════════════════════


def test_contains_existing_key() -> None:
    s = ChainingHashSet("k")
    assert s.contains("k") is True


def test_contains_missing_key() -> None:
    s = ChainingHashSet()
    assert s.contains("x") is False


def test_contains_after_remove() -> None:
    s = ChainingHashSet("k")
    s.remove("k")
    assert s.contains("k") is False


def test_contains_after_add() -> None:
    s = ChainingHashSet()
    s.add("new")
    assert s.contains("new") is True


# ══════════════════════════════════════════════════════════════════════════════
# Clear / Copy
# ══════════════════════════════════════════════════════════════════════════════


def test_clear_empties_set() -> None:
    s = ChainingHashSet("a", "b", "c")
    s.clear()
    assert len(s) == 0
    assert not s


def test_clear_resets_capacity() -> None:
    s = ChainingHashSet("a")
    s.clear()
    assert s._capacity == 11


def test_copy_preserves_keys() -> None:
    s = ChainingHashSet("a", "b")
    c = s.copy()
    assert c.contains("a")
    assert c.contains("b")


def test_copy_is_independent() -> None:
    s = ChainingHashSet("a")
    c = s.copy()
    c.add("b")
    assert not s.contains("b")


def test_copy_remove_does_not_affect_original() -> None:
    s = ChainingHashSet("a", "b")
    c = s.copy()
    c.remove("a")
    assert s.contains("a")


def test_copy_same_size() -> None:
    s = ChainingHashSet(1, 2, 3)
    assert len(s.copy()) == 3


# ══════════════════════════════════════════════════════════════════════════════
# is_empty / __len__ / __bool__
# ══════════════════════════════════════════════════════════════════════════════


def test_is_empty_true() -> None:
    assert not ChainingHashSet()


def test_is_empty_false() -> None:
    assert ChainingHashSet("a")


def test_bool_empty() -> None:
    assert not bool(ChainingHashSet())


def test_bool_not_empty() -> None:
    assert bool(ChainingHashSet("a"))


def test_len_empty() -> None:
    assert len(ChainingHashSet()) == 0


def test_len_after_adds() -> None:
    s = ChainingHashSet()
    s.add("a")
    s.add("b")
    assert len(s) == 2


# ══════════════════════════════════════════════════════════════════════════════
# __delitem__
# ══════════════════════════════════════════════════════════════════════════════


def test_delitem_removes() -> None:
    s = ChainingHashSet("k")
    del s["k"]
    assert not s.contains("k")


def test_delitem_missing_does_nothing() -> None:
    s = ChainingHashSet("k")
    del s["missing"]
    assert len(s) == 1


# ══════════════════════════════════════════════════════════════════════════════
# __iter__ / __reversed__ / __contains__
# ══════════════════════════════════════════════════════════════════════════════


def test_iter_yields_all_keys() -> None:
    s = ChainingHashSet("a", "b", "c")
    assert set(s) == {"a", "b", "c"}


def test_iter_empty() -> None:
    assert list(ChainingHashSet()) == []


def test_reversed_yields_all_keys() -> None:
    s = ChainingHashSet("a", "b", "c")
    assert set(reversed(s)) == {"a", "b", "c"}


def test_iter_does_not_modify() -> None:
    s = ChainingHashSet(1, 2, 3)
    _ = list(s)
    assert len(s) == 3


def test_contains_existing() -> None:
    assert "a" in ChainingHashSet("a", "b")


def test_contains_missing() -> None:
    assert "z" not in ChainingHashSet("a", "b")


# ══════════════════════════════════════════════════════════════════════════════
# __eq__
# ══════════════════════════════════════════════════════════════════════════════


def test_eq_same_keys() -> None:
    a = ChainingHashSet(1, 2, 3)
    b = ChainingHashSet(1, 2, 3)
    assert a == b


def test_eq_both_empty() -> None:
    assert ChainingHashSet() == ChainingHashSet()


def test_eq_different_keys() -> None:
    a = ChainingHashSet(1, 2)
    b = ChainingHashSet(1, 9)
    assert a != b


def test_eq_different_size() -> None:
    a = ChainingHashSet(1, 2, 3)
    b = ChainingHashSet(1, 2)
    assert a != b


def test_eq_order_does_not_matter() -> None:
    a = ChainingHashSet(1, 2, 3)
    b = ChainingHashSet(3, 1, 2)
    assert a == b


def test_eq_not_implemented_for_other_type() -> None:
    assert ChainingHashSet().__eq__({1, 2}) is NotImplemented


# ══════════════════════════════════════════════════════════════════════════════
# __repr__
# ══════════════════════════════════════════════════════════════════════════════


def test_repr_empty() -> None:
    assert repr(ChainingHashSet()) == "ChainingHashSet(size=0){}"


def test_repr_contains_size() -> None:
    s = ChainingHashSet("a")
    assert "size=1" in repr(s)


def test_repr_contains_key() -> None:
    s = ChainingHashSet("hello")
    assert "'hello'" in repr(s)
