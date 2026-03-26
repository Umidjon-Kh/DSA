import pytest

from data_structures.linked_lists import SinglyLinkedList


class TestSinglyLinkedListIndex:
    def test_returns_index_of_existing_value(self):
        lst = SinglyLinkedList(10, 20, 30)
        assert lst.index(20) == 1

    def test_returns_index_of_head(self):
        lst = SinglyLinkedList(10, 20, 30)
        assert lst.index(10) == 0

    def test_returns_index_of_tail(self):
        lst = SinglyLinkedList(10, 20, 30)
        assert lst.index(30) == 2

    def test_returns_first_occurrence_for_duplicates(self):
        lst = SinglyLinkedList(1, 2, 1)
        assert lst.index(1) == 0

    def test_finds_none_value(self):
        lst = SinglyLinkedList(1, None, 3)
        assert lst.index(None) == 1

    def test_raises_value_error_when_not_found(self):
        lst = SinglyLinkedList(1, 2, 3)
        with pytest.raises(ValueError):
            lst.index(99)

    def test_raises_value_error_on_empty_list(self):
        lst = SinglyLinkedList()
        with pytest.raises(ValueError):
            lst.index(1)


class TestSinglyLinkedListClear:
    def test_clear_empties_list(self):
        lst = SinglyLinkedList(1, 2, 3)
        lst.clear()
        assert len(lst) == 0

    def test_clear_sets_head_to_none(self):
        lst = SinglyLinkedList(1, 2, 3)
        lst.clear()
        assert lst._head is None

    def test_clear_sets_tail_to_none(self):
        lst = SinglyLinkedList(1, 2, 3)
        lst.clear()
        assert lst._tail is None

    def test_clear_allows_reuse(self):
        lst = SinglyLinkedList(1, 2, 3)
        lst.clear()
        lst.append(99)
        assert list(lst) == [99]

    def test_clear_on_empty_list_is_safe(self):
        lst = SinglyLinkedList()
        lst.clear()
        assert len(lst) == 0


class TestSinglyLinkedListCopy:
    def test_copy_has_same_elements(self):
        lst = SinglyLinkedList(1, 2, 3)
        c = lst.copy()
        assert list(c) == [1, 2, 3]

    def test_copy_is_independent(self):
        lst = SinglyLinkedList(1, 2, 3)
        c = lst.copy()
        c.append(4)
        assert len(lst) == 3

    def test_copy_of_empty_list(self):
        lst = SinglyLinkedList()
        c = lst.copy()
        assert len(c) == 0

    def test_copy_returns_same_type(self):
        lst = SinglyLinkedList(1, 2, 3)
        c = lst.copy()
        assert type(c) is SinglyLinkedList

    def test_copy_tail_next_is_none(self):
        lst = SinglyLinkedList(1, 2, 3)
        c = lst.copy()
        assert c._tail.next is None  # type: ignore[testing]


class TestSinglyLinkedListBool:
    def test_bool_true_when_not_empty(self):
        lst = SinglyLinkedList(1)
        assert bool(lst) is True

    def test_bool_false_when_empty(self):
        lst = SinglyLinkedList()
        assert bool(lst) is False

    def test_bool_true_after_append(self):
        lst = SinglyLinkedList()
        lst.append(1)
        assert bool(lst) is True

    def test_bool_false_after_clear(self):
        lst = SinglyLinkedList(1, 2, 3)
        lst.clear()
        assert bool(lst) is False


class TestSinglyLinkedListContainsUsesIndex:
    def test_contains_existing_value(self):
        lst = SinglyLinkedList(1, 2, 3)
        assert 2 in lst

    def test_contains_missing_value(self):
        lst = SinglyLinkedList(1, 2, 3)
        assert 99 not in lst

    def test_contains_none(self):
        lst = SinglyLinkedList(1, None, 3)
        assert None in lst
