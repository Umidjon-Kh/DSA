import pytest

from data_structures.arrays import StaticUniversalArray


class TestStaticUniversalArrayInit:
    def test_creates_array_with_given_capacity(self):
        arr = StaticUniversalArray(5)
        assert len(arr) == 5

    def test_all_slots_default_to_none(self):
        arr = StaticUniversalArray(3)
        assert list(arr) == [None, None, None]

    def test_creates_array_with_initial_elements(self):
        arr = StaticUniversalArray(5, 1, "hi", 3.0)
        assert arr[0] == 1
        assert arr[1] == "hi"
        assert arr[2] == 3.0

    def test_remaining_slots_are_none_after_partial_fill(self):
        arr = StaticUniversalArray(5, 1, 2)
        assert arr[2] is None
        assert arr[3] is None
        assert arr[4] is None

    def test_accepts_mixed_types(self):
        arr = StaticUniversalArray(4, 1, "hello", 3.14, True)
        assert arr[0] == 1
        assert arr[1] == "hello"
        assert arr[2] == 3.14
        assert arr[3] is True

    def test_accepts_none_as_element(self):
        arr = StaticUniversalArray(3, None, None)
        assert arr[0] is None

    def test_raises_type_error_for_non_int_capacity(self):
        with pytest.raises(TypeError):
            StaticUniversalArray("5")  # type: ignore[testing]

    def test_raises_type_error_for_bool_capacity(self):
        with pytest.raises(TypeError):
            StaticUniversalArray(True)

    def test_raises_value_error_for_zero_capacity(self):
        with pytest.raises(ValueError):
            StaticUniversalArray(0)

    def test_raises_value_error_for_negative_capacity(self):
        with pytest.raises(ValueError):
            StaticUniversalArray(-3)

    def test_raises_value_error_when_too_many_args(self):
        with pytest.raises(OverflowError):
            StaticUniversalArray(2, 1, 2, 3)

    def test_capacity_one_is_valid(self):
        arr = StaticUniversalArray(1)
        assert len(arr) == 1


class TestStaticUniversalArrayGetItem:
    def test_returns_element_at_index(self):
        arr = StaticUniversalArray(3, 10, 20, 30)
        assert arr[0] == 10
        assert arr[1] == 20
        assert arr[2] == 30

    def test_supports_negative_indexing(self):
        arr = StaticUniversalArray(3, 10, 20, 30)
        assert arr[-1] == 30
        assert arr[-2] == 20
        assert arr[-3] == 10

    def test_raises_index_error_for_out_of_range(self):
        arr = StaticUniversalArray(3)
        with pytest.raises(IndexError):
            arr[3]

    def test_raises_index_error_for_negative_out_of_range(self):
        arr = StaticUniversalArray(3)
        with pytest.raises(IndexError):
            arr[-4]

    def test_raises_type_error_for_float_index(self):
        arr = StaticUniversalArray(3)
        with pytest.raises(TypeError):
            arr[1.0]  # type: ignore[testing]

    def test_raises_type_error_for_string_index(self):
        arr = StaticUniversalArray(3)
        with pytest.raises(TypeError):
            arr["0"]  # type: ignore[testing]

    def test_raises_type_error_for_bool_index(self):
        arr = StaticUniversalArray(3)
        with pytest.raises(TypeError):
            arr[True]


class TestStaticUniversalArraySetItem:
    def test_sets_element_at_index(self):
        arr = StaticUniversalArray(3)
        arr[0] = 42
        assert arr[0] == 42

    def test_overwrites_existing_element(self):
        arr = StaticUniversalArray(3, 1, 2, 3)
        arr[1] = 99
        assert arr[1] == 99

    def test_sets_none_value(self):
        arr = StaticUniversalArray(3, 1, 2, 3)
        arr[0] = None
        assert arr[0] is None

    def test_supports_negative_index(self):
        arr = StaticUniversalArray(3, 1, 2, 3)
        arr[-1] = 99
        assert arr[2] == 99

    def test_raises_index_error_for_out_of_range(self):
        arr = StaticUniversalArray(3)
        with pytest.raises(IndexError):
            arr[3] = 1

    def test_raises_type_error_for_bool_index(self):
        arr = StaticUniversalArray(3)
        with pytest.raises(TypeError):
            arr[True] = 1


class TestStaticUniversalArrayLen:
    def test_returns_capacity(self):
        arr = StaticUniversalArray(5)
        assert len(arr) == 5

    def test_len_equals_capacity_not_filled_count(self):
        arr = StaticUniversalArray(5, 1, 2)
        assert len(arr) == 5


class TestStaticUniversalArrayIter:
    def test_iterates_all_elements_in_order(self):
        arr = StaticUniversalArray(4, 1, 2, 3, 4)
        assert list(arr) == [1, 2, 3, 4]

    def test_iterates_including_none_slots(self):
        arr = StaticUniversalArray(4, 1, 2)
        assert list(arr) == [1, 2, None, None]

    def test_iterates_fully_empty_array(self):
        arr = StaticUniversalArray(3)
        assert list(arr) == [None, None, None]


class TestStaticUniversalArrayReversed:
    def test_yields_elements_in_reverse_order(self):
        arr = StaticUniversalArray(4, 1, 2, 3, 4)
        assert list(reversed(arr)) == [4, 3, 2, 1]

    def test_reversed_includes_none_slots(self):
        arr = StaticUniversalArray(4, 1, 2)
        assert list(reversed(arr)) == [None, None, 2, 1]


class TestStaticUniversalArrayContains:
    def test_returns_true_for_existing_element(self):
        arr = StaticUniversalArray(4, 1, 2, 3)
        assert 2 in arr

    def test_returns_false_for_missing_element(self):
        arr = StaticUniversalArray(4, 1, 2, 3)
        assert 99 not in arr

    def test_returns_true_for_none(self):
        arr = StaticUniversalArray(3, 1)
        assert None in arr

    def test_returns_true_for_mixed_types(self):
        arr = StaticUniversalArray(3, "hi", 3.14, True)
        assert "hi" in arr
        assert 3.14 in arr


class TestStaticUniversalArrayRepr:
    def test_repr_format_with_elements(self):
        arr = StaticUniversalArray(3, 1, 2, 3)
        assert repr(arr) == "StaticUniversalArray(capacity=3)[1, 2, 3]"

    def test_repr_format_with_none_slots(self):
        arr = StaticUniversalArray(3, 1)
        assert repr(arr) == "StaticUniversalArray(capacity=3)[1, None, None]"

    def test_repr_empty_array(self):
        arr = StaticUniversalArray(2)
        assert repr(arr) == "StaticUniversalArray(capacity=2)[None, None]"
