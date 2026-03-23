import pytest

from data_structures.linked_lists import DoublyLinkedList


class TestDoublyLinkedListInit:
    def test_creates_empty_list(self):
        lst = DoublyLinkedList()
        assert len(lst) == 0

    def test_head_and_tail_are_none_when_empty(self):
        lst = DoublyLinkedList()
        assert lst._head is None
        assert lst._tail is None

    def test_creates_list_with_initial_values(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert list(lst) == [1, 2, 3]

    def test_size_equals_number_of_initial_values(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert len(lst) == 3

    def test_head_and_tail_set_correctly_on_single_element(self):
        lst = DoublyLinkedList(42)
        assert lst._head.value == 42  # type: ignore[testing]
        assert lst._tail.value == 42  # type: ignore[testing]

    def test_head_prev_is_none(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert lst._head.prev is None  # type: ignore[testing]

    def test_tail_next_is_none(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert lst._tail.next is None  # type: ignore[testing]

    def test_bidirectional_links_are_correct(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert lst._head.next.value == 2  # type: ignore[testing]
        assert lst._head.next.prev is lst._head  # type: ignore[testing]


class TestDoublyLinkedListAppend:
    def test_appends_to_empty_list(self):
        lst = DoublyLinkedList()
        lst.append(1)
        assert lst[0] == 1
        assert len(lst) == 1

    def test_appends_multiple_elements_in_order(self):
        lst = DoublyLinkedList()
        lst.append(1)
        lst.append(2)
        lst.append(3)
        assert list(lst) == [1, 2, 3]

    def test_tail_updates_after_append(self):
        lst = DoublyLinkedList(1)
        lst.append(2)
        assert lst._tail.value == 2  # type: ignore[testing]

    def test_prev_link_set_correctly_after_append(self):
        lst = DoublyLinkedList(1)
        lst.append(2)
        assert lst._tail.prev.value == 1  # type: ignore[testing]

    def test_tail_next_remains_none_after_append(self):
        lst = DoublyLinkedList(1, 2)
        lst.append(3)
        assert lst._tail.next is None  # type: ignore[testing]


class TestDoublyLinkedListPrepend:
    def test_prepends_to_empty_list(self):
        lst = DoublyLinkedList()
        lst.prepend(1)
        assert lst[0] == 1
        assert len(lst) == 1

    def test_prepends_to_existing_list(self):
        lst = DoublyLinkedList(2, 3)
        lst.prepend(1)
        assert list(lst) == [1, 2, 3]

    def test_head_updates_after_prepend(self):
        lst = DoublyLinkedList(2)
        lst.prepend(1)
        assert lst._head.value == 1  # type: ignore[testing]

    def test_next_link_set_correctly_after_prepend(self):
        lst = DoublyLinkedList(2)
        lst.prepend(1)
        assert lst._head.next.value == 2  # type: ignore[testing]

    def test_head_prev_remains_none_after_prepend(self):
        lst = DoublyLinkedList(2, 3)
        lst.prepend(1)
        assert lst._head.prev is None  # type: ignore[testing]


class TestDoublyLinkedListInsert:
    def test_inserts_at_beginning(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst.insert(0, 99)
        assert list(lst) == [99, 1, 2, 3]

    def test_inserts_at_middle(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst.insert(1, 99)
        assert list(lst) == [1, 99, 2, 3]

    def test_inserts_at_end(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst.insert(3, 99)
        assert list(lst) == [1, 2, 3, 99]

    def test_supports_negative_index(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst.insert(-1, 99)
        assert list(lst) == [1, 2, 99, 3]

    def test_bidirectional_links_intact_after_insert(self):
        lst = DoublyLinkedList(1, 3)
        lst.insert(1, 2)
        node = lst._head.next  # type: ignore[testing]
        assert node.value == 2  # type: ignore[testing]
        assert node.prev.value == 1  # type: ignore[testing]
        assert node.next.value == 3  # type: ignore[testing]

    def test_size_increases_after_insert(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst.insert(1, 99)
        assert len(lst) == 4

    def test_raises_index_error_for_out_of_range(self):
        lst = DoublyLinkedList(1, 2, 3)
        with pytest.raises(IndexError):
            lst.insert(10, 99)

    def test_raises_type_error_for_float_index(self):
        lst = DoublyLinkedList(1, 2, 3)
        with pytest.raises(TypeError):
            lst.insert(1.0, 99)  # type: ignore[testing]

    def test_raises_type_error_for_bool_index(self):
        lst = DoublyLinkedList(1, 2, 3)
        with pytest.raises(TypeError):
            lst.insert(True, 99)


class TestDoublyLinkedListRemove:
    def test_removes_and_returns_value_at_index(self):
        lst = DoublyLinkedList(1, 2, 3)
        value = lst.remove(1)
        assert value == 2

    def test_shifts_elements_after_remove(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst.remove(1)
        assert list(lst) == [1, 3]

    def test_removes_head(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst.remove(0)
        assert lst._head.value == 2  # type: ignore[testing]
        assert lst._head.prev is None  # type: ignore[testing]

    def test_removes_tail(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst.remove(2)
        assert lst._tail.value == 2  # type: ignore[testing]
        assert lst._tail.next is None  # type: ignore[testing]

    def test_removes_last_remaining_element(self):
        lst = DoublyLinkedList(1)
        lst.remove(0)
        assert len(lst) == 0
        assert lst._head is None
        assert lst._tail is None

    def test_bidirectional_links_intact_after_remove(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst.remove(1)
        assert lst._head.next.value == 3  # type: ignore[testing]
        assert lst._tail.prev.value == 1  # type: ignore[testing]

    def test_supports_negative_index(self):
        lst = DoublyLinkedList(1, 2, 3)
        value = lst.remove(-1)
        assert value == 3
        assert list(lst) == [1, 2]

    def test_size_decreases_after_remove(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst.remove(0)
        assert len(lst) == 2

    def test_raises_index_error_on_empty_list(self):
        lst = DoublyLinkedList()
        with pytest.raises(IndexError):
            lst.remove(0)

    def test_raises_index_error_for_out_of_range(self):
        lst = DoublyLinkedList(1, 2, 3)
        with pytest.raises(IndexError):
            lst.remove(5)

    def test_raises_type_error_for_float_index(self):
        lst = DoublyLinkedList(1, 2, 3)
        with pytest.raises(TypeError):
            lst.remove(1.0)  # type: ignore[testing]

    def test_raises_type_error_for_bool_index(self):
        lst = DoublyLinkedList(1, 2, 3)
        with pytest.raises(TypeError):
            lst.remove(True)


class TestDoublyLinkedListFind:
    def test_returns_index_of_existing_value(self):
        lst = DoublyLinkedList(10, 20, 30)
        assert lst.find(20) == 1

    def test_returns_index_of_head(self):
        lst = DoublyLinkedList(10, 20, 30)
        assert lst.find(10) == 0

    def test_returns_index_of_tail(self):
        lst = DoublyLinkedList(10, 20, 30)
        assert lst.find(30) == 2

    def test_returns_minus_one_when_not_found(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert lst.find(99) == -1

    def test_returns_first_occurrence_for_duplicate_values(self):
        lst = DoublyLinkedList(1, 2, 1)
        assert lst.find(1) == 0

    def test_returns_minus_one_on_empty_list(self):
        lst = DoublyLinkedList()
        assert lst.find(1) == -1


class TestDoublyLinkedListGetItem:
    def test_returns_value_at_index(self):
        lst = DoublyLinkedList(10, 20, 30)
        assert lst[0] == 10
        assert lst[2] == 30

    def test_supports_negative_indexing(self):
        lst = DoublyLinkedList(10, 20, 30)
        assert lst[-1] == 30
        assert lst[-3] == 10

    def test_raises_index_error_for_out_of_range(self):
        lst = DoublyLinkedList(1, 2, 3)
        with pytest.raises(IndexError):
            lst[3]

    def test_raises_type_error_for_float_index(self):
        lst = DoublyLinkedList(1, 2, 3)
        with pytest.raises(TypeError):
            lst[1.0]  # type: ignore[testing]

    def test_raises_type_error_for_bool_index(self):
        lst = DoublyLinkedList(1, 2, 3)
        with pytest.raises(TypeError):
            lst[True]


class TestDoublyLinkedListSetItem:
    def test_sets_value_at_index(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst[1] = 99
        assert lst[1] == 99

    def test_supports_negative_index(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst[-1] = 99
        assert lst[2] == 99

    def test_raises_index_error_for_out_of_range(self):
        lst = DoublyLinkedList(1, 2, 3)
        with pytest.raises(IndexError):
            lst[5] = 99

    def test_raises_type_error_for_bool_index(self):
        lst = DoublyLinkedList(1, 2, 3)
        with pytest.raises(TypeError):
            lst[True] = 99


class TestDoublyLinkedListLen:
    def test_returns_zero_for_empty_list(self):
        lst = DoublyLinkedList()
        assert len(lst) == 0

    def test_returns_correct_size(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert len(lst) == 3

    def test_updates_after_append(self):
        lst = DoublyLinkedList()
        lst.append(1)
        assert len(lst) == 1

    def test_updates_after_remove(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst.remove(0)
        assert len(lst) == 2


class TestDoublyLinkedListIter:
    def test_yields_values_in_order(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert list(lst) == [1, 2, 3]

    def test_yields_nothing_for_empty_list(self):
        lst = DoublyLinkedList()
        assert list(lst) == []

    def test_yields_single_element(self):
        lst = DoublyLinkedList(42)
        assert list(lst) == [42]


class TestDoublyLinkedListReversed:
    def test_yields_values_in_reverse_order(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert list(reversed(lst)) == [3, 2, 1]

    def test_reversed_empty_list(self):
        lst = DoublyLinkedList()
        assert list(reversed(lst)) == []

    def test_reversed_single_element(self):
        lst = DoublyLinkedList(42)
        assert list(reversed(lst)) == [42]

    def test_original_list_unchanged_after_reversed(self):
        lst = DoublyLinkedList(1, 2, 3)
        list(reversed(lst))
        assert list(lst) == [1, 2, 3]


class TestDoublyLinkedListContains:
    def test_returns_true_for_existing_value(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert 2 in lst

    def test_returns_false_for_missing_value(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert 99 not in lst

    def test_returns_true_for_none_value(self):
        lst = DoublyLinkedList(1, None, 3)
        assert None in lst


class TestDoublyLinkedListRepr:
    def test_repr_format_with_elements(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert repr(lst) == "DoublyLinkedList(size=3)[1 <-> 2 <-> 3]"

    def test_repr_empty_list(self):
        lst = DoublyLinkedList()
        assert repr(lst) == "DoublyLinkedList(size=0)[]"

    def test_repr_single_element(self):
        lst = DoublyLinkedList(42)
        assert repr(lst) == "DoublyLinkedList(size=1)[42]"

    def test_repr_string_values(self):
        lst = DoublyLinkedList("a", "b")
        assert repr(lst) == "DoublyLinkedList(size=2)['a' <-> 'b']"
