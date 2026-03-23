import pytest  # noqa

from data_structures.arrays import DynamicTypedArray

# =============================================================================
# Init — str_length default = 20
# =============================================================================


class TestDynamicTypedArrayInitStrLength:
    def test_str_length_defaults_to_20(self):
        arr = DynamicTypedArray(str)
        assert arr._data._str_length == 20

    def test_str_length_custom_value(self):
        arr = DynamicTypedArray(str, str_length=50)
        assert arr._data._str_length == 50

    def test_str_length_20_can_store_typical_strings(self):
        arr = DynamicTypedArray(str)
        arr.append("hello world")
        assert arr[0] == "hello world"

    def test_str_length_ignored_for_non_str_dtype(self):
        arr = DynamicTypedArray(int, str_length=50)
        arr.append(42)
        assert arr[0] == 42


# =============================================================================
# clear
# =============================================================================


class TestDynamicTypedArrayClear:
    def test_clear_sets_size_to_zero(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr.clear()
        assert len(arr) == 0

    def test_clear_resets_int_slots_to_zero(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr.clear()
        # slots 0..2 in the underlying buffer should be reset
        assert arr._data._raw_get(0) == 0
        assert arr._data._raw_get(1) == 0
        assert arr._data._raw_get(2) == 0

    def test_clear_resets_float_slots_to_zero(self):
        arr = DynamicTypedArray(float, 1.5, 2.5)
        arr.clear()
        assert arr._data._raw_get(0) == 0.0
        assert arr._data._raw_get(1) == 0.0

    def test_clear_resets_bool_slots_to_false(self):
        arr = DynamicTypedArray(bool, True, False, True)
        arr.clear()
        assert arr._data._raw_get(0) is False
        assert arr._data._raw_get(1) is False
        assert arr._data._raw_get(2) is False

    def test_clear_resets_str_slots_to_empty_string(self):
        arr = DynamicTypedArray(str, "hello", "world")
        arr.clear()
        assert arr._data._raw_get(0) == ""
        assert arr._data._raw_get(1) == ""

    def test_clear_empty_array_does_not_raise(self):
        arr = DynamicTypedArray(int)
        arr.clear()
        assert len(arr) == 0

    def test_clear_preserves_capacity(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        cap_before = arr._capacity
        arr.clear()
        assert arr._capacity == cap_before

    def test_clear_allows_append_after(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr.clear()
        arr.append(99)
        assert list(arr) == [99]

    def test_clear_iter_yields_nothing(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr.clear()
        assert list(arr) == []

    def test_clear_bool_becomes_false(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr.clear()
        assert not arr

    def test_clear_twice_is_safe(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr.clear()
        arr.clear()
        assert len(arr) == 0


# =============================================================================
# copy
# =============================================================================


class TestDynamicTypedArrayCopy:
    def test_copy_returns_new_instance(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        copy = arr.copy()
        assert copy is not arr

    def test_copy_has_same_elements(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        copy = arr.copy()
        assert list(copy) == [1, 2, 3]

    def test_copy_has_same_dtype(self):
        arr = DynamicTypedArray(float, 1.0, 2.0)
        copy = arr.copy()
        assert copy._dtype is float

    def test_copy_has_same_size(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        copy = arr.copy()
        assert len(copy) == len(arr)

    def test_copy_is_independent_append(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        copy = arr.copy()
        copy.append(99)
        assert list(arr) == [1, 2, 3]

    def test_copy_is_independent_setitem(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        copy = arr.copy()
        copy[0] = 99
        assert arr[0] == 1

    def test_copy_of_empty_array(self):
        arr = DynamicTypedArray(int)
        copy = arr.copy()
        assert len(copy) == 0
        assert copy._dtype is int

    def test_copy_preserves_str_length(self):
        arr = DynamicTypedArray(str, str_length=50)
        arr.append("hello world")
        copy = arr.copy()
        assert copy[0] == "hello world"
        assert copy._data._str_length == 50

    def test_copy_equal_to_original(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        copy = arr.copy()
        assert arr == copy


# =============================================================================
# __bool__
# =============================================================================


class TestDynamicTypedArrayBool:
    def test_empty_array_is_false(self):
        arr = DynamicTypedArray(int)
        assert not arr

    def test_non_empty_array_is_true(self):
        arr = DynamicTypedArray(int, 1)
        assert arr

    def test_becomes_false_after_remove_all(self):
        arr = DynamicTypedArray(int, 42)
        arr.remove(0)
        assert not arr

    def test_becomes_true_after_append(self):
        arr = DynamicTypedArray(int)
        arr.append(1)
        assert arr

    def test_becomes_false_after_clear(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr.clear()
        assert not arr


# =============================================================================
# __eq__
# =============================================================================


class TestDynamicTypedArrayEq:
    def test_equal_arrays_are_equal(self):
        a = DynamicTypedArray(int, 1, 2, 3)
        b = DynamicTypedArray(int, 1, 2, 3)
        assert a == b

    def test_different_elements_are_not_equal(self):
        a = DynamicTypedArray(int, 1, 2, 3)
        b = DynamicTypedArray(int, 1, 2, 99)
        assert a != b

    def test_different_sizes_are_not_equal(self):
        a = DynamicTypedArray(int, 1, 2, 3)
        b = DynamicTypedArray(int, 1, 2)
        assert a != b

    def test_different_dtypes_are_not_equal(self):
        a = DynamicTypedArray(int, 1, 2, 3)
        b = DynamicTypedArray(float, 1.0, 2.0, 3.0)
        assert a != b

    def test_two_empty_arrays_same_dtype_are_equal(self):
        a = DynamicTypedArray(int)
        b = DynamicTypedArray(int)
        assert a == b

    def test_comparing_with_non_array_returns_not_implemented(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        assert arr.__eq__([1, 2, 3]) is NotImplemented

    def test_equal_arrays_after_copy(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        copy = arr.copy()
        assert arr == copy

    def test_not_equal_after_mutation(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        copy = arr.copy()
        copy[0] = 99
        assert arr != copy
