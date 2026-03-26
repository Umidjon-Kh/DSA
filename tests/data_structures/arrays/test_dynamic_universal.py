import pytest

from data_structures import DynamicUniversalArray


class TestDynamicUniversalArrayInit:
    """
    Testing DynamicUniversalArray initialization.
    """

    def test_empty_init_has_capacity_four(self) -> None:
        arr = DynamicUniversalArray()

        assert len(arr) == 0
        assert arr._capacity == 4

    def test_init_with_args(self) -> None:
        arr = DynamicUniversalArray(1, "hi", 3.0)

        assert len(arr) == 3
        assert arr[0] == 1
        assert arr[1] == "hi"
        assert arr[2] == 3.0

    def test_capacity_is_max_4_or_args(self) -> None:
        # Less than 4 args — capacity stays 4
        arr = DynamicUniversalArray(1, 2)
        assert arr._capacity == 4

        # More than 4 args — capacity equals len(args)
        arr = DynamicUniversalArray(1, 2, 3, 4, 5)
        assert arr._capacity == 5

    def test_stores_mixed_types(self) -> None:
        arr = DynamicUniversalArray(42, "text", 3.14, None, [1, 2])

        assert arr[0] == 42
        assert arr[1] == "text"
        assert arr[2] == 3.14
        assert arr[3] is None
        assert arr[4] == [1, 2]


class TestDynamicUniversalArrayMutation:
    """
    Testing append, insert and remove.
    """

    def test_append_single_element(self) -> None:
        arr = DynamicUniversalArray()
        arr.append(99)

        assert len(arr) == 1
        assert arr[0] == 99

    def test_append_multiple_elements(self) -> None:
        arr = DynamicUniversalArray()
        arr.append(1)
        arr.append(2)
        arr.append(3)

        assert list(arr) == [1, 2, 3]

    def test_append_triggers_resize(self) -> None:
        arr = DynamicUniversalArray()

        # Fill to capacity
        for i in range(4):
            arr.append(i)

        assert arr._capacity == 4

        # One more triggers resize: 4 + 0 + 3 = 7
        arr.append(99)

        assert len(arr) == 5
        assert arr._capacity == 7
        assert arr[4] == 99

    def test_insert_at_beginning(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)
        arr.insert(0, 0)

        assert list(arr) == [0, 1, 2, 3]

    def test_insert_at_middle(self) -> None:
        arr = DynamicUniversalArray(1, 2, 4)
        arr.insert(2, 3)

        assert list(arr) == [1, 2, 3, 4]

    def test_insert_at_end(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)
        arr.insert(3, 4)

        assert list(arr) == [1, 2, 3, 4]

    def test_insert_negative_index(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)
        arr.insert(-1, 99)

        assert list(arr) == [1, 2, 99, 3]

    def test_insert_triggers_resize(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3, 4)
        arr.insert(0, 0)

        assert arr._capacity == 7
        assert list(arr) == [0, 1, 2, 3, 4]

    def test_remove_from_beginning(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)
        val = arr.remove(0)

        assert val == 1
        assert list(arr) == [2, 3]

    def test_remove_from_middle(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)
        val = arr.remove(1)

        assert val == 2
        assert list(arr) == [1, 3]

    def test_remove_from_end(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)
        val = arr.remove(2)

        assert val == 3
        assert list(arr) == [1, 2]

    def test_remove_negative_index(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)
        val = arr.remove(-1)

        assert val == 3
        assert list(arr) == [1, 2]

    def test_remove_decrements_size(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)
        arr.remove(0)

        assert len(arr) == 2


class TestDynamicUniversalArrayMutationErrors:
    """
    Testing mutation error cases.
    """

    def test_insert_out_of_range_raises(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)

        with pytest.raises(IndexError):
            arr.insert(10, 99)

    def test_insert_bool_index_raises(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)

        with pytest.raises(TypeError):
            arr.insert(True, 99)  # type: ignore[arg-type]

    def test_remove_from_empty_raises(self) -> None:
        arr = DynamicUniversalArray()

        with pytest.raises(IndexError):
            arr.remove(0)

    def test_remove_out_of_range_raises(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)

        with pytest.raises(IndexError):
            arr.remove(10)

    def test_remove_bool_index_raises(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)

        with pytest.raises(TypeError):
            arr.remove(True)  # type: ignore[arg-type]


class TestDynamicUniversalArrayOperations:
    """
    Testing clear and copy.
    """

    def test_clear_resets_size_to_zero(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)
        arr.clear()

        assert len(arr) == 0

    def test_clear_preserves_capacity(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)
        capacity_before = arr._capacity
        arr.clear()

        assert arr._capacity == capacity_before

    def test_clear_makes_array_falsy(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)
        arr.clear()

        assert not arr

    def test_copy_returns_independent_array(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)
        copy = arr.copy()

        assert list(copy) == [1, 2, 3]

        arr[0] = 999
        assert copy[0] == 1

    def test_copy_mutating_copy_does_not_affect_original(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)
        copy = arr.copy()
        copy.append(99)

        assert len(arr) == 3

    def test_copy_of_empty_array(self) -> None:
        arr = DynamicUniversalArray()
        copy = arr.copy()

        assert len(copy) == 0


class TestDynamicUniversalArrayDunder:
    """
    Testing all dunder methods.
    """

    def test_len_returns_size_not_capacity(self) -> None:
        arr = DynamicUniversalArray(1, 2)

        assert len(arr) == 2
        assert arr._capacity == 4

    def test_bool_false_when_empty(self) -> None:
        arr = DynamicUniversalArray()

        assert bool(arr) is False

    def test_bool_true_when_not_empty(self) -> None:
        arr = DynamicUniversalArray(1)

        assert bool(arr) is True

    def test_bool_false_after_clear(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)
        arr.clear()

        assert bool(arr) is False

    def test_getitem_positive_index(self) -> None:
        arr = DynamicUniversalArray(10, 20, 30)

        assert arr[0] == 10
        assert arr[2] == 30

    def test_getitem_negative_index(self) -> None:
        arr = DynamicUniversalArray(10, 20, 30)

        assert arr[-1] == 30
        assert arr[-3] == 10

    def test_getitem_out_of_range_raises(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)

        with pytest.raises(IndexError):
            _ = arr[3]

    def test_setitem_updates_value(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)
        arr[1] = 99

        assert arr[1] == 99

    def test_setitem_out_of_range_raises(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)

        with pytest.raises(IndexError):
            arr[10] = 99

    def test_iter_yields_filled_elements_only(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)

        assert list(arr) == [1, 2, 3]

    def test_reversed_yields_right_to_left(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)

        assert list(reversed(arr)) == [3, 2, 1]

    def test_contains_existing_value(self) -> None:
        arr = DynamicUniversalArray(1, "hi", 3.0)

        assert 1 in arr
        assert "hi" in arr
        assert 3.0 in arr

    def test_contains_missing_value(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)

        assert 99 not in arr

    def test_eq_same_elements(self) -> None:
        a = DynamicUniversalArray(1, 2, 3)
        b = DynamicUniversalArray(1, 2, 3)

        assert a == b

    def test_eq_different_elements(self) -> None:
        a = DynamicUniversalArray(1, 2, 3)
        b = DynamicUniversalArray(1, 2, 99)

        assert a != b

    def test_eq_different_sizes(self) -> None:
        a = DynamicUniversalArray(1, 2, 3)
        b = DynamicUniversalArray(1, 2)

        assert a != b

    def test_eq_non_array_returns_not_implemented(self) -> None:
        arr = DynamicUniversalArray(1, 2, 3)

        assert arr.__eq__([1, 2, 3]) is NotImplemented

    def test_repr_format(self) -> None:
        arr = DynamicUniversalArray(1, "hi", 3.0)

        assert repr(arr) == "DynamicUniversalArray(size=3, capacity=4)[1, 'hi', 3.0]"

    def test_repr_empty(self) -> None:
        arr = DynamicUniversalArray()

        assert repr(arr) == "DynamicUniversalArray(size=0, capacity=4)[]"
