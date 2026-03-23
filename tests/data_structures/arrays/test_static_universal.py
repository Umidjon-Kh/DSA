import pytest

from data_structures.arrays import StaticUniversalArray

# =============================================================================
# Init — capacity=None
# =============================================================================


class TestStaticUniversalArrayInitCapacityOptional:
    def test_capacity_derived_from_args_when_not_provided(self):
        arr = StaticUniversalArray(1, "hi", 3)
        assert len(arr) == 3

    def test_capacity_keyword_only_no_args(self):
        arr = StaticUniversalArray(capacity=5)
        assert len(arr) == 5
        assert list(arr) == [None, None, None, None, None]

    def test_capacity_and_args_together(self):
        arr = StaticUniversalArray(1, "hi", capacity=5)
        assert len(arr) == 5
        assert list(arr) == [1, "hi", None, None, None]

    def test_raises_type_error_when_neither_capacity_nor_args(self):
        with pytest.raises(TypeError):
            StaticUniversalArray()

    def test_raises_overflow_error_when_args_exceed_capacity(self):
        with pytest.raises(OverflowError):
            StaticUniversalArray(1, 2, 3, capacity=2)

    def test_raises_value_error_for_zero_capacity(self):
        with pytest.raises(ValueError):
            StaticUniversalArray(capacity=0)

    def test_raises_type_error_for_non_int_capacity(self):
        with pytest.raises(TypeError):
            StaticUniversalArray(capacity="5")  # type: ignore[testing]

    def test_raises_type_error_for_bool_capacity(self):
        with pytest.raises(TypeError):
            StaticUniversalArray(capacity=True)

    def test_single_arg_no_capacity(self):
        arr = StaticUniversalArray(42)
        assert len(arr) == 1
        assert arr[0] == 42


# =============================================================================
# copy
# =============================================================================


class TestStaticUniversalArrayCopy:
    def test_copy_returns_new_instance(self):
        arr = StaticUniversalArray(1, 2, 3)
        copy = arr.copy()
        assert copy is not arr

    def test_copy_has_same_elements(self):
        arr = StaticUniversalArray(1, 2, 3)
        copy = arr.copy()
        assert list(copy) == [1, 2, 3]

    def test_copy_has_same_capacity(self):
        arr = StaticUniversalArray(1, "hi", capacity=5)
        copy = arr.copy()
        assert len(copy) == len(arr)

    def test_copy_is_independent(self):
        arr = StaticUniversalArray(1, 2, 3)
        copy = arr.copy()
        copy[0] = 99
        assert arr[0] == 1

    def test_copy_preserves_none_slots(self):
        arr = StaticUniversalArray(1, capacity=4)
        copy = arr.copy()
        assert list(copy) == [1, None, None, None]

    def test_copy_preserves_mixed_types(self):
        arr = StaticUniversalArray(1, "hi", 3.14)
        copy = arr.copy()
        assert list(copy) == [1, "hi", 3.14]

    def test_copy_is_shallow(self):
        inner = [1, 2, 3]
        arr = StaticUniversalArray(inner, "x")
        copy = arr.copy()
        inner.append(99)
        assert copy[0] is inner

    def test_copy_equal_to_original(self):
        arr = StaticUniversalArray(1, 2, 3)
        copy = arr.copy()
        assert arr == copy


# =============================================================================
# __bool__
# =============================================================================


class TestStaticUniversalArrayBool:
    def test_array_with_capacity_is_true(self):
        arr = StaticUniversalArray(capacity=3)
        assert arr

    def test_array_with_one_slot_is_true(self):
        arr = StaticUniversalArray(capacity=1)
        assert arr

    def test_bool_works_in_if_statement(self):
        arr = StaticUniversalArray(1, 2, 3)
        result = "yes" if arr else "no"
        assert result == "yes"


# =============================================================================
# __eq__
# =============================================================================


class TestStaticUniversalArrayEq:
    def test_equal_arrays_are_equal(self):
        a = StaticUniversalArray(1, 2, 3)
        b = StaticUniversalArray(1, 2, 3)
        assert a == b

    def test_different_elements_are_not_equal(self):
        a = StaticUniversalArray(1, 2, 3)
        b = StaticUniversalArray(1, 2, 99)
        assert a != b

    def test_different_capacities_are_not_equal(self):
        a = StaticUniversalArray(1, 2, 3)
        b = StaticUniversalArray(1, 2, 3, capacity=4)
        assert a != b

    def test_two_none_arrays_same_capacity_are_equal(self):
        a = StaticUniversalArray(capacity=3)
        b = StaticUniversalArray(capacity=3)
        assert a == b

    def test_equal_with_mixed_types(self):
        a = StaticUniversalArray(1, "hi", None)
        b = StaticUniversalArray(1, "hi", capacity=3)
        assert a == b

    def test_comparing_with_non_array_returns_not_implemented(self):
        arr = StaticUniversalArray(1, 2, 3)
        assert arr.__eq__([1, 2, 3]) is NotImplemented

    def test_not_equal_after_mutation(self):
        arr = StaticUniversalArray(1, 2, 3)
        copy = arr.copy()
        copy[0] = 99
        assert arr != copy
