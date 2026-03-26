import pytest

from data_structures import StaticUniversalArray


class TestStaticUniversalArrayInit:
    """
    Testing StaticUniversalArray initialization.
    """

    def test_capacity_only(self) -> None:
        arr = StaticUniversalArray(capacity=5)

        assert len(arr) == 5
        for i in range(5):
            assert arr[i] is None

    def test_args_only(self) -> None:
        arr = StaticUniversalArray(1, "hi", 3.0)

        assert len(arr) == 3
        assert arr[0] == 1
        assert arr[1] == "hi"
        assert arr[2] == 3.0

    def test_args_with_capacity(self) -> None:
        arr = StaticUniversalArray(1, "hi", capacity=5)

        assert len(arr) == 5
        assert arr[0] == 1
        assert arr[1] == "hi"
        assert arr[2] is None
        assert arr[3] is None
        assert arr[4] is None

    def test_capacity_inferred_from_args(self) -> None:
        arr = StaticUniversalArray(10, 20, 30)

        assert len(arr) == 3

    def test_stores_none_explicitly(self) -> None:
        arr = StaticUniversalArray(None, None, capacity=3)

        assert arr[0] is None
        assert arr[1] is None

    def test_stores_mixed_types(self) -> None:
        arr = StaticUniversalArray(42, "text", 3.14, True, [1, 2], capacity=6)

        assert arr[0] == 42
        assert arr[1] == "text"
        assert arr[2] == 3.14
        assert arr[3] is True
        assert arr[4] == [1, 2]
        assert arr[5] is None


class TestStaticUniversalArrayInitErrors:
    """
    Testing StaticUniversalArray initialization errors.
    """

    def test_no_args_no_capacity_raises(self) -> None:
        with pytest.raises(TypeError):
            StaticUniversalArray()

    def test_capacity_zero_raises(self) -> None:
        with pytest.raises(ValueError):
            StaticUniversalArray(capacity=0)

    def test_capacity_negative_raises(self) -> None:
        with pytest.raises(ValueError):
            StaticUniversalArray(capacity=-3)

    def test_capacity_float_raises(self) -> None:
        with pytest.raises(TypeError):
            StaticUniversalArray(capacity=3.0)  # type: ignore[arg-type]

    def test_capacity_bool_raises(self) -> None:
        with pytest.raises(TypeError):
            StaticUniversalArray(capacity=True)  # type: ignore[arg-type]

    def test_too_many_args_raises(self) -> None:
        with pytest.raises(OverflowError):
            StaticUniversalArray(1, 2, 3, 4, 5, capacity=3)


class TestStaticUniversalArrayGetSet:
    """
    Testing __getitem__ and __setitem__.
    """

    def test_getitem_positive_index(self) -> None:
        arr = StaticUniversalArray(10, 20, 30)

        assert arr[0] == 10
        assert arr[1] == 20
        assert arr[2] == 30

    def test_getitem_negative_index(self) -> None:
        arr = StaticUniversalArray(10, 20, 30)

        assert arr[-1] == 30
        assert arr[-2] == 20
        assert arr[-3] == 10

    def test_setitem_positive_index(self) -> None:
        arr = StaticUniversalArray(capacity=3)
        arr[0] = "hello"
        arr[1] = 42
        arr[2] = [1, 2, 3]

        assert arr[0] == "hello"
        assert arr[1] == 42
        assert arr[2] == [1, 2, 3]

    def test_setitem_negative_index(self) -> None:
        arr = StaticUniversalArray(1, 2, 3)
        arr[-1] = 99
        arr[-3] = 11

        assert arr[0] == 11
        assert arr[2] == 99

    def test_getitem_index_error(self) -> None:
        arr = StaticUniversalArray(capacity=3)

        with pytest.raises(IndexError):
            _ = arr[3]

    def test_getitem_negative_index_error(self) -> None:
        arr = StaticUniversalArray(capacity=3)

        with pytest.raises(IndexError):
            _ = arr[-4]

    def test_getitem_type_error(self) -> None:
        arr = StaticUniversalArray(capacity=3)

        with pytest.raises(TypeError):
            _ = arr["0"]  # type: ignore[index]

    def test_getitem_bool_index_raises(self) -> None:
        arr = StaticUniversalArray(capacity=3)

        with pytest.raises(TypeError):
            _ = arr[True]  # type: ignore[index]

    def test_setitem_index_error(self) -> None:
        arr = StaticUniversalArray(capacity=3)

        with pytest.raises(IndexError):
            arr[3] = "x"

    def test_setitem_type_error(self) -> None:
        arr = StaticUniversalArray(capacity=3)

        with pytest.raises(TypeError):
            arr[1.0] = "x"  # type: ignore[index]


class TestStaticUniversalArrayOperations:
    """
    Testing clear and copy.
    """

    def test_clear_resets_to_none(self) -> None:
        arr = StaticUniversalArray(1, 2, 3)
        arr.clear()

        assert len(arr) == 3
        for i in range(3):
            assert arr[i] is None

    def test_copy_returns_independent_array(self) -> None:
        arr = StaticUniversalArray(1, "hi", 3.0)
        copy = arr.copy()

        assert copy[0] == 1
        assert copy[1] == "hi"
        assert copy[2] == 3.0

        # Mutating original does not affect copy
        arr[0] = 999
        assert copy[0] == 1

    def test_copy_mutating_copy_does_not_affect_original(self) -> None:
        arr = StaticUniversalArray(10, 20, 30)
        copy = arr.copy()
        copy[1] = 999

        assert arr[1] == 20

    def test_copy_preserves_capacity(self) -> None:
        arr = StaticUniversalArray(1, 2, capacity=5)
        copy = arr.copy()

        assert len(copy) == 5


class TestStaticUniversalArrayDunder:
    """
    Testing all dunder methods.
    """

    def test_len_returns_capacity(self) -> None:
        arr = StaticUniversalArray(capacity=7)

        assert len(arr) == 7

    def test_bool_true_for_valid_array(self) -> None:
        arr = StaticUniversalArray(capacity=1)

        assert bool(arr) is True

    def test_iter_yields_all_elements(self) -> None:
        arr = StaticUniversalArray(10, 20, 30)

        assert list(arr) == [10, 20, 30]

    def test_iter_yields_none_for_empty_slots(self) -> None:
        arr = StaticUniversalArray(1, capacity=3)

        assert list(arr) == [1, None, None]

    def test_reversed_yields_right_to_left(self) -> None:
        arr = StaticUniversalArray(10, 20, 30)

        assert list(reversed(arr)) == [30, 20, 10]

    def test_contains_existing_value(self) -> None:
        arr = StaticUniversalArray(1, "hi", 3.0)

        assert "hi" in arr
        assert 1 in arr
        assert 3.0 in arr

    def test_contains_missing_value(self) -> None:
        arr = StaticUniversalArray(1, 2, 3)

        assert 99 not in arr

    def test_contains_none_slot(self) -> None:
        arr = StaticUniversalArray(1, capacity=3)

        assert None in arr

    def test_eq_same_elements(self) -> None:
        a = StaticUniversalArray(1, 2, 3)
        b = StaticUniversalArray(1, 2, 3)

        assert a == b

    def test_eq_different_elements(self) -> None:
        a = StaticUniversalArray(1, 2, 3)
        b = StaticUniversalArray(1, 2, 99)

        assert a != b

    def test_eq_different_capacity(self) -> None:
        a = StaticUniversalArray(1, 2, capacity=3)
        b = StaticUniversalArray(1, 2, capacity=5)

        assert a != b

    def test_eq_non_array_returns_not_implemented(self) -> None:
        arr = StaticUniversalArray(1, 2, 3)

        assert arr.__eq__([1, 2, 3]) is NotImplemented

    def test_repr_format(self) -> None:
        arr = StaticUniversalArray(1, "hi", capacity=3)

        assert repr(arr) == "StaticUniversalArray(capacity=3)[1, 'hi', None]"

    def test_repr_all_none(self) -> None:
        arr = StaticUniversalArray(capacity=2)

        assert repr(arr) == "StaticUniversalArray(capacity=2)[None, None]"
