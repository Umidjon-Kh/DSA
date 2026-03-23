import pytest

from data_structures.arrays import StaticTypedArray

# =============================================================================
# Init — capacity=None
# =============================================================================


class TestStaticTypedArrayInitCapacityOptional:
    def test_capacity_derived_from_args_when_not_provided(self):
        arr = StaticTypedArray(int, 1, 2, 3)
        assert len(arr) == 3

    def test_capacity_keyword_only_no_args(self):
        arr = StaticTypedArray(int, capacity=5)
        assert len(arr) == 5

    def test_capacity_and_args_together(self):
        arr = StaticTypedArray(int, 1, 2, 3, capacity=5)
        assert len(arr) == 5
        assert list(arr) == [1, 2, 3, 0, 0]

    def test_raises_type_error_when_neither_capacity_nor_args(self):
        with pytest.raises(TypeError):
            StaticTypedArray(int)

    def test_raises_overflow_error_when_args_exceed_capacity(self):
        with pytest.raises(OverflowError):
            StaticTypedArray(int, 1, 2, 3, capacity=2)

    def test_raises_value_error_for_zero_capacity(self):
        with pytest.raises(ValueError):
            StaticTypedArray(int, capacity=0)

    def test_raises_type_error_for_non_int_capacity(self):
        with pytest.raises(TypeError):
            StaticTypedArray(int, capacity="5")  # type: ignore[testing]

    def test_raises_type_error_for_bool_capacity(self):
        with pytest.raises(TypeError):
            StaticTypedArray(int, capacity=True)


# =============================================================================
# Init — str_length default = 20
# =============================================================================


class TestStaticTypedArrayInitStrLength:
    def test_str_length_defaults_to_20(self):
        arr = StaticTypedArray(str, capacity=3)
        assert arr._str_length == 20

    def test_str_length_custom_value(self):
        arr = StaticTypedArray(str, capacity=3, str_length=8)
        assert arr._str_length == 8

    def test_str_length_20_can_store_long_string(self):
        arr = StaticTypedArray(str, capacity=1)
        arr[0] = "hello world"
        assert arr[0] == "hello world"

    def test_str_length_ignored_for_non_str_dtype(self):
        arr = StaticTypedArray(int, capacity=3, str_length=50)
        assert list(arr) == [0, 0, 0]

    def test_raises_type_error_for_non_int_str_length(self):
        with pytest.raises(TypeError):
            StaticTypedArray(str, capacity=3, str_length="5")  # type: ignore[testing]

    def test_raises_value_error_for_zero_str_length(self):
        with pytest.raises(ValueError):
            StaticTypedArray(str, capacity=3, str_length=0)

    def test_raises_value_error_for_negative_str_length(self):
        with pytest.raises(ValueError):
            StaticTypedArray(str, capacity=3, str_length=-1)

    def test_str_length_none_uses_default(self):
        arr = StaticTypedArray(str, capacity=2, str_length=None)
        assert arr._str_length == 20


# =============================================================================
# clear
# =============================================================================


class TestStaticTypedArrayClear:
    def test_clear_resets_int_elements_to_zero(self):
        arr = StaticTypedArray(int, 1, 2, 3)
        arr.clear()
        assert list(arr) == [0, 0, 0]

    def test_clear_resets_float_elements_to_zero(self):
        arr = StaticTypedArray(float, 1.5, 2.5, capacity=3)
        arr.clear()
        assert list(arr) == [0.0, 0.0, 0.0]

    def test_clear_resets_bool_elements_to_false(self):
        arr = StaticTypedArray(bool, True, True, capacity=3)
        arr.clear()
        assert list(arr) == [False, False, False]

    def test_clear_resets_str_elements_to_empty_string(self):
        arr = StaticTypedArray(str, capacity=3)
        arr[0] = "hello"
        arr[1] = "world"
        arr.clear()
        assert list(arr) == ["", "", ""]

    def test_clear_preserves_capacity(self):
        arr = StaticTypedArray(int, 1, 2, 3, capacity=5)
        arr.clear()
        assert len(arr) == 5

    def test_clear_twice_is_safe(self):
        arr = StaticTypedArray(int, 1, 2, 3)
        arr.clear()
        arr.clear()
        assert list(arr) == [0, 0, 0]

    def test_clear_allows_setitem_after(self):
        arr = StaticTypedArray(int, 1, 2, 3)
        arr.clear()
        arr[0] = 99
        assert arr[0] == 99


# =============================================================================
# copy
# =============================================================================


class TestStaticTypedArrayCopy:
    def test_copy_returns_new_instance(self):
        arr = StaticTypedArray(int, 1, 2, 3)
        copy = arr.copy()
        assert copy is not arr

    def test_copy_has_same_elements(self):
        arr = StaticTypedArray(int, 1, 2, 3)
        copy = arr.copy()
        assert list(copy) == list(arr)

    def test_copy_has_same_capacity(self):
        arr = StaticTypedArray(int, 1, 2, capacity=5)
        copy = arr.copy()
        assert len(copy) == len(arr)

    def test_copy_has_same_dtype(self):
        arr = StaticTypedArray(float, 1.0, 2.0, capacity=3)
        copy = arr.copy()
        assert copy._dtype is float

    def test_copy_is_independent(self):
        arr = StaticTypedArray(int, 1, 2, 3)
        copy = arr.copy()
        copy[0] = 99
        assert arr[0] == 1

    def test_copy_preserves_str_length(self):
        arr = StaticTypedArray(str, capacity=2, str_length=10)
        arr[0] = "hello"
        copy = arr.copy()
        assert copy[0] == "hello"
        assert copy._str_length == 10

    def test_copy_equal_to_original(self):
        arr = StaticTypedArray(int, 1, 2, 3)
        copy = arr.copy()
        assert arr == copy


# =============================================================================
# __bool__
# =============================================================================


class TestStaticTypedArrayBool:
    def test_array_with_capacity_is_true(self):
        arr = StaticTypedArray(int, capacity=3)
        assert arr

    def test_bool_works_in_if_statement(self):
        arr = StaticTypedArray(int, 1, 2, 3)
        result = "yes" if arr else "no"
        assert result == "yes"


# =============================================================================
# __eq__
# =============================================================================


class TestStaticTypedArrayEq:
    def test_equal_arrays_are_equal(self):
        a = StaticTypedArray(int, 1, 2, 3)
        b = StaticTypedArray(int, 1, 2, 3)
        assert a == b

    def test_different_elements_are_not_equal(self):
        a = StaticTypedArray(int, 1, 2, 3)
        b = StaticTypedArray(int, 1, 2, 99)
        assert a != b

    def test_different_capacities_are_not_equal(self):
        a = StaticTypedArray(int, 1, 2, 3)
        b = StaticTypedArray(int, 1, 2, 3, capacity=4)
        assert a != b

    def test_different_dtypes_are_not_equal(self):
        a = StaticTypedArray(int, capacity=3)
        b = StaticTypedArray(float, capacity=3)
        assert a != b

    def test_default_arrays_same_dtype_and_capacity_are_equal(self):
        a = StaticTypedArray(int, capacity=4)
        b = StaticTypedArray(int, capacity=4)
        assert a == b

    def test_comparing_with_non_array_returns_not_implemented(self):
        arr = StaticTypedArray(int, 1, 2, 3)
        assert arr.__eq__([1, 2, 3]) is NotImplemented

    def test_not_equal_after_mutation(self):
        arr = StaticTypedArray(int, 1, 2, 3)
        copy = arr.copy()
        copy[0] = 99
        assert arr != copy
