import pytest

from data_structures import ChainingHashMap

# ══════════════════════════════════════════════════════════════════════════════
# Init
# ══════════════════════════════════════════════════════════════════════════════


def test_init_empty() -> None:
    m = ChainingHashMap()
    assert len(m) == 0
    assert not m


def test_init_with_pairs() -> None:
    m = ChainingHashMap(("name", "Umidjon"), ("age", 25))
    assert len(m) == 2


def test_init_single_pair() -> None:
    m = ChainingHashMap(("x", 1))
    assert m.get("x") == 1


def test_init_preserves_all_values() -> None:
    m = ChainingHashMap(("a", 1), ("b", 2), ("c", 3))
    assert m.get("a") == 1
    assert m.get("b") == 2
    assert m.get("c") == 3


# ══════════════════════════════════════════════════════════════════════════════
# Insert
# ══════════════════════════════════════════════════════════════════════════════


def test_insert_increases_size() -> None:
    m = ChainingHashMap()
    m.insert("key", "value")
    assert len(m) == 1


def test_insert_new_key() -> None:
    m = ChainingHashMap()
    m.insert("name", "Umidjon")
    assert m.get("name") == "Umidjon"


def test_insert_updates_existing_key() -> None:
    m = ChainingHashMap()
    m.insert("key", "old")
    m.insert("key", "new")
    assert m.get("key") == "new"
    assert len(m) == 1


def test_insert_does_not_increase_size_on_update() -> None:
    m = ChainingHashMap()
    m.insert("key", 1)
    m.insert("key", 2)
    assert len(m) == 1


def test_insert_int_key() -> None:
    m = ChainingHashMap()
    m.insert(42, "answer")
    assert m.get(42) == "answer"


def test_insert_tuple_key() -> None:
    m = ChainingHashMap()
    m.insert((1, 2), "pair")
    assert m.get((1, 2)) == "pair"


def test_insert_none_value() -> None:
    m = ChainingHashMap()
    m.insert("key", None)
    assert m.get("key") is None
    assert len(m) == 1


def test_insert_unhashable_key_raises() -> None:
    m = ChainingHashMap()
    with pytest.raises(TypeError):
        m.insert([1, 2], "value")


def test_insert_triggers_resize() -> None:
    m = ChainingHashMap()
    for i in range(20):
        m.insert(i, i * 10)
    assert len(m) == 20
    for i in range(20):
        assert m.get(i) == i * 10


# ══════════════════════════════════════════════════════════════════════════════
# Get
# ══════════════════════════════════════════════════════════════════════════════


def test_get_existing_key() -> None:
    m = ChainingHashMap(("k", 99))
    assert m.get("k") == 99


def test_get_missing_key_returns_none() -> None:
    m = ChainingHashMap()
    assert m.get("missing") is None


def test_get_missing_key_returns_default() -> None:
    m = ChainingHashMap()
    assert m.get("missing", "fallback") == "fallback"


def test_get_after_update() -> None:
    m = ChainingHashMap()
    m.insert("x", 1)
    m.insert("x", 2)
    assert m.get("x") == 2


# ══════════════════════════════════════════════════════════════════════════════
# Delete
# ══════════════════════════════════════════════════════════════════════════════


def test_delete_existing_key() -> None:
    m = ChainingHashMap(("a", 1), ("b", 2))
    m.delete("a")
    assert not m.contains("a")
    assert len(m) == 1


def test_delete_decreases_size() -> None:
    m = ChainingHashMap(("a", 1))
    m.delete("a")
    assert len(m) == 0


def test_delete_missing_key_does_nothing() -> None:
    m = ChainingHashMap(("a", 1))
    m.delete("missing")
    assert len(m) == 1


def test_delete_only_element() -> None:
    m = ChainingHashMap(("only", 0))
    m.delete("only")
    assert not m


def test_delete_does_not_affect_other_keys() -> None:
    m = ChainingHashMap(("a", 1), ("b", 2), ("c", 3))
    m.delete("b")
    assert m.get("a") == 1
    assert m.get("c") == 3


# ══════════════════════════════════════════════════════════════════════════════
# Contains
# ══════════════════════════════════════════════════════════════════════════════


def test_contains_existing_key() -> None:
    m = ChainingHashMap(("k", 1))
    assert m.contains("k") is True


def test_contains_missing_key() -> None:
    m = ChainingHashMap()
    assert m.contains("x") is False


def test_contains_after_delete() -> None:
    m = ChainingHashMap(("k", 1))
    m.delete("k")
    assert m.contains("k") is False


def test_contains_after_insert() -> None:
    m = ChainingHashMap()
    m.insert("new", 42)
    assert m.contains("new") is True


# ══════════════════════════════════════════════════════════════════════════════
# Setdefault
# ══════════════════════════════════════════════════════════════════════════════


def test_setdefault_returns_existing_value() -> None:
    m = ChainingHashMap(("k", 10))
    assert m.setdefault("k", 99) == 10


def test_setdefault_inserts_and_returns_default() -> None:
    m = ChainingHashMap()
    result = m.setdefault("new", 42)
    assert result == 42
    assert m.get("new") == 42


def test_setdefault_does_not_overwrite() -> None:
    m = ChainingHashMap(("k", 10))
    m.setdefault("k", 99)
    assert m.get("k") == 10


def test_setdefault_none_default() -> None:
    m = ChainingHashMap()
    result = m.setdefault("k")
    assert result is None
    assert m.contains("k")


# ══════════════════════════════════════════════════════════════════════════════
# Keys / Values / Items
# ══════════════════════════════════════════════════════════════════════════════


def test_keys_yields_all_keys() -> None:
    m = ChainingHashMap(("a", 1), ("b", 2), ("c", 3))
    assert set(m.keys()) == {"a", "b", "c"}


def test_values_yields_all_values() -> None:
    m = ChainingHashMap(("a", 1), ("b", 2), ("c", 3))
    assert set(m.values()) == {1, 2, 3}


def test_items_yields_all_pairs() -> None:
    m = ChainingHashMap(("a", 1), ("b", 2))
    assert set(m.items()) == {("a", 1), ("b", 2)}


def test_keys_empty_map() -> None:
    assert list(ChainingHashMap().keys()) == []


def test_values_empty_map() -> None:
    assert list(ChainingHashMap().values()) == []


def test_items_empty_map() -> None:
    assert list(ChainingHashMap().items()) == []


# ══════════════════════════════════════════════════════════════════════════════
# Clear / Copy / Deepcopy
# ══════════════════════════════════════════════════════════════════════════════


def test_clear_empties_map() -> None:
    m = ChainingHashMap(("a", 1), ("b", 2))
    m.clear()
    assert len(m) == 0
    assert not m


def test_clear_resets_capacity() -> None:
    m = ChainingHashMap(("a", 1))
    m.clear()
    assert m._capacity == 11


def test_copy_preserves_pairs() -> None:
    m = ChainingHashMap(("a", 1), ("b", 2))
    c = m.copy()
    assert c.get("a") == 1
    assert c.get("b") == 2


def test_copy_is_independent() -> None:
    m = ChainingHashMap(("a", 1))
    c = m.copy()
    c.insert("b", 2)
    assert not m.contains("b")


def test_copy_does_not_share_mutations() -> None:
    m = ChainingHashMap(("a", 1))
    c = m.copy()
    c.delete("a")
    assert m.contains("a")


def test_deepcopy_is_independent() -> None:
    m = ChainingHashMap(("a", 1))
    d = m.deepcopy()
    d.insert("b", 99)
    assert not m.contains("b")


def test_deepcopy_nested_list() -> None:
    m = ChainingHashMap(("data", [1, 2, 3]))
    d = m.deepcopy()
    d.get("data").append(99)
    assert m.get("data") == [1, 2, 3]


# ══════════════════════════════════════════════════════════════════════════════
# is_empty / __len__ / __bool__
# ══════════════════════════════════════════════════════════════════════════════


def test_is_empty_true() -> None:
    assert not ChainingHashMap()


def test_is_empty_false() -> None:
    assert ChainingHashMap(("a", 1))


def test_bool_empty() -> None:
    assert not bool(ChainingHashMap())


def test_bool_not_empty() -> None:
    assert bool(ChainingHashMap(("a", 1)))


def test_len_empty() -> None:
    assert len(ChainingHashMap()) == 0


def test_len_after_inserts() -> None:
    m = ChainingHashMap()
    m.insert("a", 1)
    m.insert("b", 2)
    assert len(m) == 2


# ══════════════════════════════════════════════════════════════════════════════
# __getitem__ / __setitem__ / __delitem__
# ══════════════════════════════════════════════════════════════════════════════


def test_getitem_existing() -> None:
    m = ChainingHashMap(("k", 42))
    assert m["k"] == 42


def test_getitem_missing_raises() -> None:
    m = ChainingHashMap()
    with pytest.raises(KeyError):
        _ = m["missing"]


def test_setitem_inserts() -> None:
    m = ChainingHashMap()
    m["key"] = "value"
    assert m["key"] == "value"


def test_setitem_updates() -> None:
    m = ChainingHashMap(("k", 1))
    m["k"] = 99
    assert m["k"] == 99
    assert len(m) == 1


def test_delitem_removes() -> None:
    m = ChainingHashMap(("k", 1))
    del m["k"]
    assert not m.contains("k")


def test_delitem_missing_does_nothing() -> None:
    m = ChainingHashMap(("k", 1))
    del m["missing"]
    assert len(m) == 1


# ══════════════════════════════════════════════════════════════════════════════
# __iter__ / __reversed__ / __contains__
# ══════════════════════════════════════════════════════════════════════════════


def test_iter_yields_values() -> None:
    m = ChainingHashMap(("a", 1), ("b", 2))
    assert set(m) == {1, 2}


def test_iter_empty() -> None:
    assert list(ChainingHashMap()) == []


def test_reversed_yields_values() -> None:
    m = ChainingHashMap(("a", 1), ("b", 2))
    assert set(reversed(m)) == {1, 2}


def test_contains_existing() -> None:
    assert "a" in ChainingHashMap(("a", 1))


def test_contains_missing() -> None:
    assert "z" not in ChainingHashMap(("a", 1))


# ══════════════════════════════════════════════════════════════════════════════
# __eq__
# ══════════════════════════════════════════════════════════════════════════════


def test_eq_same_pairs() -> None:
    a = ChainingHashMap(("x", 1), ("y", 2))
    b = ChainingHashMap(("x", 1), ("y", 2))
    assert a == b


def test_eq_both_empty() -> None:
    assert ChainingHashMap() == ChainingHashMap()


def test_eq_different_values() -> None:
    a = ChainingHashMap(("x", 1))
    b = ChainingHashMap(("x", 99))
    assert a != b


def test_eq_different_keys() -> None:
    a = ChainingHashMap(("a", 1))
    b = ChainingHashMap(("b", 1))
    assert a != b


def test_eq_different_size() -> None:
    a = ChainingHashMap(("a", 1), ("b", 2))
    b = ChainingHashMap(("a", 1))
    assert a != b


def test_eq_not_implemented_for_other_type() -> None:
    assert ChainingHashMap().__eq__({"a": 1}) is NotImplemented


# ══════════════════════════════════════════════════════════════════════════════
# __repr__
# ══════════════════════════════════════════════════════════════════════════════


def test_repr_empty() -> None:
    assert repr(ChainingHashMap()) == "ChainingHashMap(size=0){}"


def test_repr_contains_size() -> None:
    m = ChainingHashMap(("a", 1))
    assert "size=1" in repr(m)


def test_repr_contains_key_value() -> None:
    m = ChainingHashMap(("name", "Umidjon"))
    r = repr(m)
    assert "'name'" in r
    assert "'Umidjon'" in r
