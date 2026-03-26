import pytest

from data_structures.linked_lists import DoublyLinkedList


class TestDoublyLinkedListIndex:
    def test_returns_index_of_existing_value(self):
        lst = DoublyLinkedList(10, 20, 30)
        assert lst.index(20) == 1

    def test_returns_index_of_head(self):
        lst = DoublyLinkedList(10, 20, 30)
        assert lst.index(10) == 0

    def test_returns_index_of_tail(self):
        lst = DoublyLinkedList(10, 20, 30)
        assert lst.index(30) == 2

    def test_returns_first_occurrence_for_duplicates(self):
        lst = DoublyLinkedList(1, 2, 1)
        assert lst.index(1) == 0

    def test_finds_none_value(self):
        lst = DoublyLinkedList(1, None, 3)
        assert lst.index(None) == 1

    def test_raises_value_error_when_not_found(self):
        lst = DoublyLinkedList(1, 2, 3)
        with pytest.raises(ValueError):
            lst.index(99)

    def test_raises_value_error_on_empty_list(self):
        lst = DoublyLinkedList()
        with pytest.raises(ValueError):
            lst.index(1)


class TestDoublyLinkedListClear:
    def test_clear_empties_list(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst.clear()
        assert len(lst) == 0

    def test_clear_sets_head_and_tail_to_none(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst.clear()
        assert lst._head is None
        assert lst._tail is None

    def test_clear_allows_reuse(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst.clear()
        lst.append(99)
        assert list(lst) == [99]
        assert lst._head.prev is None  # type: ignore[testing]
        assert lst._tail.next is None  # type: ignore[testing]

    def test_clear_on_empty_list_is_safe(self):
        lst = DoublyLinkedList()
        lst.clear()
        assert len(lst) == 0


class TestDoublyLinkedListCopy:
    def test_copy_has_same_elements(self):
        lst = DoublyLinkedList(1, 2, 3)
        c = lst.copy()
        assert list(c) == [1, 2, 3]

    def test_copy_is_independent(self):
        lst = DoublyLinkedList(1, 2, 3)
        c = lst.copy()
        c.append(4)
        assert len(lst) == 3

    def test_copy_of_empty_list(self):
        lst = DoublyLinkedList()
        c = lst.copy()
        assert len(c) == 0

    def test_copy_returns_same_type(self):
        lst = DoublyLinkedList(1, 2, 3)
        c = lst.copy()
        assert type(c) is DoublyLinkedList

    def test_copy_head_prev_is_none(self):
        lst = DoublyLinkedList(1, 2, 3)
        c = lst.copy()
        assert c._head.prev is None  # type: ignore[testing]

    def test_copy_tail_next_is_none(self):
        lst = DoublyLinkedList(1, 2, 3)
        c = lst.copy()
        assert c._tail.next is None  # type: ignore[testing]

    def test_copy_bidirectional_links_intact(self):
        lst = DoublyLinkedList(1, 2, 3)
        c = lst.copy()
        assert c._head.next.prev is c._head  # type: ignore[testing]


class TestDoublyLinkedListBool:
    def test_bool_true_when_not_empty(self):
        lst = DoublyLinkedList(1)
        assert bool(lst) is True

    def test_bool_false_when_empty(self):
        lst = DoublyLinkedList()
        assert bool(lst) is False

    def test_bool_false_after_clear(self):
        lst = DoublyLinkedList(1, 2, 3)
        lst.clear()
        assert bool(lst) is False


class TestDoublyLinkedListContainsUsesIndex:
    def test_contains_existing_value(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert 2 in lst

    def test_contains_missing_value(self):
        lst = DoublyLinkedList(1, 2, 3)
        assert 99 not in lst

    def test_contains_none(self):
        lst = DoublyLinkedList(1, None, 3)
        assert None in lst
