import pytest

from data_structures import OpenAddressingHashMap

# ══════════════════════════════════════════════════════════════════════════════
# Init
# ══════════════════════════════════════════════════════════════════════════════


def test_init_empty() -> None:
    m = OpenAddressingHashMap()
    assert len(m) == 0
    assert not m


def test_init_with_pairs() -> None:
    m = OpenAddressingHashMap(("name", "Umidjon"), ("age", 25))
    assert len(m) == 2


def test_init_single_pair() -> None:
    m = OpenAddressingHashMap(("x", 1))
    assert m.get("x") == 1


def test_init_preserves_all_values() -> None:
    m = OpenAddressingHashMap(("a", 1), ("b", 2), ("c", 3))
    assert m.get("a") == 1
    assert m.get("b") == 2
    assert m.get("c") == 3


# ══════════════════════════════════════════════════════════════════════════════
# Insert
# ══════════════════════════════════════════════════════════════════════════════


def test_insert_increases_size() -> None:
    m = OpenAddressingHashMap()
    m.insert("key", "value")
    assert len(m) == 1


def test_insert_new_key() -> None:
    m = OpenAddressingHashMap()
    m.insert("name", "Umidjon")
    assert m.get("name") == "Umidjon"


def test_insert_updates_existing_key() -> None:
    m = OpenAddressingHashMap()
    m.insert("key", "old")
    m.insert("key", "new")
    assert m.get("key") == "new"
    assert len(m) == 1


def test_insert_does_not_increase_size_on_update() -> None:
    m = OpenAddressingHashMap()
    m.insert("key", 1)
    m.insert("key", 2)
    assert len(m) == 1


def test_insert_int_key() -> None:
    m = OpenAddressingHashMap()
    m.insert(42, "answer")
    assert m.get(42) == "answer"


def test_insert_tuple_key() -> None:
    m = OpenAddressingHashMap()
    m.insert((1, 2), "pair")
    assert m.get((1, 2)) == "pair"


def test_insert_none_value() -> None:
    m = OpenAddressingHashMap()
    m.insert("key", None)
    assert m.get("key") is None
    assert len(m) == 1


def test_insert_unhashable_key_raises() -> None:
    m = OpenAddressingHashMap()
    with pytest.raises(TypeError):
        m.insert([1, 2], "value")


def test_insert_triggers_resize() -> None:
    m = OpenAddressingHashMap()
    for i in range(20):
        m.insert(i, i * 10)
    assert len(m) == 20
    for i in range(20):
        assert m.get(i) == i * 10


# ══════════════════════════════════════════════════════════════════════════════
# Get
# ══════════════════════════════════════════════════════════════════════════════


def test_get_existing_key() -> None:
    m = OpenAddressingHashMap(("k", 99))
    assert m.get("k") == 99


def test_get_missing_key_returns_none() -> None:
    m = OpenAddressingHashMap()
    assert m.get("missing") is None


def test_get_missing_key_returns_default() -> None:
    m = OpenAddressingHashMap()
    assert m.get("missing", "fallback") == "fallback"


def test_get_after_update() -> None:
    m = OpenAddressingHashMap()
    m.insert("x", 1)
    m.insert("x", 2)
    assert m.get("x") == 2


# ══════════════════════════════════════════════════════════════════════════════
# Delete
# ══════════════════════════════════════════════════════════════════════════════


def test_delete_existing_key() -> None:
    m = OpenAddressingHashMap(("a", 1), ("b", 2))
    m.delete("a")
    assert not m.contains("a")
    assert len(m) == 1


def test_delete_decreases_size() -> None:
    m = OpenAddressingHashMap(("a", 1))
    m.delete("a")
    assert len(m) == 0


def test_delete_missing_key_does_nothing() -> None:
    m = OpenAddressingHashMap(("a", 1))
    m.delete("missing")
    assert len(m) == 1


def test_delete_only_element() -> None:
    m = OpenAddressingHashMap(("only", 0))
    m.delete("only")
    assert not m


def test_delete_does_not_affect_other_keys() -> None:
    m = OpenAddressingHashMap(("a", 1), ("b", 2), ("c", 3))
    m.delete("b")
    assert m.get("a") == 1
    assert m.get("c") == 3


def test_delete_leaves_tombstone_probe_intact() -> None:
    # Insert keys that may collide, delete middle, still find last
    m = OpenAddressingHashMap()
    m.insert("alpha", 1)
    m.insert("beta", 2)
    m.insert("gamma", 3)
    m.delete("beta")
    assert m.get("gamma") == 3


# ══════════════════════════════════════════════════════════════════════════════
# Contains
# ══════════════════════════════════════════════════════════════════════════════


def test_contains_existing_key() -> None:
    m = OpenAddressingHashMap(("k", 1))
    assert m.contains("k") is True


def test_contains_missing_key() -> None:
    m = OpenAddressingHashMap()
    assert m.contains("x") is False


def test_contains_after_delete() -> None:
    m = OpenAddressingHashMap(("k", 1))
    m.delete("k")
    assert m.contains("k") is False


def test_contains_after_insert() -> None:
    m = OpenAddressingHashMap()
    m.insert("new", 42)
    assert m.contains("new") is True


# ══════════════════════════════════════════════════════════════════════════════
# Setdefault
# ══════════════════════════════════════════════════════════════════════════════


def test_setdefault_returns_existing_value() -> None:
    m = OpenAddressingHashMap(("k", 10))
    assert m.setdefault("k", 99) == 10


def test_setdefault_inserts_and_returns_default() -> None:
    m = OpenAddressingHashMap()
    result = m.setdefault("new", 42)
    assert result == 42
    assert m.get("new") == 42


def test_setdefault_does_not_overwrite() -> None:
    m = OpenAddressingHashMap(("k", 10))
    m.setdefault("k", 99)
    assert m.get("k") == 10


def test_setdefault_none_default() -> None:
    m = OpenAddressingHashMap()
    result = m.setdefault("k")
    assert result is None
    assert m.contains("k")


# ══════════════════════════════════════════════════════════════════════════════
# Keys / Values / Items
# ══════════════════════════════════════════════════════════════════════════════


def test_keys_yields_all_keys() -> None:
    m = OpenAddressingHashMap(("a", 1), ("b", 2), ("c", 3))
    assert set(m.keys()) == {"a", "b", "c"}


def test_values_yields_all_values() -> None:
    m = OpenAddressingHashMap(("a", 1), ("b", 2), ("c", 3))
    assert set(m.values()) == {1, 2, 3}


def test_items_yields_all_pairs() -> None:
    m = OpenAddressingHashMap(("a", 1), ("b", 2))
    assert set(m.items()) == {("a", 1), ("b", 2)}


def test_keys_empty_map() -> None:
    assert list(OpenAddressingHashMap().keys()) == []


def test_values_empty_map() -> None:
    assert list(OpenAddressingHashMap().values()) == []


def test_items_empty_map() -> None:
    assert list(OpenAddressingHashMap().items()) == []


def test_keys_skips_deleted_slots() -> None:
    m = OpenAddressingHashMap(("a", 1), ("b", 2))
    m.delete("a")
    assert "a" not in set(m.keys())


# ══════════════════════════════════════════════════════════════════════════════
# Clear / Copy / Deepcopy
# ══════════════════════════════════════════════════════════════════════════════


def test_clear_empties_map() -> None:
    m = OpenAddressingHashMap(("a", 1), ("b", 2))
    m.clear()
    assert len(m) == 0
    assert not m


def test_clear_resets_capacity() -> None:
    m = OpenAddressingHashMap(("a", 1))
    m.clear()
    assert m._capacity == 11


def test_copy_preserves_pairs() -> None:
    m = OpenAddressingHashMap(("a", 1), ("b", 2))
    c = m.copy()
    assert c.get("a") == 1
    assert c.get("b") == 2


def test_copy_is_independent() -> None:
    m = OpenAddressingHashMap(("a", 1))
    c = m.copy()
    c.insert("b", 2)
    assert not m.contains("b")


def test_copy_does_not_share_mutations() -> None:
    m = OpenAddressingHashMap(("a", 1))
    c = m.copy()
    c.delete("a")
    assert m.contains("a")


def test_deepcopy_is_independent() -> None:
    m = OpenAddressingHashMap(("a", 1))
    d = m.deepcopy()
    d.insert("b", 99)
    assert not m.contains("b")


def test_deepcopy_nested_list() -> None:
    m = OpenAddressingHashMap(("data", [1, 2, 3]))
    d = m.deepcopy()
    d.get("data").append(99)
    assert m.get("data") == [1, 2, 3]


# ══════════════════════════════════════════════════════════════════════════════
# is_empty / __len__ / __bool__
# ══════════════════════════════════════════════════════════════════════════════


def test_is_empty_true() -> None:
    assert not OpenAddressingHashMap()


def test_is_empty_false() -> None:
    assert OpenAddressingHashMap(("a", 1))


def test_bool_empty() -> None:
    assert not bool(OpenAddressingHashMap())


def test_bool_not_empty() -> None:
    assert bool(OpenAddressingHashMap(("a", 1)))


def test_len_empty() -> None:
    assert len(OpenAddressingHashMap()) == 0


def test_len_after_inserts() -> None:
    m = OpenAddressingHashMap()
    m.insert("a", 1)
    m.insert("b", 2)
    assert len(m) == 2


# ══════════════════════════════════════════════════════════════════════════════
# __getitem__ / __setitem__ / __delitem__
# ══════════════════════════════════════════════════════════════════════════════


def test_getitem_existing() -> None:
    m = OpenAddressingHashMap(("k", 42))
    assert m["k"] == 42


def test_getitem_missing_raises() -> None:
    m = OpenAddressingHashMap()
    with pytest.raises(KeyError):
        _ = m["missing"]


def test_setitem_inserts() -> None:
    m = OpenAddressingHashMap()
    m["key"] = "value"
    assert m["key"] == "value"


def test_setitem_updates() -> None:
    m = OpenAddressingHashMap(("k", 1))
    m["k"] = 99
    assert m["k"] == 99
    assert len(m) == 1


def test_delitem_removes() -> None:
    m = OpenAddressingHashMap(("k", 1))
    del m["k"]
    assert not m.contains("k")


def test_delitem_missing_does_nothing() -> None:
    m = OpenAddressingHashMap(("k", 1))
    del m["missing"]
    assert len(m) == 1


# ══════════════════════════════════════════════════════════════════════════════
# __iter__ / __reversed__ / __contains__
# ══════════════════════════════════════════════════════════════════════════════


def test_iter_yields_values() -> None:
    m = OpenAddressingHashMap(("a", 1), ("b", 2))
    assert set(m) == {1, 2}


def test_iter_empty() -> None:
    assert list(OpenAddressingHashMap()) == []


def test_iter_skips_deleted_slots() -> None:
    m = OpenAddressingHashMap(("a", 1), ("b", 2))
    m.delete("a")
    assert list(m) == [2]


def test_reversed_yields_values() -> None:
    m = OpenAddressingHashMap(("a", 1), ("b", 2))
    assert set(reversed(m)) == {1, 2}


def test_contains_existing() -> None:
    assert "a" in OpenAddressingHashMap(("a", 1))


def test_contains_missing() -> None:
    assert "z" not in OpenAddressingHashMap(("a", 1))


# ══════════════════════════════════════════════════════════════════════════════
# __eq__
# ══════════════════════════════════════════════════════════════════════════════


def test_eq_same_pairs() -> None:
    a = OpenAddressingHashMap(("x", 1), ("y", 2))
    b = OpenAddressingHashMap(("x", 1), ("y", 2))
    assert a == b


def test_eq_both_empty() -> None:
    assert OpenAddressingHashMap() == OpenAddressingHashMap()


def test_eq_different_values() -> None:
    a = OpenAddressingHashMap(("x", 1))
    b = OpenAddressingHashMap(("x", 99))
    assert a != b


def test_eq_different_keys() -> None:
    a = OpenAddressingHashMap(("a", 1))
    b = OpenAddressingHashMap(("b", 1))
    assert a != b


def test_eq_different_size() -> None:
    a = OpenAddressingHashMap(("a", 1), ("b", 2))
    b = OpenAddressingHashMap(("a", 1))
    assert a != b


def test_eq_not_implemented_for_other_type() -> None:
    assert OpenAddressingHashMap().__eq__({"a": 1}) is NotImplemented


# ══════════════════════════════════════════════════════════════════════════════
# __repr__
# ══════════════════════════════════════════════════════════════════════════════


def test_repr_empty() -> None:
    assert repr(OpenAddressingHashMap()) == "OpenAddressingHashMap(size=0){}"


def test_repr_contains_size() -> None:
    m = OpenAddressingHashMap(("a", 1))
    assert "size=1" in repr(m)


def test_repr_contains_key_value() -> None:
    m = OpenAddressingHashMap(("name", "Umidjon"))
    r = repr(m)
    assert "'name'" in r
    assert "'Umidjon'" in r
