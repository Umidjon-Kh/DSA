import pytest

from data_structures.arrays import StaticTypedArray


class TestStaticTypedArrayInit:
    def test_creates_int_array_with_zero_defaults(self):
        arr = StaticTypedArray(int, 3)
        assert list(arr) == [0, 0, 0]

    def test_creates_float_array_with_zero_defaults(self):
        arr = StaticTypedArray(float, 3)
        assert list(arr) == [0.0, 0.0, 0.0]

    def test_creates_bool_array_with_false_defaults(self):
        arr = StaticTypedArray(bool, 3)
        assert list(arr) == [False, False, False]

    def test_creates_str_array_with_empty_string_defaults(self):
        arr = StaticTypedArray(str, 3)
        assert list(arr) == ["", "", ""]

    def test_creates_array_with_initial_elements(self):
        arr = StaticTypedArray(int, 5, 1, 2, 3)
        assert arr[0] == 1
        assert arr[1] == 2
        assert arr[2] == 3

    def test_remaining_slots_are_default_after_partial_fill(self):
        arr = StaticTypedArray(int, 5, 1, 2)
        assert arr[2] == 0
        assert arr[3] == 0
        assert arr[4] == 0

    def test_raises_type_error_for_unsupported_dtype(self):
        with pytest.raises(TypeError):
            StaticTypedArray(list, 3)

    def test_raises_type_error_for_none_dtype(self):
        with pytest.raises(TypeError):
            StaticTypedArray(None, 3)  # type: ignore[testing]

    def test_raises_type_error_for_non_int_capacity(self):
        with pytest.raises(TypeError):
            StaticTypedArray(int, "5")  # type: ignore[testing]

    def test_raises_type_error_for_bool_capacity(self):
        with pytest.raises(TypeError):
            StaticTypedArray(int, True)

    def test_raises_value_error_for_zero_capacity(self):
        with pytest.raises(ValueError):
            StaticTypedArray(int, 0)

    def test_raises_value_error_for_negative_capacity(self):
        with pytest.raises(ValueError):
            StaticTypedArray(int, -1)

    def test_raises_value_error_when_too_many_args(self):
        with pytest.raises(ValueError):
            StaticTypedArray(int, 2, 1, 2, 3)

    def test_raises_type_error_for_wrong_element_type(self):
        with pytest.raises(TypeError):
            StaticTypedArray(int, 3, 1, "hello", 3)

    def test_raises_type_error_for_bool_in_int_array(self):
        with pytest.raises(TypeError):
            StaticTypedArray(int, 3, 1, True, 3)

    def test_str_dtype_with_str_length(self):
        arr = StaticTypedArray(str, 3, str_length=5)
        arr[0] = "hello"
        assert arr[0] == "hello"

    def test_str_dtype_raises_type_error_for_non_int_str_length(self):
        with pytest.raises(TypeError):
            StaticTypedArray(str, 3, str_length="5")  # type: ignore[testing]

    def test_str_dtype_raises_value_error_for_zero_str_length(self):
        with pytest.raises(ValueError):
            StaticTypedArray(str, 3, str_length=0)

    def test_str_dtype_raises_value_error_for_negative_str_length(self):
        with pytest.raises(ValueError):
            StaticTypedArray(str, 3, str_length=-1)

    def test_str_length_ignored_for_non_str_dtype(self):
        arr = StaticTypedArray(int, 3, str_length=10)
        assert list(arr) == [0, 0, 0]


class TestStaticTypedArrayGetItem:
    def test_returns_element_at_index(self):
        arr = StaticTypedArray(int, 3, 10, 20, 30)
        assert arr[0] == 10
        assert arr[2] == 30

    def test_supports_negative_indexing(self):
        arr = StaticTypedArray(int, 3, 10, 20, 30)
        assert arr[-1] == 30
        assert arr[-3] == 10

    def test_raises_index_error_for_out_of_range(self):
        arr = StaticTypedArray(int, 3)
        with pytest.raises(IndexError):
            arr[3]

    def test_raises_index_error_for_negative_out_of_range(self):
        arr = StaticTypedArray(int, 3)
        with pytest.raises(IndexError):
            arr[-4]

    def test_raises_type_error_for_float_index(self):
        arr = StaticTypedArray(int, 3)
        with pytest.raises(TypeError):
            arr[1.0]  # type: ignore[testing]

    def test_raises_type_error_for_bool_index(self):
        arr = StaticTypedArray(int, 3)
        with pytest.raises(TypeError):
            arr[True]


class TestStaticTypedArraySetItem:
    def test_sets_int_element(self):
        arr = StaticTypedArray(int, 3)
        arr[0] = 42
        assert arr[0] == 42

    def test_sets_float_element(self):
        arr = StaticTypedArray(float, 3)
        arr[1] = 3.14
        assert arr[1] == 3.14

    def test_sets_bool_element(self):
        arr = StaticTypedArray(bool, 3)
        arr[0] = True
        assert arr[0] is True

    def test_sets_str_element(self):
        arr = StaticTypedArray(str, 3, str_length=5)
        arr[0] = "hello"
        assert arr[0] == "hello"

    def test_overwrites_existing_element(self):
        arr = StaticTypedArray(int, 3, 1, 2, 3)
        arr[1] = 99
        assert arr[1] == 99

    def test_supports_negative_index(self):
        arr = StaticTypedArray(int, 3, 1, 2, 3)
        arr[-1] = 99
        assert arr[2] == 99

    def test_raises_type_error_for_wrong_value_type(self):
        arr = StaticTypedArray(int, 3)
        with pytest.raises(TypeError):
            arr[0] = "hello"

    def test_raises_type_error_for_bool_in_int_array(self):
        arr = StaticTypedArray(int, 3)
        with pytest.raises(TypeError):
            arr[0] = True

    def test_raises_type_error_for_int_in_bool_array(self):
        arr = StaticTypedArray(bool, 3)
        with pytest.raises(TypeError):
            arr[0] = 1

    def test_raises_index_error_for_out_of_range(self):
        arr = StaticTypedArray(int, 3)
        with pytest.raises(IndexError):
            arr[3] = 1

    def test_raises_type_error_for_bool_index(self):
        arr = StaticTypedArray(int, 3)
        with pytest.raises(TypeError):
            arr[True] = 1


class TestStaticTypedArrayLen:
    def test_returns_capacity(self):
        arr = StaticTypedArray(int, 5)
        assert len(arr) == 5

    def test_len_equals_capacity_not_filled_count(self):
        arr = StaticTypedArray(int, 5, 1, 2)
        assert len(arr) == 5


class TestStaticTypedArrayIter:
    def test_iterates_all_elements_in_order(self):
        arr = StaticTypedArray(int, 4, 1, 2, 3, 4)
        assert list(arr) == [1, 2, 3, 4]

    def test_iterates_including_default_slots(self):
        arr = StaticTypedArray(int, 4, 1, 2)
        assert list(arr) == [1, 2, 0, 0]

    def test_iterates_fully_default_array(self):
        arr = StaticTypedArray(float, 3)
        assert list(arr) == [0.0, 0.0, 0.0]


class TestStaticTypedArrayReversed:
    def test_yields_elements_in_reverse_order(self):
        arr = StaticTypedArray(int, 4, 1, 2, 3, 4)
        assert list(reversed(arr)) == [4, 3, 2, 1]

    def test_reversed_includes_default_slots(self):
        arr = StaticTypedArray(int, 4, 1, 2)
        assert list(reversed(arr)) == [0, 0, 2, 1]


class TestStaticTypedArrayContains:
    def test_returns_true_for_existing_element(self):
        arr = StaticTypedArray(int, 4, 1, 2, 3)
        assert 2 in arr

    def test_returns_false_for_missing_element(self):
        arr = StaticTypedArray(int, 4, 1, 2, 3)
        assert 99 not in arr

    def test_returns_false_for_wrong_type(self):
        arr = StaticTypedArray(int, 3, 1, 2, 3)
        assert "1" not in arr

    def test_returns_false_for_bool_in_int_array(self):
        arr = StaticTypedArray(int, 3, 1, 2, 3)
        assert True not in arr

    def test_returns_true_for_default_value(self):
        arr = StaticTypedArray(int, 4, 1, 2)
        assert 0 in arr


class TestStaticTypedArrayRepr:
    def test_repr_format_int_array(self):
        arr = StaticTypedArray(int, 3, 1, 2, 3)
        assert repr(arr) == "StaticTypedArray(int, capacity=3)[1, 2, 3]"

    def test_repr_format_with_default_slots(self):
        arr = StaticTypedArray(int, 4, 1, 2)
        assert repr(arr) == "StaticTypedArray(int, capacity=4)[1, 2, 0, 0]"

    def test_repr_format_float_array(self):
        arr = StaticTypedArray(float, 2)
        assert repr(arr) == "StaticTypedArray(float, capacity=2)[0.0, 0.0]"
