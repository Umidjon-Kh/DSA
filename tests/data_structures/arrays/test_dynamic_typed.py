import pytest

from data_structures import DynamicTypedArray


class TestDynamicTypedArrayInit:
    """
    Testing DynamicTypedArray initialization for all dtypes.
    """

    def test_int_empty(self) -> None:
        arr = DynamicTypedArray(int)

        assert len(arr) == 0
        assert arr._capacity == 4
        assert arr._dtype is int

    def test_float_empty(self) -> None:
        arr = DynamicTypedArray(float)

        assert len(arr) == 0
        assert arr._dtype is float

    def test_bool_empty(self) -> None:
        arr = DynamicTypedArray(bool)

        assert len(arr) == 0
        assert arr._dtype is bool

    def test_str_empty(self) -> None:
        arr = DynamicTypedArray(str)

        assert len(arr) == 0
        assert arr._dtype is str

    def test_int_with_args(self) -> None:
        arr = DynamicTypedArray(int, 1, 2, 3)

        assert len(arr) == 3
        assert arr[0] == 1
        assert arr[1] == 2
        assert arr[2] == 3

    def test_str_with_custom_str_length(self) -> None:
        arr = DynamicTypedArray(str, str_length=50)

        assert arr._data._str_length == 50

    def test_str_default_str_length_is_20(self) -> None:
        arr = DynamicTypedArray(str)

        assert arr._data._str_length == 20

    def test_capacity_is_max_4_or_args(self) -> None:
        arr_small = DynamicTypedArray(int, 1, 2)
        assert arr_small._capacity == 4

        arr_large = DynamicTypedArray(int, 1, 2, 3, 4, 5)
        assert arr_large._capacity == 5


class TestDynamicTypedArrayInitErrors:
    """
    Testing DynamicTypedArray initialization errors.
    """

    def test_unsupported_dtype_raises(self) -> None:
        with pytest.raises(TypeError):
            DynamicTypedArray(list)  # type: ignore[arg-type]

    def test_dtype_as_string_raises(self) -> None:
        with pytest.raises(TypeError):
            DynamicTypedArray("int")  # type: ignore[arg-type]

    def test_wrong_type_in_args_raises(self) -> None:
        with pytest.raises(TypeError):
            DynamicTypedArray(int, 1, "two", 3)

    def test_bool_in_int_args_raises(self) -> None:
        with pytest.raises(TypeError):
            DynamicTypedArray(int, 1, True, 3)

    def test_int_in_bool_args_raises(self) -> None:
        with pytest.raises(TypeError):
            DynamicTypedArray(bool, True, 1, False)


class TestDynamicTypedArrayMutation:
    """
    Testing append, insert and remove with type enforcement.
    """

    def test_append_correct_type(self) -> None:
        arr = DynamicTypedArray(int)
        arr.append(42)

        assert len(arr) == 1
        assert arr[0] == 42

    def test_append_wrong_type_raises(self) -> None:
        arr = DynamicTypedArray(int)

        with pytest.raises(TypeError):
            arr.append("not an int")

    def test_append_bool_to_int_raises(self) -> None:
        arr = DynamicTypedArray(int)

        with pytest.raises(TypeError):
            arr.append(True)

    def test_append_int_to_bool_raises(self) -> None:
        arr = DynamicTypedArray(bool)

        with pytest.raises(TypeError):
            arr.append(1)

    def test_append_triggers_resize(self) -> None:
        arr = DynamicTypedArray(int)

        for i in range(4):
            arr.append(i)

        assert arr._capacity == 4

        # Resize: 4 + 0 + 3 = 7
        arr.append(99)

        assert len(arr) == 5
        assert arr._capacity == 7
        assert arr[4] == 99

    def test_insert_at_beginning(self) -> None:
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr.insert(0, 0)

        assert list(arr) == [0, 1, 2, 3]

    def test_insert_at_middle(self) -> None:
        arr = DynamicTypedArray(int, 1, 2, 4)
        arr.insert(2, 3)

        assert list(arr) == [1, 2, 3, 4]

    def test_insert_wrong_type_raises(self) -> None:
        arr = DynamicTypedArray(int, 1, 2, 3)

        with pytest.raises(TypeError):
            arr.insert(1, "x")

    def test_insert_bool_in_int_raises(self) -> None:
        arr = DynamicTypedArray(int, 1, 2, 3)

        with pytest.raises(TypeError):
            arr.insert(0, True)

    def test_remove_returns_value(self) -> None:
        arr = DynamicTypedArray(int, 10, 20, 30)
        val = arr.remove(1)

        assert val == 20
        assert list(arr) == [10, 30]

    def test_remove_resets_freed_slot_to_default(self) -> None:
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr.remove(2)

        # After remove, size=2, the slot at index 2 should be 0 in the buffer
        # We verify indirectly: iter should only yield 2 elements
        assert list(arr) == [1, 2]
        assert len(arr) == 2

    def test_remove_from_empty_raises(self) -> None:
        arr = DynamicTypedArray(int)

        with pytest.raises(IndexError):
            arr.remove(0)

    def test_remove_out_of_range_raises(self) -> None:
        arr = DynamicTypedArray(int, 1, 2, 3)

        with pytest.raises(IndexError):
            arr.remove(10)


class TestDynamicTypedArrayOperations:
    """
    Testing clear and copy.
    """

    def test_clear_resets_size_and_slots(self) -> None:
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr.clear()

        assert len(arr) == 0

    def test_clear_preserves_capacity(self) -> None:
        arr = DynamicTypedArray(int, 1, 2, 3)
        capacity_before = arr._capacity
        arr.clear()

        assert arr._capacity == capacity_before

    def test_clear_makes_array_falsy(self) -> None:
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr.clear()

        assert not arr

    def test_copy_returns_independent_array(self) -> None:
        arr = DynamicTypedArray(int, 1, 2, 3)
        copy = arr.copy()

        assert list(copy) == [1, 2, 3]

        arr.remove(0)
        assert list(copy) == [1, 2, 3]

    def test_copy_preserves_dtype(self) -> None:
        arr = DynamicTypedArray(float, 1.1, 2.2)
        copy = arr.copy()

        assert copy._dtype is float

    def test_copy_preserves_str_length(self) -> None:
        arr = DynamicTypedArray(str, str_length=30)
        copy = arr.copy()

        assert copy._data._str_length == 30


class TestDynamicTypedArrayDunder:
    """
    Testing all dunder methods.
    """

    def test_len_returns_size_not_capacity(self) -> None:
        arr = DynamicTypedArray(int, 1, 2)

        assert len(arr) == 2
        assert arr._capacity == 4

    def test_bool_false_when_empty(self) -> None:
        arr = DynamicTypedArray(int)

        assert bool(arr) is False

    def test_bool_true_when_not_empty(self) -> None:
        arr = DynamicTypedArray(int, 1)

        assert bool(arr) is True

    def test_getitem_positive_index(self) -> None:
        arr = DynamicTypedArray(int, 10, 20, 30)

        assert arr[0] == 10
        assert arr[2] == 30

    def test_getitem_negative_index(self) -> None:
        arr = DynamicTypedArray(int, 10, 20, 30)

        assert arr[-1] == 30
        assert arr[-3] == 10

    def test_setitem_correct_type(self) -> None:
        arr = DynamicTypedArray(int, 1, 2, 3)
        arr[1] = 99

        assert arr[1] == 99

    def test_setitem_wrong_type_raises(self) -> None:
        arr = DynamicTypedArray(int, 1, 2, 3)

        with pytest.raises(TypeError):
            arr[0] = "x"

    def test_setitem_bool_in_int_raises(self) -> None:
        arr = DynamicTypedArray(int, 1, 2, 3)

        with pytest.raises(TypeError):
            arr[0] = True

    def test_iter_yields_filled_elements_only(self) -> None:
        arr = DynamicTypedArray(int, 1, 2, 3)

        assert list(arr) == [1, 2, 3]

    def test_reversed_yields_right_to_left(self) -> None:
        arr = DynamicTypedArray(int, 1, 2, 3)

        assert list(reversed(arr)) == [3, 2, 1]

    def test_contains_existing_value(self) -> None:
        arr = DynamicTypedArray(int, 10, 20, 30)

        assert 10 in arr
        assert 30 in arr

    def test_contains_missing_value(self) -> None:
        arr = DynamicTypedArray(int, 1, 2, 3)

        assert 99 not in arr

    def test_contains_wrong_type_returns_false(self) -> None:
        arr = DynamicTypedArray(int, 1, 2, 3)

        # Should not raise — short-circuits to False
        assert "1" not in arr
        assert 1.0 not in arr

    def test_contains_bool_in_int_returns_false(self) -> None:
        arr = DynamicTypedArray(int, 1, 0)

        assert True not in arr
        assert False not in arr

    def test_eq_same_elements(self) -> None:
        a = DynamicTypedArray(int, 1, 2, 3)
        b = DynamicTypedArray(int, 1, 2, 3)

        assert a == b

    def test_eq_different_elements(self) -> None:
        a = DynamicTypedArray(int, 1, 2, 3)
        b = DynamicTypedArray(int, 1, 2, 99)

        assert a != b

    def test_eq_different_dtype(self) -> None:
        a = DynamicTypedArray(int)
        b = DynamicTypedArray(float)

        assert a != b

    def test_eq_different_sizes(self) -> None:
        a = DynamicTypedArray(int, 1, 2, 3)
        b = DynamicTypedArray(int, 1, 2)

        assert a != b

    def test_eq_non_array_returns_not_implemented(self) -> None:
        arr = DynamicTypedArray(int, 1, 2, 3)

        assert arr.__eq__([1, 2, 3]) is NotImplemented

    def test_repr_format(self) -> None:
        arr = DynamicTypedArray(int, 1, 2, 3)

        assert repr(arr) == "DynamicTypedArray(int, size=3, capacity=4)[1, 2, 3]"

    def test_repr_empty(self) -> None:
        arr = DynamicTypedArray(int)

        assert repr(arr) == "DynamicTypedArray(int, size=0, capacity=4)[]"
