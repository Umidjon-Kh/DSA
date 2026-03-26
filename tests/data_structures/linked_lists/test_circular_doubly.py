import pytest

from data_structures.linked_lists import CircularDoublyLinkedList


class TestCircularDoublyLinkedListInit:
    def test_empty_list(self):
        lst = CircularDoublyLinkedList()
        assert len(lst) == 0
        assert lst._head is None
        assert lst._tail is None

    def test_single_element_circular_invariant(self):
        lst = CircularDoublyLinkedList(42)
        assert lst._head is lst._tail
        assert (
            lst._head.next is lst._head
        )  # points to itself # type: ignore[union-attr]
        assert (
            lst._head.prev is lst._head
        )  # points to itself # type: ignore[union-attr]

    def test_multiple_elements(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        assert len(lst) == 3
        assert list(lst) == [1, 2, 3]

    def test_tail_next_points_to_head(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        assert lst._tail.next is lst._head  # type: ignore[union-attr]

    def test_head_prev_points_to_tail(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        assert lst._head.prev is lst._tail  # type: ignore[union-attr]

    def test_bidirectional_links(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        assert lst._head.next.prev is lst._head  # type: ignore[union-attr]
        assert lst._tail.prev.next is lst._tail  # type: ignore[union-attr]


class TestCircularDoublyLinkedListAppend:
    def test_append_to_empty(self):
        lst = CircularDoublyLinkedList()
        lst.append(1)
        assert lst._head is lst._tail
        assert lst._head.next is lst._head  # type: ignore[union-attr]
        assert lst._head.prev is lst._head  # type: ignore[union-attr]

    def test_append_updates_tail(self):
        lst = CircularDoublyLinkedList(1, 2)
        lst.append(3)
        assert lst._tail.value == 3  # type: ignore[union-attr]

    def test_append_maintains_circular_invariant(self):
        lst = CircularDoublyLinkedList(1, 2)
        lst.append(3)
        assert lst._tail.next is lst._head  # type: ignore[union-attr]
        assert lst._head.prev is lst._tail  # type: ignore[union-attr]

    def test_append_bidirectional_link(self):
        lst = CircularDoublyLinkedList(1)
        lst.append(2)
        assert lst._tail.prev is lst._head  # type: ignore[union-attr]
        assert lst._head.next is lst._tail  # type: ignore[union-attr]


class TestCircularDoublyLinkedListPrepend:
    def test_prepend_to_empty(self):
        lst = CircularDoublyLinkedList()
        lst.prepend(1)
        assert lst._head is lst._tail
        assert lst._head.next is lst._head  # type: ignore[union-attr]
        assert lst._head.prev is lst._head  # type: ignore[union-attr]

    def test_prepend_updates_head(self):
        lst = CircularDoublyLinkedList(2, 3)
        lst.prepend(1)
        assert lst._head.value == 1  # type: ignore[union-attr]
        assert list(lst) == [1, 2, 3]

    def test_prepend_maintains_circular_invariant(self):
        lst = CircularDoublyLinkedList(2, 3)
        lst.prepend(1)
        assert lst._tail.next is lst._head  # type: ignore[union-attr]
        assert lst._head.prev is lst._tail  # type: ignore[union-attr]

    def test_prepend_does_not_change_tail(self):
        lst = CircularDoublyLinkedList(2, 3)
        lst.prepend(1)
        assert lst._tail.value == 3  # type: ignore[union-attr]


class TestCircularDoublyLinkedListInsert:
    def test_insert_at_beginning(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        lst.insert(0, 0)
        assert list(lst) == [0, 1, 2, 3]
        assert lst._head.value == 0  # type: ignore[union-attr]

    def test_insert_at_end(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        lst.insert(3, 4)
        assert list(lst) == [1, 2, 3, 4]
        assert lst._tail.value == 4  # type: ignore[union-attr]

    def test_insert_in_middle(self):
        lst = CircularDoublyLinkedList(1, 2, 4)
        lst.insert(2, 3)
        assert list(lst) == [1, 2, 3, 4]

    def test_insert_bidirectional_links(self):
        lst = CircularDoublyLinkedList(1, 3)
        lst.insert(1, 2)
        mid = lst._head.next  # type: ignore[union-attr]
        assert mid.value == 2  # type: ignore[union-attr]
        assert mid.prev is lst._head  # type: ignore[union-attr]
        assert mid.next is lst._tail  # type: ignore[union-attr]

    def test_insert_maintains_circular_invariant(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        lst.insert(1, 99)
        assert lst._tail.next is lst._head  # type: ignore[union-attr]
        assert lst._head.prev is lst._tail  # type: ignore[union-attr]

    def test_insert_negative_index(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        lst.insert(-1, 99)
        assert list(lst) == [1, 2, 99, 3]

    def test_insert_out_of_range_raises(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        with pytest.raises(IndexError):
            lst.insert(10, 99)

    def test_insert_bool_index_raises(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        with pytest.raises(TypeError):
            lst.insert(True, 99)  # type: ignore[arg-type]


class TestCircularDoublyLinkedListRemove:
    def test_remove_head(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        val = lst.remove(0)
        assert val == 1
        assert list(lst) == [2, 3]
        assert lst._head.value == 2  # type: ignore[union-attr]
        assert lst._tail.next is lst._head  # type: ignore[union-attr]
        assert lst._head.prev is lst._tail  # type: ignore[union-attr]

    def test_remove_tail(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        val = lst.remove(2)
        assert val == 3
        assert list(lst) == [1, 2]
        assert lst._tail.value == 2  # type: ignore[union-attr]
        assert lst._tail.next is lst._head  # type: ignore[union-attr]
        assert lst._head.prev is lst._tail  # type: ignore[union-attr]

    def test_remove_middle(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        val = lst.remove(1)
        assert val == 2
        assert list(lst) == [1, 3]
        assert lst._head.next is lst._tail  # type: ignore[union-attr]
        assert lst._tail.prev is lst._head  # type: ignore[union-attr]
        assert lst._tail.next is lst._head  # type: ignore[union-attr]
        assert lst._head.prev is lst._tail  # type: ignore[union-attr]

    def test_remove_only_element(self):
        lst = CircularDoublyLinkedList(42)
        val = lst.remove(0)
        assert val == 42
        assert lst._head is None
        assert lst._tail is None
        assert len(lst) == 0

    def test_remove_negative_index(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        val = lst.remove(-1)
        assert val == 3
        assert list(lst) == [1, 2]

    def test_remove_from_empty_raises(self):
        lst = CircularDoublyLinkedList()
        with pytest.raises(IndexError):
            lst.remove(0)

    def test_remove_out_of_range_raises(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        with pytest.raises(IndexError):
            lst.remove(10)

    def test_remove_decrements_size(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        lst.remove(0)
        assert len(lst) == 2


class TestCircularDoublyLinkedListGetSetItem:
    def test_getitem_positive(self):
        lst = CircularDoublyLinkedList(10, 20, 30)
        assert lst[0] == 10
        assert lst[1] == 20
        assert lst[2] == 30

    def test_getitem_negative(self):
        lst = CircularDoublyLinkedList(10, 20, 30)
        assert lst[-1] == 30
        assert lst[-3] == 10

    def test_getitem_out_of_range_raises(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        with pytest.raises(IndexError):
            _ = lst[3]

    def test_getitem_bool_index_raises(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        with pytest.raises(TypeError):
            _ = lst[True]  # type: ignore[index]

    def test_setitem_positive(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        lst[1] = 99
        assert lst[1] == 99
        assert list(lst) == [1, 99, 3]

    def test_setitem_does_not_break_circular_invariant(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        lst[0] = 99
        assert lst._tail.next is lst._head  # type: ignore[union-attr]
        assert lst._head.prev is lst._tail  # type: ignore[union-attr]

    def test_setitem_does_not_change_size(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        lst[1] = 99
        assert len(lst) == 3


class TestCircularDoublyLinkedListIterReversed:
    def test_iter_order(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        assert list(lst) == [1, 2, 3]

    def test_iter_empty(self):
        assert list(CircularDoublyLinkedList()) == []

    def test_iter_stops_after_size_steps(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        result = []
        for v in lst:
            result.append(v)
            if len(result) > 10:
                pytest.fail("Iterator looped infinitely")
        assert result == [1, 2, 3]

    def test_reversed_order(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        assert list(reversed(lst)) == [3, 2, 1]

    def test_reversed_empty(self):
        assert list(reversed(CircularDoublyLinkedList())) == []

    def test_reversed_single(self):
        lst = CircularDoublyLinkedList(42)
        assert list(reversed(lst)) == [42]

    def test_reversed_stops_after_size_steps(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        result = []
        for v in reversed(lst):
            result.append(v)
            if len(result) > 10:
                pytest.fail("Reversed iterator looped infinitely")
        assert result == [3, 2, 1]

    def test_reversed_does_not_modify_list(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        _ = list(reversed(lst))
        assert list(lst) == [1, 2, 3]
        assert lst._tail.next is lst._head  # type: ignore[union-attr]
        assert lst._head.prev is lst._tail  # type: ignore[union-attr]


class TestCircularDoublyLinkedListEq:
    def test_equal_lists(self):
        a = CircularDoublyLinkedList(1, 2, 3)
        b = CircularDoublyLinkedList(1, 2, 3)
        assert a == b

    def test_both_empty(self):
        assert CircularDoublyLinkedList() == CircularDoublyLinkedList()

    def test_different_middle(self):
        a = CircularDoublyLinkedList(1, 2, 3)
        b = CircularDoublyLinkedList(1, 9, 3)
        assert a != b

    def test_different_size(self):
        a = CircularDoublyLinkedList(1, 2, 3)
        b = CircularDoublyLinkedList(1, 2)
        assert a != b

    def test_different_head(self):
        a = CircularDoublyLinkedList(1, 2, 3)
        b = CircularDoublyLinkedList(9, 2, 3)
        assert a != b

    def test_different_tail(self):
        a = CircularDoublyLinkedList(1, 2, 3)
        b = CircularDoublyLinkedList(1, 2, 9)
        assert a != b

    def test_not_implemented_for_other_type(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        assert lst.__eq__([1, 2, 3]) is NotImplemented

    def test_with_none_values(self):
        a = CircularDoublyLinkedList(1, None, 3)
        b = CircularDoublyLinkedList(1, None, 3)
        assert a == b

    def test_single_element_equal(self):
        assert CircularDoublyLinkedList(1) == CircularDoublyLinkedList(1)

    def test_single_element_not_equal(self):
        assert CircularDoublyLinkedList(1) != CircularDoublyLinkedList(2)


class TestCircularDoublyLinkedListRepr:
    def test_repr_empty(self):
        lst = CircularDoublyLinkedList()
        assert repr(lst) == "CircularDoublyLinkedList(size=0)[]"

    def test_repr_single(self):
        lst = CircularDoublyLinkedList(1)
        assert repr(lst) == "CircularDoublyLinkedList(size=1)[... <-> 1 <-> ...]"

    def test_repr_multiple(self):
        lst = CircularDoublyLinkedList(1, 2, 3)
        assert (
            repr(lst)
            == "CircularDoublyLinkedList(size=3)[... <-> 1 <-> 2 <-> 3 <-> ...]"
        )
