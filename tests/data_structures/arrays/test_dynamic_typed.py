import pytest

from data_structures.arrays import DynamicTypedArray


class TestDynamicTypedArrayInit:
    def test_creates_empty_int_array_with_default_capacity(self):
        arr = DynamicTypedArray(int)
        assert len(arr) == 0
        assert arr._capacity == 4

    def test_creates_array_with_initial_elements(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        assert arr[0] == 1
        assert arr[1] == 2
        assert arr[2] == 3

    def test_size_equals_number_of_initial_elements(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        assert len(arr) == 3

    def test_capacity_is_max_of_4_and_arg_count(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        assert arr._capacity == 4

    def test_capacity_grows_beyond_4_for_large_init(self):
        arr = DynamicTypedArray(int, *range(10))
        assert arr._capacity >= 10

    def test_supports_float_dtype(self):
        arr = DynamicTypedArray(float, 1.1, 2.2)
        assert arr[0] == pytest.approx(1.1)
        assert arr[1] == pytest.approx(2.2)

    def test_supports_bool_dtype(self):
        arr = DynamicTypedArray(bool, True, False)
        assert arr[0] is True
        assert arr[1] is False

    def test_supports_str_dtype(self):
        arr = DynamicTypedArray(str, str_length=5)
        arr.append("hello")
        assert arr[0] == "hello"

    def test_raises_type_error_for_wrong_element_type_in_init(self):
        with pytest.raises(TypeError):
            DynamicTypedArray(int, 1, "two", 3)

    def test_raises_type_error_for_bool_in_int_array_on_init(self):
        with pytest.raises(TypeError):
            DynamicTypedArray(int, 1, True, 3)


class TestDynamicTypedArrayAppend:
    def test_appends_int_element(self):
        arr = DynamicTypedArray(int)
        arr.append(42)
        assert arr[0] == 42
        assert len(arr) == 1

    def test_appends_multiple_elements_in_order(self):
        arr = DynamicTypedArray(int)
        arr.append(1)
        arr.append(2)
        arr.append(3)
        assert list(arr) == [1, 2, 3]

    def test_triggers_resize_when_capacity_exceeded(self):
        arr = DynamicTypedArray(int)
        for i in range(5):
            arr.append(i)
        assert len(arr) == 5
        assert arr._capacity > 4

    def test_all_elements_preserved_after_resize(self):
        arr = DynamicTypedArray(int)
        for i in range(10):
            arr.append(i)
        assert list(arr) == list(range(10))

    def test_raises_type_error_for_wrong_type(self):
        arr = DynamicTypedArray(int)
        with pytest.raises(TypeError):
            arr.append("hello")

    def test_raises_type_error_for_float_in_int_array(self):
        arr = DynamicTypedArray(int)
        with pytest.raises(TypeError):
            arr.append(1.0)

    def test_raises_type_error_for_bool_in_int_array(self):
        arr = DynamicTypedArray(int)
        with pytest.raises(TypeError):
            arr.append(True)

    def test_raises_type_error_for_int_in_bool_array(self):
        arr = DynamicTypedArray(bool)
        with pytest.raises(TypeError):
            arr.append(1)

    def test_appends_bool_to_bool_array(self):
        arr = DynamicTypedArray(bool)
        arr.append(True)
        assert arr[0] is True


class TestDynamicTypedArrayInsert:
    def test_inserts_at_beginning(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr.insert(0, 99)
        assert list(arr) == [99, 1, 2, 3]

    def test_inserts_at_middle(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr.insert(1, 99)
        assert list(arr) == [1, 99, 2, 3]

    def test_inserts_at_end(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr.insert(3, 99)
        assert list(arr) == [1, 2, 3, 99]

    def test_supports_negative_index(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr.insert(-1, 99)
        assert list(arr) == [1, 2, 99, 3]

    def test_size_increases_after_insert(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr.insert(0, 99)
        assert len(arr) == 4

    def test_triggers_resize_on_insert_when_full(self):
        arr = DynamicTypedArray(int, 1, 2, 3, 4)
        arr.insert(0, 99)
        assert len(arr) == 5
        assert arr._capacity > 4

    def test_raises_type_error_for_wrong_value_type(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        with pytest.raises(TypeError):
            arr.insert(0, "hello")

    def test_raises_type_error_for_bool_value_in_int_array(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        with pytest.raises(TypeError):
            arr.insert(0, True)

    def test_raises_index_error_for_out_of_range(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        with pytest.raises(IndexError):
            arr.insert(10, 99)

    def test_raises_type_error_for_float_index(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        with pytest.raises(TypeError):
            arr.insert(1.0, 99)  # type: ignore[testing]

    def test_raises_type_error_for_bool_index(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        with pytest.raises(TypeError):
            arr.insert(True, 99)


class TestDynamicTypedArrayRemove:
    def test_removes_and_returns_element_at_index(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        value = arr.remove(1)
        assert value == 2

    def test_shifts_elements_left_after_remove(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr.remove(0)
        assert list(arr) == [2, 3]

    def test_removes_last_element(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr.remove(2)
        assert list(arr) == [1, 2]

    def test_supports_negative_index(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        value = arr.remove(-1)
        assert value == 3
        assert list(arr) == [1, 2]

    def test_size_decreases_after_remove(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr.remove(0)
        assert len(arr) == 2

    def test_last_slot_reset_to_default_after_remove(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr.remove(0)
        assert arr._data._raw_get(2) == 0

    def test_raises_index_error_on_empty_array(self):
        arr = DynamicTypedArray(int)
        with pytest.raises(IndexError):
            arr.remove(0)

    def test_raises_index_error_for_out_of_range(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        with pytest.raises(IndexError):
            arr.remove(5)

    def test_raises_type_error_for_float_index(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        with pytest.raises(TypeError):
            arr.remove(1.0)  # type: ignore[testing]

    def test_raises_type_error_for_bool_index(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        with pytest.raises(TypeError):
            arr.remove(True)


class TestDynamicTypedArrayGetItem:
    def test_returns_element_at_index(self):
        arr = DynamicTypedArray(int, 10, 20, 30)
        assert arr[0] == 10
        assert arr[2] == 30

    def test_supports_negative_indexing(self):
        arr = DynamicTypedArray(int, 10, 20, 30)
        assert arr[-1] == 30
        assert arr[-3] == 10

    def test_raises_index_error_for_out_of_range(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        with pytest.raises(IndexError):
            arr[3]

    def test_raises_index_error_beyond_size_not_capacity(self):
        arr = DynamicTypedArray(int, 1)
        with pytest.raises(IndexError):
            arr[1]

    def test_raises_type_error_for_float_index(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        with pytest.raises(TypeError):
            arr[1.0]  # type: ignore[testing]

    def test_raises_type_error_for_bool_index(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        with pytest.raises(TypeError):
            arr[True]


class TestDynamicTypedArraySetItem:
    def test_sets_element_at_index(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr[1] = 99
        assert arr[1] == 99

    def test_supports_negative_index(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr[-1] = 99
        assert arr[2] == 99

    def test_raises_type_error_for_wrong_value_type(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        with pytest.raises(TypeError):
            arr[0] = "hello"

    def test_raises_type_error_for_bool_in_int_array(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        with pytest.raises(TypeError):
            arr[0] = True

    def test_raises_index_error_for_out_of_range(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        with pytest.raises(IndexError):
            arr[5] = 99

    def test_raises_index_error_beyond_size_not_capacity(self):
        arr = DynamicTypedArray(int, 1)
        with pytest.raises(IndexError):
            arr[1] = 99

    def test_raises_type_error_for_bool_index(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        with pytest.raises(TypeError):
            arr[True] = 99


class TestDynamicTypedArrayLen:
    def test_returns_zero_for_empty_array(self):
        arr = DynamicTypedArray(int)
        assert len(arr) == 0

    def test_returns_size_not_capacity(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        assert len(arr) == 3
        assert arr._capacity == 4

    def test_len_updates_after_append(self):
        arr = DynamicTypedArray(int)
        arr.append(1)
        arr.append(2)
        assert len(arr) == 2

    def test_len_updates_after_remove(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr.remove(0)
        assert len(arr) == 2


class TestDynamicTypedArrayIter:
    def test_iterates_elements_in_order(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        assert list(arr) == [1, 2, 3]

    def test_iterates_only_filled_elements_not_capacity(self):
        arr = DynamicTypedArray(int, 1, 2)
        assert list(arr) == [1, 2]

    def test_iterates_empty_array(self):
        arr = DynamicTypedArray(int)
        assert list(arr) == []


class TestDynamicTypedArrayReversed:
    def test_yields_elements_in_reverse_order(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        assert list(reversed(arr)) == [3, 2, 1]

    def test_reversed_only_covers_filled_elements(self):
        arr = DynamicTypedArray(int, 1, 2)
        assert list(reversed(arr)) == [2, 1]

    def test_reversed_empty_array(self):
        arr = DynamicTypedArray(int)
        assert list(reversed(arr)) == []


class TestDynamicTypedArrayContains:
    def test_returns_true_for_existing_element(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        assert 2 in arr

    def test_returns_false_for_missing_element(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        assert 99 not in arr

    def test_returns_false_for_wrong_type(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        assert "1" not in arr

    def test_returns_false_for_bool_in_int_array(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        assert True not in arr

    def test_does_not_find_elements_beyond_size(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr.remove(2)
        assert 3 not in arr


class TestDynamicTypedArrayRepr:
    def test_repr_format_with_elements(self):
        arr = DynamicTypedArray(int, 1, 2, 3)
        assert repr(arr) == "DynamicTypedArray(int, size=3, capacity=4)[1, 2, 3]"

    def test_repr_empty_array(self):
        arr = DynamicTypedArray(int)
        assert repr(arr) == "DynamicTypedArray(int, size=0, capacity=4)[]"

    def test_repr_float_array(self):
        arr = DynamicTypedArray(float, 1.0, 2.0)
        assert repr(arr) == "DynamicTypedArray(float, size=2, capacity=4)[1.0, 2.0]"
