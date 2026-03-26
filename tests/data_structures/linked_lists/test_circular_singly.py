import pytest

from data_structures.linked_lists import CircularSinglyLinkedList


class TestCircularSinglyLinkedListIndex:
    def test_returns_index_of_existing_value(self):
        lst = CircularSinglyLinkedList(10, 20, 30)
        assert lst.index(20) == 1

    def test_returns_index_of_head(self):
        lst = CircularSinglyLinkedList(10, 20, 30)
        assert lst.index(10) == 0

    def test_returns_index_of_tail(self):
        lst = CircularSinglyLinkedList(10, 20, 30)
        assert lst.index(30) == 2

    def test_returns_first_occurrence_for_duplicates(self):
        lst = CircularSinglyLinkedList(1, 2, 1)
        assert lst.index(1) == 0

    def test_raises_value_error_when_not_found(self):
        lst = CircularSinglyLinkedList(1, 2, 3)
        with pytest.raises(ValueError):
            lst.index(99)

    def test_raises_value_error_on_empty_list(self):
        lst = CircularSinglyLinkedList()
        with pytest.raises(ValueError):
            lst.index(1)

    def test_does_not_loop_infinitely(self):
        # index() must stop after size steps, not loop forever
        lst = CircularSinglyLinkedList(1, 2, 3)
        with pytest.raises(ValueError):
            lst.index(99)


class TestCircularSinglyLinkedListClear:
    def test_clear_empties_list(self):
        lst = CircularSinglyLinkedList(1, 2, 3)
        lst.clear()
        assert len(lst) == 0

    def test_clear_sets_head_and_tail_to_none(self):
        lst = CircularSinglyLinkedList(1, 2, 3)
        lst.clear()
        assert lst._head is None
        assert lst._tail is None

    def test_clear_allows_reuse(self):
        lst = CircularSinglyLinkedList(1, 2, 3)
        lst.clear()
        lst.append(99)
        assert list(lst) == [99]
        assert lst._tail.next is lst._head  # type: ignore[testing]

    def test_clear_on_empty_list_is_safe(self):
        lst = CircularSinglyLinkedList()
        lst.clear()
        assert len(lst) == 0


class TestCircularSinglyLinkedListCopy:
    def test_copy_has_same_elements(self):
        lst = CircularSinglyLinkedList(1, 2, 3)
        c = lst.copy()
        assert list(c) == [1, 2, 3]

    def test_copy_is_independent(self):
        lst = CircularSinglyLinkedList(1, 2, 3)
        c = lst.copy()
        c.append(4)
        assert len(lst) == 3

    def test_copy_of_empty_list(self):
        lst = CircularSinglyLinkedList()
        c = lst.copy()
        assert len(c) == 0

    def test_copy_returns_same_type(self):
        lst = CircularSinglyLinkedList(1, 2, 3)
        c = lst.copy()
        assert type(c) is CircularSinglyLinkedList

    def test_copy_maintains_circular_invariant(self):
        lst = CircularSinglyLinkedList(1, 2, 3)
        c = lst.copy()
        assert c._tail.next is c._head  # type: ignore[testing]

    def test_copy_does_not_share_nodes_with_original(self):
        lst = CircularSinglyLinkedList(1, 2, 3)
        c = lst.copy()
        assert c._head is not lst._head


class TestCircularSinglyLinkedListBool:
    def test_bool_true_when_not_empty(self):
        lst = CircularSinglyLinkedList(1)
        assert bool(lst) is True

    def test_bool_false_when_empty(self):
        lst = CircularSinglyLinkedList()
        assert bool(lst) is False

    def test_bool_false_after_clear(self):
        lst = CircularSinglyLinkedList(1, 2, 3)
        lst.clear()
        assert bool(lst) is False


class TestCircularSinglyLinkedListContainsUsesIndex:
    def test_contains_existing_value(self):
        lst = CircularSinglyLinkedList(1, 2, 3)
        assert 2 in lst

    def test_contains_missing_value(self):
        lst = CircularSinglyLinkedList(1, 2, 3)
        assert 99 not in lst

    def test_contains_none(self):
        lst = CircularSinglyLinkedList(1, None, 3)
        assert None in lst

    def test_contains_does_not_loop_infinitely(self):
        lst = CircularSinglyLinkedList(1, 2, 3)
        assert 99 not in lst
