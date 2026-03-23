import pytest

from data_structures.arrays import DynamicUniversalArray


class TestDynamicUniversalArrayInit:
    def test_creates_empty_array_with_default_capacity(self):
        arr = DynamicUniversalArray()
        assert len(arr) == 0
        assert arr._capacity == 4

    def test_creates_array_with_initial_elements(self):
        arr = DynamicUniversalArray(1, "hi", 3.0)
        assert arr[0] == 1
        assert arr[1] == "hi"
        assert arr[2] == 3.0

    def test_size_equals_number_of_initial_elements(self):
        arr = DynamicUniversalArray(1, 2, 3)
        assert len(arr) == 3

    def test_capacity_is_max_of_4_and_arg_count(self):
        arr = DynamicUniversalArray(1, 2, 3)
        assert arr._capacity == 4

    def test_capacity_grows_beyond_4_for_large_init(self):
        arr = DynamicUniversalArray(*range(10))
        assert arr._capacity >= 10

    def test_accepts_none_as_element(self):
        arr = DynamicUniversalArray(None, 1)
        assert arr[0] is None

    def test_accepts_mixed_types(self):
        arr = DynamicUniversalArray(1, "hello", 3.14, True, None)
        assert len(arr) == 5


class TestDynamicUniversalArrayAppend:
    def test_appends_element_to_empty_array(self):
        arr = DynamicUniversalArray()
        arr.append(1)
        assert arr[0] == 1
        assert len(arr) == 1

    def test_appends_multiple_elements_in_order(self):
        arr = DynamicUniversalArray()
        arr.append(1)
        arr.append(2)
        arr.append(3)
        assert list(arr) == [1, 2, 3]

    def test_appends_none(self):
        arr = DynamicUniversalArray()
        arr.append(None)
        assert arr[0] is None

    def test_triggers_resize_when_capacity_exceeded(self):
        arr = DynamicUniversalArray()
        for i in range(5):
            arr.append(i)
        assert len(arr) == 5
        assert arr._capacity > 4

    def test_all_elements_preserved_after_resize(self):
        arr = DynamicUniversalArray()
        for i in range(10):
            arr.append(i)
        assert list(arr) == list(range(10))


class TestDynamicUniversalArrayInsert:
    def test_inserts_at_beginning(self):
        arr = DynamicUniversalArray(1, 2, 3)
        arr.insert(0, 99)
        assert arr[0] == 99
        assert list(arr) == [99, 1, 2, 3]

    def test_inserts_at_middle(self):
        arr = DynamicUniversalArray(1, 2, 3)
        arr.insert(1, 99)
        assert list(arr) == [1, 99, 2, 3]

    def test_inserts_at_end(self):
        arr = DynamicUniversalArray(1, 2, 3)
        arr.insert(3, 99)
        assert list(arr) == [1, 2, 3, 99]

    def test_supports_negative_index(self):
        arr = DynamicUniversalArray(1, 2, 3)
        arr.insert(-1, 99)
        assert list(arr) == [1, 2, 99, 3]

    def test_size_increases_after_insert(self):
        arr = DynamicUniversalArray(1, 2, 3)
        arr.insert(0, 99)
        assert len(arr) == 4

    def test_triggers_resize_on_insert_when_full(self):
        arr = DynamicUniversalArray(1, 2, 3, 4)
        arr.insert(0, 99)
        assert len(arr) == 5
        assert arr._capacity > 4

    def test_raises_index_error_for_out_of_range(self):
        arr = DynamicUniversalArray(1, 2, 3)
        with pytest.raises(IndexError):
            arr.insert(10, 99)

    def test_raises_type_error_for_float_index(self):
        arr = DynamicUniversalArray(1, 2, 3)
        with pytest.raises(TypeError):
            arr.insert(1.0, 99)  # type: ignore[testing]

    def test_raises_type_error_for_bool_index(self):
        arr = DynamicUniversalArray(1, 2, 3)
        with pytest.raises(TypeError):
            arr.insert(True, 99)


class TestDynamicUniversalArrayRemove:
    def test_removes_and_returns_element_at_index(self):
        arr = DynamicUniversalArray(1, 2, 3)
        value = arr.remove(1)
        assert value == 2

    def test_shifts_elements_left_after_remove(self):
        arr = DynamicUniversalArray(1, 2, 3)
        arr.remove(0)
        assert list(arr) == [2, 3]

    def test_removes_last_element(self):
        arr = DynamicUniversalArray(1, 2, 3)
        arr.remove(2)
        assert list(arr) == [1, 2]

    def test_supports_negative_index(self):
        arr = DynamicUniversalArray(1, 2, 3)
        value = arr.remove(-1)
        assert value == 3
        assert list(arr) == [1, 2]

    def test_size_decreases_after_remove(self):
        arr = DynamicUniversalArray(1, 2, 3)
        arr.remove(0)
        assert len(arr) == 2

    def test_raises_index_error_on_empty_array(self):
        arr = DynamicUniversalArray()
        with pytest.raises(IndexError):
            arr.remove(0)

    def test_raises_index_error_for_out_of_range(self):
        arr = DynamicUniversalArray(1, 2, 3)
        with pytest.raises(IndexError):
            arr.remove(5)

    def test_raises_type_error_for_float_index(self):
        arr = DynamicUniversalArray(1, 2, 3)
        with pytest.raises(TypeError):
            arr.remove(1.0)  # type: ignore[testing]

    def test_raises_type_error_for_bool_index(self):
        arr = DynamicUniversalArray(1, 2, 3)
        with pytest.raises(TypeError):
            arr.remove(True)


class TestDynamicUniversalArrayGetItem:
    def test_returns_element_at_index(self):
        arr = DynamicUniversalArray(10, 20, 30)
        assert arr[0] == 10
        assert arr[2] == 30

    def test_supports_negative_indexing(self):
        arr = DynamicUniversalArray(10, 20, 30)
        assert arr[-1] == 30
        assert arr[-3] == 10

    def test_raises_index_error_for_out_of_range(self):
        arr = DynamicUniversalArray(1, 2, 3)
        with pytest.raises(IndexError):
            arr[3]

    def test_raises_index_error_beyond_size_not_capacity(self):
        arr = DynamicUniversalArray(1)
        with pytest.raises(IndexError):
            arr[1]

    def test_raises_type_error_for_float_index(self):
        arr = DynamicUniversalArray(1, 2, 3)
        with pytest.raises(TypeError):
            arr[1.0]  # type: ignore[testing]

    def test_raises_type_error_for_bool_index(self):
        arr = DynamicUniversalArray(1, 2, 3)
        with pytest.raises(TypeError):
            arr[True]


class TestDynamicUniversalArraySetItem:
    def test_sets_element_at_index(self):
        arr = DynamicUniversalArray(1, 2, 3)
        arr[1] = 99
        assert arr[1] == 99

    def test_supports_negative_index(self):
        arr = DynamicUniversalArray(1, 2, 3)
        arr[-1] = 99
        assert arr[2] == 99

    def test_sets_none_value(self):
        arr = DynamicUniversalArray(1, 2, 3)
        arr[0] = None
        assert arr[0] is None

    def test_raises_index_error_for_out_of_range(self):
        arr = DynamicUniversalArray(1, 2, 3)
        with pytest.raises(IndexError):
            arr[5] = 99

    def test_raises_index_error_beyond_size_not_capacity(self):
        arr = DynamicUniversalArray(1)
        with pytest.raises(IndexError):
            arr[1] = 99

    def test_raises_type_error_for_bool_index(self):
        arr = DynamicUniversalArray(1, 2, 3)
        with pytest.raises(TypeError):
            arr[True] = 99


class TestDynamicUniversalArrayLen:
    def test_returns_zero_for_empty_array(self):
        arr = DynamicUniversalArray()
        assert len(arr) == 0

    def test_returns_size_not_capacity(self):
        arr = DynamicUniversalArray(1, 2, 3)
        assert len(arr) == 3
        assert arr._capacity == 4

    def test_len_updates_after_append(self):
        arr = DynamicUniversalArray()
        arr.append(1)
        arr.append(2)
        assert len(arr) == 2

    def test_len_updates_after_remove(self):
        arr = DynamicUniversalArray(1, 2, 3)
        arr.remove(0)
        assert len(arr) == 2


class TestDynamicUniversalArrayIter:
    def test_iterates_elements_in_order(self):
        arr = DynamicUniversalArray(1, 2, 3)
        assert list(arr) == [1, 2, 3]

    def test_iterates_only_filled_elements_not_capacity(self):
        arr = DynamicUniversalArray(1, 2)
        assert list(arr) == [1, 2]

    def test_iterates_empty_array(self):
        arr = DynamicUniversalArray()
        assert list(arr) == []

    def test_iterates_mixed_types(self):
        arr = DynamicUniversalArray(1, "hi", None)
        assert list(arr) == [1, "hi", None]


class TestDynamicUniversalArrayReversed:
    def test_yields_elements_in_reverse_order(self):
        arr = DynamicUniversalArray(1, 2, 3)
        assert list(reversed(arr)) == [3, 2, 1]

    def test_reversed_only_covers_filled_elements(self):
        arr = DynamicUniversalArray(1, 2)
        assert list(reversed(arr)) == [2, 1]

    def test_reversed_empty_array(self):
        arr = DynamicUniversalArray()
        assert list(reversed(arr)) == []


class TestDynamicUniversalArrayContains:
    def test_returns_true_for_existing_element(self):
        arr = DynamicUniversalArray(1, 2, 3)
        assert 2 in arr

    def test_returns_false_for_missing_element(self):
        arr = DynamicUniversalArray(1, 2, 3)
        assert 99 not in arr

    def test_returns_true_for_none(self):
        arr = DynamicUniversalArray(None, 1)
        assert None in arr

    def test_does_not_find_elements_beyond_size(self):
        arr = DynamicUniversalArray(1, 2, 3)
        arr.remove(2)
        assert 3 not in arr


class TestDynamicUniversalArrayRepr:
    def test_repr_format_with_elements(self):
        arr = DynamicUniversalArray(1, 2, 3)
        assert repr(arr) == "DynamicUniversalArray(size=3, capacity=4)[1, 2, 3]"

    def test_repr_empty_array(self):
        arr = DynamicUniversalArray()
        assert repr(arr) == "DynamicUniversalArray(size=0, capacity=4)[]"

    def test_repr_with_mixed_types(self):
        arr = DynamicUniversalArray(1, "hi", 3.0)
        assert repr(arr) == "DynamicUniversalArray(size=3, capacity=4)[1, 'hi', 3.0]"
