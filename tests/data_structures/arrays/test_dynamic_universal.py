import pytest  # noqa

from data_structures.arrays import DynamicUniversalArray

# =============================================================================
# clear
# =============================================================================


class TestDynamicUniversalArrayClear:
    def test_clear_sets_size_to_zero(self):
        arr = DynamicUniversalArray(1, 2, 3)
        arr.clear()
        assert len(arr) == 0

    def test_clear_empty_array_does_not_raise(self):
        arr = DynamicUniversalArray()
        arr.clear()
        assert len(arr) == 0

    def test_clear_preserves_capacity(self):
        arr = DynamicUniversalArray(1, 2, 3)
        cap_before = arr._capacity
        arr.clear()
        assert arr._capacity == cap_before

    def test_clear_allows_append_after(self):
        arr = DynamicUniversalArray(1, 2, 3)
        arr.clear()
        arr.append(99)
        assert list(arr) == [99]

    def test_clear_iter_yields_nothing(self):
        arr = DynamicUniversalArray(1, 2, 3)
        arr.clear()
        assert list(arr) == []

    def test_clear_bool_becomes_false(self):
        arr = DynamicUniversalArray(1, 2, 3)
        arr.clear()
        assert not arr

    def test_clear_twice_is_safe(self):
        arr = DynamicUniversalArray(1, 2, 3)
        arr.clear()
        arr.clear()
        assert len(arr) == 0

    def test_clear_works_with_mixed_types(self):
        arr = DynamicUniversalArray(1, "hi", None, 3.14)
        arr.clear()
        assert len(arr) == 0


# =============================================================================
# copy
# =============================================================================


class TestDynamicUniversalArrayCopy:
    def test_copy_returns_new_instance(self):
        arr = DynamicUniversalArray(1, 2, 3)
        copy = arr.copy()
        assert copy is not arr

    def test_copy_has_same_elements(self):
        arr = DynamicUniversalArray(1, 2, 3)
        copy = arr.copy()
        assert list(copy) == [1, 2, 3]

    def test_copy_has_same_size(self):
        arr = DynamicUniversalArray(1, 2, 3)
        copy = arr.copy()
        assert len(copy) == len(arr)

    def test_copy_is_independent_append(self):
        arr = DynamicUniversalArray(1, 2, 3)
        copy = arr.copy()
        copy.append(99)
        assert list(arr) == [1, 2, 3]

    def test_copy_is_independent_setitem(self):
        arr = DynamicUniversalArray(1, 2, 3)
        copy = arr.copy()
        copy[0] = 99
        assert arr[0] == 1

    def test_copy_of_empty_array(self):
        arr = DynamicUniversalArray()
        copy = arr.copy()
        assert len(copy) == 0

    def test_copy_preserves_none_values(self):
        arr = DynamicUniversalArray(1, None, 3)
        copy = arr.copy()
        assert copy[1] is None

    def test_copy_preserves_mixed_types(self):
        arr = DynamicUniversalArray(1, "hi", 3.14)
        copy = arr.copy()
        assert list(copy) == [1, "hi", 3.14]

    def test_copy_is_shallow(self):
        inner = [1, 2, 3]
        arr = DynamicUniversalArray(inner)
        copy = arr.copy()
        inner.append(99)
        assert copy[0] is inner
        assert copy[0] == [1, 2, 3, 99]

    def test_copy_equal_to_original(self):
        arr = DynamicUniversalArray(1, 2, 3)
        copy = arr.copy()
        assert arr == copy


# =============================================================================
# __bool__
# =============================================================================


class TestDynamicUniversalArrayBool:
    def test_empty_array_is_false(self):
        arr = DynamicUniversalArray()
        assert not arr

    def test_non_empty_array_is_true(self):
        arr = DynamicUniversalArray(1)
        assert arr

    def test_array_with_none_element_is_true(self):
        arr = DynamicUniversalArray(None)
        assert arr

    def test_becomes_false_after_remove_all(self):
        arr = DynamicUniversalArray(42)
        arr.remove(0)
        assert not arr

    def test_becomes_true_after_append(self):
        arr = DynamicUniversalArray()
        arr.append(1)
        assert arr

    def test_becomes_false_after_clear(self):
        arr = DynamicUniversalArray(1, 2, 3)
        arr.clear()
        assert not arr


# =============================================================================
# __eq__
# =============================================================================


class TestDynamicUniversalArrayEq:
    def test_equal_arrays_are_equal(self):
        a = DynamicUniversalArray(1, 2, 3)
        b = DynamicUniversalArray(1, 2, 3)
        assert a == b

    def test_different_elements_are_not_equal(self):
        a = DynamicUniversalArray(1, 2, 3)
        b = DynamicUniversalArray(1, 2, 99)
        assert a != b

    def test_different_sizes_are_not_equal(self):
        a = DynamicUniversalArray(1, 2, 3)
        b = DynamicUniversalArray(1, 2)
        assert a != b

    def test_two_empty_arrays_are_equal(self):
        a = DynamicUniversalArray()
        b = DynamicUniversalArray()
        assert a == b

    def test_equal_with_mixed_types(self):
        a = DynamicUniversalArray(1, "hi", None)
        b = DynamicUniversalArray(1, "hi", None)
        assert a == b

    def test_comparing_with_non_array_returns_not_implemented(self):
        arr = DynamicUniversalArray(1, 2, 3)
        assert arr.__eq__([1, 2, 3]) is NotImplemented

    def test_equal_arrays_after_copy(self):
        arr = DynamicUniversalArray(1, 2, 3)
        copy = arr.copy()
        assert arr == copy

    def test_not_equal_after_mutation(self):
        arr = DynamicUniversalArray(1, 2, 3)
        copy = arr.copy()
        copy[0] = 99
        assert arr != copy
