import pytest

from data_structures import StaticTypedArray


class TestStaticTypedArrayInit:
    """
    Testing StaticTypedArray initialization for all dtypes.
    """

    def test_int_capacity_only(self) -> None:
        arr = StaticTypedArray(int, capacity=4)

        assert len(arr) == 4
        for i in range(4):
            assert arr[i] == 0

    def test_float_capacity_only(self) -> None:
        arr = StaticTypedArray(float, capacity=3)

        assert len(arr) == 3
        for i in range(3):
            assert arr[i] == 0.0

    def test_bool_capacity_only(self) -> None:
        arr = StaticTypedArray(bool, capacity=3)

        assert len(arr) == 3
        for i in range(3):
            assert arr[i] is False

    def test_str_capacity_only(self) -> None:
        arr = StaticTypedArray(str, capacity=3)

        assert len(arr) == 3
        for i in range(3):
            assert arr[i] == ""

    def test_args_only(self) -> None:
        arr = StaticTypedArray(int, 1, 2, 3)

        assert len(arr) == 3
        assert arr[0] == 1
        assert arr[1] == 2
        assert arr[2] == 3

    def test_args_with_capacity(self) -> None:
        arr = StaticTypedArray(int, 1, 2, capacity=5)

        assert len(arr) == 5
        assert arr[0] == 1
        assert arr[1] == 2
        assert arr[2] == 0
        assert arr[3] == 0
        assert arr[4] == 0

    def test_str_with_custom_str_length(self) -> None:
        arr = StaticTypedArray(str, capacity=3, str_length=8)

        assert arr._str_length == 8

    def test_str_default_str_length_is_20(self) -> None:
        arr = StaticTypedArray(str, capacity=3)

        assert arr._str_length == 20


class TestStaticTypedArrayInitErrors:
    """
    Testing StaticTypedArray initialization errors.
    """

    def test_unsupported_dtype_raises(self) -> None:
        with pytest.raises(TypeError):
            StaticTypedArray(list, capacity=3)  # type: ignore[arg-type]

    def test_dtype_as_string_raises(self) -> None:
        with pytest.raises(TypeError):
            StaticTypedArray("int", capacity=3)  # type: ignore[arg-type]

    def test_dtype_none_raises(self) -> None:
        with pytest.raises(TypeError):
            StaticTypedArray(None, capacity=3)  # type: ignore[arg-type]

    def test_no_args_no_capacity_raises(self) -> None:
        with pytest.raises(TypeError):
            StaticTypedArray(int)

    def test_capacity_zero_raises(self) -> None:
        with pytest.raises(ValueError):
            StaticTypedArray(int, capacity=0)

    def test_capacity_negative_raises(self) -> None:
        with pytest.raises(ValueError):
            StaticTypedArray(int, capacity=-1)

    def test_capacity_float_raises(self) -> None:
        with pytest.raises(TypeError):
            StaticTypedArray(int, capacity=3.0)  # type: ignore[arg-type]

    def test_too_many_args_raises(self) -> None:
        with pytest.raises(OverflowError):
            StaticTypedArray(int, 1, 2, 3, 4, capacity=2)

    def test_wrong_type_in_args_raises(self) -> None:
        with pytest.raises(TypeError):
            StaticTypedArray(int, 1, "two", 3)

    def test_bool_in_int_args_raises(self) -> None:
        with pytest.raises(TypeError):
            StaticTypedArray(int, 1, True, 3)

    def test_int_in_bool_args_raises(self) -> None:
        with pytest.raises(TypeError):
            StaticTypedArray(bool, True, 1, False)

    def test_str_length_zero_raises(self) -> None:
        with pytest.raises(ValueError):
            StaticTypedArray(str, capacity=3, str_length=0)

    def test_str_length_float_raises(self) -> None:
        with pytest.raises(TypeError):
            StaticTypedArray(str, capacity=3, str_length=5.0)  # type: ignore[arg-type]


class TestStaticTypedArrayGetSet:
    """
    Testing __getitem__ and __setitem__ with type enforcement.
    """

    def test_getitem_positive_index(self) -> None:
        arr = StaticTypedArray(int, 10, 20, 30)

        assert arr[0] == 10
        assert arr[1] == 20
        assert arr[2] == 30

    def test_getitem_negative_index(self) -> None:
        arr = StaticTypedArray(float, 1.1, 2.2, 3.3)

        assert arr[-1] == 3.3
        assert arr[-3] == 1.1

    def test_setitem_correct_type(self) -> None:
        arr = StaticTypedArray(int, capacity=3)
        arr[0] = 100
        arr[1] = -50
        arr[2] = 0

        assert arr[0] == 100
        assert arr[1] == -50
        assert arr[2] == 0

    def test_setitem_wrong_type_raises(self) -> None:
        arr = StaticTypedArray(int, capacity=3)

        with pytest.raises(TypeError):
            arr[0] = "not an int"

    def test_setitem_bool_in_int_raises(self) -> None:
        arr = StaticTypedArray(int, capacity=3)

        with pytest.raises(TypeError):
            arr[0] = True

    def test_setitem_int_in_bool_raises(self) -> None:
        arr = StaticTypedArray(bool, capacity=3)

        with pytest.raises(TypeError):
            arr[0] = 1

    def test_setitem_out_of_range_raises(self) -> None:
        arr = StaticTypedArray(int, capacity=3)

        with pytest.raises(IndexError):
            arr[3] = 10

    def test_setitem_bool_index_raises(self) -> None:
        arr = StaticTypedArray(int, capacity=3)

        with pytest.raises(TypeError):
            arr[True] = 10  # type: ignore[index]

    def test_str_stores_and_retrieves(self) -> None:
        arr = StaticTypedArray(str, "hello", "world", capacity=3)

        assert arr[0] == "hello"
        assert arr[1] == "world"
        assert arr[2] == ""


class TestStaticTypedArrayOperations:
    """
    Testing clear and copy.
    """

    def test_clear_resets_int_to_zero(self) -> None:
        arr = StaticTypedArray(int, 1, 2, 3)
        arr.clear()

        for i in range(3):
            assert arr[i] == 0

    def test_clear_resets_float_to_zero(self) -> None:
        arr = StaticTypedArray(float, 1.1, 2.2, 3.3)
        arr.clear()

        for i in range(3):
            assert arr[i] == 0.0

    def test_clear_resets_bool_to_false(self) -> None:
        arr = StaticTypedArray(bool, True, True, True)
        arr.clear()

        for i in range(3):
            assert arr[i] is False

    def test_clear_resets_str_to_empty(self) -> None:
        arr = StaticTypedArray(str, "hi", "there", capacity=3)
        arr.clear()

        for i in range(3):
            assert arr[i] == ""

    def test_clear_preserves_capacity(self) -> None:
        arr = StaticTypedArray(int, 1, 2, 3)
        arr.clear()

        assert len(arr) == 3

    def test_copy_returns_independent_array(self) -> None:
        arr = StaticTypedArray(int, 1, 2, 3)
        copy = arr.copy()

        assert copy[0] == 1
        assert copy[1] == 2
        assert copy[2] == 3

        arr[0] = 999
        assert copy[0] == 1

    def test_copy_preserves_dtype(self) -> None:
        arr = StaticTypedArray(float, 1.1, 2.2)
        copy = arr.copy()

        assert copy._dtype is float

    def test_copy_preserves_str_length(self) -> None:
        arr = StaticTypedArray(str, capacity=3, str_length=10)
        copy = arr.copy()

        assert copy._str_length == 10


class TestStaticTypedArrayDunder:
    """
    Testing all dunder methods.
    """

    def test_len_returns_capacity(self) -> None:
        arr = StaticTypedArray(int, capacity=6)

        assert len(arr) == 6

    def test_bool_true_for_valid_array(self) -> None:
        arr = StaticTypedArray(int, capacity=1)

        assert bool(arr) is True

    def test_iter_yields_all_elements(self) -> None:
        arr = StaticTypedArray(int, 1, 2, 3)

        assert list(arr) == [1, 2, 3]

    def test_iter_yields_defaults_for_empty_slots(self) -> None:
        arr = StaticTypedArray(int, 10, capacity=3)

        assert list(arr) == [10, 0, 0]

    def test_reversed_yields_right_to_left(self) -> None:
        arr = StaticTypedArray(int, 1, 2, 3)

        assert list(reversed(arr)) == [3, 2, 1]

    def test_contains_existing_value(self) -> None:
        arr = StaticTypedArray(int, 10, 20, 30)

        assert 10 in arr
        assert 20 in arr
        assert 30 in arr

    def test_contains_missing_value(self) -> None:
        arr = StaticTypedArray(int, 1, 2, 3)

        assert 99 not in arr

    def test_contains_wrong_type_returns_false(self) -> None:
        arr = StaticTypedArray(int, 1, 2, 3)

        # Should not raise — returns False immediately
        assert "1" not in arr
        assert 1.0 not in arr

    def test_contains_bool_in_int_returns_false(self) -> None:
        arr = StaticTypedArray(int, 1, 0, 1)

        assert True not in arr
        assert False not in arr

    def test_eq_same_arrays(self) -> None:
        a = StaticTypedArray(int, 1, 2, 3)
        b = StaticTypedArray(int, 1, 2, 3)

        assert a == b

    def test_eq_different_elements(self) -> None:
        a = StaticTypedArray(int, 1, 2, 3)
        b = StaticTypedArray(int, 1, 2, 99)

        assert a != b

    def test_eq_different_dtype(self) -> None:
        a = StaticTypedArray(int, capacity=3)
        b = StaticTypedArray(float, capacity=3)

        assert a != b

    def test_eq_non_array_returns_not_implemented(self) -> None:
        arr = StaticTypedArray(int, 1, 2, 3)

        assert arr.__eq__([1, 2, 3]) is NotImplemented

    def test_repr_int(self) -> None:
        arr = StaticTypedArray(int, 1, 2, 3)

        assert repr(arr) == "StaticTypedArray(int, capacity=3)[1, 2, 3]"

    def test_repr_with_defaults(self) -> None:
        arr = StaticTypedArray(int, 1, capacity=3)

        assert repr(arr) == "StaticTypedArray(int, capacity=3)[1, 0, 0]"
